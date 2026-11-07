# -*- coding: utf-8 -*-
"""One-click registration for the Solar Test certificate: /join.html (EN) and /th/join.html (TH).
A candidate who scored 100% arrives from the test result or the certificate link (?cert=SESS-L1-XXXX&phone=..&name=..),
fills in 4 fields (type, name, phone, province), and the page registers them as a TSIA Installer Partner
through /api/itest?a=register, then opens /certificate.html?id=... straight away.
Kris still reviews every registration at /members-admin.html before a profile is published.
Run from the repo root:  python3 tools/itest/join_page.py   (then python3 tools/analytics_tag.py)"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(Path(__file__).parent))
from partners_page import PROVINCES, REGIONS  # noqa: E402
from page import CSS  # noqa: E402

T = {
"en": dict(pre="", title="Register and get your Solar Test certificate | Solar ESS",
    desc="Register free in one minute as a TSIA Installer Partner and download your Solar ESS Solar Test certificate.",
    eyebrow="Solar Test · Certificate", h1="Get your certificate",
    lede="Register free in one minute. As soon as you send this form, your certificate opens. Use the same phone number you used for the test.",
    type="I am", types=[("Individual installer", "An individual installer"), ("Installation team (not registered)", "An installation team"), ("Registered company / partnership", "A registered company")],
    name="Your name, or your team or company name", phone="Phone (the one you used for the test)", prov="Province", choose="Choose your province",
    cert="Certificate number", agree="I join TSIA as an Installer Partner (free) and agree to the TSIA Statement of Purpose. Solar ESS may check my details and, after approval, show my team name and province on solaress.org. My phone is never published.",
    btn="Register and open my certificate", sending="Registering…", req="Please fill in all fields and tick the box.",
    e_cert="We could not find this certificate with this phone number. Use the phone you used for the test, or check the certificate number.",
    e_fail="Sending failed. Please try again.", nocert_h="No certificate yet?", nocert="A certificate is given for 100% (25/25) on any level. Take the test first, then come back here.", test="Take the Solar Test",
    done="Done! Opening your certificate…"),
"th": dict(pre="/th", title="ลงทะเบียนและรับใบประกาศแบบทดสอบโซลาร์ | Solar ESS",
    desc="ลงทะเบียนฟรีใน 1 นาที เป็นช่างพันธมิตร TSIA และดาวน์โหลดใบประกาศแบบทดสอบโซลาร์ของ Solar ESS",
    eyebrow="แบบทดสอบโซลาร์ · ใบประกาศ", h1="รับใบประกาศของคุณ",
    lede="ลงทะเบียนฟรีใน 1 นาที เมื่อกดส่งแบบฟอร์มนี้ ใบประกาศจะเปิดทันที กรุณาใช้เบอร์โทรเดียวกับที่ใช้ทำแบบทดสอบ",
    type="ฉันเป็น", types=[("Individual installer", "ช่างอิสระ"), ("Installation team (not registered)", "ทีมช่าง"), ("Registered company / partnership", "บริษัทหรือห้างหุ้นส่วน")],
    name="ชื่อของคุณ หรือชื่อทีม/บริษัท", phone="เบอร์โทร (เบอร์ที่ใช้ทำแบบทดสอบ)", prov="จังหวัด", choose="เลือกจังหวัด",
    cert="เลขที่ใบประกาศ", agree="ข้าพเจ้าสมัครเป็นช่างพันธมิตร TSIA (ฟรี) และยอมรับแถลงการณ์วัตถุประสงค์ของ TSIA ยินยอมให้ Solar ESS ตรวจสอบข้อมูล และแสดงชื่อทีมกับจังหวัดบน solaress.org หลังอนุมัติ ไม่เผยแพร่เบอร์โทร",
    btn="ลงทะเบียนและเปิดใบประกาศ", sending="กำลังลงทะเบียน…", req="กรุณากรอกให้ครบทุกช่องและติ๊กยอมรับ",
    e_cert="ไม่พบใบประกาศนี้กับเบอร์โทรนี้ กรุณาใช้เบอร์ที่ใช้ทำแบบทดสอบ หรือตรวจเลขที่ใบประกาศ",
    e_fail="ส่งไม่สำเร็จ กรุณาลองอีกครั้ง", nocert_h="ยังไม่มีใบประกาศ?", nocert="ใบประกาศให้สำหรับผู้ที่ได้ 100% (25/25) ในระดับใดก็ได้ ทำแบบทดสอบก่อน แล้วกลับมาที่หน้านี้", test="ทำแบบทดสอบโซลาร์",
    done="เรียบร้อย! กำลังเปิดใบประกาศ…"),
}


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build(lang):
    t, th = T[lang], lang == "th"
    src = (ROOT / ("th/installer-test.html" if th else "installer-test.html")).read_text(encoding="utf-8")
    head = src[:src.index('<section class="dark band"')]
    foot = src[src.index("<footer>"):]
    foot = re.sub(r"<script>window\.IT_T=.*?</script>\s*<script>.*?</script>\s*", "", foot, flags=re.S)
    head = re.sub(r"<title>.*?</title>", f"<title>{esc(t['title'])}</title>", head, count=1)
    head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + esc(t["desc"]), head, count=1)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + esc(t["title"]), head, count=1)
    head = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + f"https://solaress.org{t['pre']}/join.html", head, count=1)
    head = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="https://solaress.org{t["pre"]}/join.html">', head, count=1)
    head = re.sub(r'<span class="langsw">.*?</span>(?=</nav>)',
                  '<span class="langsw"><a href="/join.html" lang="en"' + ('' if th else ' aria-current="true"') + '>EN</a>'
                  '<a href="/th/join.html" lang="th" style="font-family:var(--thai)"' + (' aria-current="true"' if th else '') + '>ไทย</a></span>',
                  head, count=1, flags=re.S)
    if 'id="itest-css"' not in head:
        head = head.replace("</head>", CSS + "\n</head>", 1)
    rnames = {k: (tn if th else en) for k, en, tn in REGIONS}
    prov = f'<option value="">{esc(t["choose"])}</option>' + "".join(
        f'<optgroup label="{esc(rnames[k])}">' + "".join(f'<option value="{esc(pe)}" data-region="{k}">{esc(pt if th else pe)}</option>' for pe, pt in PROVINCES[k]) + "</optgroup>"
        for k, _, _ in REGIONS)
    types = "".join(f'<label class="op" style="display:flex;gap:8px;align-items:center;font-weight:500"><input type="radio" name="ptype" value="{esc(v)}"{" checked" if i == 0 else ""}><span>{esc(lbl)}</span></label>' for i, (v, lbl) in enumerate(t["types"]))
    body = (
        f'<section class="dark band" style="padding-block:56px"><div class="wrap"><p class="eyebrow">{esc(t["eyebrow"])}</p>'
        f'<h1 style="font-size:clamp(34px,5.5vw,56px)">{esc(t["h1"])}</h1><p class="lede" style="margin-top:16px">{esc(t["lede"])}</p></div></section>\n'
        f'<section class="band light" style="padding-block:40px"><div class="wrap itw">'
        f'<form id="jn" class="itbox" novalidate style="margin-top:0">'
        f'<div><p style="margin:0 0 6px;font-weight:600;color:var(--navy)">{esc(t["type"])}</p><div style="display:flex;gap:16px;flex-wrap:wrap">{types}</div></div>'
        f'<label>{esc(t["name"])} *<input id="jn-name" required maxlength="80" autocomplete="name"></label>'
        f'<div class="two"><label>{esc(t["phone"])} *<input id="jn-phone" type="tel" required autocomplete="tel"></label>'
        f'<label>{esc(t["prov"])} *<select id="jn-prov" required style="font:inherit;font-size:15px;border:1.5px solid var(--line);border-radius:10px;padding:10px 12px;background:#fff">{prov}</select></label></div>'
        f'<label>{esc(t["cert"])} *<input id="jn-cert" required placeholder="SESS-L1-XXXXXXXX" style="text-transform:uppercase"></label>'
        f'<label style="display:flex;gap:10px;align-items:flex-start;font-weight:400"><input type="checkbox" id="jn-agree" style="width:auto;margin-top:4px"><span>{esc(t["agree"])}</span></label>'
        f'<div><button class="btn" type="submit" id="jn-btn">{esc(t["btn"])}</button> <span id="jn-msg" class="fine" style="color:#B42318"></span></div>'
        f'</form>'
        f'<div class="itbox"><h3 style="margin:0">{esc(t["nocert_h"])}</h3><p style="margin:0">{esc(t["nocert"])}</p><p style="margin:0"><a class="btn ghost" href="{t["pre"]}/installer-test.html">{esc(t["test"])}</a></p></div>'
        f'</div></section>\n')
    L = {k: t[k] for k in ["req", "sending", "btn", "e_cert", "e_fail", "done"]}
    L["lang"] = "Thai" if th else "English"
    script = "<script>window.JN_T=" + json.dumps(L, ensure_ascii=False) + ";</script>\n" + r"""<script>
