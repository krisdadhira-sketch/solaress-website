// Admin-only static files: Monthly Report pages, Monthly Report PDFs and their preview images.
// A valid "ss_admin" cookie (set by /api/admin-session after the admin password) lets the file through.
// Without it: pages show a sign-in box, PDFs/images return 404. Same password as all admin pages.
const enc = new TextEncoder();
const hex = (buf) => [...new Uint8Array(buf)].map((x) => x.toString(16).padStart(2, "0")).join("");
async function sign(exp, s) {
  const k = await crypto.subtle.digest("SHA-256", enc.encode("solaress-admin-session|" + s));
  const key = await crypto.subtle.importKey("raw", k, { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  return hex(await crypto.subtle.sign("HMAC", key, enc.encode(String(exp))));
}
function same(a, b) { if (a.length !== b.length) return false; let d = 0; for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i); return d === 0; }
async function valid(req) {
  const s = String(Netlify.env.get("ADMIN_SESSION_SECRET") || Netlify.env.get("MEMBERS_ADMIN_PASSWORD") || Netlify.env.get("VOCAB_ADMIN_PASSWORD") || "").trim();
  if (!s) return false;
  const m = /(?:^|;\s*)ss_admin=(\d+)\.([0-9a-f]{64})/.exec(req.headers.get("cookie") || "");
  if (!m || Number(m[1]) < Date.now() / 1000) return false;
  return same(m[2], await sign(m[1], s));
}
const TXT = {
  en: ["Solar ESS Admin", "The Monthly Report is for Solar ESS staff only. Same password as all admin pages.", "Admin password", "Sign in", "Password is not right."],
  th: ["Solar ESS Admin", "รายงานประจำเดือนสำหรับเจ้าหน้าที่ Solar ESS เท่านั้น ใช้รหัสผ่านเดียวกับหน้าผู้ดูแลระบบทุกหน้า", "รหัสผ่านผู้ดูแลระบบ", "เข้าสู่ระบบ", "รหัสผ่านไม่ถูกต้อง"],
};
function page(lang) {
  const t = TXT[lang];
  return `<!DOCTYPE html><html lang="${lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>${t[0]}</title>
<style>:root{--navy:#0B1736;--violet:#4B4FD8;--line:#D7DAEA}*{box-sizing:border-box}body{margin:0;font-family:"IBM Plex Sans Thai","Sarabun",system-ui,-apple-system,"Segoe UI",sans-serif;background:#F5F6FB;color:#1d2333}
header{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:14px 22px;background:#fff;border-bottom:3px solid var(--navy)}header img{height:54px}.addr{text-align:right;font-size:12.5px;line-height:1.45;color:#5A6275}.addr b{color:var(--navy)}
.box{max-width:380px;margin:12vh auto;background:#fff;border:1px solid var(--line);border-radius:16px;padding:26px;box-shadow:0 10px 30px rgba(11,23,54,.08)}h1{margin:0 0 6px;font-size:22px;color:var(--navy)}p{margin:0 0 12px;color:#5A6275;font-size:14px;line-height:1.5}
input{width:100%;padding:11px 12px;border:1.5px solid var(--line);border-radius:10px;font:inherit;margin:4px 0 12px}button{width:100%;padding:11px;border:0;border-radius:10px;background:var(--violet);color:#fff;font:600 15px/1 inherit;cursor:pointer}.err{color:#B42318;min-height:20px;margin:10px 0 0;font-size:13.5px}</style></head>
<body><header><img src="/images/solar-ess-report-logo.jpg" alt="Solar ESS"><div class="addr"><b>Solar ESS Co. Ltd.</b><br>53 Moo 2, Tambon Nanglae, Amphoe Muang, Chiang Rai 57100<br>Tel 063 151 6694 · www.solaress.org · www.โซลาร์เอสส์.com</div></header>
<main><div class="box"><h1>${t[0]}</h1><p>${t[1]}</p><form id="f"><input type="password" id="pw" placeholder="${t[2]}" aria-label="${t[2]}" autocomplete="current-password"><button>${t[3]}</button></form><p class="err" id="e" role="status"></p></div></main>
<script>(function(){var e=document.getElementById('e');function go(pw,auto){if(!pw)return;fetch('/api/admin-session',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({password:pw})})
.then(function(r){return r.json().then(function(j){if(r.ok){try{sessionStorage.setItem('members-admin-pw',pw)}catch(x){}location.reload();return}if(!auto)e.textContent=r.status===401?'${t[4]}':(j.error||r.status)})}).catch(function(x){if(!auto)e.textContent=x.message})}
var s='';try{s=sessionStorage.getItem('members-admin-pw')||''}catch(x){}go(s,true);
document.getElementById('f').addEventListener('submit',function(v){v.preventDefault();go(document.getElementById('pw').value.trim(),false)})})();</script></body></html>`;
}
export default async (req, context) => {
  if (await valid(req)) {
    const res = await context.next();
    const h = new Headers(res.headers); h.set("cache-control", "private, no-store"); h.set("x-robots-tag", "noindex");
    return new Response(res.body, { status: res.status, headers: h });
  }
  const p = new URL(req.url).pathname;
  if (/\.(pdf|jpe?g|png|webp|gif)$/i.test(p)) return new Response("Not found", { status: 404, headers: { "cache-control": "no-store" } });
  return new Response(page(p.startsWith("/th/") ? "th" : "en"), { status: 401, headers: { "content-type": "text/html; charset=utf-8", "cache-control": "no-store", "x-robots-tag": "noindex" } });
};
export const config = {
  pattern: ["^/(th/)?monthly-report(\\.html)?$", "^/downloads/Solar-ESS-Monthly-Report-.*$", "^/images/note-monthly-.*$"],
};
