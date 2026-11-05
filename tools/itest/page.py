# -*- coding: utf-8 -*-
"""Installer test pages: /installer-test.html (EN chrome) and /th/installer-test.html (TH chrome).
Every question is shown in Thai and English. Questions load from /api/itest (answers never reach the page).
Run from the repo root:  python3 tools/itest/page.py   (then python3 tools/analytics_tag.py)"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

T = {
"en": dict(pre="", title="Practical Solar Installation Test for Installers | Solar ESS",
    desc="100-question practical test for solar installers in Thai and English: electrical design, wiring, mounting and customer care. Free; Solar ESS reviews your score.",
    eyebrow="Installer test · แบบทดสอบช่างติดตั้ง", h1="Practical Solar Installation Test",
    lede="100 multiple-choice questions in Thai and English, from real installation work. Take your time: about 60–90 minutes. Pass mark 70%. Solar ESS uses your score when choosing installer partners, TSIA members and job candidates.",
    secs="What it covers", s1="Your details", name="Full name", phone="Phone", email="Email (optional)", prov="Province", team="Team or company (optional)",
    start="Start the test", qof="question", answered="answered", submit="Submit my answers", sending="Checking your answers…",
    unanswered="You have {n} unanswered questions. Submit anyway?", fail="Sending failed. Please try again.",
    r_h="Your result", r_pass="Passed", r_fail="Not passed yet", r_note="Solar ESS has received your result and will contact you. You may retake the test later; every attempt is recorded.",
    req="Please enter your name and phone first."),
"th": dict(pre="/th", title="แบบทดสอบการติดตั้งโซลาร์ภาคปฏิบัติ สำหรับช่าง | Solar ESS",
    desc="แบบทดสอบ 100 ข้อ ภาษาไทยและอังกฤษ สำหรับช่างติดตั้งโซลาร์: ระบบไฟฟ้า การเดินสาย โครงสร้าง และการดูแลลูกค้า ฟรี Solar ESS พิจารณาคะแนนของคุณ",
    eyebrow="แบบทดสอบช่างติดตั้ง · Installer test", h1="แบบทดสอบการติดตั้งโซลาร์ภาคปฏิบัติ",
    lede="ข้อสอบปรนัย 100 ข้อ ภาษาไทยและอังกฤษ จากงานติดตั้งจริง ใช้เวลาประมาณ 60–90 นาที เกณฑ์ผ่าน 70% Solar ESS ใช้คะแนนนี้ประกอบการคัดเลือกทีมช่างพันธมิตร สมาชิก TSIA และผู้สมัครงาน",
    secs="เนื้อหาที่ทดสอบ", s1="ข้อมูลของคุณ", name="ชื่อ-นามสกุล", phone="เบอร์โทร", email="อีเมล (ไม่บังคับ)", prov="จังหวัด", team="ทีมหรือบริษัท (ไม่บังคับ)",
    start="เริ่มทำแบบทดสอบ", qof="ข้อ", answered="ตอบแล้ว", submit="ส่งคำตอบ", sending="กำลังตรวจคำตอบ…",
    unanswered="ยังไม่ได้ตอบ {n} ข้อ ต้องการส่งเลยหรือไม่", fail="ส่งไม่สำเร็จ กรุณาลองอีกครั้ง",
    r_h="ผลการทดสอบ", r_pass="ผ่าน", r_fail="ยังไม่ผ่าน", r_note="Solar ESS ได้รับผลการทดสอบของคุณแล้ว และจะติดต่อกลับ คุณทำแบบทดสอบซ้ำได้ภายหลัง ทุกครั้งจะถูกบันทึกไว้",
    req="กรุณากรอกชื่อและเบอร์โทรก่อน"),
}

CSS = """<style id="itest-css">
.itw{max-width:860px}
.itw label{display:grid;gap:5px;font-size:14px;font-weight:600;color:var(--navy)}
.itw input:not([type=radio]){font:inherit;font-size:15px;font-weight:400;border:1.5px solid var(--line);border-radius:10px;padding:10px 12px;width:100%;box-sizing:border-box;background:#fff}
.itw .two{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.itbox{background:#fff;border:1.5px solid var(--line);border-radius:16px;padding:18px 20px;display:grid;gap:14px;margin-top:18px}
.itsecs{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-top:12px}.itsecs div{background:#fff;border:1px solid var(--line);border-radius:12px;padding:10px 12px;font-size:14px}.itsecs b{color:var(--navy)}
.itsec{margin-top:30px;padding:10px 14px;background:var(--navy);color:#fff;border-radius:10px;font-weight:700}
.itq{background:#fff;border:1.5px solid var(--line);border-radius:14px;padding:14px 16px;margin-top:12px}
.itq.done{border-color:#93C5FD}
.itq .n{font-family:var(--mono);font-size:12px;color:var(--mute)}
.itq .th{font-weight:700;margin:4px 0 2px;font-family:var(--thai)}.itq .en{color:var(--mute);font-size:14px;margin:0 0 10px}
.itq .op{display:flex;gap:10px;align-items:flex-start;padding:8px 10px;border:1px solid var(--line);border-radius:10px;margin-top:6px;cursor:pointer;font-weight:400}
.itq .op:hover{background:var(--paper)}.itq .op input{margin-top:4px;flex:none;accent-color:var(--blue)}
.itq .op span{display:grid;gap:1px}.itq .op small{color:var(--mute);font-size:13px}
.itbar{position:sticky;bottom:0;z-index:5;background:rgba(250,252,255,.96);border-top:1px solid var(--line);padding:10px 0;margin-top:20px;display:flex;gap:12px;align-items:center;justify-content:space-between;flex-wrap:wrap}
body.it-on .fab{display:none!important}
.itres{background:#fff;border:2px solid var(--line);border-radius:16px;padding:20px;margin-top:18px}
.itres .big{font-size:44px;font-weight:800;color:var(--navy)}
.itres .ok{color:#15803D}.itres .no{color:#B42318}
.itres table{width:100%;border-collapse:collapse;margin-top:10px;font-size:14px}.itres td{padding:7px 8px;border-bottom:1px solid var(--line)}
@media (max-width:640px){.itw .two,.itsecs{grid-template-columns:1fr}}
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
    secs = "".join(f'<div><b>{s["id"]}. {esc(s["th"] if th else s["en"])}</b><br><small>{esc(s["en"] if th else s["th"])} · {s["count"]} {"ข้อ" if th else "questions"}</small></div>' for s in bank["sections"])
    body = (
        f'<section class="dark band" style="padding-block:64px"><div class="wrap"><p class="eyebrow">{esc(t["eyebrow"])}</p>'
        f'<h1 style="font-size:clamp(34px,5.5vw,60px)">{esc(t["h1"])}</h1><p class="lede" style="margin-top:18px">{esc(t["lede"])}</p></div></section>\n'
        f'<section class="band light" style="padding-block:40px"><div class="wrap itw">'
        f'<h3>{esc(t["secs"])}</h3><div class="itsecs">{secs}</div>'
        f'<form id="it-who" class="itbox"><h3 style="margin:0">{esc(t["s1"])}</h3>'
        f'<div class="two"><label>{esc(t["name"])}<input id="it-name" required autocomplete="name"></label><label>{esc(t["phone"])}<input id="it-phone" type="tel" required autocomplete="tel"></label></div>'
        f'<div class="two"><label>{esc(t["prov"])}<input id="it-prov"></label><label>{esc(t["team"])}<input id="it-team"></label></div>'
        f'<label>{esc(t["email"])}<input id="it-email" type="email" autocomplete="email"></label>'
        f'<div><button class="btn" type="submit">{esc(t["start"])}</button> <span id="it-req" class="fine" style="color:#B42318"></span></div></form>'
        f'<div id="it-qs" hidden></div>'
        f'<div class="itbar" id="it-bar" hidden><span id="it-count"></span><button class="btn" id="it-send" type="button">{esc(t["submit"])}</button></div>'
        f'<div id="it-res" hidden></div>'
        f'</div></section>\n')
    L = {k: t[k] for k in ["qof", "answered", "submit", "sending", "unanswered", "fail", "r_h", "r_pass", "r_fail", "r_note", "req"]}
    L["lang"] = "Thai" if th else "English"
    script = "<script>window.IT_T=" + json.dumps(L, ensure_ascii=False) + ";</script>\n" + r"""<script>
(function(){var T=window.IT_T,$=function(i){return document.getElementById(i)},Q=[],S=[],ans=[],t0=0,who={};
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function count(){var n=ans.filter(function(v){return v!==null}).length;$('it-count').textContent=n+' / '+Q.length+' '+T.answered}
function render(){var h='',cur='';Q.forEach(function(q){if(q.sec!==cur){cur=q.sec;var s=S.filter(function(x){return x.id===cur})[0]||{};h+='<div class="itsec">'+esc(cur+'. '+(s.th||'')+' · '+(s.en||''))+'</div>'}
 h+='<div class="itq" id="q'+q.i+'"><div class="n">'+(T.lang==='Thai'?T.qof+' '+(q.i+1):T.qof.charAt(0).toUpperCase()+T.qof.slice(1)+' '+(q.i+1))+' / '+Q.length+'</div><p class="th">'+esc(q.th)+'</p><p class="en">'+esc(q.en)+'</p>'
 +q.options.map(function(o,k){return '<label class="op"><input type="radio" name="q'+q.i+'" value="'+k+'"><span>'+esc(o.th)+(o.en!==o.th?'<small>'+esc(o.en)+'</small>':'')+'</span></label>'}).join('')+'</div>'});
 $('it-qs').innerHTML=h;$('it-qs').hidden=false;$('it-bar').hidden=false;document.body.classList.add('it-on');count()}
$('it-qs').addEventListener('change',function(e){var m=/^q(\d+)$/.exec(e.target.name);if(!m)return;ans[+m[1]]=+e.target.value;$('q'+m[1]).classList.add('done');count()});
$('it-who').addEventListener('submit',function(e){e.preventDefault();who={name:$('it-name').value.trim(),phone:$('it-phone').value.trim(),email:$('it-email').value.trim(),province:$('it-prov').value.trim(),team:$('it-team').value.trim()};
 if(!who.name||who.phone.replace(/\D/g,'').length<9){$('it-req').textContent=T.req;return}$('it-req').textContent='';
 fetch('/api/itest?a=questions').then(function(r){return r.json()}).then(function(d){Q=d.questions;S=d.sections;ans=Q.map(function(){return null});t0=Date.now();
  $('it-who').hidden=true;render();window.scrollTo({top:$('it-qs').getBoundingClientRect().top+window.scrollY-90,behavior:'smooth'})})});
$('it-send').addEventListener('click',function(){var miss=ans.filter(function(v){return v===null}).length;if(miss&&!confirm(T.unanswered.replace('{n}',miss)))return;
 var b=$('it-send');b.disabled=true;b.textContent=T.sending;
 fetch('/api/itest?a=submit',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(Object.assign({},who,{language:T.lang,seconds:Math.round((Date.now()-t0)/1000),answers:ans}))})
 .then(function(r){return r.ok?r.json():Promise.reject()}).then(function(r){
  try{gtag('event','installer_test_sent',{score:r.pct,pass:r.pass})}catch(x){}
  var rows=S.map(function(s){var x=r.sections[s.id]||{correct:0,total:0};return '<tr><td>'+esc(s.id+'. '+s.th+' / '+s.en)+'</td><td style="text-align:right;white-space:nowrap"><b>'+x.correct+' / '+x.total+'</b></td></tr>'}).join('');
  $('it-qs').hidden=true;$('it-bar').hidden=true;document.body.classList.remove('it-on');$('it-res').hidden=false;
  $('it-res').innerHTML='<div class="itres"><h3 style="margin:0">'+esc(T.r_h)+'</h3><div class="big">'+r.score+' / '+r.total+' <span class="'+(r.pass?'ok':'no')+'" style="font-size:24px">('+r.pct+'% · '+esc(r.pass?T.r_pass:T.r_fail)+')</span></div><table>'+rows+'</table><p class="fine" style="margin-top:12px">'+esc(T.r_note)+'</p></div>';
  window.scrollTo({top:$('it-res').getBoundingClientRect().top+window.scrollY-90,behavior:'smooth'})})
 .catch(function(){b.disabled=false;b.textContent=T.submit;alert(T.fail)})});
})();
</script>
"""
    out = ROOT / ("th/installer-test.html" if th else "installer-test.html")
    out.write_text(head + body + script + foot, encoding="utf-8")
    print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    build("en")
    build("th")
