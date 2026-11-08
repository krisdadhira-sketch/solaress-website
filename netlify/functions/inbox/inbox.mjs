// Form inbox for the admin area (same admin password as all admin pages, header "x-admin-password").
//   GET  /api/inbox?a=list                 -> {items}
//   GET  /api/inbox?a=file&id=..&f=..      -> an uploaded file
//   POST /api/inbox?a=set     {id,status?,note?}
//   POST /api/inbox?a=delete  {id}
import crypto from "node:crypto";
import { getStore } from "@netlify/blobs";

const VOCAB_ADMIN_HASH = "162cdaefe4e9558d229a4846cd021775:5c036e020b55e8727a91b98d8e554c7456200d65599147cff4efea07459dc0fd";
const STATUSES = ["new", "contacted", "in-progress", "done", "archived"];
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
const clean = (s) => String(s || "").replace(/[^A-Za-z0-9_-]/g, "");

export default async (req) => {
  if (!isAdmin(req)) return json({ error: "401" }, 401);
  const s = getStore({ name: "inbox", consistency: "strong" });
  const u = new URL(req.url), a = u.searchParams.get("a");
  if (a === "list") {
    const { blobs } = await s.list({ prefix: "sub/" });
    const items = (await Promise.all(blobs.map((b) => s.get(b.key, { type: "json" })))).filter(Boolean);
    items.sort((x, y) => String(y.created).localeCompare(String(x.created)));
    return json({ items });
  }
  if (a === "file") {
    const id = clean(u.searchParams.get("id")), f = String(u.searchParams.get("f") || "").replace(/[^A-Za-z0-9_.-]/g, "");
    const r = await s.getWithMetadata(`file/${id}/${f}`, { type: "arrayBuffer" });
    if (!r) return json({ error: "not found" }, 404);
    const name = String((r.metadata && r.metadata.name) || f).replace(/[^\w.\- ]/g, "_");
    return new Response(r.data, { headers: { "content-type": (r.metadata && r.metadata.type) || "application/octet-stream", "content-disposition": `attachment; filename="${name}"`, "cache-control": "no-store" } });
  }
  if (req.method !== "POST") return json({ error: "unknown action" }, 400);
  let b = {}; try { b = await req.json(); } catch {}
  const id = clean(b.id), key = "sub/" + id;
  const item = id ? await s.get(key, { type: "json" }) : null;
  if (!item) return json({ error: "not found" }, 404);
  if (a === "set") {
    if (b.status !== undefined) { if (!STATUSES.includes(b.status)) return json({ error: "bad status" }, 400); item.status = b.status; }
    if (b.note !== undefined) item.note = String(b.note).slice(0, 4000);
    item.updated = new Date().toISOString();
    await s.setJSON(key, item);
    return json({ ok: true, item });
  }
  if (a === "delete") {
    for (const f of item.files || []) await s.delete(`file/${id}/${f.field}`);
    await s.delete(key);
    return json({ ok: true });
  }
  return json({ error: "unknown action" }, 400);
};
export const config = { path: "/api/inbox" };
