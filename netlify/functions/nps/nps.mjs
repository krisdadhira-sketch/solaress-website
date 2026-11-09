// Reader NPS for www.solaress.org: "How likely are you to recommend Solar ESS to a friend or colleague?" 1–10.
// One score per visitor network address (IP) per calendar month (Bangkok time). The IP is never stored in clear:
// only a salted hash, which cannot be turned back into the address.
//   GET  /api/nps?a=status              (public) -> {done, month}
//   POST /api/nps                       (public) {score 1-10, comment?, lang?, page?, website (honeypot)} -> {ok} | 409 {done}
//   GET  /api/nps?a=list[&month=YYYY-MM] (admin, header x-admin-password) -> {items, months, total}
//   POST /api/nps?a=delete              (admin) {key}
//   GET  /api/nps?a=score               (public) -> {nps, n, avg, since} over the last 12 months (CDN-cached 5 min)
// NPS = % promoters (9–10) − % detractors (1–6), from −100 to +100. Passives: 7–8.
// Records live in Netlify Blobs store "nps", keyed "<YYYY-MM>/<ip hash>".
import crypto from "node:crypto";
import { getStore } from "@netlify/blobs";

const VOCAB_ADMIN_HASH = "162cdaefe4e9558d229a4846cd021775:5c036e020b55e8727a91b98d8e554c7456200d65599147cff4efea07459dc0fd";
const json = (b, s = 200) => new Response(JSON.stringify(b), { status: s, headers: { "content-type": "application/json", "cache-control": "no-store" } });
function eq(a, b) { a = Buffer.from(String(a)); b = Buffer.from(String(b)); return a.length === b.length && crypto.timingSafeEqual(a, b); }
function checkHash(pw, stored) {
  const [salt, h] = stored.split(":");
  const got = crypto.scryptSync(String(pw), salt, 32), want = Buffer.from(h, "hex");
  return got.length === want.length && crypto.timingSafeEqual(got, want);
}
function isAdmin(req) {
  const pw = String(req.headers.get("x-admin-password") || "").trim();
  if (!pw) return false;
  const mp = String(process.env.MEMBERS_ADMIN_PASSWORD || "").trim(), vp = String(process.env.VOCAB_ADMIN_PASSWORD || "").trim();
  if (mp) return eq(pw, mp);
  if (vp) return eq(pw, vp);
  return checkHash(pw, VOCAB_ADMIN_HASH);
}
const str = (v, n = 120) => String(v == null ? "" : v).replace(/[\u0000-\u0008\u000b-\u001f<>]/g, " ").trim().slice(0, n);
const month = () => new Date(Date.now() + 7 * 3600e3).toISOString().slice(0, 7); // Asia/Bangkok, UTC+7
const group = (s) => (s >= 9 ? "promoter" : s >= 7 ? "passive" : "detractor");
function stats(list) {
  const n = list.length, p = list.filter((x) => x.score >= 9).length, d = list.filter((x) => x.score <= 6).length;
  return { n, promoters: p, passives: n - p - d, detractors: d, nps: n ? Math.round(((p - d) / n) * 100) : null,
    avg: n ? Math.round((list.reduce((a, x) => a + x.score, 0) / n) * 10) / 10 : null };
}

export default async (req, context) => {
  const url = new URL(req.url), a = url.searchParams.get("a") || "";
  const store = getStore({ name: "nps", consistency: "strong" });
  const ip = context.ip || req.headers.get("x-nf-client-connection-ip") || "";
  const salt = process.env.NPS_SALT || "solaress-nps-v1";
  const h = crypto.createHash("sha256").update(`${ip}|${salt}`).digest("hex").slice(0, 32);
  const m = month(), key = `${m}/${h}`;

  if (req.method === "GET" && a === "status") {
    return json({ done: !!(ip && (await store.get(key))), month: m });
  }

  if (req.method === "POST" && !a) {
    if (!ip) return json({ error: "no address" }, 400);
    let b = {};
    try { b = await req.json(); } catch (e) {}
    if (b.website) return json({ ok: true }); // bot honeypot
    const score = parseInt(b.score, 10);
    if (!(score >= 1 && score <= 10)) return json({ error: "score must be 1–10" }, 400);
    if (await store.get(key)) return json({ done: true, month: m }, 409);
    const rec = { score, group: group(score), comment: str(b.comment, 600), lang: str(b.lang, 5), page: str(b.page, 120), at: new Date().toISOString(), month: m };
    await store.setJSON(key, rec);
    return json({ ok: true, month: m });
  }

  if (req.method === "GET" && a === "score") {
    // Public headline score for the home page: last 12 months (this month and the 11 before it).
    const months = [];
    for (let i = 0; i < 12; i++) { const d = new Date(Date.now() + 7 * 3600e3); d.setUTCDate(1); d.setUTCMonth(d.getUTCMonth() - i); months.push(d.toISOString().slice(0, 7)); }
    const lists = await Promise.all(months.map((mo) => store.list({ prefix: mo + "/" })));
    const keys = lists.flatMap((l) => l.blobs.map((x) => x.key));
    const recs = (await Promise.all(keys.map((k) => store.get(k, { type: "json" })))).filter(Boolean);
    const t = stats(recs);
    return new Response(JSON.stringify({ nps: t.nps, n: t.n, avg: t.avg, promoters: t.promoters, detractors: t.detractors, since: months[11] }), {
      status: 200, headers: { "content-type": "application/json", "cache-control": "public, max-age=60", "netlify-cdn-cache-control": "public, s-maxage=300, stale-while-revalidate=600" } });
  }

  if (a === "list" || a === "delete") {
    if (!isAdmin(req)) return json({ error: "401" }, 401);
    if (a === "delete" && req.method === "POST") {
      let b = {};
      try { b = await req.json(); } catch (e) {}
      if (!/^\d{4}-\d{2}\/[0-9a-f]{32}$/.test(String(b.key || ""))) return json({ error: "bad key" }, 400);
      await store.delete(b.key);
      return json({ ok: true });
    }
    const only = url.searchParams.get("month") || "";
    const { blobs } = await store.list(only ? { prefix: only + "/" } : {});
    const items = (await Promise.all(blobs.map(async (x) => {
      const r = await store.get(x.key, { type: "json" });
      return r ? { key: x.key, ...r } : null;
    }))).filter(Boolean).sort((x, y) => (x.at < y.at ? 1 : -1));
    const byMonth = {};
    for (const it of items) (byMonth[it.month] = byMonth[it.month] || []).push(it);
    const months = Object.keys(byMonth).sort().reverse().map((k) => ({ month: k, ...stats(byMonth[k]) }));
    return json({ items, months, total: stats(items) });
  }

  return json({ error: "method" }, 405);
};

export const config = { path: "/api/nps" };