(function(){var T=window.JN_T,$=function(i){return document.getElementById(i)},q=new URLSearchParams(location.search);
var who={};try{who=JSON.parse(localStorage.getItem('itest-who')||'{}')||{}}catch(x){}
$('jn-cert').value=(q.get('cert')||'').toUpperCase();$('jn-phone').value=q.get('phone')||who.phone||'';$('jn-name').value=q.get('name')||who.team||who.name||'';
$('jn').addEventListener('submit',function(e){e.preventDefault();
 var p=$('jn-prov'),o=p.options[p.selectedIndex],ty=document.querySelector('input[name=ptype]:checked');
 var d={cert:$('jn-cert').value.trim().toUpperCase(),phone:$('jn-phone').value.trim(),name:$('jn-name').value.trim(),province:p.value,region:o?(o.getAttribute('data-region')||''):'',type:ty?ty.value:'',agree:$('jn-agree').checked,language:T.lang};
 if(!d.cert||!d.name||!d.province||d.phone.replace(/\D/g,'').length<9||!d.agree){$('jn-msg').textContent=T.req;return}
 var b=$('jn-btn');b.disabled=true;b.textContent=T.sending;$('jn-msg').textContent='';
 fetch('/api/itest?a=register',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(d)}).then(function(r){return r.json()}).then(function(r){
  if(r.ok){$('jn-msg').style.color='#15803D';$('jn-msg').textContent=T.done;try{gtag('event','form_sent',{form_name:'solar-test-register'})}catch(x){}location.href='/certificate.html?id='+encodeURIComponent(d.cert);return}
  b.disabled=false;b.textContent=T.btn;$('jn-msg').textContent=r.error==='cert'?T.e_cert:(r.error||T.e_fail)}).catch(function(){b.disabled=false;b.textContent=T.btn;$('jn-msg').textContent=T.e_fail})});
})();
</script>
"""
    out = ROOT / ("th/join.html" if th else "join.html")
    out.write_text(head + body + script + foot, encoding="utf-8")
    print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    build("en")
    build("th")
