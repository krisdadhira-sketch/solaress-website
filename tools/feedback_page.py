# -*- coding: utf-8 -*-
"""Customer satisfaction feedback page after a job: /feedback.html and /th/feedback.html.

10 questions scored 5/4/2/1 (no middle score) (work, personality, interaction), NPS 0-10 and "will you bring more business?".
Form "job-feedback" (Netlify Forms) -> netlify/functions/submission-created.mjs saves it in Blobs store
"feedback" -> team scorecards at /feedback-admin.html (same password as /members-admin.html).

Prefill: /feedback.html?job=<job title>&team=<team name> (send this link to the customer after a job).
Job list is read from the Jobs page; teams come from approved installer partners and TSIA members.
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

MORE = {"en": [("yes-job", "Yes: I have another job for this team or Solar ESS"), ("yes-referral", "Yes: I will refer a friend, family member or business"),
               ("maybe", "Maybe later"), ("no", "No, not at the moment")],
        "th": [("yes-job", "ใช่: มีงานอื่นให้ทีมนี้หรือ Solar ESS อีก"), ("yes-referral", "ใช่: จะแนะนำเพื่อน ญาติ หรือธุรกิจที่รู้จัก"),
               ("maybe", "อาจจะในภายหลัง"), ("no", "ยังไม่มีในตอนนี้")]}

T = {
"en": dict(pre="", title="Rate a Finished Job · Customer Feedback | Solar ESS",
    desc="Tell us how the installer did: 10 quick questions on the work, the team and communication, scored 1 to 5.",
    eyebrow="Customer feedback", h1="How did the job go?",
    lede="Your scores keep every installer team honest. Ten quick questions, about two minutes. Your answers go to Solar ESS only and are never published with your name.",
    s_job="1. The job", job="Which job?", job_other="Other or not listed", team="Which team did the work?", team_sol="Solar ESS team", team_other="Team name, if not listed",
    s_q="2. Your scores", scale_note="5 Perfect · 4 Good · 2 Fair · 1 Poor (there is no middle score: please choose the one closest to your experience)",
    s_nps="3. Would you recommend us?", nps_q="How likely are you to recommend this team and Solar ESS to a friend or colleague?", nps_lo="0 = not at all", nps_hi="10 = extremely likely",
    more_q="Will you bring us more business?", ref="Who should we contact? Name and phone (optional)",
    s_you="4. About you", name="Your name", phone="Phone (optional, kept private)", comment="Anything else we should know: what went well, what to improve (optional)",
    send="Send feedback", choose="Choose one", privacy="We use your answers only to check and improve our installer teams."),
"th": dict(pre="/th", title="ประเมินความพึงพอใจหลังจบงาน | Solar ESS",
    desc="บอกเราว่าทีมช่างทำงานเป็นอย่างไร 10 คำถามสั้น ๆ เรื่องงาน ทีม และการสื่อสาร ให้คะแนน 1 ถึง 5",
    eyebrow="ประเมินความพึงพอใจ", h1="งานเป็นอย่างไรบ้าง",
    lede="คะแนนของคุณช่วยให้ทีมช่างทุกทีมรักษามาตรฐาน 10 คำถามสั้น ๆ ใช้เวลาประมาณ 2 นาที คำตอบส่งถึง Solar ESS เท่านั้น และจะไม่เผยแพร่พร้อมชื่อของคุณ",
    s_job="1. งานที่ประเมิน", job="งานไหน", job_other="งานอื่น หรือไม่มีในรายการ", team="ทีมไหนเป็นผู้ทำงาน", team_sol="ทีม Solar ESS", team_other="ชื่อทีม (หากไม่มีในรายการ)",
    s_q="2. คะแนนของคุณ", scale_note="5 ดีเยี่ยม · 4 ดี · 2 พอใช้ · 1 ควรปรับปรุง (ไม่มีคะแนนกลาง กรุณาเลือกข้อที่ใกล้เคียงกับความรู้สึกของคุณที่สุด)",
    s_nps="3. คุณจะแนะนำเราไหม", nps_q="คุณมีแนวโน้มจะแนะนำทีมนี้และ Solar ESS ให้เพื่อนหรือคนรู้จักมากน้อยเพียงใด", nps_lo="0 = ไม่แนะนำเลย", nps_hi="10 = แนะนำแน่นอน",
    more_q="คุณจะมีงานเพิ่มเติมหรือแนะนำลูกค้าให้เราไหม", ref="ให้เราติดต่อใคร ชื่อและเบอร์โทร (ไม่บังคับ)",
    s_you="4. ข้อมูลของคุณ", name="ชื่อของคุณ", phone="เบอร์โทร (ไม่บังคับ เก็บเป็นความลับ)", comment="ความเห็นเพิ่มเติม: สิ่งที่ดี และสิ่งที่ควรปรับปรุง (ไม่บังคับ)",
    send="ส่งแบบประเมิน", choose="เลือก", privacy="เราใช้คำตอบของคุณเพื่อตรวจสอบและพัฒนาทีมช่างของเราเท่านั้น"),
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
.fbw .fine{font-size:13px;color:var(--mute);margin:0}
@media (max-width:640px){.fbw .two{grid-template-columns:minmax(0,1fr)}.rate span{padding:7px 10px}.nps span{min-width:36px}}
</style>"""


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def jobs(lang):
    h = (ROOT / ("th/job.html" if lang == "th" else "job.html")).read_text(encoding="utf-8")
    m = re.search(r'<select id="j-role"[^>]*>(.*?)</select>', h, re.S)
    out = re.findall(r"<option[^>]*>(.*?)</option>", m.group(1)) if m else []
    return [re.sub(r"<[^>]+>", "", o).strip() for o in out if o.strip()]


