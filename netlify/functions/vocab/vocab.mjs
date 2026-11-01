// Solar ESS vocabulary tests (www.solaress.org/vocabulary).
// 100 synonym tests x 20 questions, easiest (test 1) to hardest (test 100).
// Student accounts, attempts and scores are kept in Netlify Blobs (store "vocab").
// The answer key lives only here (bank.json), so the test page never receives the answers before grading.
//
// Student API (token from register/login in "Authorization: Bearer <token>"):
//   POST /api/vocab?a=register {name,email,password,school}  -> {token,user}
//   POST /api/vocab?a=login    {email,password}              -> {token,user}
//   GET  /api/vocab?a=tests                                  -> {user,tests:[{n,level,attempts,best,last}]}
//   GET  /api/vocab?a=test&n=1                               -> {n,level,questions:[{i,word,pos,options}]}
//   POST /api/vocab?a=submit {n,answers:[..20 options..],seconds} -> {score,total,review}
// Teacher API (header "x-admin-password"):
//   GET  /api/vocab?a=admin                                  -> every student with per-test results
//   GET  /api/vocab?a=attempt&email=..&n=..&ts=..            -> one attempt's answers
//   POST /api/vocab?a=reset {email,password}                 -> set a new password for a student
//
// Teacher password: set the VOCAB_ADMIN_PASSWORD environment variable in Netlify to change it.
// Without it, the password whose scrypt hash is ADMIN_HASH below is accepted.
import { getStore } from "@netlify/blobs";
import crypto from "node:crypto";
import bank from "./bank.json" with { type: "json" };

const ADMIN_HASH = "162cdaefe4e9558d229a4846cd021775:5c036e020b55e8727a91b98d8e554c7456200d65599147cff4efea07459dc0fd";
const LEVELS = ["Starter", "Elementary", "Pre-intermediate", "Intermediate", "Upper-intermediate", "Advanced", "Proficient", "Expert", "Scholar", "Master"];
const levelOf = (n) => Math.ceil(n / 10);

const json = (b, s = 200) => new Response(JSON.stringify(b), { status: s, headers: { "content-type": "application/json", "cache-control": "no-store" } });
const store = () => getStore({ name: "vocab", consistency: "strong" });
const cleanEmail = (e) => String(e || "").trim().toLowerCase();
const okEmail = (e) => /^[^\s@]{1,64}@[^\s@]{1,255}\.[^\s@]{2,}$/.test(e);
const key = (e) => encodeURIComponent(e);

function hashPw(pw, salt = crypto.randomBytes(16).toString("hex")) {
  return salt + ":" + crypto.scryptSync(String(pw), salt, 32).toString("hex");
}
function checkPw(pw, stored) {
  const [salt, h] = String(stored).split(":");
  if (!salt || !h) return false;
  const got = crypto.scryptSync(String(pw), salt, 32);
  const want = Buffer.from(h, "hex");
  return got.length === want.length && crypto.timingSafeEqual(got, want);
}

async function secret(s) {
  if (process.env.VOCAB_SECRET) return process.env.VOCAB_SECRET;
  let v = await s.get("config/secret");
  if (!v) { v = crypto.randomBytes(32).toString("hex"); await s.set("config/secret", v); }
  return v;
}
async function makeToken(s, email) {
  const exp = Date.now() + 30 * 24 * 3600e3;
  const body = Buffer.from(JSON.stringify({ e: email, x: exp })).toString("base64url");
  const sig = crypto.createHmac("sha256", await secret(s)).update(body).digest("base64url");
  return body + "." + sig;
}
async function readToken(s, req) {
  const t = (req.headers.get("authorization") || "").replace(/^Bearer\s+/i, "");
  const [body, sig] = t.split(".");
  if (!body || !sig) return null;
  const want = crypto.createHmac("sha256", await secret(s)).update(body).digest("base64url");
  if (sig.length !== want.length || !crypto.timingSafeEqual(Buffer.from(sig), Buffer.from(want))) return null;
  try { const p = JSON.parse(Buffer.from(body, "base64url").toString()); return p.x > Date.now() ? p.e : null; } catch { return null; }
}
function isAdmin(req) {
  const pw = req.headers.get("x-admin-password") || "";
  if (!pw) return false;
  if (process.env.VOCAB_ADMIN_PASSWORD) {
    const a = Buffer.from(pw), b = Buffer.from(process.env.VOCAB_ADMIN_PASSWORD);
    return a.length === b.length && crypto.timingSafeEqual(a, b);
  }
  return checkPw(pw, ADMIN_HASH);
}
const publicUser = (u) => ({ name: u.name, email: u.email, school: u.school || "", created: u.created });
const shuffle = (a) => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = crypto.randomInt(i + 1); [a[i], a[j]] = [a[j], a[i]]; } return a; };

async function getResults(s, email) {
  return (await s.get("results/" + key(email), { type: "json" })) || { tests: {} };
}

