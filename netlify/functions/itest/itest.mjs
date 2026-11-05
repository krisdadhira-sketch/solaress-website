// Practical Solar Installation test for installers (www.solaress.org/installer-test).
// 100 multiple-choice questions, Thai + English: A electrical (50), B wiring (20), C mounting (20), D customer (10).
// The answer key lives only here (bank.json); candidates get their score and section scores, never the answers.
//
// Public:
//   GET  /api/itest?a=questions                         -> {sections, questions:[{i, sec, th, en, options:[{th,en}]}]}
//   POST /api/itest?a=submit {name, phone, email, province, team, language, seconds, answers:[0-3 or null x100]}
//        -> {score, total, pct, pass, sections:{A:{correct,total},...}}
// Admin (header "x-admin-password", same password as /members-admin.html):
//   GET  /api/itest?a=list                              -> {attempts:[summary...]}
//   GET  /api/itest?a=attempt&id=..                     -> attempt with every question, the candidate's answer and the key
//   POST /api/itest?a=delete {id}
import { getStore } from "@netlify/blobs";
import crypto from "node:crypto";
import bank from "./bank.json" with { type: "json" };

const PASS_PCT = 70;
const VOCAB_ADMIN_HASH = "162cdaefe4e9558d229a4846cd021775:5c036e020b55e8727a91b98d8e554c7456200d65599147cff4efea07459dc0fd";
const json = (b, s = 200, cache = "no-store") => new Response(JSON.stringify(b), { status: s, headers: { "content-type": "application/json", "cache-control": cache } });
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
const store = () => getStore({ name: "itest", consistency: "strong" });

async function all(s) {
  const { blobs } = await s.list({ prefix: "att/" });
  const out = [];
  for (const b of blobs) { const v = await s.get(b.key, { type: "json" }); if (v) out.push(v); }
  return out.sort((x, y) => String(y.created).localeCompare(String(x.created)));
}
const summary = (a) => ({ id: a.id, created: a.created, name: a.name, phone: a.phone, email: a.email, province: a.province, team: a.team,
  language: a.language, seconds: a.seconds, score: a.score, total: a.total, pct: a.pct, pass: a.pass, sections: a.sections });

export default async (req) => {
  const u = new URL(req.url), a = u.searchParams.get("a");

  if (a === "questions") {
    return json({ sections: bank.sections, pass: PASS_PCT,
      questions: bank.questions.map((q, i) => ({ i, sec: q.sec, th: q.th, en: q.en, options: q.options })) }, 200, "public, max-age=300");
  }

  if (a === "submit" && req.method === "POST") {
    let b = {}; try { b = await req.json(); } catch {}
    const name = txt(b.name), phone = txt(b.phone, 30);
    if (!name || phone.replace(/\D/g, "").length < 9) return json({ error: "Name and phone are required." }, 400);
    const answers = Array.isArray(b.answers) ? b.answers.slice(0, bank.questions.length) : [];
    const sections = {};
    for (const s of bank.sections) sections[s.id] = { correct: 0, total: s.count };
    let score = 0;
    const given = bank.questions.map((q, i) => {
      const v = answers[i] === null || answers[i] === undefined || answers[i] === "" ? null : parseInt(answers[i], 10);
      const ok = v === q.answer;
      if (ok) { score++; sections[q.sec].correct++; }
      return v;
    });
    const total = bank.questions.length, pct = Math.round((score / total) * 100), pass = pct >= PASS_PCT;
    const id = Date.now().toString(36) + crypto.randomBytes(4).toString("hex");
    const att = { id, created: new Date().toISOString(), name, phone, email: txt(b.email), province: txt(b.province), team: txt(b.team),
      language: txt(b.language, 20), seconds: Math.max(0, Math.min(36000, parseInt(b.seconds, 10) || 0)), answers: given, score, total, pct, pass, sections };
    await store().setJSON("att/" + id, att);
    return json({ score, total, pct, pass, passMark: PASS_PCT, sections });
  }

  if (!isAdmin(req)) return json({ error: "Admin password is not right." }, 401);
  const s = store();
  if (a === "list") return json({ attempts: (await all(s)).map(summary), sections: bank.sections, pass: PASS_PCT });
  if (a === "attempt") {
    const att = await s.get("att/" + cleanId(u.searchParams.get("id")), { type: "json" });
    if (!att) return json({ error: "not found" }, 404);
    return json({ attempt: summary(att), items: bank.questions.map((q, i) => ({ i, sec: q.sec, th: q.th, en: q.en, options: q.options,
      answer: q.answer, given: att.answers[i], correct: att.answers[i] === q.answer, explain: q.explain })) });
  }
  if (a === "delete" && req.method === "POST") {
    let b = {}; try { b = await req.json(); } catch {}
    await s.delete("att/" + cleanId(b.id));
    return json({ ok: true });
  }
  return json({ error: "unknown action" }, 400);
};

export const config = { path: "/api/itest" };
