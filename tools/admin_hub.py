# -*- coding: utf-8 -*-
"""www.solaress.org/admin : one sign-in for all admin pages, with a menu.
- Signs in once (same admin password: MEMBERS_ADMIN_PASSWORD) and keeps it in sessionStorage 'members-admin-pw',
  which every admin page reads, so each page opens without asking again.
- Each admin page loads inside the hub (iframe, same origin). A small bridge script in each admin page hides its own
  header when shown inside the hub, and adds an "Admin home" button when opened on its own.
Run from the repo root:  python3 tools/admin_hub.py"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
idx = (ROOT / "index.html").read_text(encoding="utf-8")
LOGO = re.search(r'<header class="nav">.*?<img src="(data:image/[^"]+)"', idx, re.S).group(1)

PAGES = [  # id, file, label, description
    ("jobs", "/feedback-admin.html", "Jobs & payment release", "Job posts, installer reports, customer feedback, close jobs and release payment."),
    ("applications", "/members-admin.html", "TSIA & partner applications", "Approve, reject or hide TSIA members and installer partners."),
    ("test", "/itest-admin.html", "Installer test & certificates", "Level 1–5 results, wrong answers, certificate numbers, CSV."),
    ("vocab", "/vocab-admin.html", "Vocabulary test results", "Students, scores per test and progress."),
]
PUBLIC = [("/job.html", "Job board"), ("/installer-test.html", "Installer test"), ("/partners.html", "Installer partners"),
          ("/members.html", "Members"), ("/team.html#join-tsia", "TSIA registration"), ("/vocabulary.html", "Vocabulary test"), ("/", "Home page")]

menu = "".join(f'<a href="#{i}" data-p="{i}">{l}</a>' for i, f, l, d in PAGES)
cards = "".join(f'<a class="tile" href="#{i}"><b>{l}</b><span>{d}</span><em id="n-{i}">…</em></a>' for i, f, l, d in PAGES)
pub = "".join(f'<a href="{h}" target="_blank" rel="noopener">{l} ↗</a>' for h, l in PUBLIC)
pages_js = "{" + ",".join(f'"{i}":"{f}"' for i, f, l, d in PAGES) + "}"

HTML = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>Admin | Solar ESS</title>
<style>
:root{{--navy:#0A1230;--blue:#2563EB;--violet:#4338CA;--ink:#0A0E2E;--mute:#3E548E;--line:#DEE3ED;--paper:#F6F8FC}}
*{{box-sizing:border-box}}html,body{{height:100%}}body{{margin:0;font:15px/1.5 "IBM Plex Sans Thai","Inter",system-ui,sans-serif;color:var(--ink);background:var(--paper)}}
.login{{max-width:420px;margin:12vh auto 0;background:#fff;border:1px solid var(--line);border-radius:18px;padding:28px;text-align:center}}
.login img{{height:64px;border-radius:8px}}.login h1{{font-size:22px;margin:12px 0 4px}}
.login input{{width:100%;font:inherit;padding:11px 12px;border:1.5px solid var(--line);border-radius:10px;margin:14px 0 10px}}
button{{font:inherit;border:0;border-radius:10px;padding:10px 18px;font-weight:600;cursor:pointer;background:var(--blue);color:#fff}}
.err{{color:#B42318;font-size:14px;min-height:20px}}.meta{{color:var(--mute);font-size:13px}}
.app{{display:grid;grid-template-columns:250px 1fr;height:100vh}}
aside{{background:var(--navy);color:#fff;display:flex;flex-direction:column;padding:16px 12px;gap:4px;overflow:auto}}
aside .brand{{display:flex;gap:10px;align-items:center;padding:4px 8px 14px;border-bottom:1px solid rgba(255,255,255,.12);margin-bottom:8px}}
aside .brand img{{height:40px;border-radius:6px;background:#fff}}aside .brand b{{font-size:15px;line-height:1.2}}
aside a{{color:#D6DCF5;text-decoration:none;padding:9px 12px;border-radius:10px;font-size:14.5px}}
aside a:hover{{background:rgba(255,255,255,.08)}}aside a.on{{background:var(--violet);color:#fff;font-weight:600}}
aside h4{{margin:14px 12px 4px;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#8E9BC7}}
aside .pub{{display:grid;gap:2px}}aside .sp{{flex:1}}aside button{{background:transparent;border:1px solid rgba(255,255,255,.3);color:#fff;margin:8px}}
main{{position:relative;overflow:auto}}
iframe{{border:0;width:100%;height:100%;display:block;background:var(--paper)}}
.top{{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:10px 18px;border-bottom:1px solid var(--line);background:#fff;font-size:14px}}
.top a{{color:var(--blue)}}
.frame{{position:absolute;inset:45px 0 0 0}}
.ov{{padding:28px;max-width:1100px}}
.ov h2{{margin:0 0 4px}}.tiles{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px;margin-top:18px}}
.tile{{background:#fff;border:1px solid var(--line);border-radius:16px;padding:18px;text-decoration:none;color:var(--ink);display:grid;gap:6px}}
.tile:hover{{border-color:var(--violet);box-shadow:0 6px 20px rgba(67,56,202,.12)}}
.tile b{{font-size:16px;color:var(--navy)}}.tile span{{font-size:13.5px;color:var(--mute)}}.tile em{{font-style:normal;font-weight:700;color:var(--violet);font-size:14px}}
@media (max-width:800px){{.app{{display:block;height:auto}}
 aside{{flex-direction:row;flex-wrap:nowrap;align-items:center;overflow-x:auto;padding:8px;gap:4px;position:sticky;top:0;z-index:5}}
 aside .brand,aside h4,aside .sp,aside .pub{{display:none}}aside a{{white-space:nowrap}}aside button{{margin:0;white-space:nowrap}}
 main{{min-height:calc(100vh - 56px)}}.frame{{position:static;height:calc(100vh - 100px)}}}}
</style></head><body>
<div class="login" id="login"><img src="{LOGO}" alt="Solar ESS"><h1>Solar ESS Admin</h1><p class="meta">One password for all admin pages.</p>
<form id="lf"><input type="password" id="pw" placeholder="Admin password" autocomplete="current-password" autofocus><button type="submit" style="width:100%">Sign in</button></form><p class="err" id="lerr"></p></div>
<div class="app" id="app" hidden>
<aside><div class="brand"><img src="{LOGO}" alt=""><b>Solar ESS<br>Admin</b></div>
<a href="#home" data-p="home">Overview</a>{menu}
<h4>Public pages</h4><div class="pub">{pub}</div>
<div class="sp"></div><button type="button" id="out">Sign out</button></aside>
<main><div id="home" class="ov"><h2>Overview</h2><p class="meta">Choose a page from the menu. Everything opens with the password you just entered.</p><div class="tiles">{cards}</div></div>
<div id="fr" hidden><div class="top"><b id="ft"></b><a id="fo" target="_blank" rel="noopener">Open in new tab ↗</a></div><div class="frame"><iframe id="ifr" title="Admin page"></iframe></div></div></main>
</div>
<script>
(function(){{var $=function(i){{return document.getElementById(i)}},P={pages_js},PW='';
try{{PW=sessionStorage.getItem('members-admin-pw')||''}}catch(e){{}}
function api(u){{return fetch(u,{{headers:{{'x-admin-password':PW}}}}).then(function(r){{return r.json().then(function(j){{if(!r.ok)throw new Error(j.error||r.status);return j}})}})}}
function counts(){{
 api('/api/members?a=list').then(function(j){{var it=j.items||[],p=it.filter(function(x){{return x.status==='pending'}}).length;$('n-applications').textContent=p+' pending · '+it.filter(function(x){{return x.status==='approved'}}).length+' approved'}}).catch(function(){{$('n-applications').textContent=''}});
 api('/api/feedback?a=list').then(function(j){{$('n-jobs').textContent=(j.jobs||[]).length+' jobs · '+(j.items||[]).length+' reports & feedback'}}).catch(function(){{$('n-jobs').textContent=''}});
 api('/api/itest?a=list').then(function(j){{var a=j.attempts||[];$('n-test').textContent=a.length+' attempts · '+a.filter(function(x){{return x.pass}}).length+' certificates'}}).catch(function(){{$('n-test').textContent=''}});
 api('/api/vocab?a=admin').then(function(j){{$('n-vocab').textContent=(j.students||[]).length+' students'}}).catch(function(){{$('n-vocab').textContent=''}});
}}
function show(){{var id=(location.hash||'#home').slice(1);if(id!=='home'&&!P[id])id='home';
 [].forEach.call(document.querySelectorAll('aside [data-p]'),function(a){{a.classList.toggle('on',a.getAttribute('data-p')===id)}});
 $('home').hidden=id!=='home';$('fr').hidden=id==='home';
 if(id==='home'){{counts();return}}
 var lab=document.querySelector('aside [data-p="'+id+'"]').textContent;$('ft').textContent=lab;$('fo').href=P[id];document.title=lab+' | Solar ESS Admin';
 if($('ifr').getAttribute('src')!==P[id])$('ifr').src=P[id]}}
function enter(){{try{{sessionStorage.setItem('members-admin-pw',PW);sessionStorage.setItem('vocabAdmin',PW)}}catch(e){{}}$('login').hidden=true;$('app').hidden=false;show()}}
$('lf').addEventListener('submit',function(e){{e.preventDefault();PW=$('pw').value.trim();if(!PW)return;$('lerr').textContent='Checking…';
 api('/api/itest?a=list').then(function(){{$('lerr').textContent='';enter()}}).catch(function(x){{$('lerr').textContent=x.message==='401'?'Password is not right.':x.message}})}});
$('out').onclick=function(){{try{{sessionStorage.removeItem('members-admin-pw');sessionStorage.removeItem('vocabAdmin')}}catch(e){{}}PW='';$('ifr').removeAttribute('src');$('app').hidden=true;$('login').hidden=false;$('pw').value='';location.hash=''}};
addEventListener('hashchange',function(){{if(PW)show()}});
if(PW)api('/api/itest?a=list').then(enter).catch(function(){{PW=''}});
}})();
</script>
</body></html>
"""
(ROOT / "admin.html").write_text(HTML, encoding="utf-8")

