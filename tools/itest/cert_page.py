# -*- coding: utf-8 -*-
"""/certificate.html?id=SESS-L1-XXXXXXXX : formal, printable A4-landscape certificate for a passed installer-test level.
Issued only for 100% (25/25); valid for 1 year (validFrom/validUntil from the API, EXPIRED stamp after).
 Level 3+ carries 'Accepted for Solar ESS installation work'.
Each level has its own metal tier (Bronze, Silver, Gold, Platinum, Diamond) for the seal, frame and ribbon.
Security look: guilloche frame and rosettes, microtext border, logo watermark, QR code to the verify link.
Data comes from GET /api/itest?a=cert&id=... (name, level, score, date; never the phone). Anyone can open the link to verify.
No personal signature: issued by Solar ESS Co. Ltd. / Solar ESS Working Group.
QR library: qrcode-generator 1.4.4 (MIT, Kazuhiko Arase), vendored in tools/itest/vendor and inlined.
Run from the repo root:  python3 tools/itest/cert_page.py   (then python3 tools/analytics_tag.py)"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
idx = (ROOT / "index.html").read_text(encoding="utf-8")
LOGO = re.search(r'<header class="nav">.*?<img src="(data:image/[^"]+)"', idx, re.S).group(1)
QR = (Path(__file__).parent / "vendor/qrcode.min.js").read_text(encoding="utf-8")

HTML = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Solar Installer Certificate | Solar ESS</title>
<meta name="description" content="Verify a Solar ESS practical solar installation certificate.">
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;800&family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Noto+Serif+Thai:wght@400;600;700&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root{--navy:#0A1230;--ink:#101A44;--mute:#4B5470;--m1:#C9A227;--m2:#F3E2A0;--m3:#8A6A12}
*{box-sizing:border-box}body{margin:0;background:#E9ECF4;font-family:Inter,'Noto Serif Thai',sans-serif;color:var(--ink)}
.bar{max-width:1123px;margin:18px auto 0;padding:0 16px;display:flex;gap:10px;justify-content:space-between;align-items:center;flex-wrap:wrap;font-size:14px}
.bar a,.bar button{font:inherit;font-weight:600;border:1.5px solid var(--navy);color:var(--navy);background:#fff;border-radius:99px;padding:8px 16px;cursor:pointer;text-decoration:none}
.bar button{background:var(--navy);color:#fff}
.ok{display:inline-flex;align-items:center;gap:8px;color:#166534;font-weight:600}
.wrapc{padding:16px;overflow:hidden}
.cert{width:1123px;height:794px;margin:0 auto;position:relative;background:var(--navy);box-shadow:0 18px 50px rgba(10,18,48,.28);overflow:hidden;font-family:'Cormorant Garamond','Noto Serif Thai',serif}
.cert svg.frame{position:absolute;inset:0}
.paper{position:absolute;inset:34px;background:radial-gradient(ellipse at 50% 45%,#FFFFFF 0%,#FBF8EF 62%,#F2ECDB 100%)}
.paper svg.bg{position:absolute;inset:0}
.wm{position:absolute;left:50%;top:50%;width:330px;transform:translate(-50%,-52%);opacity:.06;filter:grayscale(1)}
.in{position:absolute;inset:0;padding:30px 54px}
.top{display:flex;justify-content:space-between;align-items:flex-start}
.top img{height:70px;border-radius:8px}
.addr{text-align:right;font-family:Inter,sans-serif;font-size:11.5px;line-height:1.55;color:var(--mute)}.addr b{color:var(--ink);font-size:12.5px}
.mid{text-align:center;position:absolute;left:0;right:0;top:92px}
.k{font-family:Cinzel,serif;letter-spacing:.42em;font-size:13px;font-weight:700;color:var(--m3)}
h1{font-family:Cinzel,serif;font-size:50px;line-height:1.05;margin:8px 0 0;color:var(--ink);font-weight:800;letter-spacing:.06em}
.h1t{font-family:'Noto Serif Thai',serif;font-size:16px;color:var(--mute);margin-top:4px}
.rule{width:420px;height:12px;margin:12px auto 0;display:block}
.cer{font-style:italic;font-size:20px;color:var(--mute);margin-top:12px}.cer span{font-style:normal;font-family:'Noto Serif Thai',serif;font-size:14px}
.nm{font-family:'Cormorant Garamond','Noto Serif Thai',serif;font-weight:600;font-size:56px;line-height:1.1;color:var(--navy);margin:4px auto 0;padding:0 30px 4px;display:inline-block;min-width:560px;border-bottom:1.5px solid var(--m1)}
.has{font-size:19px;color:var(--mute);margin-top:10px;font-style:italic}.has span{font-style:normal;font-family:'Noto Serif Thai',serif;font-size:14px}
.ttl{font-family:Cinzel,serif;font-weight:800;font-size:34px;letter-spacing:.08em;color:var(--ink);margin-top:6px}
.ttlt{font-family:'Noto Serif Thai',serif;font-size:18px;font-weight:600;color:var(--ink)}
.tier{display:inline-block;margin-top:8px;font-family:Cinzel,serif;font-size:12px;letter-spacing:.32em;font-weight:700;color:var(--navy);padding:5px 16px;border-radius:99px;background:linear-gradient(90deg,var(--m3),var(--m2),var(--m1),var(--m2),var(--m3))}
.work{margin-top:8px;font-family:Cinzel,serif;font-weight:700;font-size:12.5px;letter-spacing:.12em;color:#166534}.work span{font-family:'Noto Serif Thai',serif;letter-spacing:0;font-size:13px}
.seal{position:absolute;left:52px;bottom:40px;width:190px;height:232px}
.qr{position:absolute;right:40px;bottom:44px;text-align:center;font-family:Inter,sans-serif;font-size:9.5px;color:var(--mute);width:190px}
.qr .box{background:#fff;border:1.5px solid var(--m1);padding:6px;display:inline-block;border-radius:6px}.qr svg{display:block;width:104px;height:104px}
.qr b{display:block;color:var(--ink);font-size:10.5px;margin-top:4px;white-space:nowrap}
.meta{position:absolute;left:258px;right:228px;bottom:84px;display:grid;grid-template-columns:.9fr 1.6fr 1.2fr;gap:10px;text-align:center;font-family:Inter,sans-serif;font-size:10.5px;color:var(--mute);letter-spacing:.04em}
.meta b{display:block;font-family:'Cormorant Garamond',serif;font-size:21px;color:var(--ink);letter-spacing:0;margin-top:2px;white-space:nowrap}.meta i{font-style:normal;font-family:'Noto Serif Thai',serif;font-size:11px}
.iss{position:absolute;left:270px;right:240px;bottom:28px;text-align:center;font-family:Inter,sans-serif;font-size:11px;color:var(--mute)}
.iss .ln{width:300px;margin:0 auto 6px;border-top:1px solid var(--m3)}.iss b{color:var(--ink);font-size:12.5px;letter-spacing:.02em}
.exp{position:absolute;left:50%;top:46%;transform:translate(-50%,-50%) rotate(-18deg);font-family:Cinzel,serif;font-weight:800;font-size:76px;letter-spacing:.08em;color:rgba(180,35,24,.55);border:6px solid rgba(180,35,24,.55);border-radius:14px;padding:6px 30px;white-space:nowrap;pointer-events:none}
.msg{max-width:640px;margin:60px auto;background:#fff;border-radius:16px;padding:28px;text-align:center}
@page{size:A4 landscape;margin:0}
@media print{body{background:#fff}.bar{display:none}.wrapc{padding:0}.cert{box-shadow:none;zoom:1!important;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
</style></head><body>
<div class="bar"><a href="/installer-test.html">← Solar Test · แบบทดสอบโซลาร์</a><span class="ok" id="okv" hidden>✓ Verified by Solar ESS · ตรวจสอบแล้ว</span><button type="button" onclick="print()">Print / Save PDF · พิมพ์</button></div>
<div class="wrapc"><div id="c"><div class="msg">Loading… · กำลังโหลด…</div></div></div>
<script>__QR__</script>
<script>
(function(){var id=new URLSearchParams(location.search).get('id')||'',LOGO='__LOGO__';
var TIERS={1:['BRONZE','#B9773A','#F2C9A0','#6E3F16'],2:['SILVER','#9AA3B2','#F1F4F8','#4E5666'],3:['GOLD','#C9A227','#F6E7A8','#7E5F0E'],
 4:['PLATINUM','#8E9BB8','#EEF2FB','#3D4A6B'],5:['DIAMOND','#6D5BD0','#E3DEFF','#2E2580']};
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function bad(){document.getElementById('c').innerHTML='<div class="msg"><h2>Certificate not found</h2><p>ไม่พบใบประกาศเลขที่นี้</p><p>'+esc(id)+'</p></div>'}
// guilloche: spirograph-style closed curve
function rose(cx,cy,R,r,d,turns,steps){var p='';for(var i=0;i<=steps;i++){var t=i/steps*Math.PI*2*turns,x=cx+(R-r)*Math.cos(t)+d*Math.cos((R-r)/r*t),y=cy+(R-r)*Math.sin(t)-d*Math.sin((R-r)/r*t);p+=(i?'L':'M')+x.toFixed(1)+' '+y.toFixed(1)}return p}
// wavy line running round a rectangle (frame engraving)
function band(x0,y0,w,h,amp,per,ph){var pts=[],L=2*(w+h),n=Math.round(L/3);for(var i=0;i<=n;i++){var s=i/n*L,x,y,nx,ny;
 if(s<w){x=x0+s;y=y0;nx=0;ny=-1}else if(s<w+h){x=x0+w;y=y0+s-w;nx=1;ny=0}else if(s<2*w+h){x=x0+w-(s-w-h);y=y0+h;nx=0;ny=1}else{x=x0;y=y0+h-(s-2*w-h);nx=-1;ny=0}
 var o=amp*Math.sin(s/per*Math.PI*2+ph);pts.push((i?'L':'M')+(x+nx*o).toFixed(1)+' '+(y+ny*o).toFixed(1))}return pts.join('')+'Z'}
function frame(T){var W=1123,H=794,g='';
 g+='<defs><linearGradient id="mg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="'+T[3]+'"/><stop offset=".35" stop-color="'+T[2]+'"/><stop offset=".55" stop-color="'+T[1]+'"/><stop offset=".8" stop-color="'+T[2]+'"/><stop offset="1" stop-color="'+T[3]+'"/></linearGradient>'
 +'<path id="mt" d="M24 24 H1099 V770 H24 Z"/></defs>';
 for(var k=0;k<7;k++)g+='<path d="'+band(16,16,W-32,H-32,5,26,k*Math.PI/3.5)+'" fill="none" stroke="'+T[1]+'" stroke-opacity=".55" stroke-width=".7"/>';
 g+='<rect x="6" y="6" width="'+(W-12)+'" height="'+(H-12)+'" fill="none" stroke="url(#mg)" stroke-width="3"/>';
 g+='<rect x="30" y="30" width="'+(W-60)+'" height="'+(H-60)+'" fill="none" stroke="url(#mg)" stroke-width="5"/>';
 g+='<text font-family="Inter" font-size="4.6" letter-spacing="1" fill="'+T[2]+'" fill-opacity=".85" dominant-baseline="middle"><textPath href="#mt">'+Array(40).join('SOLAR ESS · PRACTICAL SOLAR INSTALLATION · VERIFIED CERTIFICATE · ')+'</textPath></text>';
 [[34,34],[W-34,34],[34,H-34],[W-34,H-34]].forEach(function(c){g+='<path d="'+rose(c[0],c[1],26,9.4,11,7,600)+'" fill="none" stroke="url(#mg)" stroke-width=".8"/><circle cx="'+c[0]+'" cy="'+c[1]+'" r="5" fill="url(#mg)"/>'});
 return '<svg class="frame" viewBox="0 0 '+W+' '+H+'" width="100%" height="100%">'+g+'</svg>'}
function bg(T){var W=1055,H=726,g='';g+='<path d="'+rose(W/2,H/2-14,250,92,150,23,4000)+'" fill="none" stroke="'+T[1]+'" stroke-opacity=".14" stroke-width=".6"/>';
 g+='<path d="'+rose(W/2,H/2-14,190,71,110,71,4000)+'" fill="none" stroke="#4338CA" stroke-opacity=".06" stroke-width=".5"/>';
 return '<svg class="bg" viewBox="0 0 '+W+' '+H+'" width="100%" height="100%">'+g+'</svg>'}
function seal(T,n){var cx=95,cy=95,g='<defs><linearGradient id="sg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="'+T[2]+'"/><stop offset=".5" stop-color="'+T[1]+'"/><stop offset="1" stop-color="'+T[3]+'"/></linearGradient>'
 +'<path id="sc" d="M'+(cx-57)+' '+cy+' a57 57 0 1 1 114 0 a57 57 0 1 1 -114 0"/></defs>';
 g+='<path d="M62 150 L44 226 L66 212 L80 230 L92 160Z" fill="#0A1230"/><path d="M128 150 L146 226 L124 212 L110 230 L98 160Z" fill="#0A1230"/>';
 g+='<path d="M66 152 L52 214 L66 205 L78 220 L88 160Z" fill="url(#sg)" opacity=".85"/><path d="M124 152 L138 214 L124 205 L112 220 L102 160Z" fill="url(#sg)" opacity=".85"/>';
 var p='';for(var i=0;i<=96;i++){var a=i/96*Math.PI*2,r=i%2?84:91;p+=(i?'L':'M')+(cx+r*Math.cos(a)).toFixed(1)+' '+(cy+r*Math.sin(a)).toFixed(1)}
 g+='<path d="'+p+'Z" fill="url(#sg)" stroke="'+T[3]+'" stroke-width="1"/>';
 g+='<circle cx="'+cx+'" cy="'+cy+'" r="76" fill="#0A1230"/><circle cx="'+cx+'" cy="'+cy+'" r="72" fill="none" stroke="url(#sg)" stroke-width="1.5"/>';
 g+='<text font-family="Cinzel" font-weight="700" font-size="10" fill="'+T[2]+'" dominant-baseline="middle"><textPath href="#sc" textLength="350" lengthAdjust="spacing">SOLAR ESS ✦ CERTIFIED INSTALLER ✦ THAILAND ✦</textPath></text>';
 g+='<circle cx="'+cx+'" cy="'+cy+'" r="45" fill="url(#sg)"/><path d="'+rose(cx,cy,40,14.3,18,15,1200)+'" fill="none" stroke="#0A1230" stroke-opacity=".18" stroke-width=".5"/><circle cx="'+cx+'" cy="'+cy+'" r="41" fill="none" stroke="#0A1230" stroke-opacity=".5" stroke-width=".8"/>';
 g+='<text x="'+cx+'" y="'+(cy-14)+'" text-anchor="middle" font-family="Cinzel" font-weight="700" font-size="9" letter-spacing="2" fill="#0A1230">LEVEL</text>';
 g+='<text x="'+cx+'" y="'+(cy+16)+'" text-anchor="middle" font-family="Cinzel" font-weight="800" font-size="38" fill="#0A1230">'+n+'</text>';
 var st='';for(var s=0;s<n;s++){var sx=cx-(n-1)*7+s*14,sy=cy+29;st+='<path transform="translate('+sx+' '+sy+') scale(.55)" d="M0-10 2.9-3.1 10-3.1 4.3 1.2 6.5 8.1 0 3.9-6.5 8.1-4.3 1.2-10-3.1-2.9-3.1Z" fill="#0A1230"/>'}
 return '<svg class="seal" viewBox="0 0 190 232">'+g+st+'</svg>'}
function qr(text){try{var q=qrcode(0,'M');q.addData(text);q.make();return q.createSvgTag({cellSize:3,margin:0,scalable:true})}catch(e){return ''}}
function fmt(iso,loc){return new Date(iso).toLocaleDateString(loc,{day:'numeric',month:'short',year:'numeric'})}
function fit(){var el=document.querySelector('.cert');if(el)el.style.zoom=Math.min(1,(innerWidth-32)/1123)}
if(!id){bad();return}
fetch('/api/itest?a=cert&id='+encodeURIComponent(id)).then(function(r){return r.ok?r.json():Promise.reject()}).then(function(c){
 var T=TIERS[c.level]||TIERS[1],url='https://solaress.org/certificate.html?id='+c.id;
 if(!c.validFrom){c.validFrom=c.date;var u=new Date(c.date);u.setFullYear(u.getFullYear()+1);u.setDate(u.getDate()-1);c.validUntil=u.toISOString()}
 document.title=c.name+' · Level '+c.level+' '+c.title_en+' | Solar ESS Certificate';
 var ok=document.getElementById('okv');ok.hidden=false;if(c.valid===false){ok.style.color='#B42318';ok.textContent='✕ Expired on '+fmt(c.validUntil,'en-GB')+' · หมดอายุแล้ว'}else{ok.textContent='✓ Verified by Solar ESS · valid until '+fmt(c.validUntil,'en-GB')+' · ตรวจสอบแล้ว'}
 document.getElementById('c').innerHTML='<div class="cert" style="--m1:'+T[1]+';--m2:'+T[2]+';--m3:'+T[3]+'">'+frame(T)
 +'<div class="paper">'+bg(T)+'<img class="wm" src="'+LOGO+'" alt=""><div class="in">'
 +'<div class="top"><img src="'+LOGO+'" alt="Solar ESS"><div class="addr"><b>Solar ESS Co. Ltd.</b><br>53 Moo 2, Nang Lae, Mueang Chiang Rai<br>Chiang Rai 57100, Thailand<br>www.solaress.org · www.โซลาร์เอสส์.com</div></div>'
 +'<div class="mid"><div class="k">CERTIFICATE OF ACHIEVEMENT</div><h1>Practical Solar Installation</h1><div class="h1t">ใบประกาศนียบัตร การติดตั้งระบบโซลาร์ภาคปฏิบัติ</div>'
 +'<svg class="rule" viewBox="0 0 420 12"><path d="M0 6H180M240 6H420" stroke="'+T[1]+'" stroke-width="1"/><path d="M210 0 216 6 210 12 204 6Z" fill="'+T[1]+'"/><circle cx="192" cy="6" r="2" fill="'+T[1]+'"/><circle cx="228" cy="6" r="2" fill="'+T[1]+'"/></svg>'
 +'<div class="cer">This is to certify that <span>· ขอมอบใบประกาศนียบัตรนี้เพื่อแสดงว่า</span></div><div class="nm">'+esc(c.name)+'</div>'
 +'<div class="has">has successfully passed the Solar ESS installer examination at <span>· ได้สอบผ่านการทดสอบช่างติดตั้งโซลาร์ ระดับ</span></div>'
 +'<div class="ttl">LEVEL '+c.level+' · '+esc(c.title_en.toUpperCase())+'</div><div class="ttlt">ระดับ '+c.level+' · '+esc(c.title_th)+'</div>'
 +'<div class="tier">'+T[0]+' TIER</div>'+(c.work?'<div class="work">✓ ACCEPTED FOR SOLAR ESS INSTALLATION WORK · <span>ผ่านเกณฑ์รับงานติดตั้งกับ Solar ESS</span></div>':'')+'</div>'
 +seal(T,c.level)
 +'<div class="meta"><div>SCORE · <i>คะแนน</i><b>'+c.score+' / '+c.total+' ('+c.pct+'%)</b></div><div>VALID FROM – TO · <i>มีอายุตั้งแต่ – ถึง</i><b>'+esc(fmt(c.validFrom,'en-GB'))+' – '+esc(fmt(c.validUntil,'en-GB'))+'</b><i>'+esc(fmt(c.validFrom,'th-TH'))+' – '+esc(fmt(c.validUntil,'th-TH'))+'</i></div><div>CERTIFICATE NO. · <i>เลขที่</i><b>'+esc(c.id)+'</b></div></div>'
 +'<div class="iss"><div class="ln"></div>Issued by · ออกโดย<br><b>Solar ESS Co. Ltd. · Solar ESS Working Group</b></div>'
 +'<div class="qr"><div class="box">'+qr(url)+'</div><b>Scan to verify · สแกนเพื่อตรวจสอบ</b></div>'
 +(c.valid===false?'<div class="exp">EXPIRED · หมดอายุ</div>':'')+'</div></div></div>';
 fit();addEventListener('resize',fit)}).catch(bad);
addEventListener('beforeprint',function(){var el=document.querySelector('.cert');if(el)el.style.zoom=''});addEventListener('afterprint',fit)})();
</script>
</body></html>
"""

(ROOT / "certificate.html").write_text(HTML.replace("__LOGO__", LOGO).replace("__QR__", QR), encoding="utf-8")
print("wrote certificate.html")
