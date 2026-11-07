#!/usr/bin/env python3
"""Builds /community.html (EN) and /th/community.html (TH): the Solar Enthusiast community.

Anyone can register (free); Solar ESS approves each member in /members-admin.html (tab "Solar Enthusiasts").
Approved members can post questions (tab "Questions"); a question shows on this page only after
Solar ESS writes an answer and publishes it. Approved members also receive the member price-list
password for /members.html (sent by Solar ESS by LINE or phone).

API: /api/members?a=enthusiast | a=ask | a=qa  (netlify/functions/members/members.mjs)
Uses members.html / th/members.html as the page shell (head, nav, footer).
Run from the repo root:  python3 tools/community_page.py && python3 tools/form_ink.py
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from partners_page import PROVINCES, REGIONS  # noqa: E402

T = {
"en": dict(
  lang="en", path="/community.html", title="Solar Enthusiast community | Solar ESS",
  desc="Join the Solar ESS Solar Enthusiast community: register free, ask questions answered by Solar ESS, and buy our products at member prices.",
  eyebrow="Solar Enthusiast community", h1="Join the<br>solar enthusiasts.",
  lede="Register free to ask questions, learn from answers by the Solar ESS team, and buy our products at member prices.",
  steps=["Free to join", "Approved within 2 business days", "Member prices on panels, inverters and batteries"],
  f_name="Full name", f_phone="Mobile phone", f_email="Email (optional)", f_prov="Province", f_prov_ph="Choose your province",
  f_int="What interests you", ints=[("home","Home solar"),("hybrid","Hybrid and batteries"),("offgrid","Off-grid"),("ev","EV charging"),("learn","Learning and DIY"),("business","Business or farm")],
  f_agree="I agree that Solar ESS may contact me about my registration.", f_btn="Register",
  r_ok="Thank you! Your registration is waiting for approval. We will contact you within 2 business days.",
  r_exist="This phone number is already registered.", r_exist_ok=" You are approved: you can ask questions below.",
  r_err="Please fill in your name, a valid mobile number and tick the agreement.", r_fail="Sending failed. Please try again, or contact us by LINE solaress1.",
  b_title="What members get",
  benefits=[("Ask and interact","Post your solar questions. The Solar ESS team answers, and good questions are shared with everyone."),
            ("Learn from real answers","Read questions from other homeowners, farmers and installers, answered from real installations across Thailand."),
            ("Member prices","Buy panels, inverters, batteries and parts at member prices. Approved members receive the member price-list password.")],
  a_eyebrow="Ask a question", a_title="Ask the Solar ESS team.",
  a_lede="For approved members. Use the mobile number you registered with. Your question appears on this page after we answer it, with your first name and province only.",
  a_phone="Registered mobile phone", a_topic="Topic", a_q="Your question", a_q_ph="For example: my bill is 3,000 baht a month, which system size fits?", a_btn="Send question",
  topics=["Panels","Inverters","Batteries","Design and sizing","Installation","Bills and sell-back","EV charging","Other"],
  q_ok="Thank you! Your question has been sent. It will appear here after the Solar ESS team answers it.",
  q_reg="This number is not registered yet. Please register above first.", q_wait="Your registration is still waiting for approval. You can ask questions once it is approved.",
  q_limit="You already have 5 questions waiting for an answer. Please wait for our replies.", q_err="Please enter your registered mobile number and a question of at least 10 characters.",
  l_eyebrow="Answered questions", l_title="Questions from the community.", l_all="All", l_empty="No answered questions yet. Be the first to ask!", l_ans="Solar ESS answers", l_by="Asked by",
  p_title="Member prices", p_text="Approved members receive the password for the member price list. Download the latest list on the Members page.", p_btn="Go to the Members page", p_href="/members.html",
  footer_link="Community",
),
"th": dict(
  lang="th", path="/th/community.html", title="ชุมชนคนรักโซลาร์ | Solar ESS",
  desc="สมัครเป็นสมาชิกชุมชนคนรักโซลาร์ของโซลาร์ เอสส์ ฟรี ถามคำถามโดยทีมงานโซลาร์ เอสส์ตอบ และซื้อสินค้าในราคาสมาชิก",
  eyebrow="ชุมชนคนรักโซลาร์ (Solar Enthusiast)", h1="ร่วมเป็น<br>คนรักโซลาร์",
  lede="สมัครฟรี เพื่อถามคำถาม เรียนรู้จากคำตอบของทีมงานโซลาร์ เอสส์ และซื้อสินค้าของเราในราคาสมาชิก",
  steps=["สมัครฟรี", "อนุมัติภายใน 2 วันทำการ", "ราคาสมาชิกสำหรับแผง อินเวอร์เตอร์ และแบตเตอรี่"],
  f_name="ชื่อ-นามสกุล", f_phone="เบอร์มือถือ", f_email="อีเมล (ไม่บังคับ)", f_prov="จังหวัด", f_prov_ph="เลือกจังหวัด",
  f_int="สนใจเรื่องใด", ints=[("home","โซลาร์บ้าน"),("hybrid","ไฮบริดและแบตเตอรี่"),("offgrid","ออฟกริด"),("ev","ชาร์จรถไฟฟ้า"),("learn","เรียนรู้และติดตั้งเอง"),("business","ธุรกิจหรือฟาร์ม")],
  f_agree="ยินยอมให้โซลาร์ เอสส์ติดต่อเกี่ยวกับการสมัครสมาชิก", f_btn="สมัครสมาชิก",
  r_ok="ขอบคุณครับ การสมัครของคุณรอการอนุมัติ เราจะติดต่อกลับภายใน 2 วันทำการ",
  r_exist="เบอร์นี้สมัครไว้แล้ว", r_exist_ok=" ได้รับอนุมัติแล้ว ถามคำถามด้านล่างได้เลย",
  r_err="กรุณากรอกชื่อ เบอร์มือถือที่ถูกต้อง และติ๊กยินยอม", r_fail="ส่งไม่สำเร็จ กรุณาลองใหม่ หรือติดต่อทาง LINE solaress1",
  b_title="สิทธิประโยชน์ของสมาชิก",
  benefits=[("ถามและพูดคุย","ส่งคำถามเรื่องโซลาร์ ทีมงานโซลาร์ เอสส์ตอบ และคำถามที่เป็นประโยชน์จะแบ่งปันให้ทุกคน"),
            ("เรียนรู้จากคำตอบจริง","อ่านคำถามจากเจ้าของบ้าน เกษตรกร และช่างติดตั้ง พร้อมคำตอบจากงานติดตั้งจริงทั่วประเทศไทย"),
            ("ราคาสมาชิก","ซื้อแผง อินเวอร์เตอร์ แบตเตอรี่ และอุปกรณ์ในราคาสมาชิก สมาชิกที่ได้รับอนุมัติจะได้รับรหัสดาวน์โหลดรายการราคาสมาชิก")],
  a_eyebrow="ถามคำถาม", a_title="ถามทีมงานโซลาร์ เอสส์",
  a_lede="สำหรับสมาชิกที่ได้รับอนุมัติแล้ว ใช้เบอร์มือถือที่สมัครไว้ คำถามจะแสดงในหน้านี้หลังจากเราตอบแล้ว โดยแสดงเฉพาะชื่อและจังหวัดของคุณ",
  a_phone="เบอร์มือถือที่สมัครไว้", a_topic="หัวข้อ", a_q="คำถามของคุณ", a_q_ph="เช่น ค่าไฟเดือนละ 3,000 บาท ควรติดตั้งระบบขนาดเท่าไร", a_btn="ส่งคำถาม",
  topics=["แผงโซลาร์","อินเวอร์เตอร์","แบตเตอรี่","ออกแบบและเลือกขนาด","การติดตั้ง","ค่าไฟและการขายไฟ","ชาร์จรถไฟฟ้า","อื่น ๆ"],
  q_ok="ขอบคุณครับ ส่งคำถามแล้ว คำถามจะแสดงในหน้านี้หลังจากทีมงานโซลาร์ เอสส์ตอบ",
  q_reg="เบอร์นี้ยังไม่ได้สมัคร กรุณาสมัครสมาชิกด้านบนก่อน", q_wait="การสมัครของคุณยังรอการอนุมัติ ถามคำถามได้เมื่อได้รับอนุมัติแล้ว",
  q_limit="คุณมีคำถามรอคำตอบอยู่ 5 ข้อแล้ว กรุณารอคำตอบจากเราก่อน", q_err="กรุณากรอกเบอร์มือถือที่สมัครไว้ และคำถามอย่างน้อย 10 ตัวอักษร",
  l_eyebrow="คำถามที่ตอบแล้ว", l_title="คำถามจากชุมชน", l_all="ทั้งหมด", l_empty="ยังไม่มีคำถามที่ตอบแล้ว มาเป็นคนแรกที่ถามกัน", l_ans="โซลาร์ เอสส์ตอบ", l_by="ถามโดย",
  p_title="ราคาสมาชิก", p_text="สมาชิกที่ได้รับอนุมัติจะได้รับรหัสสำหรับดาวน์โหลดรายการราคาสมาชิก ดาวน์โหลดรายการล่าสุดได้ที่หน้าสมาชิก", p_btn="ไปที่หน้าสมาชิก", p_href="/th/members.html",
  footer_link="ชุมชน",
),
}

CSS = """<style id="cm-css">
.cm-wrap{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:56px;align-items:start}
.cm-form{display:grid;gap:14px;max-width:460px}
.cm-form label{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;display:grid;gap:6px;opacity:.85}
.cm-form input,.cm-form select,.cm-form textarea{font:inherit;font-size:16px;padding:10px 12px;border:1px solid #CBD2E6;border-radius:8px;text-transform:none;letter-spacing:0}
.cm-form textarea{min-height:120px;resize:vertical}
.cm-chips{display:flex;flex-wrap:wrap;gap:8px}
.cm-chips label{display:inline-flex;align-items:center;gap:6px;font-family:inherit;font-size:14px;letter-spacing:0;text-transform:none;border:1px solid rgba(255,255,255,.35);border-radius:999px;padding:6px 12px;cursor:pointer;opacity:1}
.light .cm-chips label{border-color:#CBD2E6}
.cm-agree{display:flex!important;grid-template-columns:none;align-items:flex-start;gap:8px;font-family:inherit!important;font-size:14px!important;letter-spacing:0!important;text-transform:none!important}
.cm-msg{font-size:15px;line-height:1.5;min-height:1em}.cm-msg.ok{color:#22C55E}.cm-msg.err{color:#F87171}.light .cm-msg.ok{color:#15803D}.light .cm-msg.err{color:#B42318}
.cm-ben{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;margin-top:26px}
.cm-ben div{border:1px solid #D9DDF5;border-top:4px solid var(--blue,#2563EB);border-radius:12px;padding:20px;background:#fff}
.cm-ben h3{margin:0 0 8px;font-size:19px}
.cm-ask{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:48px;align-items:start}
.cm-topics{display:flex;flex-wrap:wrap;gap:8px;margin:22px 0}
.cm-topics button{font:inherit;font-size:14px;border:1px solid #CBD2E6;background:#fff;border-radius:999px;padding:6px 14px;cursor:pointer}
.cm-topics button.on{background:var(--navy,#0A0E2E);color:#fff;border-color:var(--navy,#0A0E2E)}
.cm-q{border:1px solid #D9DDF5;border-radius:12px;padding:20px 22px;margin-bottom:14px;background:#fff}
.cm-q .tp{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--hot)}
.cm-q h3{margin:8px 0 6px;font-size:18px;line-height:1.45;white-space:pre-wrap}
.cm-q .by{font-size:13px;opacity:.65}
.cm-q .an{margin-top:12px;padding:12px 14px;background:#F3F4FC;border-left:4px solid var(--navy,#0A0E2E);border-radius:6px;white-space:pre-wrap;line-height:1.6}
.cm-q .an b{display:block;font-size:12px;font-family:var(--mono);letter-spacing:.1em;text-transform:uppercase;margin-bottom:4px}
@media(max-width:860px){.cm-wrap,.cm-ask{grid-template-columns:minmax(0,1fr)}.cm-ben{grid-template-columns:minmax(0,1fr)}}
</style>"""


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def province_options(lang):
    out = []
    for key, en, th in REGIONS:
        out.append(f'<optgroup label="{en if lang == "en" else th}">')
        for pe, pt in sorted(PROVINCES[key], key=lambda p: p[0] if lang == "en" else p[1]):
            out.append(f'<option value="{pe}" data-region="{key}">{pe if lang == "en" else pt}</option>')
        out.append("</optgroup>")
    return "".join(out)


def body(t):
    L = t["lang"]
    steps = "".join(f"<li>{s}</li>" for s in t["steps"])
    ints = "".join(f'<label><input type="checkbox" name="interests" value="{v}"> {lab}</label>' for v, lab in t["ints"])
    ben = "".join(f"<div><h3>{h}</h3><p>{p}</p></div>" for h, p in t["benefits"])
    topics = "".join(f'<option value="{esc(x)}">{x}</option>' for x in t["topics"])
    msgs = {k: t[k] for k in ("r_ok", "r_exist", "r_exist_ok", "r_err", "r_fail", "q_ok", "q_reg", "q_wait", "q_limit", "q_err", "l_all", "l_empty", "l_ans", "l_by")}
    import json
    return f"""
<section class="dark band" style="padding-block:72px"><div class="wrap cm-wrap">
<div><p class="eyebrow">{t["eyebrow"]}</p><h1 style="font-size:clamp(36px,6vw,64px)">{t["h1"]}</h1>
<p class="lede" style="margin-top:18px">{t["lede"]}</p><ul class="steps">{steps}</ul></div>
<form class="cm-form" id="cm-reg" novalidate>
<p hidden><label>Leave empty<input name="bot-field"></label></p>
<label>{t["f_name"]} *<input name="name" autocomplete="name" required maxlength="80"></label>
<label>{t["f_phone"]} *<input name="phone" type="tel" inputmode="tel" autocomplete="tel" required placeholder="08x xxx xxxx"></label>
<label>{t["f_email"]}<input name="email" type="email" autocomplete="email"></label>
<label>{t["f_prov"]}<select name="province"><option value="">{t["f_prov_ph"]}</option>{province_options(L)}</select></label>
<input type="hidden" name="region">
<div><label style="margin-bottom:8px">{t["f_int"]}</label><div class="cm-chips">{ints}</div></div>
<label class="cm-agree"><input type="checkbox" name="agree" required> <span>{t["f_agree"]}</span></label>
<button class="btn" type="submit">{t["f_btn"]}</button>
<div class="cm-msg" id="cm-reg-msg" role="status"></div>
</form>
</div></section>
<section class="band light" style="padding-block:60px"><div class="wrap"><h2 style="font-size:clamp(26px,3.4vw,38px)">{t["b_title"]}</h2><div class="cm-ben">{ben}</div></div></section>
<section class="band" style="padding-block:60px;background:var(--paper)" id="ask"><div class="wrap cm-ask light">
<div><p class="eyebrow">{t["a_eyebrow"]}</p><h2 style="font-size:clamp(26px,3.4vw,38px)">{t["a_title"]}</h2><p style="margin-top:12px;line-height:1.6">{t["a_lede"]}</p></div>
<form class="cm-form" id="cm-ask" novalidate style="max-width:none">
<p hidden><label>Leave empty<input name="bot-field"></label></p>
<label>{t["a_phone"]} *<input name="phone" type="tel" inputmode="tel" autocomplete="tel" required placeholder="08x xxx xxxx"></label>
<label>{t["a_topic"]}<select name="topic">{topics}</select></label>
<label>{t["a_q"]} *<textarea name="question" required maxlength="1500" placeholder="{esc(t["a_q_ph"])}"></textarea></label>
<button class="btn" type="submit">{t["a_btn"]}</button>
<div class="cm-msg" id="cm-ask-msg" role="status"></div>
</form></div></section>
<section class="band light" style="padding-block:60px" id="questions"><div class="wrap">
<p class="eyebrow">{t["l_eyebrow"]}</p><h2 style="font-size:clamp(26px,3.4vw,38px)">{t["l_title"]}</h2>
<div class="cm-topics" id="cm-topics"></div><div id="cm-list"></div>
</div></section>
<section class="dark band" style="padding-block:56px"><div class="wrap"><h2 style="font-size:clamp(24px,3.2vw,36px)">{t["p_title"]}</h2><p class="lede" style="margin-top:12px">{t["p_text"]}</p><p style="margin-top:22px"><a class="btn" href="{t["p_href"]}">{t["p_btn"]}</a></p></div></section>
<script>
(function(){{
var M={json.dumps(msgs, ensure_ascii=False)}, LANG="{L}";
function $(id){{return document.getElementById(id)}}
function esc(s){{return String(s==null?'':s).replace(/[&<>"']/g,function(c){{return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]}})}}
function say(el,cls,txt){{el.className='cm-msg '+cls;el.textContent=txt}}
function post(a,data){{return fetch('/api/members?a='+a,{{method:'POST',headers:{{'content-type':'application/json'}},body:JSON.stringify(data)}}).then(function(r){{return r.json().then(function(j){{j._s=r.status;return j}})}})}}
var reg=$('cm-reg'),prov=reg.querySelector('[name=province]');
prov.addEventListener('change',function(){{var o=prov.selectedOptions[0];reg.querySelector('[name=region]').value=o?(o.getAttribute('data-region')||''):''}});
reg.addEventListener('submit',function(e){{e.preventDefault();var f=new FormData(reg),m=$('cm-reg-msg');
 var d={{name:f.get('name'),phone:f.get('phone'),email:f.get('email'),province:f.get('province'),region:f.get('region'),interests:f.getAll('interests'),agree:!!f.get('agree'),language:LANG,'bot-field':f.get('bot-field')}};
 var digits=String(d.phone||'').replace(/\\D/g,'');
 if(!String(d.name||'').trim()||digits.length<9||!d.agree){{say(m,'err',M.r_err);return}}
 var b=reg.querySelector('button');b.disabled=true;
 post('enthusiast',d).then(function(j){{b.disabled=false;
  if(j._s===200&&j.existing){{say(m,'ok',M.r_exist+(j.status==='approved'?M.r_exist_ok:' '+M.r_ok))}}
  else if(j._s===200){{say(m,'ok',M.r_ok);reg.reset()}} else say(m,'err',j.error==='fields'||j.error==='agree'?M.r_err:M.r_fail)}})
 .catch(function(){{b.disabled=false;say(m,'err',M.r_fail)}})}});
var ask=$('cm-ask');
ask.addEventListener('submit',function(e){{e.preventDefault();var f=new FormData(ask),m=$('cm-ask-msg');
 var d={{phone:f.get('phone'),topic:f.get('topic'),question:f.get('question'),language:LANG,'bot-field':f.get('bot-field')}};
 if(String(d.phone||'').replace(/\\D/g,'').length<9||String(d.question||'').trim().length<10){{say(m,'err',M.q_err);return}}
 var b=ask.querySelector('button');b.disabled=true;
 post('ask',d).then(function(j){{b.disabled=false;
  if(j._s===200){{say(m,'ok',M.q_ok);ask.querySelector('textarea').value=''}}
  else say(m,'err',{{register:M.q_reg,waiting:M.q_wait,limit:M.q_limit,fields:M.q_err}}[j.error]||M.r_fail)}})
 .catch(function(){{b.disabled=false;say(m,'err',M.r_fail)}})}});
var items=[],cur='';
function draw(){{var l=items.filter(function(q){{return !cur||q.topic===cur}});
 $('cm-list').innerHTML=l.length?l.map(function(q){{var dt=q.answered?new Date(q.answered).toLocaleDateString(LANG==='th'?'th-TH':'en-GB',{{day:'numeric',month:'short',year:'numeric'}}):'';
  return '<article class="cm-q"><span class="tp">'+esc(q.topic)+'</span><h3>'+esc(q.question)+'</h3><div class="by">'+M.l_by+' '+esc(q.name)+(q.province?' · '+esc(q.province):'')+'</div><div class="an"><b>'+M.l_ans+(dt?' · '+dt:'')+'</b>'+esc(q.answer)+'</div></article>'}}).join(''):'<p>'+M.l_empty+'</p>'}}
fetch('/api/members?a=qa').then(function(r){{return r.json()}}).then(function(j){{items=j.items||[];
 var tps=[];items.forEach(function(q){{if(q.topic&&tps.indexOf(q.topic)<0)tps.push(q.topic)}});
 $('cm-topics').innerHTML=tps.length?['<button class="on" data-t="">'+M.l_all+'</button>'].concat(tps.map(function(t){{return '<button data-t="'+esc(t)+'">'+esc(t)+'</button>'}})).join(''):'';
 draw()}}).catch(function(){{draw()}});
$('cm-topics').addEventListener('click',function(e){{var t=e.target.closest('button');if(!t)return;cur=t.getAttribute('data-t');
 Array.prototype.forEach.call(this.children,function(b){{b.classList.toggle('on',b===t)}});draw()}});
}})();
</script>
"""


def build(lang, src):
    t = T[lang]
    s = (ROOT / src).read_text(encoding="utf-8")
    head_end = s.index("<!--/mnav-->") + len("<!--/mnav-->")
    foot = s.index("<footer")
    tail = re.sub(r"<script>\s*const form=document.getElementById\('mform'\).*?</script>\n?", "", s[foot:], flags=re.S)
    page = s[:head_end] + "\n" + body(t) + "\n" + tail
    # strip the members page's own script/css that comes after the shell, keep shell
    page = re.sub(r"<title>.*?</title>", f"<title>{t['title']}</title>", page, count=1, flags=re.S)
    page = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{esc(t["desc"])}">', page, count=1)
    page = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{esc(t["title"])}">', page)
    page = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{esc(t["desc"])}">', page)
    page = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="https://solaress.org{t["path"].replace(".html", "")}">', page)
    page = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="https://solaress.org{t["path"].replace(".html", "")}">', page)
    page = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?', "", page)
    alt = ('<link rel="alternate" hreflang="en" href="https://solaress.org/community">\n'
           '<link rel="alternate" hreflang="th" href="https://solaress.org/th/community">\n'
           '<link rel="alternate" hreflang="x-default" href="https://solaress.org/community">\n')
    page = page.replace('<link rel="canonical"', alt + '<link rel="canonical"', 1)
    en_cur = ' aria-current="true"' if lang == "en" else ""
    th_cur = ' aria-current="true"' if lang == "th" else ""
    page = re.sub(r'<span class="langsw">.*?</span></nav>',
                  f'<span class="langsw"><a href="/community.html" lang="en"{en_cur}>EN</a><a href="/th/community.html" lang="th" style="font-family:var(--thai)"{th_cur}>ไทย</a></span></nav>',
                  page, count=1, flags=re.S)
    page = re.sub(r'<style id="cm-css">.*?</style>', "", page, flags=re.S).replace("</head>", CSS + "</head>", 1)
    (ROOT / t["path"].lstrip("/")).write_text(page, encoding="utf-8")
    print("wrote", t["path"])


if __name__ == "__main__":
    build("en", "members.html")
    build("th", "th/members.html")
