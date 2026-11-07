// Solar ESS installer test (www.solaress.org/installer-test): 5 levels x 25 questions, Thai + English,
// plus the Brand & Product Test (tests 11-15: Inverter, PV Modules, Battery, Cable, Breakers; 15 questions each).
//   Level 1 Solar Enterer · 2 Solar Enthusiast · 3 Solar in Practice · 4 Solar Professional · 5 Solar Expert
// Rules (Nov 2026): anyone can take any level and see their score; only name and phone are required.
// Pass = 100% (25/25); only a pass issues a certificate number. To open or download the certificate
// (/certificate.html?id=...), the phone used for the test must be registered as TSIA member or Installer Partner
// (store "members", any status except rejected/hidden). /join.html registers in one step via a=register. Certificates issued before this change (no needReg flag)
// stay open. Solar ESS accepts installation work from Level 3 (work: true on the certificate).
// Each start shuffles question and answer order (session ses/<id>, valid 3 h). After an attempt at a level, the same
// phone or email must wait 30 days before taking that level again. Certificates are valid for 1 year; a level with a valid
// certificate cannot be retaken, an expired one can (renewal). Any pass, even expired, counts as the prerequisite.
// The answer key lives only here (bank.json).
//
// Public:
//   POST /api/itest?a=status {phone}                 -> {registered, regName, passed:{n:certId}, next}
//   POST /api/itest?a=start  {phone, level}          -> {level, questions:[{i, sec, th, en, options}]} if eligible
//   POST /api/itest?a=submit {phone, level, name, email, province, team, language, seconds, answers:[0-3|null x25]}
//        -> {score, total, pct, pass, sections, cert}
//   GET  /api/itest?a=cert&id=..                     -> {id, name, level, title_en, title_th, pct, date}
// Admin (header "x-admin-password", same as /members-admin.html):
//   GET  /api/itest?a=list ; GET /api/itest?a=attempt&id=.. ; POST /api/itest?a=delete {id}
import { getStore } from "@netlify/blobs";
import crypto from "node:crypto";
import bank from "./bank.json" with { type: "json" };

const PASS_PCT = bank.pass_pct || 100;   // certificate and next level only at this score
const WORK_LEVEL = bank.work_level || 3;  // Solar ESS accepts installation work from this level
const RETAKE_DAYS = 30, SESSION_MS = 3 * 3600 * 1000, VALID_DAYS = 365;   // certificates are valid for 1 year
const validUntil = (iso) => { const d = new Date(iso); d.setFullYear(d.getFullYear() + 1); d.setDate(d.getDate() - 1); return d.toISOString(); };
const isValid = (iso) => Date.now() <= Date.parse(validUntil(iso)) + 864e5;
const normEmail = (v) => String(v || "").trim().toLowerCase();
const shuffled = (n) => { const a = [...Array(n).keys()]; for (let i = n - 1; i > 0; i--) { const j = crypto.randomInt(i + 1); [a[i], a[j]] = [a[j], a[i]]; } return a; };
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
const txt = (v, k = 120) => String(v == null ? "" : v).trim().slice(0, k);
const cleanId = (v) => String(v || "").replace(/[^A-Za-z0-9_-]/g, "");
function normPhone(v) {
  let d = String(v || "").replace(/\D/g, "");
  if (d.startsWith("66") && d.length >= 11) d = "0" + d.slice(2);
  return d.length >= 9 ? d : "";
}
const store = () => getStore({ name: "itest", consistency: "strong" });
const LEVELS = bank.levels;
const PRODUCTS = bank.products || [];          // Brand & Product Test (tests 11-15), outside the level ladder
const ALL = LEVELS.concat(PRODUCTS);
const levelInfo = (n) => ALL.find((l) => l.n === n);
const isProduct = (n) => PRODUCTS.some((p) => p.n === n);
// Certificate titles: levels "Solar in Practice"; product tests "Brand & Product Test · Inverter"
const titleEn = (l) => isProduct(l.n) ? `${l.group_en} · ${l.en}` : l.en;
const titleTh = (l) => isProduct(l.n) ? `${l.group_th} · ${l.th}` : l.th;
const qsOf = (n) => bank.questions.map((q, i) => ({ ...q, i })).filter((q) => q.level === n);

