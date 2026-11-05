// Finished jobs, customer feedback and team scorecards.
//
// Flow: the installer team sends a job report (/job-report.html, Netlify form "job-report") with the
// customer's phone -> submission-created.mjs saves it as a finished job (store "feedback", key job/<id>).
// Payment rule: a job is "ready to pay" only when both the team's job report and the customer's feedback are in.
// The customer opens /feedback.html, enters that phone number, and can rate each finished job once.
// Only feedback tied to a finished job counts in the team record; the team comes from the job, not the customer.
//
// Public:
//   POST /api/feedback?a=check  {phone}                         -> {jobs:[{id, job, team, date}]} (unrated, not blocked)
//   POST /api/feedback?a=submit {phone, jobId, q1..q10, nps, name, comment, language}
// Admin (header "x-admin-password", same password as /members-admin.html):
//   GET  /api/feedback?a=list                                   -> {items, jobs, teams}
//   POST /api/feedback?a=jobset {id, blocked?, paid?}           block / unblock feedback; mark paid (only when report + feedback are in)
//   POST /api/feedback?a=jobdel {id}                            delete a finished job (and its files)
//   POST /api/feedback?a=delete {id}                            delete one feedback (its job can be rated again)
//   GET  /api/feedback?a=file&id=..&f=..                        a file from a job report
import { getStore } from "@netlify/blobs";
import crypto from "node:crypto";

const VOCAB_ADMIN_HASH = "162cdaefe4e9558d229a4846cd021775:5c036e020b55e8727a91b98d8e554c7456200d65599147cff4efea07459dc0fd";
const json = (b, s = 200) => new Response(JSON.stringify(b), { status: s, headers: { "content-type": "application/json", "cache-control": "no-store" } });
function eq(a, b) { a = Buffer.from(String(a)); b = Buffer.from(String(b)); return a.length === b.length && crypto.timingSafeEqual(a, b); }
function checkHash(pw, stored) {
  const [salt, h] = stored.split(":");
  const got = crypto.scryptSync(String(pw), salt, 32), want = Buffer.from(h, "hex");
  return got.length === want.length && crypto.timingSafeEqual(got, want);
}
function isAdmin(req) {
  const pw = req.headers.get("x-admin-password") || "";
  if (!pw) return false;
  if (process.env.MEMBERS_ADMIN_PASSWORD) return eq(pw, process.env.MEMBERS_ADMIN_PASSWORD);
  if (process.env.VOCAB_ADMIN_PASSWORD) return eq(pw, process.env.VOCAB_ADMIN_PASSWORD);
  return checkHash(pw, VOCAB_ADMIN_HASH);
}

// Thai phone numbers: keep digits, turn +66 / 66 into a leading 0.
function normPhone(v) {
  let d = String(v || "").replace(/\D/g, "");
  if (d.startsWith("66") && d.length >= 11) d = "0" + d.slice(2);
  return d.length >= 9 ? d : "";
}

const QUESTIONS = ["q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10"];
const SCORES = ["5", "4", "2", "1"];
const GROUPS = { work: ["q1", "q2", "q3", "q4", "q5"], personality: ["q6", "q7", "q8"], interaction: ["q9", "q10"] };
const n = (v) => { const x = parseFloat(v); return isFinite(x) ? x : null; };
const avg = (a) => a.length ? Math.round((a.reduce((s, x) => s + x, 0) / a.length) * 100) / 100 : null;
const txt = (v, k = 300) => String(v == null ? "" : v).trim().slice(0, k);
const newId = () => Date.now().toString(36) + crypto.randomBytes(4).toString("hex");

async function all(s, prefix) {
  const { blobs } = await s.list({ prefix });
  const out = [];
  for (const b of blobs) { const v = await s.get(b.key, { type: "json" }); if (v) out.push(v); }
  return out.sort((x, y) => String(y.created).localeCompare(String(x.created)));
}

function scorecards(items) {
  const by = {};
  for (const it of items) if (it.jobId) (by[it.team || "Not stated"] ||= []).push(it);
  return Object.entries(by).map(([team, rs]) => {
    const q = {}; for (const k of QUESTIONS) q[k] = avg(rs.map((r) => n(r.data[k])).filter((x) => x != null));
    const g = {}; for (const [name, ks] of Object.entries(GROUPS)) g[name] = avg(ks.map((k) => q[k]).filter((x) => x != null));
    const all = rs.flatMap((r) => QUESTIONS.map((k) => n(r.data[k])).filter((x) => x != null));
    const nps = rs.map((r) => n(r.data.nps)).filter((x) => x != null);
    const pro = nps.filter((x) => x >= 9).length, det = nps.filter((x) => x <= 6).length;
    return {
      team, responses: rs.length, overall: avg(all), groups: g, questions: q,
      nps: nps.length ? Math.round(((pro - det) / nps.length) * 100) : null, promoters: pro, passives: nps.length - pro - det, detractors: det,
      last: rs.map((r) => r.created).sort().pop(),
    };
  }).sort((a, b) => (b.overall ?? 0) - (a.overall ?? 0));
}