export default async (req) => {
  const url = new URL(req.url);
  const a = url.searchParams.get("a");
  const s = store();
  let body = {};
  if (req.method === "POST") { try { body = await req.json(); } catch {} }

  try {
    // ---------- accounts ----------
    if (a === "register" && req.method === "POST") {
      const email = cleanEmail(body.email), name = String(body.name || "").trim().slice(0, 80), school = String(body.school || "").trim().slice(0, 120);
      if (!name) return json({ error: "Please enter your full name." }, 400);
      if (!okEmail(email)) return json({ error: "Please enter a valid email address." }, 400);
      if (String(body.password || "").length < 6) return json({ error: "Choose a password of at least 6 characters." }, 400);
      if (await s.get("users/" + key(email))) return json({ error: "This email already has an account. Please log in." }, 409);
      const u = { name, email, school, pw: hashPw(body.password), created: new Date().toISOString() };
      await s.setJSON("users/" + key(email), u);
      return json({ token: await makeToken(s, email), user: publicUser(u) });
    }
    if (a === "login" && req.method === "POST") {
      const email = cleanEmail(body.email);
      const u = await s.get("users/" + key(email), { type: "json" });
      if (!u || !checkPw(body.password || "", u.pw)) return json({ error: "Email or password is not right." }, 401);
      return json({ token: await makeToken(s, email), user: publicUser(u) });
    }

    // ---------- teacher ----------
    if (a === "admin" || a === "attempt" || a === "reset") {
      if (!isAdmin(req)) return json({ error: "Teacher password is not right." }, 401);
      if (a === "admin") {
        const { blobs } = await s.list({ prefix: "users/" });
        const students = await Promise.all(blobs.map(async (b) => {
          const u = await s.get(b.key, { type: "json" });
          const r = await getResults(s, u.email);
          return { ...publicUser(u), tests: r.tests };
        }));
        students.sort((x, y) => x.name.localeCompare(y.name));
        return json({ students, levels: LEVELS, testCount: bank.length });
      }
      if (a === "attempt") {
        const email = cleanEmail(url.searchParams.get("email")), n = +url.searchParams.get("n"), ts = url.searchParams.get("ts");
        const d = await s.get(`attempts/${key(email)}/${n}/${ts}`, { type: "json" });
        return d ? json(d) : json({ error: "not found" }, 404);
      }
      if (a === "reset" && req.method === "POST") {
        const email = cleanEmail(body.email);
        const u = await s.get("users/" + key(email), { type: "json" });
        if (!u) return json({ error: "No student with that email." }, 404);
        if (String(body.password || "").length < 6) return json({ error: "Password must be at least 6 characters." }, 400);
        u.pw = hashPw(body.password);
        await s.setJSON("users/" + key(email), u);
        return json({ ok: true });
      }
    }

    // ---------- student (logged in) ----------
    const email = await readToken(s, req);
    if (!email) return json({ error: "Please log in again." }, 401);
    const u = await s.get("users/" + key(email), { type: "json" });
    if (!u) return json({ error: "Please log in again." }, 401);

    if (a === "tests") {
      const r = await getResults(s, email);
      const tests = bank.map((_, i) => {
        const t = r.tests[i + 1];
        return { n: i + 1, level: levelOf(i + 1), attempts: t ? t.attempts.length : 0, best: t ? t.best : null, last: t ? t.attempts[t.attempts.length - 1] : null };
      });
      return json({ user: publicUser(u), levels: LEVELS, tests });
    }
    if (a === "test") {
      const n = +url.searchParams.get("n");
      const t = bank[n - 1];
      if (!t) return json({ error: "No such test." }, 404);
      return json({
        n, level: levelOf(n), levelName: LEVELS[levelOf(n) - 1],
        questions: t.map((q, i) => ({ i, word: q.word, pos: q.pos, options: shuffle([q.answer, ...q.distractors]) })),
      });
    }
    if (a === "submit" && req.method === "POST") {
      const n = +body.n;
      const t = bank[n - 1];
      if (!t) return json({ error: "No such test." }, 404);
      const answers = Array.isArray(body.answers) ? body.answers : [];
      const review = t.map((q, i) => ({ word: q.word, pos: q.pos, chosen: answers[i] ? String(answers[i]).slice(0, 40) : "", answer: q.answer, correct: answers[i] === q.answer }));
      const score = review.filter((x) => x.correct).length;
      const ts = Date.now();
      const seconds = Math.max(0, Math.min(36000, Math.round(+body.seconds || 0)));
      await s.setJSON(`attempts/${key(email)}/${n}/${ts}`, { email, name: u.name, n, ts, score, total: t.length, seconds, review });
      const r = await getResults(s, email);
      const rec = r.tests[n] || { attempts: [], best: 0 };
      rec.attempts.push({ ts, score, seconds });
      rec.best = Math.max(rec.best || 0, score);
      r.tests[n] = rec;
      await s.setJSON("results/" + key(email), r);
      return json({ n, level: levelOf(n), score, total: t.length, seconds, ts, review, attempts: rec.attempts.length, best: rec.best, user: publicUser(u) });
    }
    return json({ error: "Unknown request." }, 400);
  } catch (e) {
    console.error(e);
    return json({ error: "Something went wrong. Please try again." }, 500);
  }
};

export const config = { path: "/api/vocab" };
