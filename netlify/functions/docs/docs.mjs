// Private company documents for the admin area. Nothing here is public.
// Admin (header "x-admin-password", same password as all admin pages):
//   GET /api/docs?a=insurance      -> {html} CAR insurance policy summary
//   GET /api/docs?a=insurance-pdf  -> the scanned policy PDF
//   GET  /api/docs?a=plants        -> plant code register (code -> plant name, platform IDs); base list + plants added in admin
//   POST /api/docs?a=plant-add     -> {platform,type,postcode,inv_kw,name,...} generates the next free code and saves it
//   POST /api/docs?a=plant-del     -> {code} removes a plant added in admin (base SolisCloud list is fixed in plants.json)
import crypto from "node:crypto";
import summary from "./summary.json" with { type: "json" };
import policy from "./policy.json" with { type: "json" };
import plants from "./plants.json" with { type: "json" };
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


const PLAT = { S: "SolisCloud", D: "DeyeCloud", H: "Huawei FusionSolar", E: "SolarEdge", N: "Enphase", A: "ATMOCE" };
const store = () => getStore({ name: "plant-codes", consistency: "strong" });
async function added() { return (await store().get("added", { type: "json" })) || []; }
function codeBase(p) {
  const pf = String(p.platform || "").toUpperCase(), ty = String(p.type || "").toUpperCase();
  const pc = String(p.postcode || "").toUpperCase().replace(/\s+/g, ""), kw = Math.round(Number(p.inv_kw));
  if (!PLAT[pf]) throw new Error("Platform must be S, D, H, E, N or A");
  if (!["G", "H", "O"].includes(ty)) throw new Error("Type must be G, H or O");
  if (!/^(\d{5}|[A-Z]{5})$/.test(pc)) throw new Error("Postcode must be 5 digits (or 5 letters outside Thailand, e.g. LAVTE)");
  if (!(kw > 0 && kw < 1000)) throw new Error("Inverter kW must be a number");
  return `${pf}${ty}-${pc}-${String(kw).padStart(2, "0")}`;
}
async function plantsAll() { return [...plants.items.map(x => ({ ...x, platform: "SolisCloud", source: "register" })), ...(await added())]; }

export default async (req) => {
  if (!isAdmin(req)) return json({ error: "401" }, 401);
  const a = new URL(req.url).searchParams.get("a");
  if (a === "insurance") return json({ html: summary.html, pdf: policy.name });
  if (a === "insurance-pdf") return new Response(Buffer.from(policy.b64, "base64"), { headers: { "content-type": "application/pdf", "content-disposition": `attachment; filename="${policy.name}"`, "cache-control": "no-store" } });
  if (a === "plants") { const items = await plantsAll(); items.sort((x, y) => x.code.localeCompare(y.code)); return json({ updated: plants.updated, items }); }
  if (req.method === "POST" && (a === "plant-add" || a === "plant-preview")) {
    let p; try { p = await req.json(); } catch { return json({ error: "bad json" }, 400); }
    let base; try { base = codeBase(p); } catch (e) { return json({ error: e.message }, 400); }
    const all = await plantsAll(), used = all.filter(x => x.code.startsWith(base + "-")).map(x => Number(x.code.slice(base.length + 1)) || 0);
    const code = `${base}-${String((used.length ? Math.max(...used) : 0) + 1).padStart(2, "0")}`;
    if (a === "plant-preview") return json({ code });
    if (!String(p.name || "").trim()) return json({ error: "Plant name is required" }, 400);
    const it = { code, name: String(p.name).trim().slice(0, 120), platform: PLAT[code[0]], station_id: String(p.station_id || "").trim().slice(0, 40),
      plant_id: String(p.plant_id || p.station_id || "").trim().slice(0, 40), area: String(p.area || "").trim().slice(0, 120), postcode: code.split("-")[1],
      province: String(p.province || "").trim().slice(0, 60), pv_kwp: Number(p.pv_kwp) || 0, inverter_model: String(p.inverter_model || "").trim().slice(0, 80),
      inv_kw: Number(code.split("-")[2]), phase: ["1P", "3P"].includes(p.phase) ? p.phase : "", battery: code[1] === "H", commissioned: String(p.commissioned || "").trim().slice(0, 20),
      access: "owner", model_src: "admin", source: "admin", added: new Date().toISOString() };
    const list = await added(); list.push(it); await store().setJSON("added", list);
    return json({ ok: true, item: it });
  }
  if (req.method === "POST" && a === "plant-del") {
    let p; try { p = await req.json(); } catch { return json({ error: "bad json" }, 400); }
    const list = await added(), keep = list.filter(x => x.code !== p.code);
    if (keep.length === list.length) return json({ error: "Only plants added in admin can be removed" }, 400);
    await store().setJSON("added", keep); return json({ ok: true });
  }
  return json({ error: "unknown action" }, 400);
};
export const config = { path: "/api/docs" };