async function body(req) { try { return await req.json(); } catch { return {}; } }

export default async (req) => {
  const u = new URL(req.url), a = u.searchParams.get("a");
  const s = getStore({ name: "feedback", consistency: "strong" });

  // ---- public: customer
  if (a === "check" && req.method === "POST") {
    const phone = normPhone((await body(req)).phone);
    if (!phone) return json({ jobs: [] });
    const jobs = (await all(s, "job/")).filter((j) => j.phone === phone && !j.blocked && !j.rated)
      .map((j) => ({ id: j.id, job: j.job, team: j.team, date: j.date }));
    return json({ jobs });
  }
  if (a === "submit" && req.method === "POST") {
    const b = await body(req), phone = normPhone(b.phone);
    const key = "job/" + String(b.jobId || "").replace(/[^A-Za-z0-9_-]/g, "");
    const job = await s.get(key, { type: "json" });
    if (!job || !phone || job.phone !== phone || job.blocked) return json({ error: "not-found" }, 404);
    if (job.rated) return json({ error: "already-rated" }, 409);
    const data = {};
    for (const k of QUESTIONS) { if (!SCORES.includes(String(b[k]))) return json({ error: "missing " + k }, 400); data[k] = String(b[k]); }
    const nps = parseInt(b.nps, 10);
    if (!(nps >= 0 && nps <= 10)) return json({ error: "missing nps" }, 400);
    data.nps = String(nps);
    data.name = txt(b.name, 120); data.comment = txt(b.comment, 2000); data.language = txt(b.language, 20);
    if (!data.name) return json({ error: "missing name" }, 400);
    const id = newId();
    await s.setJSON("fb/" + id, { id, created: new Date().toISOString(), jobId: job.id, job: job.job, team: job.team, phone, data });
    job.rated = id; job.ratedAt = new Date().toISOString();
    await s.setJSON(key, job);
    return json({ ok: true });
  }

  // ---- admin
  if (!isAdmin(req)) return json({ error: "Admin password is not right." }, 401);

  if (a === "list") {
    const items = await all(s, "fb/"), jobs = await all(s, "job/");
    return json({ items, jobs, teams: scorecards(items) });
  }
  if (a === "jobset" && req.method === "POST") {
    const b = await body(req), key = "job/" + String(b.id || "").replace(/[^A-Za-z0-9_-]/g, "");
    const job = await s.get(key, { type: "json" });
    if (!job) return json({ error: "not found" }, 404);
    if ("blocked" in b) job.blocked = !!b.blocked;
    if ("paid" in b) {
      if (b.paid && !(job.rated && job.source === "report")) return json({ error: "Payment needs both the job report and the customer's feedback." }, 400);
      job.paid = b.paid ? new Date().toISOString() : null;
    }
    await s.setJSON(key, job);
    return json({ ok: true });
  }
  if (a === "jobdel" && req.method === "POST") {
    const id = String((await body(req)).id || "").replace(/[^A-Za-z0-9_-]/g, "");
    const job = await s.get("job/" + id, { type: "json" });
    if (job) for (const f of job.files || []) await s.delete(`file/${id}/${f}`);
    await s.delete("job/" + id);
    return json({ ok: true });
  }
  if (a === "delete" && req.method === "POST") {
    const id = String((await body(req)).id || "").replace(/[^A-Za-z0-9_-]/g, "");
    const fb = await s.get("fb/" + id, { type: "json" });
    if (fb && fb.jobId) {
      const job = await s.get("job/" + fb.jobId, { type: "json" });
      if (job && job.rated === id) { job.rated = null; await s.setJSON("job/" + fb.jobId, job); }
    }
    await s.delete("fb/" + id);
    return json({ ok: true });
  }
  if (a === "file") {
    const id = String(u.searchParams.get("id") || "").replace(/[^A-Za-z0-9_-]/g, ""), f = String(u.searchParams.get("f") || "").replace(/[^A-Za-z0-9_-]/g, "");
    const r = await s.getWithMetadata(`file/${id}/${f}`, { type: "arrayBuffer" });
    if (!r) return new Response("not found", { status: 404 });
    return new Response(r.data, { headers: { "content-type": (r.metadata && r.metadata.type) || "application/octet-stream", "cache-control": "no-store" } });
  }
  return json({ error: "unknown action" }, 400);
};

export const config = { path: "/api/feedback" };
