// TSIA members and installer partners: review queue and public lists.
// Submissions arrive through submission-created.mjs as "pending".
//
// Public (no password) — only approved entries, only public fields, never contact details:
//   GET /api/members?a=public&type=tsia|partner        -> {items:[...]}
//   GET /api/members?a=img&id=..&f=..                  -> photo of an approved entry
// Admin (header "x-admin-password"):
//   GET  /api/members?a=list                           -> every submission with all fields
//   POST /api/members?a=set {id, status}               -> status: approved | rejected | pending | hidden
//   POST /api/members?a=delete {id}                     -> permanently remove a rejected/hidden entry and its photos
//   GET  /api/members?a=img&id=..&f=..                 -> any photo (preview before approval)
//
// Admin password: MEMBERS_ADMIN_PASSWORD environment variable in Netlify; if not set, the same
// password as the vocabulary teacher dashboard (VOCAB_ADMIN_PASSWORD or its built-in default).
import { getStore } from "@netlify/blobs";
import crypto from "node:crypto";

const VOCAB_ADMIN_HASH = "162cdaefe4e9558d229a4846cd021775:5c036e020b55e8727a91b98d8e554c7456200d65599147cff4efea07459dc0fd";
const json = (b, s = 200, cache = "no-store") => new Response(JSON.stringify(b), { status: s, headers: { "content-type": "application/json", "cache-control": cache } });
const store = () => getStore({ name: "members", consistency: "strong" });

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

const list = (v) => Array.isArray(v) ? v.map(String).filter(Boolean) : String(v || "").split(/\s*,\s*/).filter(Boolean);
const num = (v) => { const n = parseFloat(String(v || "").replace(/,/g, "")); return isFinite(n) ? n : null; };
const txt = (v, n = 400) => String(v || "").trim().slice(0, n);
const img = (s, f) => s.images.includes(f) ? `/api/members?a=img&id=${encodeURIComponent(s.id)}&f=${f}` : "";
const month = (iso) => String(iso || "").slice(0, 7);

// Public fields only. Phone, email, LINE, address, tax/ID numbers, documents and private notes are never included.
function publicTsia(s) {
  const d = s.data;
  return {
    id: s.id, name: txt(d.organisation, 120), type: txt(d["business-type"], 60),
    province: txt(d.province, 60), regions: list(d.regions), services: list(d.services),
    year: txt(d["year-established"], 8), team: num(d["team-size"]), electricians: num(d["certified-electricians"]),
    projects: num(d["projects-completed"]), kwp: num(d["total-kwp-installed"]), brands: txt(d.brands, 160),
    intro: txt(d["public-intro"], 400), photo: img(s, "photo-1"), verified: month(s.approved),
  };
}
function publicPartner(s) {
  const d = s.data;
  const brands = list(d["inverter-brands"]).concat(list(d["other-inverter-brands"]));
  return {
    id: s.id, name: txt(d["display-name"], 80), type: txt(d["partner-type"], 60), region: txt(d.region, 20),
    province: txt(d["base-province"], 60), district: txt(d["base-district"], 60), serves: txt(d["provinces-served"], 160),
    services: list(d.services), max_size: txt(d["max-system-size"], 10),
    years: num(d["years-experience"]), team: num(d["team-size"]), electricians: num(d["certified-electricians"]),
    projects: num(d["projects-completed"]), kwp: num(d["total-kwp-installed"]),
    brands, tools: list(d.tools), tax_invoice: d["tax-invoice"] === "yes", insured: d.insurance === "yes",
    languages: list(d.languages), intro: txt(d.introduction, 400),
    engineer: txt(d["engineer-availability"], 20), engineering: list(d["engineering-licence"]),
    safety_officer: txt(d["safety-officer-availability"], 20), safety: list(d["safety-officer"]),
    work_at_height: txt(d["work-at-height-availability"], 20), work_at_height_certified: num(d["work-at-height-certified"]),
    logo: img(s, "profile-photo"), photo: img(s, "project-photo-1"), verified: month(s.approved),
  };
}

function partnerAsTsia(s) {
  const p = publicPartner(s);
  return { id: s.id, name: p.name, type: p.type, province: p.province, regions: p.region ? [p.region] : [], services: p.services,
    year: "", team: p.team, electricians: p.electricians, projects: p.projects, kwp: p.kwp, brands: p.brands.join(", "),
    intro: p.intro, photo: p.logo || p.photo, verified: p.verified, category: "partner" };
}

async function all(s) {
  const { blobs } = await s.list({ prefix: "sub/" });
  const out = [];
  for (const b of blobs) { const v = await s.get(b.key, { type: "json" }); if (v) out.push(v); }
  return out.sort((a, b) => String(b.created).localeCompare(String(a.created)));
}

export default async (req) => {
  const u = new URL(req.url), a = u.searchParams.get("a");
  const s = store();

  if (a === "public") {
    const type = u.searchParams.get("type");
    if (!["tsia", "partner"].includes(type)) return json({ error: "type" }, 400);
    // Installer Partners are TSIA members: the TSIA list includes approved partners (category "partner").
    const ok = (await all(s)).filter((x) => x.status === "approved");
    const items = type === "tsia"
      ? ok.filter((x) => x.type === "tsia").map((x) => ({ ...publicTsia(x), category: "company" }))
          .concat(ok.filter((x) => x.type === "partner").map(partnerAsTsia))
      : ok.filter((x) => x.type === "partner").map(publicPartner);
    return json({ items }, 200, "public, max-age=60");
  }

  if (a === "img") {
    const id = u.searchParams.get("id") || "", f = u.searchParams.get("f") || "";
    const sub = await s.get("sub/" + id, { type: "json" });
    if (!sub || !sub.images.includes(f)) return new Response("not found", { status: 404 });
    if (sub.status !== "approved" && !isAdmin(req)) return new Response("not found", { status: 404 });
    const r = await s.getWithMetadata(`img/${id}/${f}`, { type: "arrayBuffer" });
    if (!r) return new Response("not found", { status: 404 });
    return new Response(r.data, { headers: { "content-type": r.metadata.type || "image/jpeg", "cache-control": sub.status === "approved" ? "public, max-age=3600" : "no-store" } });
  }

  if (!isAdmin(req)) return json({ error: "Admin password is not right." }, 401);

  if (a === "list") return json({ items: await all(s) });

  if (a === "set" && req.method === "POST") {
    let b = {};
    try { b = await req.json(); } catch {}
    if (!["approved", "rejected", "pending", "hidden"].includes(b.status)) return json({ error: "status" }, 400);
    const key = "sub/" + String(b.id || "");
    const sub = await s.get(key, { type: "json" });
    if (!sub) return json({ error: "not found" }, 404);
    sub.status = b.status;
    if (b.status === "approved" && !sub.approved) sub.approved = new Date().toISOString();
    await s.setJSON(key, sub);
    return json({ ok: true, item: sub });
  }

  // Permanently remove a rejected or hidden entry and its photos (published or waiting entries cannot be deleted).
  if (a === "delete" && req.method === "POST") {
    let b = {};
    try { b = await req.json(); } catch {}
    const id = String(b.id || ""), key = "sub/" + id;
    const sub = await s.get(key, { type: "json" });
    if (!sub) return json({ error: "not found" }, 404);
    if (!["rejected", "hidden"].includes(sub.status)) return json({ error: "Reject or hide it first, then delete." }, 400);
    for (const f of sub.images || []) await s.delete(`img/${id}/${f}`);
    await s.delete(key);
    return json({ ok: true });
  }

  return json({ error: "unknown action" }, 400);
};

export const config = { path: "/api/members" };
