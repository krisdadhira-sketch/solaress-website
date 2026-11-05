// Customer satisfaction feedback: team scorecards (admin only).
// Submissions arrive through submission-created.mjs (form "job-feedback") into store "feedback".
//   GET  /api/feedback?a=list            -> {items:[...], teams:[scorecard...]}
//   POST /api/feedback?a=delete {id}     -> remove one response (e.g. a test or spam)
// Header "x-admin-password": same password as /members-admin.html.
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

const QUESTIONS = ["q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10"];
const GROUPS = { work: ["q1", "q2", "q3", "q4", "q5"], personality: ["q6", "q7", "q8"], interaction: ["q9", "q10"] };
const n = (v) => { const x = parseFloat(v); return isFinite(x) ? x : null; };
const avg = (a) => a.length ? Math.round((a.reduce((s, x) => s + x, 0) / a.length) * 100) / 100 : null;
const teamOf = (d) => String(d["team-other"] || d.team || "Not stated").trim() || "Not stated";

function scorecards(items) {
  const by = {};
  for (const it of items) (by[teamOf(it.data)] ||= []).push(it);
  return Object.entries(by).map(([team, rs]) => {
    const q = {}; for (const k of QUESTIONS) q[k] = avg(rs.map((r) => n(r.data[k])).filter((x) => x != null));
    const g = {}; for (const [name, ks] of Object.entries(GROUPS)) g[name] = avg(ks.map((k) => q[k]).filter((x) => x != null));
    const all = rs.flatMap((r) => QUESTIONS.map((k) => n(r.data[k])).filter((x) => x != null));
    const nps = rs.map((r) => n(r.data.nps)).filter((x) => x != null);
    const pro = nps.filter((x) => x >= 9).length, det = nps.filter((x) => x <= 6).length;
    const more = rs.map((r) => String(r.data["more-business"] || ""));
    return {
      team, responses: rs.length, overall: avg(all), groups: g, questions: q,
      nps: nps.length ? Math.round(((pro - det) / nps.length) * 100) : null, promoters: pro, passives: nps.length - pro - det, detractors: det,
      more_business: { job: more.filter((m) => m === "yes-job").length, referral: more.filter((m) => m === "yes-referral").length, maybe: more.filter((m) => m === "maybe").length, no: more.filter((m) => m === "no").length },
      last: rs.map((r) => r.created).sort().pop(),
    };
  }).sort((a, b) => (b.overall ?? 0) - (a.overall ?? 0));
}

export default async (req) => {
  if (!isAdmin(req)) return json({ error: "Admin password is not right." }, 401);
  const u = new URL(req.url), a = u.searchParams.get("a");
  const s = getStore({ name: "feedback", consistency: "strong" });
  if (a === "list") {
    const { blobs } = await s.list({ prefix: "fb/" });
    const items = [];
    for (const b of blobs) { const v = await s.get(b.key, { type: "json" }); if (v) items.push(v); }
    items.sort((x, y) => String(y.created).localeCompare(String(x.created)));
    return json({ items, teams: scorecards(items) });
  }
  if (a === "delete" && req.method === "POST") {
    let b = {}; try { b = await req.json(); } catch {}
    await s.delete("fb/" + String(b.id || "").replace(/[^A-Za-z0-9_-]/g, ""));
    return json({ ok: true });
  }
  return json({ error: "unknown action" }, 400);
};

export const config = { path: "/api/feedback" };
