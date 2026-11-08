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
  if (p && p.form_name) { try { await saveInbox(p); } catch { /* inbox copy is best-effort */ } }
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

// Job report from the installer team (form "job-report" on /job-report.html?c=<installer code>).
// Accepted only with a valid, unused installer code issued by Solar ESS at /feedback-admin.html; anything else is ignored.
// The report is attached to that job in store "feedback". Files are copied now because Netlify's file links expire.
const REPORT_FILES = ["photo-before", "photo-after", "photo-3", "report-file"];
const MAX_FILE = 6 * 1024 * 1024;
async function saveReport(p) {
  const store = getStore({ name: "feedback", consistency: "strong" });
  const data = {};
  for (const [k, v] of Object.entries(p.data || {})) {
    if (["bot-field", "form-name", "ip", "user_agent", "referrer"].includes(k)) continue;
    data[k] = v;
  }
  const code = String(data.code || "").toUpperCase().replace(/[^A-Z0-9]/g, "");
  const ref = code.length >= 6 ? await store.get("code/" + code, { type: "json" }) : null;
  if (!ref || ref.role !== "installer") return new Response("ignored: no valid installer code");
  const job = await store.get("job/" + ref.jobId, { type: "json" });
  if (!job || job.cancelled) return new Response("ignored: job not open");
  if (job.report) return new Response("ignored: report already sent");
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
      await store.set(`file/${job.id}/${f}`, buf, { metadata: { type } });
      files.push(f);
    } catch { /* keep the report even if a file could not be copied */ }
  }
  // admin chose "Others": the installer writes their team name on the report
  if (job.teamOpen && !job.team) job.team = String(data["team-name"] || "").trim().slice(0, 120) || "Not stated";
  delete data.code;
  for (const f of REPORT_FILES) delete data[f];
  job.report = { created: p.created_at || new Date().toISOString(), data, files };
  await store.setJSON("job/" + job.id, job);
  return new Response("saved");
}

// Form inbox: every website form submission (except vocab results, which have their own admin)
// is also copied to store "inbox" so Kris can read and manage it at /inbox-admin.html.
// Uploaded files are copied now because Netlify's file links expire.
const INBOX_SKIP = new Set(["vocab-results"]);
const INBOX_MAX_FILE = 8 * 1024 * 1024;
async function saveInbox(p) {
  if (INBOX_SKIP.has(p.form_name)) return;
  const store = getStore({ name: "inbox", consistency: "strong" });
  const id = String(p.id || p.number || Date.now()).replace(/[^A-Za-z0-9_-]/g, "");
  if (await store.get("sub/" + id)) return;
  const data = {}, files = [];
  for (const [k, v] of Object.entries(p.data || {})) {
    if (["bot-field", "form-name", "ip", "user_agent", "referrer"].includes(k)) continue;
    const url = fileUrl(v);
    if (url && (typeof v === "object" || /netlify|amazonaws|cloudfront/.test(url))) {
      try {
        const r = await fetch(url);
        const type = r.headers.get("content-type") || "application/octet-stream";
        const buf = r.ok ? await r.arrayBuffer() : null;
        if (buf && buf.byteLength <= INBOX_MAX_FILE) {
          const name = (typeof v === "object" && v.filename) || url.split("?")[0].split("/").pop() || k;
          await store.set(`file/${id}/${k}`, buf, { metadata: { type, name } });
          files.push({ field: k, name, type, size: buf.byteLength });
          continue;
        }
      } catch { /* fall through and keep the link */ }
    }
    data[k] = v;
  }
  await store.setJSON("sub/" + id, {
    id, form: p.form_name, status: "new", note: "",
    created: p.created_at || new Date().toISOString(), data, files,
  });
}
