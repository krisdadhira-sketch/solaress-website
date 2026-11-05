# -*- coding: utf-8 -*-
"""Finished-job pages: customer feedback (/feedback.html) and the installer team's job report (/job-report.html), EN + TH.

Flow: Solar ESS creates the job at /feedback-admin.html and gets two one-time codes. The installer team opens
/job-report.html?c=<code> and sends the report; the customer opens /feedback.html?c=<code> and rates the job once: 10 questions scored
5 Perfect / 4 Good / 2 Fair / 1 Poor (no middle score) and NPS 0-10. Answers go to /api/feedback (checked there).
Team record: /feedback-admin.html. Every project job post on the Jobs page links to both pages (tools/job_links.py).
Run from the repo root:  python3 tools/feedback_page.py   (then python3 tools/analytics_tag.py)
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SCALE = {"en": [("5", "Perfect"), ("4", "Good"), ("2", "Fair"), ("1", "Poor")],
         "th": [("5", "ดีเยี่ยม"), ("4", "ดี"), ("2", "พอใช้"), ("1", "ควรปรับปรุง")]}

GROUPS = [
    (("The work", "งานที่ทำ"), [
        ("q1", "Quality and neatness of the workmanship", "คุณภาพและความเรียบร้อยของงาน"),
        ("q2", "Materials used as agreed (quality, brand and quantity)", "ใช้วัสดุตามที่ตกลง (คุณภาพ ยี่ห้อ และจำนวน)"),
        ("q3", "Work finished on time, as scheduled", "งานเสร็จตรงเวลาตามที่นัดหมาย"),
        ("q4", "Safety on site, and the site left clean and tidy", "ความปลอดภัยในการทำงาน และเก็บกวาดหน้างานเรียบร้อย"),
        ("q5", "System tested and working well at handover", "ระบบได้รับการทดสอบและทำงานได้ดีเมื่อส่งมอบ"),
    ]),
    (("The team's personality", "บุคลิกและความประพฤติของทีม"), [
        ("q6", "Polite, respectful and well presented", "สุภาพ ให้เกียรติ และแต่งกายเหมาะสม"),
        ("q7", "Honest and transparent about price and scope", "ซื่อสัตย์และโปร่งใสเรื่องราคาและขอบเขตงาน"),
        ("q8", "Punctual and kept their promises", "ตรงต่อเวลาและรักษาคำพูด"),
    ]),
    (("Working with you", "การสื่อสารกับคุณ"), [
        ("q9", "Clear communication and quick replies", "สื่อสารชัดเจนและตอบกลับรวดเร็ว"),
        ("q10", "Explained how to use and look after the system", "อธิบายวิธีใช้งานและดูแลระบบให้เข้าใจ"),
    ]),
]

T = {
"en": dict(pre="", lang="en",
    title="Rate a Finished Job · Customer Feedback | Solar ESS",
    desc="Customers rate the installer team after a finished job: 10 quick questions on the work, the team and communication.",
    eyebrow="Customer feedback", h1="How did the job go?",
    lede="Your scores keep every installer team honest, and your feedback completes the job so the team can be paid. Ten quick questions, about two minutes. Your answers go to Solar ESS only and are never published with your name.",
    s_login="1. Your feedback code", login_note="Enter the code Solar ESS sent you for this job (it is filled in for you if you opened our link). Each job can be rated once.",
    phone="Feedback code", go="Open", nf="This code was not found. Check it, or contact Solar ESS: LINE solaress1 · 063 151 6694.", wrongrole="This is an installer code. Please use the job report page.",
    pick="Choose the job you want to rate", jl="Job", tl="Team", dl="Finished",
    s_q="2. Your scores", scale_note="5 Perfect · 4 Good · 2 Fair · 1 Poor (there is no middle score: please choose the one closest to your experience)",
    s_nps="3. Would you recommend us?", nps_q="How likely are you to recommend this team and Solar ESS to a friend or colleague?", nps_lo="0 = not at all", nps_hi="10 = extremely likely",
    s_you="4. About you", name="Your name", comment="Anything else we should know: what went well, what to improve (optional)",
    send="Send feedback", sending="Sending…", fail="Sending failed. Please try again, or send us your feedback by LINE solaress1.", done="This job has already been rated. Thank you!",
    privacy="We use your answers only to check and improve our installer teams.",
    # job report
    r_title="Job Report for Installer Teams | Solar ESS", r_desc="Installer teams: report a finished job to Solar ESS and open customer feedback for it.",
    r_eyebrow="Installer teams", r_h1="Job finished? Send your report.",
    r_lede="Send this when the work is handed over, using the report code Solar ESS gave you for this job. Solar ESS releases payment only after both this report and the customer's feedback are received and checked.",
    r_code="Report code", r_open="Open", r_nf="This code was not found. Check it, or contact Solar ESS: LINE solaress1 · 063 151 6694.", r_used="A report has already been sent for this job. Thank you!", r_wrong="This is a customer feedback code. Please use the feedback page.", r_s0="1. Your report code", r_code_note="Enter the code from Solar ESS (it is filled in for you if you opened our link).",
    r_s1="1. The job", r_job="Which job?", r_job_other="Job name, if not listed", other="Other or not listed", r_team="Your team", r_team_sol="Solar ESS team", r_team_other="Team name, if not listed",
    r_date="Date finished", r_s2="2. The customer", r_cname="Customer name", r_cphone="Customer phone (the customer uses it to rate your work; never published)",
    r_s3="3. The work", r_work="Work done", r_mat="Materials used (optional)", r_test="Test results or readings (optional)", r_issue="Problems found or follow-up needed (optional)",
    r_s4="4. Photos and report (optional)", r_files_note="JPG or PNG for photos, PDF for the report. Keep all files together under 8 MB.",
    r_before="Photo before", r_after="Photo after", r_ph3="Another photo", r_file="Report file (for example the PV cleaning report form, PDF)",
    r_s5="5. Sent by", r_name="Your name", r_phone="Your phone", r_send="Send job report",
    choose="Choose one"),
"th": dict(pre="/th", lang="th",
    title="ประเมินความพึงพอใจหลังจบงาน | Solar ESS",
    desc="ลูกค้าประเมินทีมช่างหลังจบงาน 10 คำถามสั้น ๆ เรื่องงาน ทีม และการสื่อสาร",
    eyebrow="ประเมินความพึงพอใจ", h1="งานเป็นอย่างไรบ้าง",
    lede="คะแนนของคุณช่วยให้ทีมช่างทุกทีมรักษามาตรฐาน และแบบประเมินของคุณคือขั้นตอนสุดท้ายของงานก่อนที่ทีมจะได้รับค่าจ้าง 10 คำถามสั้น ๆ ใช้เวลาประมาณ 2 นาที คำตอบส่งถึง Solar ESS เท่านั้น และจะไม่เผยแพร่พร้อมชื่อของคุณ",
    s_login="1. รหัสประเมินงาน", login_note="กรอกรหัสที่ Solar ESS ส่งให้คุณสำหรับงานนี้ (หากเปิดจากลิงก์ของเรา ระบบจะกรอกให้อัตโนมัติ) แต่ละงานประเมินได้ครั้งเดียว",
    phone="รหัสประเมินงาน", go="เปิดแบบประเมิน", nf="ไม่พบรหัสนี้ กรุณาตรวจสอบ หรือติดต่อ Solar ESS: LINE solaress1 · 063 151 6694", wrongrole="รหัสนี้เป็นรหัสของทีมช่าง กรุณาใช้หน้ารายงานจบงาน",
    pick="เลือกงานที่ต้องการประเมิน", jl="งาน", tl="ทีม", dl="เสร็จเมื่อ",
    s_q="2. คะแนนของคุณ", scale_note="5 ดีเยี่ยม · 4 ดี · 2 พอใช้ · 1 ควรปรับปรุง (ไม่มีคะแนนกลาง กรุณาเลือกข้อที่ใกล้เคียงกับความรู้สึกของคุณที่สุด)",
    s_nps="3. คุณจะแนะนำเราไหม", nps_q="คุณมีแนวโน้มจะแนะนำทีมนี้และ Solar ESS ให้เพื่อนหรือคนรู้จักมากน้อยเพียงใด", nps_lo="0 = ไม่แนะนำเลย", nps_hi="10 = แนะนำแน่นอน",
    s_you="4. ข้อมูลของคุณ", name="ชื่อของคุณ", comment="ความเห็นเพิ่มเติม: สิ่งที่ดี และสิ่งที่ควรปรับปรุง (ไม่บังคับ)",
    send="ส่งแบบประเมิน", sending="กำลังส่ง…", fail="ส่งไม่สำเร็จ กรุณาลองอีกครั้ง หรือส่งความเห็นทาง LINE solaress1", done="งานนี้ได้รับการประเมินแล้ว ขอบคุณค่ะ",
    privacy="เราใช้คำตอบของคุณเพื่อตรวจสอบและพัฒนาทีมช่างของเราเท่านั้น",
    r_title="รายงานจบงานสำหรับทีมช่าง | Solar ESS", r_desc="ทีมช่าง: รายงานงานที่เสร็จแล้วให้ Solar ESS และเปิดให้ลูกค้าประเมินงาน",
    r_eyebrow="สำหรับทีมช่าง", r_h1="งานเสร็จแล้ว? ส่งรายงานจบงาน",
    r_lede="ส่งเมื่อส่งมอบงานแล้ว โดยใช้รหัสรายงานที่ Solar ESS ให้ไว้สำหรับงานนี้ Solar ESS จะจ่ายค่างานเมื่อได้รับและตรวจสอบทั้งรายงานนี้และแบบประเมินจากลูกค้าแล้วเท่านั้น",
    r_code="รหัสรายงาน", r_open="เปิดแบบรายงาน", r_nf="ไม่พบรหัสนี้ กรุณาตรวจสอบ หรือติดต่อ Solar ESS: LINE solaress1 · 063 151 6694", r_used="ส่งรายงานของงานนี้แล้ว ขอบคุณค่ะ", r_wrong="รหัสนี้เป็นรหัสประเมินของลูกค้า กรุณาใช้หน้าประเมินงาน", r_s0="1. รหัสรายงาน", r_code_note="กรอกรหัสจาก Solar ESS (หากเปิดจากลิงก์ของเรา ระบบจะกรอกให้อัตโนมัติ)",
    r_s1="1. งาน", r_job="งานไหน", r_job_other="ชื่องาน (หากไม่มีในรายการ)", other="งานอื่น หรือไม่มีในรายการ", r_team="ทีมของคุณ", r_team_sol="ทีม Solar ESS", r_team_other="ชื่อทีม (หากไม่มีในรายการ)",
    r_date="วันที่งานเสร็จ", r_s2="2. ลูกค้า", r_cname="ชื่อลูกค้า", r_cphone="เบอร์โทรลูกค้า (ลูกค้าใช้เบอร์นี้ประเมินงานของคุณ ไม่เผยแพร่)",
    r_s3="3. งานที่ทำ", r_work="รายละเอียดงานที่ทำ", r_mat="วัสดุที่ใช้ (ไม่บังคับ)", r_test="ผลการทดสอบหรือค่าที่วัดได้ (ไม่บังคับ)", r_issue="ปัญหาที่พบ หรืองานที่ต้องติดตาม (ไม่บังคับ)",
    r_s4="4. รูปภาพและรายงาน (ไม่บังคับ)", r_files_note="รูปภาพเป็น JPG หรือ PNG รายงานเป็น PDF ขนาดรวมทุกไฟล์ไม่เกิน 8 MB",
    r_before="รูปก่อนทำงาน", r_after="รูปหลังทำงาน", r_ph3="รูปเพิ่มเติม", r_file="ไฟล์รายงาน (เช่น แบบฟอร์มรายงานล้างแผง PDF)",
    r_s5="5. ผู้ส่งรายงาน", r_name="ชื่อของคุณ", r_phone="เบอร์โทรของคุณ", r_send="ส่งรายงานจบงาน",
    choose="เลือก"),
}

CSS = """<style id="fb-css">
.fbw{max-width:820px}
.fbw form{display:grid;gap:22px;margin-top:28px}
.fbw fieldset{border:1.5px solid var(--line);border-radius:16px;padding:18px 20px 20px;display:grid;gap:14px;margin:0;background:#fff}
.fbw legend{font-size:16px;font-weight:700;padding:0 6px;color:var(--navy)}
.fbw label{display:grid;gap:6px;font-size:14px;font-weight:600;color:var(--navy)}
.fbw input:not([type=radio]),.fbw select,.fbw textarea{font:inherit;font-size:15px;font-weight:400;color:var(--ink);background:#fff;border:1.5px solid var(--line);border-radius:10px;padding:10px 12px;width:100%;box-sizing:border-box}
.fbw .two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:14px}
.fbw h3{font-size:15px;margin:6px 0 0;color:var(--mute);font-family:var(--mono);letter-spacing:.1em;text-transform:uppercase;font-weight:600}
.fbw .q{border-top:1px solid var(--line);padding-top:12px;display:grid;gap:8px}
.fbw .q p{margin:0;font-weight:600;color:var(--ink)}
.rate{display:flex;gap:6px;flex-wrap:wrap}
.rate label{display:block;cursor:pointer}
.rate input{position:absolute;opacity:0;width:1px;height:1px}
.rate span{display:inline-flex;align-items:center;gap:6px;border:1.5px solid var(--line);border-radius:99px;padding:7px 12px;font-size:13.5px;font-weight:600;color:var(--ink);background:#fff;user-select:none}
.rate span b{font-size:15px}
.rate input:checked+span{background:var(--navy);border-color:var(--navy);color:#fff}
.rate input:focus-visible+span{outline:2px solid var(--blue);outline-offset:2px}
.nps span{min-width:42px;justify-content:center;padding:8px 0}
.npsl{display:flex;justify-content:space-between;font-size:12px;color:var(--mute);font-weight:400}
.more{display:grid;gap:8px}.more label{display:flex;gap:10px;align-items:flex-start;font-weight:400}.more input{margin-top:4px;width:auto}
.jobbox{background:var(--sky);border-radius:14px;padding:14px 18px;font-size:15px;line-height:1.7}
.fbw .fine{font-size:13px;color:var(--mute);margin:0}
@media (max-width:640px){.fbw .two{grid-template-columns:minmax(0,1fr)}.rate span{padding:7px 10px}.nps span{min-width:36px}}
</style>"""


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def jobs(lang):
    """Every job name on the Jobs page: the apply list plus every project post (open or closed)."""
    import html as H
    h = (ROOT / ("th/job.html" if lang == "th" else "job.html")).read_text(encoding="utf-8")
    m = re.search(r'<select id="j-role"[^>]*>(.*?)</select>', h, re.S)
    out = [H.unescape(re.sub(r"<[^>]+>", "", o)).strip() for o in (re.findall(r"<option[^>]*>(.*?)</option>", m.group(1)) if m else [])]
    for art in re.findall(r'<article class="card p".*?</article>', h, re.S):
        j = re.search(r'<div class="go"><a [^>]*data-job="([^"]*)"', art)
        name = H.unescape(j.group(1)) if j else H.unescape(re.sub(r"<[^>]+>", "", (re.search(r"<h3>(.*?)</h3>", art, re.S) or [None, ""])[1])).strip()
        if name and name not in out:
            out.append(name)
    return [o for o in out if o]


def page_head(lang, title, desc, slug):
    th = lang == "th"
    src = (ROOT / ("th/team.html" if th else "team.html")).read_text(encoding="utf-8")
    head = src[:src.index('<section class="dark band"')]
    foot = re.sub(r'\n?<script src="/tsia\.js[^>]*></script>', "", src[src.index("<footer>"):])
    url = f"https://solaress.org{'/th' if th else ''}/{slug}"
    head = re.sub(r"<title>.*?</title>", f"<title>{esc(title)}</title>", head, count=1)
    for prop, val in [("og:title", title), ("og:description", desc), ("og:url", url + ".html")]:
        head = re.sub(r'(<meta property="%s" content=")[^"]*' % prop, lambda m: m.group(1) + esc(val), head, count=1)
    head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + esc(desc), head, count=1)
    head = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', head, count=1)
    head = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\s*', "", head)
    if 'name="robots"' not in head:
        head = head.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex, follow">', 1)
    head = re.sub(r'<span class="langsw">.*?</span>(?=</nav>)',
                  f'<span class="langsw"><a href="/{slug}.html" lang="en"' + ('' if th else ' aria-current="true"') + '>EN</a>'
                  f'<a href="/th/{slug}.html" lang="th" style="font-family:var(--thai)"' + (' aria-current="true"' if th else '') + '>ไทย</a></span>',
                  head, count=1, flags=re.S)
    head = head.replace("</head>", CSS + "\n</head>", 1)
    return head, foot


def hero(eyebrow, h1, lede):
    return (f'<section class="dark band" style="padding-block:64px"><div class="wrap"><p class="eyebrow">{esc(eyebrow)}</p>'
            f'<h1 style="font-size:clamp(36px,6vw,64px)">{esc(h1)}</h1><p class="lede" style="margin-top:18px">{esc(lede)}</p></div></section>\n')


def build_feedback(lang):
    t, th = T[lang], lang == "th"
    li = 1 if th else 0
    head, foot = page_head(lang, t["title"], t["desc"], "feedback")

    def rate(name):
        return '<div class="rate">' + "".join(
            f'<label><input type="radio" name="{name}" value="{v}"{" required" if i == 0 else ""}><span><b>{v}</b> {esc(lab)}</span></label>'
            for i, (v, lab) in enumerate(SCALE[lang])) + "</div>"
    qs = ""
    for (g_en, g_th), items in GROUPS:
        qs += f"<h3>{esc(g_th if th else g_en)}</h3>"
        for k, en, tth in items:
            qs += f'<div class="q"><p>{k[1:]}. {esc(tth if th else en)}</p>{rate(k)}</div>'
    nps = '<div class="rate nps">' + "".join(
        f'<label><input type="radio" name="nps" value="{i}"{" required" if i == 0 else ""}><span>{i}</span></label>' for i in range(11)) + "</div>"

    body = (hero(t["eyebrow"], t["h1"], t["lede"]) +
        '<section class="band light" style="padding-block:48px"><div class="wrap fbw">'
        f'<form id="fb-login" style="margin-top:0"><fieldset><legend>{esc(t["s_login"])}</legend><p class="fine">{esc(t["login_note"])}</p>'
        f'<div class="two"><label for="f-phone">{esc(t["phone"])}<input id="f-phone" autocomplete="off" autocapitalize="characters" spellcheck="false" required style="text-transform:uppercase;letter-spacing:.12em"></label>'
        f'<div style="align-self:end"><button class="btn" type="submit">{esc(t["go"])}</button></div></div>'
        f'<p class="fine" id="fb-nf" hidden style="color:#B42318"></p></fieldset></form>'
        f'<form id="fb-form" hidden><div class="jobbox" id="fb-job"></div>'
        f'<fieldset><legend>{esc(t["s_q"])}</legend><p class="fine">{esc(t["scale_note"])}</p>{qs}</fieldset>'
        f'<fieldset><legend>{esc(t["s_nps"])}</legend><div class="q" style="border:0;padding:0"><p>11. {esc(t["nps_q"])}</p>{nps}'
        f'<div class="npsl"><span>{esc(t["nps_lo"])}</span><span>{esc(t["nps_hi"])}</span></div></div></fieldset>'
        f'<fieldset><legend>{esc(t["s_you"])}</legend><label for="f-name">{esc(t["name"])}<input id="f-name" name="name" required autocomplete="name"></label>'
        f'<label for="f-com">{esc(t["comment"])}<textarea id="f-com" name="comment" rows="4"></textarea></label></fieldset>'
        f'<p class="fine">{esc(t["privacy"])}</p><p class="fine" id="fb-out" style="color:#B42318"></p><button class="btn" type="submit">{esc(t["send"])}</button></form>'
        '</div></section>\n')
    L = {k: t[k] for k in ["jl", "tl", "nf", "sending", "fail", "done", "send", "wrongrole"]}
    script = ("<script>window.FB_T=" + json.dumps(L, ensure_ascii=False) + ";window.FB_LANG=" + json.dumps("Thai" if th else "English") + ";</script>\n" + r"""<script>
(function(){var T=window.FB_T,$=function(i){return document.getElementById(i)},code='',cur=null;
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function api(a,b){return fetch('/api/feedback?a='+a,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(b)}).then(function(r){return r.json().then(function(j){if(!r.ok){var e=new Error(j.error||r.status);e.code=j.error;throw e}return j})})}
function msg(t){$('fb-nf').textContent=t;$('fb-nf').hidden=false}
function open(){code=$('f-phone').value.trim().toUpperCase();$('fb-nf').hidden=true;$('fb-form').hidden=true;if(!code)return;
 api('code',{code:code}).then(function(r){if(r.role!=='customer')return msg(T.wrongrole);if(r.used)return msg(T.done);cur=r;
  $('fb-job').innerHTML='<b>'+esc(T.jl)+':</b> '+esc(r.job)+'<br><b>'+esc(T.tl)+':</b> '+esc(r.team);$('fb-form').hidden=false;$('fb-form').scrollIntoView({behavior:'smooth'})})
 .catch(function(){msg(T.nf)})}
$('fb-login').addEventListener('submit',function(e){e.preventDefault();open()});
var q=new URLSearchParams(location.search).get('c');if(q){$('f-phone').value=q;open()}
$('fb-form').addEventListener('submit',function(e){e.preventDefault();if(!cur)return;var f=e.target,b={code:code,language:window.FB_LANG,name:f.name.value,comment:f.comment.value};
 for(var i=1;i<=10;i++){var c=f.querySelector('input[name=q'+i+']:checked');b['q'+i]=c?c.value:''}var n=f.querySelector('input[name=nps]:checked');b.nps=n?n.value:'';
 var btn=f.querySelector('button[type=submit]');btn.disabled=true;btn.textContent=T.sending;$('fb-out').textContent='';
 api('submit',b).then(function(){try{sessionStorage.setItem('ga_form','job-feedback')}catch(x){}location.href=(window.FB_LANG==='Thai'?'/th':'')+'/thanks.html'})
 .catch(function(err){btn.disabled=false;btn.textContent=T.send;$('fb-out').textContent=err.code==='already-rated'?T.done:T.fail})});
})();
</script>
""")
    out = ROOT / ("th/feedback.html" if th else "feedback.html")
    out.write_text(head + body + script + foot, encoding="utf-8")
    print("wrote", out.relative_to(ROOT))


def build_report(lang):
    t, th = T[lang], lang == "th"
    head, foot = page_head(lang, t["r_title"], t["r_desc"], "job-report")
    body = (hero(t["r_eyebrow"], t["r_h1"], t["r_lede"]) +
        '<section class="band light" style="padding-block:48px"><div class="wrap fbw">'
        f'<form id="rp-login" style="margin-top:0"><fieldset><legend>{esc(t["r_s0"])}</legend><p class="fine">{esc(t["r_code_note"])}</p>'
        f'<div class="two"><label for="rp-code">{esc(t["r_code"])}<input id="rp-code" autocomplete="off" autocapitalize="characters" spellcheck="false" required style="text-transform:uppercase;letter-spacing:.12em"></label>'
        f'<div style="align-self:end"><button class="btn" type="submit">{esc(t["r_open"])}</button></div></div>'
        f'<p class="fine" id="rp-msg" hidden style="color:#B42318"></p></fieldset></form>'
        f'<form name="job-report" method="POST" data-netlify="true" netlify-honeypot="bot-field" enctype="multipart/form-data" action="{t["pre"]}/thanks.html" hidden>'
        f'<input type="hidden" name="form-name" value="job-report"><input type="hidden" name="language" value="{"Thai" if th else "English"}"><p hidden><label>Leave empty <input name="bot-field"></label></p>'
        f'<input type="hidden" name="code" id="rp-c"><input type="hidden" name="job" id="rp-j"><input type="hidden" name="team" id="rp-t">'
        f'<div class="jobbox" id="rp-job"></div>'
        f'<fieldset><legend>{esc(t["r_s3"])}</legend><label for="r-date">{esc(t["r_date"])}<input id="r-date" name="completed" type="date" required></label>'
        f'<label for="r-work">{esc(t["r_work"])}<textarea id="r-work" name="work-done" rows="4" required></textarea></label>'
        f'<label for="r-mat">{esc(t["r_mat"])}<textarea id="r-mat" name="materials" rows="2"></textarea></label>'
        f'<label for="r-test">{esc(t["r_test"])}<textarea id="r-test" name="test-results" rows="2"></textarea></label>'
        f'<label for="r-issue">{esc(t["r_issue"])}<textarea id="r-issue" name="follow-up" rows="2"></textarea></label></fieldset>'
        f'<fieldset><legend>{esc(t["r_s4"])}</legend><p class="fine">{esc(t["r_files_note"])}</p>'
        f'<div class="two"><label for="r-pb">{esc(t["r_before"])}<input id="r-pb" name="photo-before" type="file" accept=".jpg,.jpeg,.png"></label>'
        f'<label for="r-pa">{esc(t["r_after"])}<input id="r-pa" name="photo-after" type="file" accept=".jpg,.jpeg,.png"></label></div>'
        f'<div class="two"><label for="r-p3">{esc(t["r_ph3"])}<input id="r-p3" name="photo-3" type="file" accept=".jpg,.jpeg,.png"></label>'
        f'<label for="r-file">{esc(t["r_file"])}<input id="r-file" name="report-file" type="file" accept=".pdf"></label></div></fieldset>'
        f'<fieldset><legend>{esc(t["r_s5"])}</legend><div class="two"><label for="r-name">{esc(t["r_name"])}<input id="r-name" name="reporter-name" required autocomplete="name"></label>'
        f'<label for="r-phone">{esc(t["r_phone"])}<input id="r-phone" name="reporter-phone" type="tel" required autocomplete="tel"></label></div></fieldset>'
        f'<button class="btn" type="submit">{esc(t["r_send"])}</button></form></div></section>\n')
    L = {"nf": t["r_nf"], "used": t["r_used"], "wrong": t["r_wrong"], "jl": t["jl"], "tl": t["tl"]}
    script = ("<script>window.RP_T=" + json.dumps(L, ensure_ascii=False) + ";</script>\n" + r"""<script>
(function(){var T=window.RP_T,$=function(i){return document.getElementById(i)},f=document.querySelector('form[name=job-report]');
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function msg(t){$('rp-msg').textContent=t;$('rp-msg').hidden=false}
function open(){var code=$('rp-code').value.trim().toUpperCase();$('rp-msg').hidden=true;f.hidden=true;if(!code)return;
 fetch('/api/feedback?a=code',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({code:code})}).then(function(r){return r.ok?r.json():Promise.reject()})
 .then(function(r){if(r.role!=='installer')return msg(T.wrong);if(r.used)return msg(T.used);
  $('rp-c').value=code;$('rp-j').value=r.job;$('rp-t').value=r.team;$('rp-job').innerHTML='<b>'+esc(T.jl)+':</b> '+esc(r.job)+'<br><b>'+esc(T.tl)+':</b> '+esc(r.team);
  var d=$('r-date');if(!d.value)d.value=new Date().toISOString().slice(0,10);f.hidden=false;f.scrollIntoView({behavior:'smooth'})}).catch(function(){msg(T.nf)})}
$('rp-login').addEventListener('submit',function(e){e.preventDefault();open()});
var q=new URLSearchParams(location.search).get('c');if(q){$('rp-code').value=q;open()}
})();
</script>
""")
    out = ROOT / ("th/job-report.html" if th else "job-report.html")
    out.write_text(head + body + script + foot, encoding="utf-8")
    print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    for lg in ("en", "th"):
        build_feedback(lg)
        build_report(lg)