# Bridge in each admin page: inside the hub -> hide own header/site chrome; on its own -> "Admin home" button.
BRIDGE = """<!--adminbridge--><script>(function(){var inHub=false;try{inHub=window.self!==window.top&&window.top.location.pathname.replace(/\\.html$/,'')==='/admin'}catch(e){}
var st=document.createElement('style');
if(inHub){st.textContent='body>header,header.nav,footer,.fab,.mnav-btn,.share{display:none!important}main{padding-top:14px!important}';}
else{st.textContent='.adm-home{position:fixed;left:14px;bottom:14px;z-index:99;background:#0A1230;color:#fff;border-radius:99px;padding:9px 16px;font:600 14px system-ui,sans-serif;text-decoration:none;box-shadow:0 6px 18px rgba(0,0,0,.25)}';
 addEventListener('DOMContentLoaded',function(){var a=document.createElement('a');a.className='adm-home';a.href='/admin';a.textContent='\\u2699 Admin home';document.body.appendChild(a)})}
document.head.appendChild(st)})();</script><!--/adminbridge-->"""
for i, f, l, d in PAGES:
    p = ROOT / f.lstrip("/")
    s = p.read_text(encoding="utf-8")
    s = re.sub(r"<!--adminbridge-->.*?<!--/adminbridge-->", "", s, flags=re.S)
    s = s.replace("</head>", BRIDGE + "\n</head>", 1)
    p.write_text(s, encoding="utf-8")
print("wrote admin.html and bridged", len(PAGES), "admin pages")
