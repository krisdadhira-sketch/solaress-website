// Candidate scoring for job applications (Nov 2026). Everything here is a number taken from the form, so the
// ranking is the same every time and Kris can see why a candidate ranks where they do.
// Candidate score (0–100) = experience, track record, team & licences, tests, certificates, tools, references, distance.
// Rank score per job = 80% candidate score + 20% price (cheapest labour-only price among applicants for that job = 100)
// + an optional AI read of the written proposal (−5…+5) when ANTHROPIC_API_KEY is set.
const num = (v) => { const n = parseFloat(String(v ?? "").replace(/[^0-9.]/g, "")); return isFinite(n) ? n : 0; };
const none = (v) => !String(v ?? "").trim() || /^(none|no|n\/a|-|ไม่มี|ไม่|ไม่มีครับ|ไม่มีค่ะ)$/i.test(String(v).trim());
const lg = (v, lo, hi) => (v <= lo ? 0 : Math.min(1, Math.log10(v / lo) / Math.log10(hi / lo)));
const yes = (v) => v && String(v).trim() !== "" && !/^(no|false|0)$/i.test(String(v));
const count = (d, prefix) => Object.keys(d).filter((k) => k.startsWith(prefix) && yes(d[k])).length;

export const MAX = { experience: 12, installs: 12, "largest-project": 8, "largest-kwp": 5, "3y-value": 5, team: 8,
  licence: 10, "solar-test": 10, certificates: 8, tools: 7, "job-types": 5, references: 6, distance: 4 };

export function jobScore(d, files = []) {
  const has = (f) => files.some((x) => x.field === f) || (d[f] && typeof d[f] === "object");
  const ref = (v) => (none(v) ? 0 : /\d{9,}/.test(String(v).replace(/[\s-]/g, "")) ? 3 : 2);
  const lic = { "none": 0, "l1": 6, "l2": 8, "engineer": 10 }[String(d["electrician-level"] || "none")] ?? 0;
  const test = Math.min(5, num(d["solar-test-level"])) * 2;
  const team = num(d["team-size"]), wah = num(d["wah-workers"]);
  const km = d["distance-km"] === undefined || d["distance-km"] === "" ? null : num(d["distance-km"]);
  const p = {
    experience: Math.min(num(d["experience-years"]), 10) * 1.2,
    installs: 12 * Math.min(1, Math.log10(num(d["installs-completed"]) + 1) / 2),
    "largest-project": 8 * lg(num(d["largest-project-value"]), 10000, 1000000),
    "largest-kwp": 5 * lg(num(d["largest-system-kwp"]), 3, 100),
    "3y-value": 5 * lg(num(d["total-project-value-3y"]), 100000, 10000000),
    team: (team >= 4 ? 5 : team >= 2 ? 3 : team >= 1 ? 1 : 0) + (wah >= 2 ? 3 : wah >= 1 ? 2 : 0),
    licence: lic,
    "solar-test": test,
    certificates: (none(d["academic-certificate"]) ? 0 : 3) + (has("certificate") ? 1 : 0) + (none(d["product-certificate"]) ? 0 : 3) + (has("product-certificate-file") ? 1 : 0),
    tools: Math.min(7, count(d, "tl-")),
    "job-types": Math.min(5, count(d, "jt-")),
    references: ref(d["reference-person"]) + ref(d["reference-company"]),
    distance: km === null ? 1 : km <= 50 ? 4 : km <= 150 ? 3 : km <= 400 ? 1 : 0,
  };
  for (const k in p) p[k] = Math.round(p[k] * 10) / 10;
  const total = Math.round(Object.values(p).reduce((a, b) => a + b, 0));
  const missing = [];
  if (!has("id-card")) missing.push("ID card");
  if (!String(d["contact-address"] || "").trim()) missing.push("address");
  if (!String(d["company-name"] || "").trim()) missing.push("company");
  const eligible = num(d.age) >= 18;
  return { total, parts: p, missing, eligible };
}

// Legacy fields kept on each inbox item (shown in the inbox table).
export function scoreFields(d, files) {
  const s = jobScore(d, files);
  const verdict = !s.eligible ? "Not eligible (under 18 or age missing)" : s.total >= 60 && !s.missing.length ? "Strong" : s.total >= 40 ? "Review" : "Weak";
  return {
    "candidate-score": `${s.total}/100 – ${verdict}`,
    "score-breakdown": Object.entries(s.parts).map(([k, v]) => `${k} ${v}/${MAX[k]}`).join(", ") + (s.missing.length ? ` · missing: ${s.missing.join(", ")}` : ""),
  };
}

// Rank the applicants of one job. items = inbox items (form job-application) for that job.
export function rankJob(items) {
  const rows = items.map((it) => {
    const d = it.data || {}, s = jobScore(d, it.files || []);
    const price = num(d["price-labour-only"]) || num(d["quoted-price"]) || 0;
    return { it, s, price };
  });
  const prices = rows.map((r) => r.price).filter((p) => p > 0);
  const best = prices.length ? Math.min(...prices) : 0;
  for (const r of rows) {
    r.priceScore = r.price > 0 && best > 0 ? Math.round((best / r.price) * 100) : 50;
    const ai = r.it.ai && typeof r.it.ai.adjust === "number" ? r.it.ai.adjust : 0;
    r.rank = Math.round((0.8 * r.s.total + 0.2 * r.priceScore + ai) * 10) / 10;
  }
  rows.sort((a, b) => (b.s.eligible - a.s.eligible) || (b.rank - a.rank));
  rows.forEach((r, i) => {
    r.position = i + 1;
    const blocked = !r.s.eligible || r.s.missing.length > 0;
    r.tier = r.it.status === "archived" ? "declined"
      : !blocked && i < 3 && r.rank >= 55 ? "top"
      : r.s.eligible && (r.rank >= 40 || (i < 5 && r.rank >= 30)) ? "chance" : "not-now";
  });
  return rows;
}