def build(lang):
    t, th = T[lang], lang == "th"
    li = 1 if th else 0
    src = (ROOT / ("th/team.html" if th else "team.html")).read_text(encoding="utf-8")
    head = src[:src.index('<section class="dark band"')]
    foot = re.sub(r'\n?<script src="/tsia\.js[^>]*></script>', "", src[src.index("<footer>"):])
    url = f"https://solaress.org{t['pre']}/feedback"
    head = re.sub(r"<title>.*?</title>", f"<title>{esc(t['title'])}</title>", head, count=1)
    for prop, val in [("og:title", t["title"]), ("og:description", t["desc"]), ("og:url", url + ".html")]:
        head = re.sub(r'(<meta property="%s" content=")[^"]*' % prop, lambda m: m.group(1) + esc(val), head, count=1)
    head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + esc(t["desc"]), head, count=1)
    head = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', head, count=1)
    head = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\s*', "", head)
    head = head.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex, follow">', 1)
    head = re.sub(r'<span class="langsw">.*?</span>(?=</nav>)',
                  '<span class="langsw"><a href="/feedback.html" lang="en"' + ('' if th else ' aria-current="true"') + '>EN</a>'
                  '<a href="/th/feedback.html" lang="th" style="font-family:var(--thai)"' + (' aria-current="true"' if th else '') + '>ไทย</a></span>',
                  head, count=1, flags=re.S)
    head = head.replace("</head>", CSS + "\n</head>", 1)

    job_opts = f'<option value="">{esc(t["choose"])}</option>' + "".join(f'<option>{esc(j)}</option>' for j in jobs(lang)) + f'<option>{esc(t["job_other"])}</option>'
    team_opts = f'<option value="">{esc(t["choose"])}</option><option>{esc(t["team_sol"])}</option><option value="__other">{esc(t["team_other"])}</option>'

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
    more = '<div class="more">' + "".join(
        f'<label><input type="radio" name="more-business" value="{v}"{" required" if i == 0 else ""}><span>{esc(l)}</span></label>' for i, (v, l) in enumerate(MORE[lang])) + "</div>"

    body = (
        f'<section class="dark band" style="padding-block:64px"><div class="wrap"><p class="eyebrow">{esc(t["eyebrow"])}</p>'
        f'<h1 style="font-size:clamp(36px,6vw,64px)">{esc(t["h1"])}</h1><p class="lede" style="margin-top:18px">{esc(t["lede"])}</p></div></section>\n'
        f'<section class="band light" style="padding-block:48px"><div class="wrap fbw">'
        f'<form name="job-feedback" method="POST" data-netlify="true" netlify-honeypot="bot-field" action="{t["pre"]}/thanks.html">'
        f'<input type="hidden" name="form-name" value="job-feedback"><input type="hidden" name="language" value="{"Thai" if th else "English"}">'
        f'<p hidden><label>Leave empty <input name="bot-field"></label></p>'
        f'<fieldset><legend>{esc(t["s_job"])}</legend>'
        f'<label for="f-job">{esc(t["job"])}<select id="f-job" name="job" required>{job_opts}</select></label>'
        f'<div class="two"><label for="f-team">{esc(t["team"])}<select id="f-team" name="team" required>{team_opts}</select></label>'
        f'<label for="f-team-other" id="f-team-other-l" hidden>{esc(t["team_other"])}<input id="f-team-other" name="team-other"></label></div></fieldset>'
        f'<fieldset><legend>{esc(t["s_q"])}</legend><p class="fine">{esc(t["scale_note"])}</p>{qs}</fieldset>'
        f'<fieldset><legend>{esc(t["s_nps"])}</legend><div class="q" style="border:0;padding:0"><p>11. {esc(t["nps_q"])}</p>{nps}'
        f'<div class="npsl"><span>{esc(t["nps_lo"])}</span><span>{esc(t["nps_hi"])}</span></div></div>'
        f'<div class="q"><p>12. {esc(t["more_q"])}</p>{more}</div>'
        f'<label for="f-ref">{esc(t["ref"])}<input id="f-ref" name="referral"></label></fieldset>'
        f'<fieldset><legend>{esc(t["s_you"])}</legend><div class="two"><label for="f-name">{esc(t["name"])}<input id="f-name" name="name" required autocomplete="name"></label>'
        f'<label for="f-phone">{esc(t["phone"])}<input id="f-phone" name="phone" type="tel" autocomplete="tel"></label></div>'
        f'<label for="f-com">{esc(t["comment"])}<textarea id="f-com" name="comment" rows="4"></textarea></label></fieldset>'
        f'<p class="fine">{esc(t["privacy"])}</p><button class="btn" type="submit">{esc(t["send"])}</button></form></div></section>\n'
    )
    script = """<script>
(function(){var f=document.querySelector('form[name=job-feedback]');if(!f)return;var q=new URLSearchParams(location.search);
var job=f.querySelector('#f-job'),team=f.querySelector('#f-team'),ol=document.getElementById('f-team-other-l'),oi=document.getElementById('f-team-other');
function pick(sel,v){if(!v)return false;for(var i=0;i<sel.options.length;i++){if(sel.options[i].text.trim()===v.trim()){sel.selectedIndex=i;return true}}return false}
function syncTeam(){var o=team.value==='__other';ol.hidden=!o;oi.required=o}
team.addEventListener('change',syncTeam);
var wantTeam=q.get('team');
function addTeams(names){var other=team.querySelector('option[value=__other]');names.forEach(function(n){if(!n)return;for(var i=0;i<team.options.length;i++)if(team.options[i].text===n)return;var o=document.createElement('option');o.textContent=n;team.insertBefore(o,other)});
 if(wantTeam&&!pick(team,wantTeam)){team.value='__other';oi.value=wantTeam}syncTeam()}
Promise.all(['partner','tsia'].map(function(t){return fetch('/api/members?a=public&type='+t).then(function(r){return r.ok?r.json():{items:[]}}).catch(function(){return{items:[]}})}))
 .then(function(rs){addTeams([].concat.apply([],rs.map(function(r){return(r.items||[]).map(function(x){return x.name})})))});
if(q.get('job')&&!pick(job,q.get('job'))){job.selectedIndex=job.options.length-1}
})();
</script>
"""
    page = head + body + script + foot
    out = ROOT / ("th/feedback.html" if th else "feedback.html")
    out.write_text(page, encoding="utf-8")
    print("wrote", out.relative_to(ROOT), len(page))


if __name__ == "__main__":
    build("en")
    build("th")
