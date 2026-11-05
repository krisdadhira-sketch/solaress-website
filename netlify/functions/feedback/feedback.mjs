// Finished jobs: admin-issued codes, installer job report, customer feedback, payment release, team scorecards.
//
// Flow (all in Blobs store "feedback"):
//  1. Admin creates a job at /feedback-admin.html -> two one-time codes: one for the installer team, one for the customer.
//  2. Installer opens /job-report.html?c=<code> and sends the report (Netlify form "job-report"; submission-created.mjs
//     attaches it to the job only if the code is a valid, unused installer code).
//  3. Customer opens /feedback.html?c=<code> and rates the job once (10 questions 5/4/2/1, NPS 0-10) via a=submit below.
//  4. When both are in and Solar ESS is satisfied, the admin clicks "Release payment".
// Only feedback tied to a job counts in the team record; the team comes from the job the admin created.
//
// Public:
//   POST /api/feedback?a=code   {code}            -> {role: "installer"|"customer", job, team, used}
//   POST /api/feedback?a=submit {code, q1..q10, nps, name, comment, language}   (customer code)
// Admin (header "x-admin-password", same password as /members-admin.html):
//   GET  /api/feedback?a=list                                   -> {items, jobs, teams}
//   POST /api/feedback?a=create {job, team, customer, phone}    -> {job} with codes
//   POST /api/feedback?a=jobset {id, released?, blocked?}       release payment (needs report + feedback) / cancel
//   POST /api/feedback?a=jobdel {id}                            delete a job, its codes, files and feedback
//   POST /api/feedback?a=delete {id}                            delete one feedback (the customer code works again)
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

const ALPHA = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"; // no 0/O, 1/I/L
const makeCode = () => Array.from(crypto.randomBytes(7), (b) => ALPHA[b % ALPHA.length]).join("");
const cleanCode = (v) => String(v || "").toUpperCase().replace(/[^A-Z0-9]/g, "").slice(0, 12);
const cleanId = (v) => String(v || "").replace(/[^A-Za-z0-9_-]/g, "");
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
async function byCode(s, code) {
  const c = cleanCode(code);
  if (c.length < 6) return null;
  const ref = await s.get("code/" + c, { type: "json" });
  if (!ref) return null;
  const job = await s.get("job/" + ref.jobId, { type: "json" });
  return job ? { role: ref.role, job } : null;
}

function scorecards(items) {
  const by = {};
  for (const it of items) if (it.jobId) (by[it.team || "Not stated"] ||= []).push(it);
  return Object.entries(by).map(([team, rs]) => {
    const q = {}; for (const k of QUESTIONS) q[k] = avg(rs.map((r) => n(r.data[k])).filter((x) => x != null));
    const g = {}; for (const [name, ks] of Object.entries(GROUPS)) g[name] = avg(ks.map((k) => q[k]).filter((x) => x != null));
    const allv = rs.flatMap((r) => QUESTIONS.map((k) => n(r.data[k])).filter((x) => x != null));
    const nps = rs.map((r) => n(r.data.nps)).filter((x) => x != null);
    const pro = nps.filter((x) => x >= 9).length, det = nps.filter((x) => x <= 6).length;
    return {
      team, responses: rs.length, overall: avg(allv), groups: g, questions: q,
      nps: nps.length ? Math.round(((pro - det) / nps.length) * 100) : null, promoters: pro, passives: nps.length - pro - det, detractors: det,
      last: rs.map((r) => r.created).sort().pop(),
    };
  }).sort((a, b) => (b.overall ?? 0) - (a.overall ?? 0));
}

async function body(req) { try { return await req.json(); } catch { return {}; } }

