// Admin sign-in cookie for admin-only static files (Monthly Report pages, report PDFs and images).
//   POST   /api/admin-session {password}  -> sets cookie "ss_admin" (12 hours), same password as all admin pages
//   DELETE /api/admin-session             -> signs out
// The cookie is "<expiry>.<HMAC>" signed with a key derived from the admin password set in Netlify
// (ADMIN_SESSION_SECRET, else MEMBERS_ADMIN_PASSWORD, else VOCAB_ADMIN_PASSWORD). The edge function
// netlify/edge-functions/admin-gate.js checks it. Nothing is signed if no password is set (fails closed).
import crypto from "node:crypto";

const VOCAB_ADMIN_HASH = "162cdaefe4e9558d229a4846cd021775:5c036e020b55e8727a91b98d8e554c7456200d65599147cff4efea07459dc0fd";
const json = (b, s = 200, h = {}) => new Response(JSON.stringify(b), { status: s, headers: { "content-type": "application/json", "cache-control": "no-store", ...h } });
function eq(a, b) { a = Buffer.from(String(a)); b = Buffer.from(String(b)); return a.length === b.length && crypto.timingSafeEqual(a, b); }
function checkHash(pw, stored) {
  const [salt, h] = stored.split(":");
  const got = crypto.scryptSync(String(pw), salt, 32), want = Buffer.from(h, "hex");
  return got.length === want.length && crypto.timingSafeEqual(got, want);
}
function isAdminPw(pw) {
  pw = String(pw || "").trim(); if (!pw) return false;
  const mp = String(process.env.MEMBERS_ADMIN_PASSWORD || "").trim(), vp = String(process.env.VOCAB_ADMIN_PASSWORD || "").trim();
  if (mp) return eq(pw, mp);
  if (vp) return eq(pw, vp);
  return checkHash(pw, VOCAB_ADMIN_HASH);
}
const secret = () => String(process.env.ADMIN_SESSION_SECRET || process.env.MEMBERS_ADMIN_PASSWORD || process.env.VOCAB_ADMIN_PASSWORD || "").trim();
function sign(exp, s) {
  const key = crypto.createHash("sha256").update("solaress-admin-session|" + s).digest();
  return crypto.createHmac("sha256", key).update(String(exp)).digest("hex");
}
const HOURS = 12;

export default async (req) => {
  if (req.method === "DELETE") return json({ ok: true }, 200, { "set-cookie": "ss_admin=; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=0" });
  if (req.method !== "POST") return json({ error: "method" }, 405);
  let b = {}; try { b = await req.json(); } catch { }
  if (!isAdminPw(b.password)) return json({ error: "401" }, 401);
  const s = secret();
  if (!s) return json({ error: "Admin password is not set in Netlify (MEMBERS_ADMIN_PASSWORD)" }, 503);
  const exp = Math.floor(Date.now() / 1000) + HOURS * 3600;
  return json({ ok: true, hours: HOURS }, 200, { "set-cookie": `ss_admin=${exp}.${sign(exp, s)}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${HOURS * 3600}` });
};
export const config = { path: "/api/admin-session" };
