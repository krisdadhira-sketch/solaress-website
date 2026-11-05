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
  if (p && p.form_name === "job-report") return saveReport(p);
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

// Job report from the installer team after a job (form "job-report" on /job-report.html).
// Saved as a finished job in store "feedback" (key job/<id>) with the customer's phone, so the customer
// can then rate the job at /feedback.html. Files are copied now because Netlify's file links expire.
function normPhone(v) {
  let d = String(v || "").replace(/\D/g, "");
  if (d.startsWith("66") && d.length >= 11) d = "0" + d.slice(2);
  return d.length >= 9 ? d : "";
}
const REPORT_FILES = ["photo-before", "photo-after", "photo-3", "report-file"];
const MAX_FILE = 6 * 1024 * 1024;
async function saveReport(p) {
  const store = getStore({ name: "feedback", consistency: "strong" });
  const id = "r" + String(p.id || p.number || Date.now()).replace(/[^A-Za-z0-9_-]/g, "");
  if (await store.get("job/" + id)) return new Response("exists");
  const data = {};
  for (const [k, v] of Object.entries(p.data || {})) {
    if (["bot-field", "form-name", "ip", "user_agent", "referrer"].includes(k)) continue;
    data[k] = v;
  }
  const files = [];
  for (const f of REPORT_FILES) {
    const url = fileUrl(data[f]);
    if (!url) continue;
    try {
      const r = await fetch(url);
      const type = r.headers.get("content-type") || "";
      if (!r.ok || !/^(image\/(jpeg|png|webp)|application\/pdf)/.test(type)) continue;
      const buf = await r.arrayBuffer();
      if (buf.byteLength > MAX_FILE) continue;
      await store.set(`file/${id}/${f}`, buf, { metadata: { type } });
      files.push(f);
    } catch { /* keep the report even if a file could not be copied */ }
  }
  // a select with an "other" option (value "__other") plus a free-text box
  const pick = (sel, other) => String(data[sel] && data[sel] !== "__other" ? data[sel] : data[other] || "").trim();
  await store.setJSON("job/" + id, {
    id, created: p.created_at || new Date().toISOString(), source: "report",
    job: pick("job", "job-other"), team: pick("team", "team-other"),
    phone: normPhone(data["customer-phone"]), customer: String(data["customer-name"] || "").trim(), date: String(data["completed"] || ""),
    data, files, blocked: false, rated: null,
  });
  return new Response("saved");
}
