// Installer locations, so Solar ESS can find and notify installers near a job.
//   POST /api/installers?a=update  (public)  {phone, name, subdistrict, district, province, lat, lng, radius, line, email, contact, consent, website(honeypot)}
//   GET  /api/installers?a=list    (admin)   -> {items}
//   POST /api/installers?a=set     (admin)   {key, note?, active?}
//   POST /api/installers?a=delete  (admin)   {key}
// Records live in Netlify Blobs store "installers", keyed by the phone number's digits.
// TSIA membership and installer-partner registrations are upserted by submission-created.mjs.
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
export const phoneKey = (p) => { let d = String(p || "").replace(/\D/g, ""); if (d.startsWith("66") && d.length === 11) d = "0" + d.slice(2); return d.length >= 9 && d.length <= 12 ? d : ""; };
const str = (v, n = 120) => String(v == null ? "" : v).replace(/[\u0000-\u001f<>]/g, " ").trim().slice(0, n);
const num = (v, lo, hi) => { const x = parseFloat(v); return Number.isFinite(x) && x >= lo && x <= hi ? Math.round(x * 1e5) / 1e5 : null; };

export async function upsertInstaller(input, source) {
  const key = phoneKey(input.phone);
  if (!key) return null;
  const s = getStore({ name: "installers", consistency: "strong" });
  const old = (await s.get("i/" + key, { type: "json" })) || { key, created: new Date().toISOString(), sources: [], history: [], active: true, note: "" };
  const lat = num(input.lat, 5, 21), lng = num(input.lng, 97, 106);
  const loc = { subdistrict: str(input.subdistrict, 60), district: str(input.district, 60), province: str(input.province, 60), lat, lng };
  const moved = ["subdistrict", "district", "province", "lat", "lng"].some((k) => loc[k] && loc[k] !== old[k]);
  if (moved && (old.province || old.lat)) old.history = [{ at: old.updated, subdistrict: old.subdistrict, district: old.district, province: old.province, lat: old.lat, lng: old.lng }, ...(old.history || [])].slice(0, 5);
  const rec = { ...old, phone: str(input.phone, 20) || old.phone };
  for (const k of ["name", "line", "email", "contact"]) if (str(input[k])) rec[k] = str(input[k], 80);
  if (loc.province && loc.province !== old.province) {   // moved province: drop old area details
    rec.subdistrict = loc.subdistrict; rec.district = loc.district;
    if (lat == null) { delete rec.lat; delete rec.lng; }
  }
  for (const k of ["subdistrict", "district", "province"]) if (loc[k]) rec[k] = loc[k];
  if (lat != null && lng != null) { rec.lat = lat; rec.lng = lng; }
  const r = parseInt(input.radius, 10); if (r >= 5 && r <= 1000) rec.radius = r;
  if (source && !rec.sources.includes(source)) rec.sources = [...rec.sources, source];
  rec.updated = new Date().toISOString();
  await s.setJSON("i/" + key, rec);
  return rec;
}

export default async (req) => {
  const u = new URL(req.url), a = u.searchParams.get("a");
  if (a === "update" && req.method === "POST") {
    let b; try { b = await req.json(); } catch { return json({ error: "bad body" }, 400); }
    if (b.website) return json({ ok: true });            // honeypot: pretend success
    if (!phoneKey(b.phone)) return json({ error: "phone" }, 400);
    if (!str(b.province) && num(b.lat, 5, 21) == null) return json({ error: "location" }, 400);
    if (!b.consent) return json({ error: "consent" }, 400);
    const rec = await upsertInstaller(b, "location-page");
    return json({ ok: true, updated: rec.updated });
  }
  if (!isAdmin(req)) return json({ error: "401" }, 401);
  const s = getStore({ name: "installers", consistency: "strong" });
  if (a === "list") {
    const { blobs } = await s.list({ prefix: "i/" });
    const items = (await Promise.all(blobs.map((x) => s.get(x.key, { type: "json" })))).filter(Boolean);
    items.sort((x, y) => String(y.updated).localeCompare(String(x.updated)));
    return json({ items });
  }
  if (req.method !== "POST") return json({ error: "method" }, 405);
  let b; try { b = await req.json(); } catch { return json({ error: "bad body" }, 400); }
  const key = phoneKey(b.key);
  if (!key) return json({ error: "key" }, 400);
  if (a === "delete") { await s.delete("i/" + key); return json({ ok: true }); }
  if (a === "set") {
    const rec = await s.get("i/" + key, { type: "json" });
    if (!rec) return json({ error: "404" }, 404);
    if (typeof b.note === "string") rec.note = b.note.slice(0, 1000);
    if (typeof b.active === "boolean") rec.active = b.active;
    await s.setJSON("i/" + key, rec);
    return json({ ok: true });
  }
  return json({ error: "unknown action" }, 400);
};
export const config = { path: "/api/installers" };
