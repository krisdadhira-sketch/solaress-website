// Runs automatically for every verified Netlify Forms submission (event-triggered function).
// TSIA membership and installer-partner registrations are saved as "pending" in Netlify Blobs
// (store "members") so Kris can review them at /members-admin.html. Nothing is published until
// he approves it there. Uploaded photos are copied now, because Netlify's file links expire.
import { getStore } from "@netlify/blobs";

const FORMS = {
  "tsia-membership": { type: "tsia", images: ["photo-1", "photo-2", "photo-3"] },
  "installer-partner": { type: "partner", images: ["profile-photo", "project-photo-1", "project-photo-2", "project-photo-3"] },
};
const MAX_IMG = 4 * 1024 * 1024;

const fileUrl = (v) => (v && typeof v === "object" ? v.url : typeof v === "string" && /^https?:\/\//.test(v) ? v : null);

export default async (req) => {
  let body;
  try { body = await req.json(); } catch { return new Response("bad body", { status: 400 }); }
  const p = body && body.payload;
  if (p && p.form_name === "job-feedback") return saveFeedback(p);
  const cfg = p && FORMS[p.form_name];
  if (!cfg) return new Response("ignored");

  const store = getStore({ name: "members", consistency: "strong" });
  const id = String(p.id || p.number || Date.now()).replace(/[^A-Za-z0-9_-]/g, "");
  if (await store.get("sub/" + id)) return new Response("exists");

  const data = {};
  for (const [k, v] of Object.entries(p.data || {})) {
    if (["bot-field", "form-name", "ip", "user_agent", "referrer"].includes(k)) continue;
    data[k] = v;
  }

  const images = [];
  for (const f of cfg.images) {
    const url = fileUrl(data[f]);
    if (!url) continue;
    try {
      const r = await fetch(url);
      const type = r.headers.get("content-type") || "";
      if (!r.ok || !/^image\/(jpeg|png|webp)/.test(type)) continue;
      const buf = await r.arrayBuffer();
      if (buf.byteLength > MAX_IMG) continue;
      await store.set(`img/${id}/${f}`, buf, { metadata: { type } });
      images.push(f);
    } catch { /* keep the submission even if a photo could not be copied */ }
  }

  await store.setJSON("sub/" + id, {
    id, type: cfg.type, form: p.form_name, status: "pending",
    created: p.created_at || new Date().toISOString(),
    data, images,
  });
  return new Response("saved");
};

// Customer satisfaction feedback after a job (form "job-feedback" on /feedback.html).
// Saved in store "feedback"; team scorecards are worked out by /api/feedback (admin only).
async function saveFeedback(p) {
  const store = getStore({ name: "feedback", consistency: "strong" });
  const id = String(p.id || p.number || Date.now()).replace(/[^A-Za-z0-9_-]/g, "");
  if (await store.get("fb/" + id)) return new Response("exists");
  const data = {};
  for (const [k, v] of Object.entries(p.data || {})) {
    if (["bot-field", "form-name", "ip", "user_agent", "referrer"].includes(k)) continue;
    data[k] = v;
  }
  await store.setJSON("fb/" + id, { id, created: p.created_at || new Date().toISOString(), data });
  return new Response("saved");
}