async function list(s, prefix) {
  const { blobs } = await s.list({ prefix });
  const out = [];
  for (const b of blobs) { const v = await s.get(b.key, { type: "json" }); if (v) out.push(v); }
  return out.sort((x, y) => String(y.created).localeCompare(String(x.created)));
}
// Registered as TSIA member or installer partner with this phone (not rejected or hidden)?
async function registration(phone) {
  const m = getStore({ name: "members", consistency: "strong" });
  for (const sub of await list(m, "sub/")) {
    if (["rejected", "hidden"].includes(sub.status)) continue;
    const d = sub.data || {};
    if (normPhone(d.phone) === phone) return { type: sub.type, status: sub.status, name: d["display-name"] || d.organisation || d["contact-name"] || "" };
  }
  return null;
}
async function history(s, phone, email) {
  const passed = {}, ever = {}, expired = {}, wait = {}, cut = Date.now() - RETAKE_DAYS * 864e5;
  for (const a of await list(s, "att/")) {          // newest first
    if (!(a.phone === phone || (email && normEmail(a.email) === email))) continue;
    if (a.pass && a.phone === phone) {
      ever[a.level] = ever[a.level] || a.cert;
      if (isValid(a.created)) { if (!passed[a.level]) passed[a.level] = a.cert; }
      else if (!expired[a.level]) expired[a.level] = a.cert;
    }
    const t = Date.parse(a.created);
    if (!a.pass && t > cut) { const until = new Date(t + RETAKE_DAYS * 864e5).toISOString(); if (!wait[a.level] || until > wait[a.level]) wait[a.level] = until; }
  }
  for (const l in passed) delete expired[l];
  return { passed, ever, expired, wait };
}
// Every level is open to anyone with a phone number; registration is only needed to open the certificate.
async function eligibility(s, phone, level, email) {
  if (!phone) return { ok: false, reason: "phone" };
  const reg = await registration(phone);
  const { passed, wait } = await history(s, phone, normEmail(email));
  if (passed[level]) return { ok: false, reason: "passed", cert: passed[level] };
  if (wait[level]) return { ok: false, reason: "wait", until: wait[level] };
  return { ok: true, reg, passed };
}
const summary = (a) => ({ id: a.id, created: a.created, level: a.level, name: a.name, phone: a.phone, email: a.email, province: a.province, team: a.team,
  language: a.language, seconds: a.seconds, score: a.score, total: a.total, pct: a.pct, pass: a.pass, sections: a.sections, cert: a.cert || null });