export default async (req) => {
  const u = new URL(req.url), a = u.searchParams.get("a");
  const s = getStore({ name: "feedback", consistency: "strong" });

  // ---- public: installer or customer with a code
  if (a === "code" && req.method === "POST") {
    const r = await byCode(s, (await body(req)).code);
    if (!r || r.job.cancelled) return json({ error: "not-found" }, 404);
    const used = r.role === "installer" ? !!r.job.report : !!r.job.rated;
    return json({ role: r.role, job: r.job.job, team: r.job.team, used });
  }
  if (a === "submit" && req.method === "POST") {
    const b = await body(req);
    const r = await byCode(s, b.code);
    if (!r || r.role !== "customer" || r.job.cancelled) return json({ error: "not-found" }, 404);
    const job = r.job;
    if (job.rated) return json({ error: "already-rated" }, 409);
    const data = {};
    for (const k of QUESTIONS) { if (!SCORES.includes(String(b[k]))) return json({ error: "missing " + k }, 400); data[k] = String(b[k]); }
    const nps = parseInt(b.nps, 10);
    if (!(nps >= 0 && nps <= 10)) return json({ error: "missing nps" }, 400);
    data.nps = String(nps);
    data.name = txt(b.name, 120); data.comment = txt(b.comment, 2000); data.language = txt(b.language, 20);
    if (!data.name) return json({ error: "missing name" }, 400);
    const id = newId();
    await s.setJSON("fb/" + id, { id, created: new Date().toISOString(), jobId: job.id, job: job.job, team: job.team, data });
    job.rated = id; job.ratedAt = new Date().toISOString();
    await s.setJSON("job/" + job.id, job);
    return json({ ok: true });
  }

  // ---- admin
  if (!isAdmin(req)) return json({ error: "Admin password is not right." }, 401);

  if (a === "list") {
    const items = await all(s, "fb/"), jobs = await all(s, "job/");
    return json({ items, jobs, teams: scorecards(items) });
  }
  if (a === "create" && req.method === "POST") {
    const b = await body(req);
    if (!txt(b.job) || !txt(b.team)) return json({ error: "Job and team are needed." }, 400);
    const id = newId();
    let ci, cc;
    do { ci = makeCode(); } while (await s.get("code/" + ci));
    do { cc = makeCode(); } while (cc === ci || await s.get("code/" + cc));
    const job = { id, created: new Date().toISOString(), job: txt(b.job), team: txt(b.team, 120),
      customer: txt(b.customer, 120), phone: txt(b.phone, 30), codes: { installer: ci, customer: cc },
      report: null, rated: null, released: null, cancelled: false };
    await s.setJSON("code/" + ci, { jobId: id, role: "installer" });
    await s.setJSON("code/" + cc, { jobId: id, role: "customer" });
    await s.setJSON("job/" + id, job);
    return json({ ok: true, job });
  }
  if (a === "jobset" && req.method === "POST") {
    const b = await body(req), key = "job/" + cleanId(b.id);
    const job = await s.get(key, { type: "json" });
    if (!job) return json({ error: "not found" }, 404);
    if ("cancelled" in b) job.cancelled = !!b.cancelled;
    if ("released" in b) {
      if (b.released && !(job.report && job.rated)) return json({ error: "Payment can be released only when both the job report and the customer's feedback are in." }, 400);
      job.released = b.released ? new Date().toISOString() : null;
    }
    await s.setJSON(key, job);
    return json({ ok: true });
  }
  if (a === "jobdel" && req.method === "POST") {
    const id = cleanId((await body(req)).id);
    const job = await s.get("job/" + id, { type: "json" });
    if (job) {
      for (const f of (job.report && job.report.files) || []) await s.delete(`file/${id}/${f}`);
      for (const c of Object.values(job.codes || {})) await s.delete("code/" + c);
      if (job.rated) await s.delete("fb/" + job.rated);
    }
    await s.delete("job/" + id);
    return json({ ok: true });
  }
  if (a === "delete" && req.method === "POST") {
    const id = cleanId((await body(req)).id);
    const fb = await s.get("fb/" + id, { type: "json" });
    if (fb && fb.jobId) {
      const job = await s.get("job/" + fb.jobId, { type: "json" });
      if (job && job.rated === id) { job.rated = null; job.released = null; await s.setJSON("job/" + fb.jobId, job); }
    }
    await s.delete("fb/" + id);
    return json({ ok: true });
  }
  if (a === "file") {
    const id = cleanId(u.searchParams.get("id")), f = cleanId(u.searchParams.get("f"));
    const r = await s.getWithMetadata(`file/${id}/${f}`, { type: "arrayBuffer" });
    if (!r) return new Response("not found", { status: 404 });
    return new Response(r.data, { headers: { "content-type": (r.metadata && r.metadata.type) || "application/octet-stream", "cache-control": "no-store" } });
  }
  return json({ error: "unknown action" }, 400);
};

export const config = { path: "/api/feedback" };
