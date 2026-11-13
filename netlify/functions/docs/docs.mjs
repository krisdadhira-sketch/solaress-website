// Private company documents for the admin area. Nothing here is public.
// Admin (header "x-admin-password", same password as all admin pages):
//   GET /api/docs?a=insurance      -> {html} CAR insurance policy summary
//   GET /api/docs?a=insurance-pdf  -> the scanned policy PDF
//   GET  /api/docs?a=plants        -> plant code register (code -> plant name, platform IDs); base list + plants added in admin
//   POST /api/docs?a=plant-add     -> {platform,type,postcode,inv_kw,name,...} generates the next free code and saves it
//   POST /api/docs?a=plant-del     -> {code} removes a plant added in admin (base SolisCloud list is fixed in plants.json)
//   GET  /api/docs?a=people        -> codes for installers, company partners, interns and customer requests:
//        [Role]-[Postcode]-[No.]  CP company/team partner · IN individual installer · TI intern · CU customer request
//        Codes are given once (oldest first) and kept in store "plant-codes" key "people", so they never change.
//        A code from the province only is provisional until the postcode is set: POST ?a=people-set {key, postcode}
import crypto from "node:crypto";
import summary from "./summary.json" with { type: "json" };
import policy from "./policy.json" with { type: "json" };
import plants from "./plants.json" with { type: "json" };
import { getStore } from "@netlify/blobs";
import TH from "./th-postcodes.json" with { type: "json" };

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
async function plantsAll() { return [...plants.items.map(x => ({ ...x, platform: x.platform || "SolisCloud", source: "register" })), ...(await added())]; }

