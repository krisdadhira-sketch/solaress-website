// Private company documents for the admin area. Nothing here is public.
// Admin (header "x-admin-password", same password as all admin pages):
//   GET /api/docs?a=insurance      -> {html} CAR insurance policy summary
//   GET /api/docs?a=insurance-pdf  -> the scanned policy PDF
import crypto from "node:crypto";
import summary from "./summary.json" with { type: "json" };
import policy from "./policy.json" with { type: "json" };

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

export default async (req) => {
  if (!isAdmin(req)) return json({ error: "401" }, 401);
  const a = new URL(req.url).searchParams.get("a");
  if (a === "insurance") return json({ html: summary.html, pdf: policy.name });
  if (a === "insurance-pdf") return new Response(Buffer.from(policy.b64, "base64"), { headers: { "content-type": "application/pdf", "content-disposition": `attachment; filename="${policy.name}"`, "cache-control": "no-store" } });
  return json({ error: "unknown action" }, 400);
};
export const config = { path: "/api/docs" };