export default async (req) => {
  const u = new URL(req.url), a = u.searchParams.get("a");
  const s = store();
  let b = {};
  if (req.method === "POST") { try { b = await req.json(); } catch {} }

  if (a === "status" && req.method === "POST") {
    const phone = normPhone(b.phone);
    if (!phone) return json({ error: "phone" }, 400);
    const reg = await registration(phone);
    const { passed, ever, expired, wait } = await history(s, phone, normEmail(b.email));
    let next = 1; while (ever[next] && next < 5) next++;
    if (ever[5]) next = null;
    return json({ registered: !!reg, regType: reg && reg.type, regName: reg ? reg.name : "", passed, ever, expired, wait, retakeDays: RETAKE_DAYS, next, levels: LEVELS, products: PRODUCTS, pass: PASS_PCT, workLevel: WORK_LEVEL });
  }

  if (a === "start" && req.method === "POST") {
    const phone = normPhone(b.phone), level = parseInt(b.level, 10);
    if (!levelInfo(level)) return json({ error: "level" }, 400);
    const el = await eligibility(s, phone, level, b.email);
    if (!el.ok) return json({ error: el.reason, need: el.need, until: el.until, cert: el.cert }, 403);
    const qs = qsOf(level), order = shuffled(qs.length), perms = order.map((k) => shuffled(qs[k].options.length));
    const sid = Date.now().toString(36) + crypto.randomBytes(8).toString("hex");
    await s.setJSON("ses/" + sid, { id: sid, phone, level, order, perms, created: Date.now() });
    return json({ session: sid, expires: new Date(Date.now() + SESSION_MS).toISOString(), level: levelInfo(level), sections: bank.sections, pass: PASS_PCT,
      questions: order.map((k, n) => ({ i: n, sec: qs[k].sec, th: qs[k].th, en: qs[k].en, options: perms[n].map((o) => qs[k].options[o]) })) });
  }

  if (a === "submit" && req.method === "POST") {
    const phone = normPhone(b.phone), level = parseInt(b.level, 10), name = txt(b.name);
    const email = txt(b.email), team = txt(b.team);
    if (!levelInfo(level) || !name || !phone) return json({ error: "Name, phone and level are required." }, 400);
    if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return json({ error: "Please enter a valid email." }, 400);
    const ses = await s.get("ses/" + cleanId(b.session), { type: "json" });
    if (!ses || ses.phone !== phone || ses.level !== level) return json({ error: "session" }, 400);
    if (Date.now() - ses.created > SESSION_MS) { await s.delete("ses/" + ses.id); return json({ error: "expired" }, 400); }
    const el = await eligibility(s, phone, level, email);
    if (!el.ok) return json({ error: el.reason, need: el.need, until: el.until }, 403);
    await s.delete("ses/" + ses.id);
    const qs = qsOf(level), shown = Array.isArray(b.answers) ? b.answers.slice(0, qs.length) : [];
    const answers = Array(qs.length).fill(null);        // back to bank order and bank option numbers
    ses.order.forEach((k, n) => { const v = shown[n]; if (v !== null && v !== undefined && v !== "" && ses.perms[n][+v] !== undefined) answers[k] = ses.perms[n][+v]; });
    const sections = {};
    let score = 0;
    const given = qs.map((q, k) => {
      const v = answers[k];
      (sections[q.sec] ||= { correct: 0, total: 0 }).total++;
      if (v === q.answer) { score++; sections[q.sec].correct++; }
      return v;
    });
    const total = qs.length, pct = Math.round((score / total) * 100), pass = pct >= PASS_PCT;
    const id = Date.now().toString(36) + crypto.randomBytes(4).toString("hex");
    const created = new Date().toISOString();
    let cert = null;
    if (pass) {
      cert = (isProduct(level) ? "SESS-P" : "SESS-L") + level + "-" + crypto.randomBytes(4).toString("hex").toUpperCase();
      await s.setJSON("cert/" + cert, { id: cert, name, level, pct, score, total, date: created, attempt: id, phone, needReg: true });
    }
    await s.setJSON("att/" + id, { id, created, level, name, phone, email, province: txt(b.province), team,
      regType: el.reg ? el.reg.type : "", language: txt(b.language, 20), seconds: Math.max(0, Math.min(36000, parseInt(b.seconds, 10) || 0)),
      answers: given, score, total, pct, pass, sections, cert });
    return json({ score, total, pct, pass, passMark: PASS_PCT, sections, cert, registered: !!el.reg, level: levelInfo(level), validFrom: pass ? created : null, validUntil: pass ? validUntil(created) : null });
  }

  // One-click registration from /join.html: the certificate number and the phone used for the test must match.
  // Saves a pending Installer Partner (TSIA) registration in store "members", reviewed by Kris at /members-admin.html.
  if (a === "register" && req.method === "POST") {
    const phone = normPhone(b.phone), name = txt(b.name, 80), certId = cleanId(b.cert).toUpperCase();
    if (!phone || !name || !txt(b.province) || b.agree !== true) return json({ error: "Please fill in all fields and tick the box." }, 400);
    const c = await s.get("cert/" + certId, { type: "json" });
    if (!c || (c.phone && c.phone !== phone)) return json({ error: "cert" }, 404);
    if (await registration(phone)) return json({ ok: true, already: true });
    const m = getStore({ name: "members", consistency: "strong" });
    const id = "st" + Date.now().toString(36) + crypto.randomBytes(3).toString("hex");
    const region = ["north", "northeast", "central", "bangkok", "east", "west", "south"].includes(b.region) ? b.region : "";
    await m.setJSON("sub/" + id, { id, type: "partner", form: "installer-partner", status: "pending", created: new Date().toISOString(), images: [],
      data: { "display-name": name, "contact-name": name, phone, "base-province": txt(b.province, 60), region, "partner-type": txt(b.type, 60),
        "agree-terms": "yes", "agree-publish": "yes", "agree-verification": "yes", "joins-tsia": "yes", language: txt(b.language, 20),
        source: "Solar Test certificate " + certId } });
    return json({ ok: true });
  }

  if (a === "cert") {
    const c = await s.get("cert/" + cleanId(u.searchParams.get("id")).toUpperCase(), { type: "json" });
    if (!c) return json({ error: "not-found" }, 404);
    const l = levelInfo(c.level);
    // New certificates open only once the test phone is registered (TSIA member or Installer Partner).
    // (any status except rejected/hidden: registering on /join.html opens the certificate at once; Kris still approves the profile).
    if (c.needReg && !(await registration(c.phone))) return json({ error: "register", id: c.id, level: c.level, product: isProduct(c.level), title_en: titleEn(l), title_th: titleTh(l), pct: c.pct }, 403);
    return json({ id: c.id, name: c.name, level: c.level, product: isProduct(c.level), title_en: titleEn(l), title_th: titleTh(l), pct: c.pct, score: c.score, total: c.total, date: c.date, validFrom: c.date, validUntil: validUntil(c.date), valid: isValid(c.date), work: !isProduct(c.level) && c.level >= WORK_LEVEL });
  }

  if (!isAdmin(req)) return json({ error: "Admin password is not right." }, 401);
  if (a === "list") return json({ attempts: (await list(s, "att/")).map(summary), sections: bank.sections, levels: ALL, pass: PASS_PCT });
  if (a === "attempt") {
    const att = await s.get("att/" + cleanId(u.searchParams.get("id")), { type: "json" });
    if (!att) return json({ error: "not found" }, 404);
    return json({ attempt: summary(att), items: qsOf(att.level).map((q, k) => ({ i: k, sec: q.sec, th: q.th, en: q.en, options: q.options,
      answer: q.answer, given: att.answers[k], correct: att.answers[k] === q.answer, explain: q.explain })) });
  }
  if (a === "delete" && req.method === "POST") {
    const att = await s.get("att/" + cleanId(b.id), { type: "json" });
    if (att && att.cert) await s.delete("cert/" + att.cert);
    await s.delete("att/" + cleanId(b.id));
    return json({ ok: true });
  }
  return json({ error: "unknown action" }, 400);
};

export const config = { path: "/api/itest" };