// ---- people & request codes -------------------------------------------------------------
const ROLE_LABEL = { CP: "Company / team partner", IN: "Individual installer", TI: "Intern", CU: "Customer request" };
const CU_FORMS = { "consultation": "Consultation", "system-check": "Free system check", "installer-request": "Installer request", "post-a-job": "Job posted" };
const norm = (x) => String(x || "").toLowerCase().replace(/^(จังหวัด|จ\.|อำเภอ|อ\.|เขต|ตำบล|ต\.|แขวง|amphoe|khet|tambon|khwaeng|chang wat)\s*/g, "").replace(/(province|district|sub-?district)$/g, "").replace(/[\s.\-]/g, "");
function findProv(p) { const n = norm(p); if (!n) return null; return TH.prov.find((x) => norm(x[0]) === n || norm(x[1]) === n || (n.length > 4 && (norm(x[0]).includes(n) || n.includes(norm(x[0])) || n.includes(norm(x[1]))))) || null; }
function postcodeOf(d) {
  const direct = String(d.postcode || d.zipcode || "").toUpperCase().replace(/\s/g, "");
  if (/^(\d{5}|[A-Z]{5})$/.test(direct)) return { pc: direct, how: "given" };
  const text = [d.address, d.location, d["job-details"], d.province, d["base-province"], d["project-province"]].filter(Boolean).join(" ");
  const m = text.match(/\b([1-9]\d{4})\b/); if (m) return { pc: m[1], how: "from address" };
  const pv = findProv(d.province || d["base-province"] || d["project-province"] || "") || TH.prov.find((x) => text.includes(x[1]) || text.toLowerCase().includes(x[0].toLowerCase()));
  if (!pv) return { pc: "", how: "missing" };
  const sub = norm(d["base-subdistrict"] || d.subdistrict || ""), dis = norm(d["base-district"] || d.district || "");
  const inProv = TH.t.filter((t) => t[2] === pv[1]);
  let hit = sub && inProv.find((t) => norm(t[0]) === sub && (!dis || norm(t[1]) === dis)); if (hit) return { pc: hit[3], how: "from sub-district" };
  hit = dis && inProv.find((t) => norm(t[1]) === dis); if (hit) return { pc: hit[3], how: "from district" };
  return { pc: pv[2], how: "province only" };
}
async function listJson(name, prefix) {
  const st = getStore({ name, consistency: "strong" }), { blobs } = await st.list({ prefix }), out = [];
  for (const b of blobs) { const v = await st.get(b.key, { type: "json" }); if (v) out.push(v); }
  return out;
}
async function peopleAll() {
  const ppl = [];
  const [mem, ins, inbox] = await Promise.all([listJson("members", "sub/"), listJson("installers", "i/"), listJson("inbox", "sub/")]);
  const phones = new Set();
  for (const m of mem) {
    if (!["tsia", "partner"].includes(m.type)) continue;
    const d = m.data || {}, pt = String(d["partner-type"] || d["business-type"] || "");
    const role = m.type === "partner" && /individual/i.test(pt) ? "IN" : "CP";
    phones.add(String(d.phone || "").replace(/\D/g, "").slice(-9));
    ppl.push({ key: "m:" + m.id, role, name: d.organisation || d["display-name"] || d["legal-name"] || d["contact-name"] || "", contact: d["contact-name"] || "", phone: d.phone || "", email: d.email || "", province: d.province || d["base-province"] || "", district: d["base-district"] || "", detail: [pt, d["team-size"] && "team " + d["team-size"], m.status].filter(Boolean).join(" · "), created: m.created, src: m.type === "tsia" ? "TSIA membership" : "Installer partner", ...postcodeOf(d) });
  }
  for (const i of ins) {
    if ((i.sources || []).some((x) => x === "tsia-membership" || x === "installer-partner")) continue;
    if (phones.has(String(i.phone || i.key || "").replace(/\D/g, "").slice(-9))) continue;
    ppl.push({ key: "i:" + i.key, role: "IN", name: i.name || "", contact: "", phone: i.phone || "", email: i.email || "", province: i.province || "", district: i.district || "", detail: (i.sources || []).join(", "), created: i.created, src: "Installer location / job application", ...postcodeOf({ ...i, "base-subdistrict": i.subdistrict, "base-district": i.district }) });
  }
  for (const x of inbox) {
    const d = x.data || {};
    if (x.form === "internship-application") ppl.push({ key: "t:" + x.id, role: "TI", name: d.name || "", contact: "", phone: d.phone || "", email: d.email || "", province: "", district: "", detail: [d.university, d.major, d.level, d.location].filter(Boolean).join(" · "), created: x.created, src: "Internship application", ...postcodeOf(d) });
    else if (CU_FORMS[x.form]) ppl.push({ key: "c:" + x.id, role: "CU", name: d.name || d.company || "", contact: "", phone: d.phone || "", email: d.email || "", province: d.province || d["project-province"] || "", district: d.district || "", detail: [CU_FORMS[x.form], d["job-type"] || d["property_type"] || "", d["system-kwp"] || d.kwp || d.size || "", d["inverter-brand"] || "", (d["monitoring-platform"] || d["monitoring-app"]) && "app " + (d["monitoring-platform"] || d["monitoring-app"]), d.battery && "battery " + d.battery, d["system-type"] && "type " + d["system-type"], d["inverter-kw"] && d["inverter-kw"] + " kW"].filter(Boolean).join(" · "), created: x.created, src: CU_FORMS[x.form], ...postcodeOf(d) });
  }
  // give each new person a code once, oldest first, and keep it
  const st = store(), map = (await st.get("people", { type: "json" })) || {}, fix = (await st.get("people-pc", { type: "json" })) || {};
  for (const p of ppl) if (fix[p.key] && !map[p.key]) { p.pc = fix[p.key]; p.how = "set in admin"; }
  let changed = false;
  ppl.sort((a, b) => String(a.created).localeCompare(String(b.created)));
  for (const p of ppl) {
    if (map[p.key]) { p.code = map[p.key]; continue; }
    if (!p.pc) { p.code = ""; continue; }
    const base = `${p.role}-${p.pc}`, used = Object.values(map).filter((c) => c.startsWith(base + "-")).map((c) => Number(c.split("-")[2]) || 0);
    p.code = `${base}-${String((used.length ? Math.max(...used) : 0) + 1).padStart(2, "0")}`;
    if (p.how === "province only") { p.provisional = true; continue; }   // not kept until the postcode is known
    map[p.key] = p.code; changed = true;
  }
  if (changed) await st.setJSON("people", map);
  return ppl;
}

export default async (req) => {
  if (!isAdmin(req)) return json({ error: "401" }, 401);
  const a = new URL(req.url).searchParams.get("a");
  if (a === "insurance") return json({ html: summary.html, pdf: policy.name });
  if (a === "insurance-pdf") return new Response(Buffer.from(policy.b64, "base64"), { headers: { "content-type": "application/pdf", "content-disposition": `attachment; filename="${policy.name}"`, "cache-control": "no-store" } });
  if (req.method === "POST" && a === "people-set") {
    let p; try { p = await req.json(); } catch { return json({ error: "bad json" }, 400); }
    const pc = String(p.postcode || "").toUpperCase().replace(/\s/g, "");
    if (!p.key || !/^(\d{5}|[A-Z]{5})$/.test(pc)) return json({ error: "Postcode must be 5 digits" }, 400);
    const st = store(), map = (await st.get("people", { type: "json" })) || {};
    if (map[p.key]) return json({ error: "This person already has a fixed code" }, 400);
    const fix = (await st.get("people-pc", { type: "json" })) || {}; fix[p.key] = pc; await st.setJSON("people-pc", fix);
    return json({ ok: true });
  }
  if (a === "people") { const items = await peopleAll(); items.sort((x, y) => String(y.created).localeCompare(String(x.created))); return json({ roles: ROLE_LABEL, items }); }
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
