# -*- coding: utf-8 -*-
"""Installer test pages: /installer-test.html (EN chrome) and /th/installer-test.html (TH chrome).
Five levels of 25 questions. Level 1 needs a TSIA or installer-partner registration (same phone);
each higher level needs the level below passed. Questions are shown in Thai and English and load from
/api/itest (answers never reach the page). A pass issues a certificate at /certificate.html?id=...
Run from the repo root:  python3 tools/itest/page.py   (then python3 tools/analytics_tag.py)"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

T = {
"en": dict(pre="", title="Solar Installer Test: 5 Levels with Certificates | Solar ESS",
    desc="Practical solar installation test in 5 levels, from Solar Enterer to Solar Expert. 25 questions per level in Thai and English, with a certificate for each level you pass.",
    eyebrow="Solar Test · แบบทดสอบโซลาร์", h1="Practical Solar Installation Test",
    lede="Five levels, 25 questions each, in Thai and English. Pass a level (70%) to get its certificate and unlock the next one. Level 1 is open to registered TSIA members and installer partners.",
    ladder="The five levels", s1="Your details", name="Full name", phone="Phone (the one you registered with)", email="Email", prov="Province (optional)",
    team="Company or team name", check="Show my levels",
    req="Please fill in name, phone, email and company or team name.", bademail="Please enter a valid email.",
    nreg_h="Register first", nreg="We could not find a TSIA or installer-partner registration with this phone number. Register first (it is free), then come back with the same phone number.",
    nreg_t="Join TSIA", nreg_p="Register as installer partner", reg_ok="Registered",
    st_pass="Passed", st_open="Open", st_lock="Locked", lock_need="Pass Level {n} first", start="Start Level {n}", retake="Retake", cert="View certificate",
    qof="Question", answered="answered", submit="Submit my answers", sending="Checking your answers…",
    unanswered="You have {n} unanswered questions. Submit anyway?", fail="Sending failed. Please try again.",
    r_h="Your result", r_pass="Passed", r_fail="Not passed yet", next="Go to Level {n}",
    r_cert="Your certificate number is {id}.", r_retry="You need 70% to pass. Study the topics and try again; every attempt is recorded.",
    back="Back to my levels", loading="Loading…", e_prereq="Please pass Level {n} first.", e_reg="Please register as TSIA member or installer partner first.",
    q_s="questions", lv="Level"),
"th": dict(pre="/th", title="แบบทดสอบช่างโซลาร์ 5 ระดับ พร้อมใบประกาศ | Solar ESS",
    desc="แบบทดสอบการติดตั้งโซลาร์ภาคปฏิบัติ 5 ระดับ ตั้งแต่ Solar Enterer ถึง Solar Expert ระดับละ 25 ข้อ ภาษาไทยและอังกฤษ ได้ใบประกาศทุกระดับที่สอบผ่าน",
    eyebrow="แบบทดสอบโซลาร์ · Solar Test", h1="แบบทดสอบการติดตั้งโซลาร์ภาคปฏิบัติ",
    lede="5 ระดับ ระดับละ 25 ข้อ ภาษาไทยและอังกฤษ สอบผ่าน 70% ได้ใบประกาศของระดับนั้นและปลดล็อกระดับถัดไป ระดับ 1 เปิดให้สมาชิก TSIA และทีมช่างพันธมิตรที่ลงทะเบียนแล้ว",
    ladder="5 ระดับ", s1="ข้อมูลของคุณ", name="ชื่อ-นามสกุล", phone="เบอร์โทร (เบอร์เดียวกับที่ลงทะเบียน)", email="อีเมล", prov="จังหวัด (ไม่บังคับ)",
    team="ชื่อบริษัทหรือทีม", check="ดูระดับของฉัน",
    req="กรุณากรอกชื่อ เบอร์โทร อีเมล และชื่อบริษัทหรือทีม", bademail="กรุณากรอกอีเมลให้ถูกต้อง",
    nreg_h="กรุณาลงทะเบียนก่อน", nreg="ไม่พบการลงทะเบียนสมาชิก TSIA หรือทีมช่างพันธมิตรด้วยเบอร์นี้ ลงทะเบียนก่อน (ฟรี) แล้วกลับมาด้วยเบอร์เดิม",
    nreg_t="สมัครสมาชิก TSIA", nreg_p="ลงทะเบียนทีมช่างพันธมิตร", reg_ok="ลงทะเบียนแล้ว",
    st_pass="ผ่านแล้ว", st_open="เปิดสอบ", st_lock="ล็อกอยู่", lock_need="ต้องผ่านระดับ {n} ก่อน", start="เริ่มระดับ {n}", retake="สอบอีกครั้ง", cert="ดูใบประกาศ",
    qof="ข้อ", answered="ตอบแล้ว", submit="ส่งคำตอบ", sending="กำลังตรวจคำตอบ…",
    unanswered="ยังไม่ได้ตอบ {n} ข้อ ต้องการส่งเลยหรือไม่", fail="ส่งไม่สำเร็จ กรุณาลองอีกครั้ง",
    r_h="ผลการทดสอบ", r_pass="ผ่าน", r_fail="ยังไม่ผ่าน", next="ไประดับ {n}",
    r_cert="เลขที่ใบประกาศของคุณ: {id}", r_retry="ต้องได้ 70% จึงจะผ่าน ทบทวนเนื้อหาแล้วสอบใหม่ได้ ทุกครั้งจะถูกบันทึกไว้",
    back="กลับไปหน้าระดับของฉัน", loading="กำลังโหลด…", e_prereq="กรุณาสอบผ่านระดับ {n} ก่อน", e_reg="กรุณาลงทะเบียนสมาชิก TSIA หรือทีมช่างพันธมิตรก่อน",
    q_s="ข้อ", lv="ระดับ"),
}

CSS = """<style id="itest-css">
.itw{max-width:860px}
.itw label{display:grid;gap:5px;font-size:14px;font-weight:600;color:var(--navy)}
.itw input:not([type=radio]){font:inherit;font-size:15px;font-weight:400;border:1.5px solid var(--line);border-radius:10px;padding:10px 12px;width:100%;box-sizing:border-box;background:#fff}
.itw .two{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.itbox{background:#fff;border:1.5px solid var(--line);border-radius:16px;padding:18px 20px;display:grid;gap:14px;margin-top:18px}
.itlad{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px;margin-top:12px}
.itlad div{background:#fff;border:1px solid var(--line);border-radius:12px;padding:10px;font-size:13px;line-height:1.35}
.itlad b{display:block;color:var(--navy);font-size:14px}.itlad span{font-family:var(--mono);font-size:11px;color:var(--mute)}
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
.itbar{position:sticky;bottom:0;z-index:5;background:rgba(250,252,255,.96);border-top:1px solid var(--line);padding:10px 0;margin-top:20px;display:flex;gap:12px;align-items:center;justify-content:space-between;flex-wrap:wrap}
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
    lad = "".join(f'<div><span>{esc(t["lv"])} {l["n"]}</span><b>{esc(l["en"])}</b>{esc(l["th"])}</div>' for l in bank["levels"])
    body = (
        f'<section class="dark band" style="padding-block:64px"><div class="wrap"><p class="eyebrow">{esc(t["eyebrow"])}</p>'
        f'<h1 style="font-size:clamp(34px,5.5vw,60px)">{esc(t["h1"])}</h1><p class="lede" style="margin-top:18px">{esc(t["lede"])}</p></div></section>\n'
        f'<section class="band light" style="padding-block:40px"><div class="wrap itw">'
        f'<h3>{esc(t["ladder"])}</h3><div class="itlad">{lad}</div>'
        f'<form id="it-who" class="itbox" novalidate><h3 style="margin:0">{esc(t["s1"])}</h3>'
        f'<div class="two"><label>{esc(t["name"])} *<input id="it-name" required autocomplete="name"></label><label>{esc(t["phone"])} *<input id="it-phone" type="tel" required autocomplete="tel"></label></div>'
        f'<div class="two"><label>{esc(t["email"])} *<input id="it-email" type="email" required autocomplete="email"></label><label>{esc(t["team"])} *<input id="it-team" required autocomplete="organization"></label></div>'
        f'<label>{esc(t["prov"])}<input id="it-prov"></label>'
        f'<div><button class="btn" type="submit" id="it-check">{esc(t["check"])}</button> <span id="it-req" class="fine" style="color:#B42318"></span></div></form>'
        f'<div id="it-nreg" class="itnreg" hidden><h3 style="margin:0 0 6px">{esc(t["nreg_h"])}</h3><p style="margin:0 0 12px">{esc(t["nreg"])}</p>'
        f'<a class="btn" href="{t["pre"]}/team.html#join-tsia">{esc(t["nreg_t"])}</a> <a class="btn" href="{t["pre"]}/partners.html#register">{esc(t["nreg_p"])}</a></div>'
        f'<div id="it-lv" class="itlv" hidden></div>'
        f'<div id="it-qs" hidden></div>'
        f'<div class="itbar" id="it-bar" hidden><span id="it-count"></span><button class="btn" id="it-send" type="button">{esc(t["submit"])}</button></div>'
        f'<div id="it-res" hidden></div>'
        f'</div></section>\n')
    keys = ["req", "bademail", "reg_ok", "st_pass", "st_open", "st_lock", "lock_need", "start", "retake", "cert", "qof", "answered", "submit",
            "sending", "unanswered", "fail", "r_h", "r_pass", "r_fail", "next", "r_cert", "r_retry", "back", "loading", "e_prereq", "e_reg", "q_s", "lv"]
    L = {k: t[k] for k in keys}
    L["lang"] = "Thai" if th else "English"
    L["th"] = th
    script = "<script>window.IT_T=" + json.dumps(L, ensure_ascii=False) + ";</script>\n" + r"""<script>
(function(){var T=window.IT_T,$=function(i){return document.getElementById(i)},Q=[],S=[],ans=[],t0=0,who={},st=null,cur=0;
var want=parseInt(new URLSearchParams(location.search).get('level'),10)||0;
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function f(s,o){return s.replace(/\{(\w+)\}/g,function(m,k){return o[k]})}
function go(el){window.scrollTo({top:el.getBoundingClientRect().top+window.scrollY-90,behavior:'smooth'})}
function post(a,b){return fetch('/api/itest?a='+a,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(b)}).then(function(r){return r.json().then(function(d){d._s=r.status;return d})})}
function lvName(l){return T.th?l.th+' · '+l.en:l.en+' · '+l.th}
try{var sv=JSON.parse(localStorage.getItem('itest-who')||'null');if(sv){['name','phone','email','team','prov'].forEach(function(k){if(sv[k])$('it-'+k).value=sv[k]})}}catch(x){}
function cards(){var h='';st.levels.forEach(function(l){var c=st.passed[l.n],open=!c&&(l.n===1||st.passed[l.n-1]),cls=c?'pass':open?'':'lock';
  h+='<div class="itcard '+cls+(want===l.n?' focus':'')+'" id="lv'+l.n+'"><div class="t"><span class="tag">'+esc(T.lv+' '+l.n)+'</span><b>'+esc(lvName(l))+'</b><small>25 '+esc(T.q_s)+' · '+(c?esc(T.st_pass):open?esc(T.st_open):esc(f(T.lock_need,{n:l.n-1})))+'</small></div><div class="act">'
  +(c?'<a class="btn ghost" href="/certificate.html?id='+encodeURIComponent(c)+'">'+esc(T.cert)+'</a><button class="btn ghost" data-go="'+l.n+'" type="button">'+esc(T.retake)+'</button>'
    :open?'<button class="btn" data-go="'+l.n+'" type="button">'+esc(f(T.start,{n:l.n}))+'</button>':'')+'</div></div>'});
 $('it-lv').innerHTML='<p class="fine" style="margin:0">✓ '+esc(T.reg_ok)+(st.regName?' · '+esc(st.regName):'')+'</p>'+h;$('it-lv').hidden=false;
 var tgt=$('lv'+(want||st.next||1));if(tgt)go(tgt)}
function status(){var b=$('it-check');b.disabled=true;
 return post('status',{phone:who.phone}).then(function(d){b.disabled=false;st=d;$('it-nreg').hidden=!!d.registered;
  if(!d.registered){$('it-lv').hidden=true;go($('it-nreg'));return}cards()}).catch(function(){b.disabled=false;$('it-req').textContent=T.fail})}
$('it-who').addEventListener('submit',function(e){e.preventDefault();
 who={name:$('it-name').value.trim(),phone:$('it-phone').value.trim(),email:$('it-email').value.trim(),province:$('it-prov').value.trim(),team:$('it-team').value.trim()};
 if(!who.name||!who.email||!who.team||who.phone.replace(/\D/g,'').length<9){$('it-req').textContent=T.req;return}
 if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(who.email)){$('it-req').textContent=T.bademail;return}
 $('it-req').textContent='';try{localStorage.setItem('itest-who',JSON.stringify({name:who.name,phone:who.phone,email:who.email,team:who.team,prov:who.province}))}catch(x){}
 status()});
function count(){var n=ans.filter(function(v){return v!==null}).length;$('it-count').textContent=n+' / '+Q.length+' '+T.answered}
function render(lvl){var h='<div class="itlvh">'+esc(T.lv+' '+lvl.n+' · '+lvName(lvl))+'</div>';Q.forEach(function(q){
 h+='<div class="itq" id="q'+q.i+'"><div class="n">'+esc(T.qof+' '+(q.i+1)+' / '+Q.length)+'</div><p class="th">'+esc(q.th)+'</p><p class="en">'+esc(q.en)+'</p>'
 +q.options.map(function(o,k){return '<label class="op"><input type="radio" name="q'+q.i+'" value="'+k+'"><span>'+esc(o.th)+(o.en!==o.th?'<small>'+esc(o.en)+'</small>':'')+'</span></label>'}).join('')+'</div>'});
 $('it-qs').innerHTML=h;$('it-qs').hidden=false;$('it-bar').hidden=false;document.body.classList.add('it-on');count()}
$('it-lv').addEventListener('click',function(e){var b=e.target.closest('[data-go]');if(!b)return;var n=+b.getAttribute('data-go');b.disabled=true;b.textContent=T.loading;
 post('start',{phone:who.phone,level:n}).then(function(d){b.disabled=false;
  if(d.error){alert(d.error==='prerequisite'?f(T.e_prereq,{n:d.need}):d.error==='not-registered'?T.e_reg:T.fail);cards();return}
  cur=n;Q=d.questions;S=d.sections;ans=Q.map(function(){return null});t0=Date.now();
  $('it-who').hidden=true;$('it-lv').hidden=true;$('it-res').hidden=true;render(d.level);go($('it-qs'));
  try{gtag('event','installer_test_start',{level:n})}catch(x){}}).catch(function(){b.disabled=false;alert(T.fail)})});
$('it-qs').addEventListener('change',function(e){var m=/^q(\d+)$/.exec(e.target.name);if(!m)return;ans[+m[1]]=+e.target.value;$('q'+m[1]).classList.add('done');count()});
$('it-send').addEventListener('click',function(){var miss=ans.filter(function(v){return v===null}).length;if(miss&&!confirm(f(T.unanswered,{n:miss})))return;
 var b=$('it-send');b.disabled=true;b.textContent=T.sending;
 post('submit',Object.assign({},who,{level:cur,language:T.lang,seconds:Math.round((Date.now()-t0)/1000),answers:ans})).then(function(r){
  b.disabled=false;b.textContent=T.submit;if(r.error){alert(r.error);return}
  try{gtag('event','installer_test_sent',{level:cur,score:r.pct,pass:r.pass})}catch(x){}
  var rows=S.map(function(s){var x=r.sections[s.id];if(!x)return '';return '<tr><td>'+esc(s.id+'. '+s.th+' / '+s.en)+'</td><td style="text-align:right;white-space:nowrap"><b>'+x.correct+' / '+x.total+'</b></td></tr>'}).join('');
  if(r.pass)st.passed[cur]=r.cert;
  var acts='';if(r.pass){acts+='<a class="btn" href="/certificate.html?id='+encodeURIComponent(r.cert)+'">'+esc(T.cert)+'</a> ';if(cur<5)acts+='<button class="btn ghost" type="button" data-next="'+(cur+1)+'">'+esc(f(T.next,{n:cur+1}))+'</button> '}
  acts+='<button class="btn ghost" type="button" data-next="0">'+esc(T.back)+'</button>';
  $('it-qs').hidden=true;$('it-bar').hidden=true;document.body.classList.remove('it-on');$('it-res').hidden=false;
  $('it-res').innerHTML='<div class="itres"><h3 style="margin:0">'+esc(T.r_h+' · '+T.lv+' '+cur+' '+lvName(r.level))+'</h3><div class="big">'+r.score+' / '+r.total+' <span class="'+(r.pass?'ok':'no')+'" style="font-size:24px">('+r.pct+'% · '+esc(r.pass?T.r_pass:T.r_fail)+')</span></div><table>'+rows+'</table><p style="margin-top:12px">'+esc(r.pass?f(T.r_cert,{id:r.cert}):T.r_retry)+'</p><div class="act" style="display:flex;gap:8px;flex-wrap:wrap;margin-top:12px">'+acts+'</div></div>';
  go($('it-res'))}).catch(function(){b.disabled=false;b.textContent=T.submit;alert(T.fail)})});
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
