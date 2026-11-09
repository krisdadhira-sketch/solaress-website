# -*- coding: utf-8 -*-
"""Installer test pages: /installer-test.html (EN chrome) and /th/installer-test.html (TH chrome).
Five levels of 25 questions, open to everyone (name + phone). A certificate needs 100%, and opening or
downloading it needs a TSIA or installer-partner registration with the same phone. Questions are shown in Thai and English and load from
/api/itest (answers never reach the page). A pass issues a certificate at /certificate.html?id=...
Run from the repo root:  python3 tools/itest/page.py   (then python3 tools/analytics_tag.py)"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

T = {
"en": dict(pre="", title="Solar Installer Test: 5 Levels with Certificates | Solar ESS",
    desc="Practical solar installation test in 5 levels, from Solar Enterer to Solar Expert. 25 questions per level in Thai and English; score 100% for each level's certificate.",
    eyebrow="Solar Test · แบบทดสอบโซลาร์", h1="Practical Solar Installation Test",
    lede="Five levels, 25 questions each, in Thai and English. Everyone can take every level and see their score straight away. A certificate (valid for 1 year) is given only for 100% (25/25). To download your certificate, register free in one minute with the same phone number and it opens straight away. Test results are valid for 1 year, for TSIA members and for Solar ESS. If you score less than 100%, you can take the same level again after at least 30 days. Solar ESS accepts installation work from Level 3 (Solar in Practice) upward.",
    work="Accepted for Solar ESS installation work", work_s="✓ Installation work",
    ladder="The five levels", s1="Your details", name="Full name", phone="Phone", email="Email (optional)", prov="Province (optional)",
    team="Company or team name (optional)", check="Show my levels",
    req="Please fill in your name and phone number.", bademail="Please enter a valid email.",
    nreg_h="All five levels are open to you", nreg="You can take any level and see your score now. To download a certificate after scoring 100%, register (free) with this same phone number: as a TSIA Installer Partner (individual, team or company) or as a company member.",
    nreg_t="TSIA company member", nreg_p="Register as TSIA Installer Partner", reg_ok="TSIA member", reg_need="Get my certificate",
    st_pass="Passed", st_open="Open", st_lock="Locked", lock_need="Pass Level {n} first", start="Start Level {n}", retake="Retake", cert="View certificate", wait="Retake from {d}", expired="Certificate expired · renew by taking this level again", valid="Valid until {d}", r_valid="Valid from {a} to {b} (1 year).", e_wait="You attempted this level recently. You can take it again from {d}.", e_passed="You have already passed this level.", e_expired="This test session has expired (3 hours). Please start the level again.",
    qof="Question", answered="answered", submit="Submit my answers", sending="Checking your answers…",
    unanswered="You have {n} unanswered questions. Submit anyway?", fail="Sending failed. Please try again.",
    r_h="Your result", r_pass="Passed", r_fail="Not passed yet", next="Go to Level {n}",
    r_cert="Your certificate number is {id}.", r_retry="A certificate needs 100% ({t}/{t}). Study the topics; you can take this test again from {d}.", r_work="This level is accepted for Solar ESS installation work.", r_reg="One step left: register free in one minute and your certificate opens straight away.",
    back="Back to my levels", loading="Loading…", e_prereq="Please pass Level {n} first.", e_reg="Please register as TSIA member or installer partner first.",
    q_s="questions", lv="Level",
    p_h="Brand & Product Test", p_lede="Product knowledge tests on what we install: inverters, PV modules, batteries, cables and breakers. 15 questions each, open to everyone, same rules: 100% for a certificate valid 1 year.", start_p="Start test", time_l="Time left", time_rule="Time limit: Levels 1–2 and brand tests 10 minutes, Level 3 12 minutes, Levels 4–5 15 minutes. The clock starts when you press Start; when time runs out the test closes and sends itself, and only the answers you gave in time are scored.", mins="min", h_h="For homeowners: Self-Appointed Electrician", h_lede="15 questions on what every homeowner should know about their own electricity: RCBO and earth leakage, earthing, EV charger circuits, meters, CT and solar safety. Based on solaress.org. 10 minutes; 100% earns a certificate.", timeup="Time is up. Your answers have been sent automatically – only questions answered in time are scored."),
"th": dict(pre="/th", title="แบบทดสอบช่างโซลาร์ 5 ระดับ พร้อมใบประกาศ | Solar ESS",
    desc="แบบทดสอบการติดตั้งโซลาร์ภาคปฏิบัติ 5 ระดับ ตั้งแต่ Solar Enterer ถึง Solar Expert ระดับละ 25 ข้อ ภาษาไทยและอังกฤษ ได้ 100% รับใบประกาศของแต่ละระดับ",
    eyebrow="แบบทดสอบโซลาร์ · Solar Test", h1="แบบทดสอบการติดตั้งโซลาร์ภาคปฏิบัติ",
    lede="5 ระดับ ระดับละ 25 ข้อ ภาษาไทยและอังกฤษ ทุกคนทำแบบทดสอบได้ทุกระดับ และเห็นคะแนนทันที ใบประกาศ (อายุ 1 ปี) ให้เฉพาะผู้ที่ได้ 100% (25/25) หากต้องการดาวน์โหลดใบประกาศ กรุณาลงทะเบียน (ฟรี) เป็นช่างพันธมิตรหรือสมาชิกบริษัท TSIA ด้วยเบอร์โทรเดียวกัน ใช้เวลา 1 นาที แล้วใบประกาศจะเปิดทันที ผลการทดสอบมีอายุ 1 ปี ทั้งสำหรับสมาชิก TSIA และ Solar ESS หากได้คะแนนไม่ถึง 100% สอบระดับเดิมใหม่ได้หลังจากอย่างน้อย 30 วัน Solar ESS รับงานติดตั้งจากผู้ที่ผ่านระดับ 3 (Solar in Practice) ขึ้นไป",
    work="ผ่านเกณฑ์รับงานติดตั้งกับ Solar ESS", work_s="✓ รับงานติดตั้งได้",
    ladder="5 ระดับ", s1="ข้อมูลของคุณ", name="ชื่อ-นามสกุล", phone="เบอร์โทร", email="อีเมล (ไม่บังคับ)", prov="จังหวัด (ไม่บังคับ)",
    team="ชื่อบริษัทหรือทีม (ไม่บังคับ)", check="ดูระดับของฉัน",
    req="กรุณากรอกชื่อและเบอร์โทร", bademail="กรุณากรอกอีเมลให้ถูกต้อง",
    nreg_h="ทำแบบทดสอบได้ทั้ง 5 ระดับ", nreg="คุณทำแบบทดสอบระดับใดก็ได้และเห็นคะแนนทันที หากได้ 100% และต้องการดาวน์โหลดใบประกาศ กรุณาลงทะเบียน (ฟรี) ด้วยเบอร์โทรเดียวกันนี้ ในฐานะช่างพันธมิตร TSIA (บุคคล ทีม หรือบริษัท) หรือสมาชิกประเภทบริษัท",
    nreg_t="สมาชิก TSIA ประเภทบริษัท", nreg_p="สมัครเป็นช่างพันธมิตร TSIA", reg_ok="สมาชิก TSIA", reg_need="รับใบประกาศของฉัน",
    st_pass="ผ่านแล้ว", st_open="เปิดสอบ", st_lock="ล็อกอยู่", lock_need="ต้องผ่านระดับ {n} ก่อน", start="เริ่มระดับ {n}", retake="สอบอีกครั้ง", cert="ดูใบประกาศ", wait="สอบใหม่ได้ตั้งแต่ {d}", expired="ใบประกาศหมดอายุ · สอบระดับนี้อีกครั้งเพื่อต่ออายุ", valid="ใช้ได้ถึง {d}", r_valid="มีอายุตั้งแต่ {a} ถึง {b} (1 ปี)", e_wait="คุณเพิ่งสอบระดับนี้ไป สอบใหม่ได้ตั้งแต่ {d}", e_passed="คุณสอบผ่านระดับนี้แล้ว", e_expired="การสอบนี้หมดเวลาแล้ว (3 ชั่วโมง) กรุณาเริ่มระดับนี้ใหม่",
    qof="ข้อ", answered="ตอบแล้ว", submit="ส่งคำตอบ", sending="กำลังตรวจคำตอบ…",
    unanswered="ยังไม่ได้ตอบ {n} ข้อ ต้องการส่งเลยหรือไม่", fail="ส่งไม่สำเร็จ กรุณาลองอีกครั้ง",
    r_h="ผลการทดสอบ", r_pass="ผ่าน", r_fail="ยังไม่ผ่าน", next="ไประดับ {n}",
    r_cert="เลขที่ใบประกาศของคุณ: {id}", r_retry="ต้องได้ 100% ({t}/{t}) จึงจะได้ใบประกาศ ทบทวนเนื้อหาแล้วสอบใหม่ได้ตั้งแต่ {d}", r_work="ระดับนี้ผ่านเกณฑ์รับงานติดตั้งกับ Solar ESS", r_reg="อีกขั้นเดียว: ลงทะเบียนฟรีใน 1 นาที แล้วใบประกาศจะเปิดทันที",
    back="กลับไปหน้าระดับของฉัน", loading="กำลังโหลด…", e_prereq="กรุณาสอบผ่านระดับ {n} ก่อน", e_reg="กรุณาลงทะเบียนสมาชิก TSIA หรือทีมช่างพันธมิตรก่อน",
    q_s="ข้อ", lv="ระดับ",
    p_h="แบบทดสอบแบรนด์และผลิตภัณฑ์", p_lede="แบบทดสอบความรู้ผลิตภัณฑ์ที่เราติดตั้ง ได้แก่ อินเวอร์เตอร์ แผงโซลาร์เซลล์ แบตเตอรี่ สายไฟ และเบรกเกอร์ ชุดละ 15 ข้อ ทุกคนทำได้ ใช้กติกาเดียวกัน คือได้ 100% รับใบประกาศอายุ 1 ปี", start_p="เริ่มทำแบบทดสอบ", time_l="เวลาที่เหลือ", time_rule="เวลาทำแบบทดสอบ: ระดับ 1–2 และแบบทดสอบผลิตภัณฑ์ 10 นาที ระดับ 3 12 นาที ระดับ 4–5 15 นาที เริ่มนับเมื่อกดเริ่ม เมื่อหมดเวลา ระบบจะปิดแบบทดสอบและส่งคำตอบให้อัตโนมัติ โดยนับคะแนนเฉพาะข้อที่ตอบทันเวลาเท่านั้น", mins="นาที", h_h="สำหรับเจ้าของบ้าน: ช่างไฟประจำบ้าน", h_lede="15 ข้อ เรื่องที่เจ้าของบ้านทุกคนควรรู้เกี่ยวกับไฟฟ้าในบ้านของตัวเอง: เบรกเกอร์กันดูดและไฟรั่ว สายดิน วงจรที่ชาร์จ EV มิเตอร์ CT และความปลอดภัยโซลาร์ อ้างอิงจาก solaress.org ใช้เวลา 10 นาที ได้ 100% รับใบประกาศ", timeup="หมดเวลา ระบบส่งคำตอบให้อัตโนมัติแล้ว นับคะแนนเฉพาะข้อที่ตอบทันเวลา"),
}

CSS = """<style id="itest-css">
.itw{max-width:860px}
.itw label{display:grid;gap:5px;font-size:14px;font-weight:600;color:var(--navy)}
.itw [hidden]{display:none!important}
.itw input:not([type=radio]){font:inherit;font-size:15px;font-weight:400;color:#0A0E2E;-webkit-text-fill-color:#0A0E2E;caret-color:#2563EB;border:1.5px solid var(--line);border-radius:10px;padding:10px 12px;width:100%;box-sizing:border-box;background:#fff}
.itw .two{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.itbox{background:#fff;border:1.5px solid var(--line);border-radius:16px;padding:18px 20px;display:grid;gap:14px;margin-top:18px}
.itlad{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px;margin-top:12px}
.itlad div{background:#fff;border:1px solid var(--line);border-radius:12px;padding:10px;font-size:13px;line-height:1.35}
.itlad b{display:block;color:var(--navy);font-size:14px}.itlad em,.itcard em{display:inline-block;font-style:normal;font-size:11px;font-weight:700;color:#15803D;margin-top:4px}.itlad span{font-family:var(--mono);font-size:11px;color:var(--mute)}
.itlv{display:grid;gap:10px;margin-top:18px}
.itcard{display:flex;gap:14px;align-items:center;justify-content:space-between;flex-wrap:wrap;background:#fff;border:1.5px solid var(--line);border-radius:14px;padding:14px 16px}
.itcard.pass{border-color:#86EFAC;background:#F0FDF4}.itcard.lock{opacity:.6;background:var(--paper)}.itcard.focus{box-shadow:0 0 0 3px #A5B4FC}
.itcard .t b{color:var(--navy);font-size:16px}.itcard .t small{display:block;color:var(--mute)}
.itcard .tag{font-family:var(--mono);font-size:11px;padding:3px 8px;border-radius:99px;border:1px solid var(--line);margin-right:8px}
.itcard .act{display:flex;gap:8px;flex-wrap:wrap}
.itcard .btn.ghost{background:#fff;color:var(--navy);border:1.5px solid var(--navy)}
.itq{background:#fff;border:1.5px solid var(--line);border-radius:14px;padding:14px 16px;margin-top:12px}
.itq.done{border-color:#93C5FD}
.itq .n{font-family:var(--mono);font-size:12px;color:var(--mute)}
.itq .th{font-weight:700;margin:4px 0 2px;font-family:var(--thai)}.itq .en{color:var(--mute);font-size:14px;margin:0 0 10px}
.itq .op{display:flex;gap:10px;align-items:flex-start;padding:8px 10px;border:1px solid var(--line);border-radius:10px;margin-top:6px;cursor:pointer;font-weight:400}
.itq .op:hover{background:var(--paper)}.itq .op input{margin-top:4px;flex:none;accent-color:var(--blue)}
.itq .op span{display:grid;gap:1px}.itq .op small{color:var(--mute);font-size:13px}
.itbar[hidden]{display:none!important}.itclock{font-weight:800;font-variant-numeric:tabular-nums;font-size:18px;color:var(--navy,#0A1230);padding:4px 12px;border:2px solid currentColor;border-radius:999px}.itclock.warn{color:#B42318;animation:itblink 1s steps(2) infinite}@keyframes itblink{50%{opacity:.45}}.ittime-rule{margin-top:12px;font-weight:600;border-left:4px solid #B42318;padding:8px 12px;background:#FFF4F2;color:#0A1230}.itbar{position:sticky;bottom:0;z-index:5;background:rgba(250,252,255,.96);border-top:1px solid var(--line);padding:10px 0;margin-top:20px;display:flex;gap:12px;align-items:center;justify-content:space-between;flex-wrap:wrap}
.itlvh{margin-top:18px;padding:12px 16px;background:var(--navy);color:#fff;border-radius:12px;font-weight:700}
body.it-on .fab{display:none!important}
.itres{background:#fff;border:2px solid var(--line);border-radius:16px;padding:20px;margin-top:18px}
.itres .big{font-size:44px;font-weight:800;color:var(--navy)}
.itres .ok{color:#15803D}.itres .no{color:#B42318}
.itres table{width:100%;border-collapse:collapse;margin-top:10px;font-size:14px}.itres td{padding:7px 8px;border-bottom:1px solid var(--line)}
.itnreg{background:#FFF7ED;border:1.5px solid #FDBA74;border-radius:14px;padding:16px 18px;margin-top:18px}
@media (max-width:760px){.itlad{grid-template-columns:1fr 1fr}}
@media (max-width:640px){.itw .two{grid-template-columns:1fr}}
</style>"""


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build(lang):
    t, th = T[lang], lang == "th"
    bank = json.loads((ROOT / "netlify/functions/itest/bank.json").read_text(encoding="utf-8"))
    src = (ROOT / ("th/team.html" if th else "team.html")).read_text(encoding="utf-8")
    head = src[:src.index('<section class="dark band"')]
    foot = re.sub(r'\n?<script src="/tsia\.js[^>]*></script>', "", src[src.index("<footer>"):])
    url = f"https://solaress.org{t['pre']}/installer-test"
    head = re.sub(r"<title>.*?</title>", f"<title>{esc(t['title'])}</title>", head, count=1)
    for prop, val in [("og:title", t["title"]), ("og:description", t["desc"]), ("og:url", url + ".html")]:
        head = re.sub(r'(<meta property="%s" content=")[^"]*' % prop, lambda m: m.group(1) + esc(val), head, count=1)
    head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + esc(t["desc"]), head, count=1)
    head = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', head, count=1)
    head = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\s*', "", head)
    head = re.sub(r'<span class="langsw">.*?</span>(?=</nav>)',
                  '<span class="langsw"><a href="/installer-test.html" lang="en"' + ('' if th else ' aria-current="true"') + '>EN</a>'
                  '<a href="/th/installer-test.html" lang="th" style="font-family:var(--thai)"' + (' aria-current="true"' if th else '') + '>ไทย</a></span>',
                  head, count=1, flags=re.S)
    head = head.replace("</head>", CSS + "\n</head>", 1)
    wl = bank.get("work_level", 3)
    lad = "".join(f'<div><span>{esc(t["lv"])} {l["n"]}</span><b>{esc(l["en"])}</b>{esc(l["th"])}' + (f'<br><em>{esc(t["work_s"])}</em>' if l["n"] >= wl else "") + '</div>' for l in bank["levels"])
    prod = "".join(f'<div><span>{esc((p["group_th"] if th else p["group_en"]) if p.get("home") else t["p_h"])}</span><b>{esc(p["th"] if th else p["en"])}</b>{esc(p["sub_th"] if th else p["sub_en"])}<br><em style="color:var(--mute)">{p["count"]} {esc(t["q_s"])}</em></div>' for p in bank.get("products", []))
    body = (
        f'<section class="dark band" style="padding-block:64px"><div class="wrap"><p class="eyebrow">{esc(t["eyebrow"])}</p>'
        f'<h1 style="font-size:clamp(34px,5.5vw,60px)">{esc(t["h1"])}</h1><p class="lede" style="margin-top:18px">{esc(t["lede"])}</p><p class="ittime-rule">⏱ {esc(t["time_rule"])}</p></div></section>\n'
        f'<section class="band light" style="padding-block:40px"><div class="wrap itw">'
        f'<h3>{esc(t["ladder"])}</h3><div class="itlad">{lad}</div>'
        f'<h3 style="margin-top:22px">{esc(t["p_h"])}</h3><p class="fine" style="margin:4px 0 0">{esc(t["p_lede"])}</p><div class="itlad">{prod}</div>'
        f'<form id="it-who" class="itbox" novalidate><h3 style="margin:0">{esc(t["s1"])}</h3>'
        f'<div class="two"><label>{esc(t["name"])} *<input id="it-name" required autocomplete="name"></label><label>{esc(t["phone"])} *<input id="it-phone" type="tel" required autocomplete="tel"></label></div>'
        f'<div class="two"><label>{esc(t["email"])}<input id="it-email" type="email" autocomplete="email"></label><label>{esc(t["team"])}<input id="it-team" autocomplete="organization"></label></div>'
        f'<label>{esc(t["prov"])}<input id="it-prov"></label>'
        f'<div><button class="btn" type="submit" id="it-check">{esc(t["check"])}</button> <span id="it-req" class="fine" style="color:#B42318"></span></div></form>'
        f'<div id="it-nreg" class="itnreg" hidden><h3 style="margin:0 0 6px">{esc(t["nreg_h"])}</h3><p style="margin:0 0 12px">{esc(t["nreg"])}</p>'
        f'<a class="btn" href="{t["pre"]}/partners.html#register">{esc(t["nreg_p"])}</a> <a class="btn ghost" href="{t["pre"]}/team.html#join-tsia">{esc(t["nreg_t"])}</a></div>'
        f'<div id="it-lv" class="itlv" hidden></div>'
        f'<div id="it-qs" hidden></div>'
        f'<div class="itbar" id="it-bar" hidden><span id="it-count"></span><span id="it-clock" class="itclock" role="timer" aria-live="off"></span><button class="btn" id="it-send" type="button">{esc(t["submit"])}</button></div>'
        f'<div id="it-res" hidden></div>'
        f'</div></section>\n')
    keys = ["req", "bademail", "reg_ok", "st_pass", "st_open", "st_lock", "lock_need", "start", "retake", "cert", "qof", "answered", "submit",
            "sending", "unanswered", "fail", "r_h", "r_pass", "r_fail", "next", "r_cert", "r_retry", "back", "loading", "e_prereq", "e_reg", "q_s", "lv", "work", "work_s", "reg_need", "r_work", "r_reg", "wait", "e_wait", "e_passed", "e_expired", "expired", "valid", "r_valid", "p_h", "p_lede", "start_p", "time_l", "timeup", "mins", "h_h", "h_lede"]
    L = {k: t[k] for k in keys}
    L["lang"] = "Thai" if th else "English"
    L["th"] = th
    script = "<script>window.IT_T=" + json.dumps(L, ensure_ascii=False) + ";</script>\n" + r"""<script>
(function(){var T=window.IT_T,$=function(i){return document.getElementById(i)},lim=600000,tick=null,timeup=false,sid='',Q=[],S=[],ans=[],t0=0,who={},st=null,cur=0;
var qp=new URLSearchParams(location.search),want=parseInt(qp.get('level'),10)||0,wantKey=qp.get('test')||'';
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function f(s,o){return s.replace(/\{(\w+)\}/g,function(m,k){return o[k]})}
function go(el){window.scrollTo({top:el.getBoundingClientRect().top+window.scrollY-90,behavior:'smooth'})}
function post(a,b){return fetch('/api/itest?a='+a,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(b)}).then(function(r){return r.json().then(function(d){d._s=r.status;return d})})}
function dt(iso){try{return new Date(iso).toLocaleDateString(T.th?'th-TH':'en-GB',{day:'numeric',month:'long',year:'numeric'})}catch(x){return iso}}
function lvName(l){return T.th?l.th+' · '+l.en:l.en+' · '+l.th}
function isP(l){return !!(l&&l.key)}
function lvTag(l){return isP(l)?(l.home?(T.th?l.group_th:l.group_en):T.p_h):T.lv+' '+l.n}
try{var sv=JSON.parse(localStorage.getItem('itest-who')||'null');if(sv){['name','phone','email','team','prov'].forEach(function(k){if(sv[k])$('it-'+k).value=sv[k]})}}catch(x){}
function card(l){var h='';var E=st.ever||st.passed,c=st.passed[l.n],x=(st.expired||{})[l.n],w=(st.wait||{})[l.n],open=!c,why='';if(open&&w){open=false;why=f(T.wait,{d:dt(w)})}var cls=c?'pass':open?'':'lock',stt=c?T.st_pass:open?(x?T.expired:T.st_open):why;
  h+='<div class="itcard '+cls+(want===l.n?' focus':'')+'" id="lv'+l.n+'"><div class="t"><span class="tag">'+esc(lvTag(l))+'</span><b>'+esc(lvName(l))+'</b><small>'+(isP(l)?esc(T.th?l.sub_th:l.sub_en)+'<br>':'')+(l.count||25)+' '+esc(T.q_s)+' · ⏱ '+(l.minutes||10)+' '+esc(T.mins)+' · '+esc(stt)+'</small>'+(!isP(l)&&l.n>=(st.workLevel||3)?'<em>'+esc(T.work_s)+'</em>':'')+'</div><div class="act">'
  +((c||x)&&!open?'<a class="btn ghost" href="/certificate.html?id='+encodeURIComponent(c||x)+'">'+esc(T.cert)+'</a>':'')+(c?''
    :open?'<button class="btn" data-go="'+l.n+'" type="button">'+esc(isP(l)?T.start_p:f(T.start,{n:l.n}))+'</button>':'')+'</div></div>';return h}
function cards(){if(wantKey&&st.products){st.products.forEach(function(p){if(p.key===wantKey)want=p.n})}
 var h='',P=st.products||[],HM=P.filter(function(p){return p.home}),BR=P.filter(function(p){return !p.home});
 if(HM.length){h+='<h3 style="margin:0">'+esc(T.h_h)+'</h3><p class="fine" style="margin:0 0 4px">'+esc(T.h_lede)+'</p>';HM.forEach(function(p){h+=card(p)});h+='<h3 style="margin:22px 0 0">'+esc(T.lv)+' 1–5</h3>'}
 st.levels.forEach(function(l){h+=card(l)});
 if(BR.length){h+='<h3 style="margin:22px 0 0">'+esc(T.p_h)+'</h3><p class="fine" style="margin:0">'+esc(T.p_lede)+'</p>';BR.forEach(function(p){h+=card(p)})}
 $('it-lv').innerHTML=(st.registered?'<p class="fine" style="margin:0">✓ '+esc(T.reg_ok)+(st.regName?' · '+esc(st.regName):'')+'</p>':'')+h;$('it-lv').hidden=false;
 var tgt=$('lv'+(want||st.next||1));if(tgt)go(tgt)}
function status(){var b=$('it-check');b.disabled=true;
 return post('status',{phone:who.phone,email:who.email}).then(function(d){b.disabled=false;st=d;$('it-nreg').hidden=!!d.registered;
  cards()}).catch(function(){b.disabled=false;$('it-req').textContent=T.fail})}
$('it-who').addEventListener('submit',function(e){e.preventDefault();
 who={name:$('it-name').value.trim(),phone:$('it-phone').value.trim(),email:$('it-email').value.trim(),province:$('it-prov').value.trim(),team:$('it-team').value.trim()};
 if(!who.name||who.phone.replace(/\D/g,'').length<9){$('it-req').textContent=T.req;return}
 if(who.email&&!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(who.email)){$('it-req').textContent=T.bademail;return}
 $('it-req').textContent='';try{localStorage.setItem('itest-who',JSON.stringify({name:who.name,phone:who.phone,email:who.email,team:who.team,prov:who.province}))}catch(x){}
 status()});
function clock(){clearInterval(tick);function up(){var left=Math.max(0,lim-(Date.now()-t0)),m=Math.floor(left/60000),sec=Math.floor(left%60000/1000);var c=$('it-clock');c.textContent='⏱ '+T.time_l+' '+m+':'+(sec<10?'0':'')+sec;c.classList.toggle('warn',left<=60000);
 if(left<=0&&!timeup){timeup=true;clearInterval(tick);[].forEach.call(document.querySelectorAll('#it-qs input'),function(i){i.disabled=true});send(true)}}up();tick=setInterval(up,500)}
function stop(){clearInterval(tick);tick=null}
function count(){var n=ans.filter(function(v){return v!==null}).length;$('it-count').textContent=n+' / '+Q.length+' '+T.answered}
function render(lvl){var h='<div class="itlvh">'+esc(lvTag(lvl)+' · '+lvName(lvl))+'</div>';Q.forEach(function(q){
 h+='<div class="itq" id="q'+q.i+'"><div class="n">'+esc(T.qof+' '+(q.i+1)+' / '+Q.length)+'</div><p class="th">'+esc(q.th)+'</p><p class="en">'+esc(q.en)+'</p>'
 +q.options.map(function(o,k){return '<label class="op"><input type="radio" name="q'+q.i+'" value="'+k+'"><span>'+esc(o.th)+(o.en!==o.th?'<small>'+esc(o.en)+'</small>':'')+'</span></label>'}).join('')+'</div>'});
 $('it-qs').innerHTML=h;$('it-qs').hidden=false;$('it-bar').hidden=false;document.body.classList.add('it-on');count()}
$('it-lv').addEventListener('click',function(e){var b=e.target.closest('[data-go]');if(!b)return;var n=+b.getAttribute('data-go');b.disabled=true;b.textContent=T.loading;
 post('start',{phone:who.phone,email:who.email,level:n}).then(function(d){b.disabled=false;
  if(d.error){alert(d.error==='prerequisite'?f(T.e_prereq,{n:d.need}):d.error==='not-registered'?T.e_reg:d.error==='wait'?f(T.e_wait,{d:dt(d.until)}):d.error==='passed'?T.e_passed:T.fail);status();return}
  cur=n;sid=d.session;Q=d.questions;S=d.sections;ans=Q.map(function(){return null});t0=Date.now();lim=(d.limit||600)*1000;timeup=false;
  $('it-who').hidden=true;$('it-lv').hidden=true;$('it-res').hidden=true;render(d.level);clock();go($('it-qs'));
  try{gtag('event','installer_test_start',{level:n})}catch(x){}}).catch(function(){b.disabled=false;alert(T.fail)})});
$('it-qs').addEventListener('change',function(e){var m=/^q(\d+)$/.exec(e.target.name);if(!m||timeup||(Date.now()-t0)>lim)return;ans[+m[1]]=+e.target.value;$('q'+m[1]).classList.add('done');count()});
function send(auto){if(!auto){var miss=ans.filter(function(v){return v===null}).length;if(miss&&!confirm(f(T.unanswered,{n:miss})))return}stop();
 var b=$('it-send');b.disabled=true;b.textContent=T.sending;
 post('submit',Object.assign({},who,{level:cur,session:sid,language:T.lang,timeup:!!auto,seconds:Math.min(Math.round(lim/1000),Math.round((Date.now()-t0)/1000)),answers:ans})).then(function(r){
  if(auto)alert(T.timeup);b.disabled=false;b.textContent=T.submit;if(r.error){alert(r.error==='expired'||r.error==='session'?T.e_expired:r.error==='wait'?f(T.e_wait,{d:dt(r.until)}):r.error);if(r.error==='expired'||r.error==='session'){$('it-qs').hidden=true;$('it-bar').hidden=true;document.body.classList.remove('it-on');$('it-who').hidden=false;status()}return}
  try{gtag('event','installer_test_sent',{level:cur,score:r.pct,pass:r.pass})}catch(x){}
  var rows=S.map(function(s){var x=r.sections[s.id];if(!x)return '';return '<tr><td>'+esc(s.id+'. '+s.th+' / '+s.en)+'</td><td style="text-align:right;white-space:nowrap"><b>'+x.correct+' / '+x.total+'</b></td></tr>'}).join('');
  if(r.pass){st.passed[cur]=r.cert;st.ever=st.ever||{};st.ever[cur]=r.cert;if(st.expired)delete st.expired[cur]}else{st.wait=st.wait||{};st.wait[cur]=new Date(Date.now()+(st.retakeDays||30)*864e5).toISOString()}
  var acts='';if(r.pass){acts+='<a class="btn" href="/certificate.html?id='+encodeURIComponent(r.cert)+'">'+esc(T.cert)+'</a> ';if(cur<5&&!st.passed[cur+1])acts+='<button class="btn ghost" type="button" data-next="'+(cur+1)+'">'+esc(f(T.next,{n:cur+1}))+'</button> '}
  acts+='<button class="btn ghost" type="button" data-next="0">'+esc(T.back)+'</button>';
  $('it-qs').hidden=true;$('it-bar').hidden=true;document.body.classList.remove('it-on');$('it-res').hidden=false;
  $('it-res').innerHTML='<div class="itres"><h3 style="margin:0">'+esc(T.r_h+' · '+lvTag(r.level)+' · '+lvName(r.level))+'</h3><div class="big">'+r.score+' / '+r.total+' <span class="'+(r.pass?'ok':'no')+'" style="font-size:24px">('+r.pct+'% · '+esc(r.pass?T.r_pass:T.r_fail)+')</span></div><table>'+rows+'</table><p style="margin-top:12px">'+esc(r.pass?f(T.r_cert,{id:r.cert})+' '+f(T.r_valid,{a:dt(r.validFrom),b:dt(r.validUntil)}):f(T.r_retry,{d:dt(st.wait[cur]),t:r.total}))+'</p>'+(r.pass&&!isP(r.level)&&cur>=(st.workLevel||3)?'<p style="color:#15803D;font-weight:700">✓ '+esc(T.r_work)+'</p>':'')+(r.pass&&!r.registered?'<p>'+esc(T.r_reg)+'</p><p><a class="btn" href="'+(T.th?'/th':'')+'/join.html?cert='+encodeURIComponent(r.cert)+'&phone='+encodeURIComponent(who.phone)+'&name='+encodeURIComponent(who.team||who.name)+'">'+esc(T.reg_need)+'</a></p>':'')+'<div class="act" style="display:flex;gap:8px;flex-wrap:wrap;margin-top:12px">'+acts+'</div></div>';
  go($('it-res'))}).catch(function(){b.disabled=false;b.textContent=T.submit;alert(T.fail)})}
$('it-send').addEventListener('click',function(){send(false)});
$('it-res').addEventListener('click',function(e){var b=e.target.closest('[data-next]');if(!b)return;want=+b.getAttribute('data-next');$('it-res').hidden=true;$('it-who').hidden=false;cards()});
})();
</script>
"""
    out = ROOT / ("th/installer-test.html" if th else "installer-test.html")
    out.write_text(head + body + script + foot, encoding="utf-8")
    print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    build("en")
    build("th")
