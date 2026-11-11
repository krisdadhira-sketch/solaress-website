// Runs automatically for every verified Netlify Forms submission (event-triggered function).
// TSIA membership and installer-partner registrations are saved as "pending" in Netlify Blobs
// (store "members") so Kris can review them at /members-admin.html. Nothing is published until
// he approves it there. Uploaded photos are copied now, because Netlify's file links expire.
import { getStore } from "@netlify/blobs";
import { upsertInstaller } from "./installers/installers.mjs";

const FORMS = {
  "tsia-membership": { type: "tsia", images: ["photo-1", "photo-2", "photo-3"] },
  "installer-partner": { type: "partner", images: ["profile-photo", "project-photo-1", "project-photo-2", "project-photo-3"] },
};
// Installer base locations (store "installers") so Kris can find and notify installers near a job.
const LOC_FORMS = {
  "tsia-membership": (d) => ({ phone: d.phone, name: d["contact-name"] || d.organisation, province: d.province, district: d["base-district"], subdistrict: d["base-subdistrict"], lat: d["base-lat"], lng: d["base-lng"], line: d["line-id"], email: d.email }),
  "installer-partner": (d) => ({ phone: d.phone, name: d["display-name"] || d["contact-name"], province: d["base-province"], district: d["base-district"], lat: d["base-lat"], lng: d["base-lng"], line: d["line-id"], email: d.email }),
  "job-application": (d) => ({ phone: d.phone, name: d.name, province: d.province, email: d.email }),
};
const MAX_IMG = 4 * 1024 * 1024;

const fileUrl = (v) => (v && typeof v === "object" ? v.url : typeof v === "string" && /^https?:\/\//.test(v) ? v : null);

export default async (req) => {
  let body;
  try { body = await req.json(); } catch { return new Response("bad body", { status: 400 }); }
  const p = body && body.payload;
  if (p && p.form_name === "job-report") return saveReport(p);
  if (p && p.form_name) { try { await saveInbox(p); } catch { /* inbox copy is best-effort */ } }
  if (p && LOC_FORMS[p.form_name]) { try { await upsertInstaller(LOC_FORMS[p.form_name](p.data || {}), p.form_name); } catch { /* best-effort */ } }
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
  if (p.form_name === "job-application") {
    try { Object.assign(data, jobScore(data, files)); } catch { /* score is a helper only */ }
  }
  await store.setJSON("sub/" + id, {
    id, form: p.form_name, status: "new", note: "",
    created: p.created_at || new Date().toISOString(), data, files,
  });
}

// Candidate score for job applications (Nov 2026), out of 100, shown in the inbox admin so Kris can pick
// the best candidate per job. Age is an eligibility check only (18+), not scored.
//   Experience in this job: 3 points/year, max 30          Largest completed project: 0 at 10k THB → 25 at 1M THB (log)
//   Project value, last 3 years: 0 at 100k → 10 at 10M (log) Academic/institute: 10 named + 5 file
//   Product certificate: 8 named + 2 file                   References: person 5, company 5 (full only with a phone no.)
// ≥ 60 Qualified (send contract) · 40–59 Review · < 40 Not yet.
export function jobScore(d, files = []) {
  const num = (v) => { const n = parseFloat(String(v ?? "").replace(/[^0-9.]/g, "")); return isFinite(n) ? n : 0; };
  const none = (v) => !String(v ?? "").trim() || /^(none|no|n\/a|-|ไม่มี|ไม่|ไม่มีครับ|ไม่มีค่ะ)$/i.test(String(v).trim());
  const has = (f) => files.some((x) => x.field === f) || (d[f] && typeof d[f] === "object");
  const lg = (v, lo, hi) => (v <= lo ? 0 : Math.min(1, Math.log10(v / lo) / Math.log10(hi / lo)));
  const ref = (v) => (none(v) ? 0 : /\d{9,}/.test(String(v).replace(/[\s-]/g, "")) ? 5 : 3);
  const age = num(d.age);
  const parts = {
    experience: Math.round(Math.min(num(d["experience-years"]), 10) * 3),
    "largest-project": Math.round(25 * lg(num(d["largest-project-value"]), 10000, 1000000)),
    "project-value-3y": Math.round(10 * lg(num(d["total-project-value-3y"]), 100000, 10000000)),
    academic: (none(d["academic-certificate"]) ? 0 : 10) + (has("certificate") ? 5 : 0),
    product: (none(d["product-certificate"]) ? 0 : 8) + (has("product-certificate-file") ? 2 : 0),
    references: ref(d["reference-person"]) + ref(d["reference-company"]),
  };
  const total = Object.values(parts).reduce((a, b) => a + b, 0);
  const missing = [];
  if (!has("id-card")) missing.push("ID card");
  if (!String(d["contact-address"] || "").trim()) missing.push("address");
  if (!String(d["company-name"] || "").trim()) missing.push("company");
  const eligible = age >= 18;
  const verdict = !eligible ? "Not eligible (under 18 or age missing)"
    : total >= 60 && !missing.length ? "Qualified – send contract"
    : total >= 40 ? "Review" : "Not yet";
  return {
    "candidate-score": `${total}/100 – ${verdict}`,
    "score-breakdown": Object.entries(parts).map(([k, v]) => `${k} ${v}`).join(", ") + (missing.length ? ` · missing: ${missing.join(", ")}` : ""),
  };
}
