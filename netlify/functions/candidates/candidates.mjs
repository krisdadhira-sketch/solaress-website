// Candidate ranking for the Jobs platform (admin only, same password as all admin pages, header "x-admin-password").
//   GET  /api/candidates?a=list            -> {jobs:[{job, jobId, count, rows:[...]}], ai:boolean}
//   POST /api/candidates?a=ai  {limit?}    -> AI reads up to `limit` written proposals not yet read (needs ANTHROPIC_API_KEY)
//   POST /api/candidates?a=set {id,status} -> same statuses as the inbox (new, contacted, in-progress, done, archived)
// Applications live in the inbox store (copied there by submission-created.mjs); this endpoint only reads, ranks and
// adds an `ai` note to each item.
import crypto from "node:crypto";
import { getStore } from "@netlify/blobs";
import { rankJob, MAX } from "./score.mjs";

const VOCAB_ADMIN_HASH = "162cdaefe4e9558d229a4846cd021775:5c036e020b55e8727a91b98d8e554c7456200d65599147cff4efea07459dc0fd";
const STATUSES = ["new", "contacted", "in-progress", "done", "archived"];
const AI_MODEL = process.env.CANDIDATES_AI_MODEL || "claude-haiku-5-5";
const json = (b, s = 200) => new Response(JSON.stringify(b), { status: s, headers: { "content-type": "application/json", "cache-control": "no-store" } });
function eq(a, b) { a = Buffer.from(String(a)); b = Buffer.from(String(b)); return a.length === b.length && crypto.timingSafeEqual(a, b); }
function checkHash(pw, stored) { const [salt, h] = stored.split(":"); const got = crypto.scryptSync(String(pw), salt, 32), want = Buffer.from(h, "hex"); return got.length === want.length && crypto.timingSafeEqual(got, want); }
function isAdmin(req) {
  const pw = String(req.headers.get("x-admin-password") || "").trim(); if (!pw) return false;
  const mp = String(process.env.MEMBERS_ADMIN_PASSWORD || "").trim(), vp = String(process.env.VOCAB_ADMIN_PASSWORD || "").trim();
  if (mp) return eq(pw, mp); if (vp) return eq(pw, vp); return checkHash(pw, VOCAB_ADMIN_HASH);
}
const clean = (s) => String(s || "").replace(/[^A-Za-z0-9_-]/g, "");

async function applications(s) {
  const { blobs } = await s.list({ prefix: "sub/" });
  const items = (await Promise.all(blobs.map((b) => s.get(b.key, { type: "json" })))).filter((x) => x && x.form === "job-application");
  return items;
}

const PUBLIC_FIELDS = ["name", "phone", "email", "province", "company-name", "position", "job-id", "price-labour-only", "price-labour-materials",
  "start-date", "days-needed", "distance-km", "experience-years", "installs-completed", "largest-system-kwp", "team-size", "electrician-level", "solar-test-level"];

export default async (req) => {
  if (!isAdmin(req)) return json({ error: "401" }, 401);
  const s = getStore({ name: "inbox", consistency: "strong" });
  const u = new URL(req.url), a = u.searchParams.get("a");
  if (a === "list") {
    const items = await applications(s), groups = {};
    for (const it of items) { const d = it.data || {}; const k = d["job-id"] || d.position || "Open application"; (groups[k] ||= { jobId: d["job-id"] || "", job: d.position || k, items: [] }).items.push(it); }
    const jobs = Object.values(groups).map((g) => ({
      job: g.job, jobId: g.jobId, count: g.items.length,
      latest: g.items.map((i) => i.created).sort().pop(),
      rows: rankJob(g.items).map((r) => ({
        id: r.it.id, created: r.it.created, status: r.it.status, note: r.it.note || "",
        position: r.position, tier: r.tier, rank: r.rank, score: r.s.total, parts: r.s.parts, missing: r.s.missing, eligible: r.s.eligible,
        price: r.price, priceScore: r.priceScore, ai: r.it.ai || null,
        data: Object.fromEntries(PUBLIC_FIELDS.map((f) => [f, (r.it.data || {})[f] ?? ""])), proposal: String((r.it.data || {}).proposal || "").slice(0, 2000),
      })),
    })).sort((x, y) => String(y.latest).localeCompare(String(x.latest)));
    return json({ jobs, max: MAX, ai: !!process.env.ANTHROPIC_API_KEY });
  }
  if (req.method !== "POST") return json({ error: "unknown action" }, 400);
  let b = {}; try { b = await req.json(); } catch {}
  if (a === "set") {
    const id = clean(b.id), key = "sub/" + id, item = id ? await s.get(key, { type: "json" }) : null;
    if (!item) return json({ error: "not found" }, 404);
    if (!STATUSES.includes(b.status)) return json({ error: "bad status" }, 400);
    item.status = b.status; item.updated = new Date().toISOString(); await s.setJSON(key, item);
    return json({ ok: true });
  }
  if (a === "ai") {
    const key = process.env.ANTHROPIC_API_KEY;
    if (!key) return json({ error: "Set ANTHROPIC_API_KEY in Netlify environment variables to turn on the AI read." }, 400);
    const limit = Math.min(10, Math.max(1, parseInt(b.limit) || 5));
    const todo = (await applications(s)).filter((it) => !it.ai && String((it.data || {}).proposal || "").trim()).slice(0, limit);
    let done = 0;
    for (const it of todo) {
      const d = it.data || {};
      const prompt = `You screen solar installer applications for Solar ESS (Thailand). Read the job and the installer's written proposal and answer ONLY with JSON {"adjust":n,"summary":"..."} where adjust is an integer from -5 (vague, off-scope, unsafe or copied text) to +5 (specific method, correct materials and sizes, realistic team and days), and summary is one short line in Thai and English saying why.\n\nJOB: ${String(d.position || "").slice(0, 300)}\nPRICES (THB): labour only ${d["price-labour-only"] || "-"}, labour+materials ${d["price-labour-materials"] || "-"}\nTEAM: ${d["team-size"] || "-"} technicians, ${d["days-needed"] || "-"} days\nPROPOSAL:\n${String(d.proposal).slice(0, 3000)}\nOTHER NOTES:\n${String(d.message || "").slice(0, 800)}`;
      try {
        const r = await fetch("https://api.anthropic.com/v1/messages", { method: "POST", headers: { "x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json" },
          body: JSON.stringify({ model: AI_MODEL, max_tokens: 200, messages: [{ role: "user", content: prompt }] }) });
        const j = await r.json(); const txt = (j.content || []).map((c) => c.text || "").join("");
        const m = txt.match(/\{[\s\S]*\}/); const o = m ? JSON.parse(m[0]) : null;
        if (!o) continue;
        it.ai = { adjust: Math.max(-5, Math.min(5, Math.round(Number(o.adjust) || 0))), summary: String(o.summary || "").slice(0, 300), model: AI_MODEL, at: new Date().toISOString() };
        await s.setJSON("sub/" + clean(it.id), it); done++;
      } catch { /* skip this one; try again next time */ }
    }
    return json({ ok: true, read: done, waiting: Math.max(0, todo.length - done) });
  }
  return json({ error: "unknown action" }, 400);
};
export const config = { path: "/api/candidates" };
