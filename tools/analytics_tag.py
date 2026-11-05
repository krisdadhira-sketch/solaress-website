# -*- coding: utf-8 -*-
"""Add Google Analytics 4 (stream "solaress.org", G-46HG0JWSZV) to every public page.

Idempotent: the tag lives between <!--ga4--> and <!--/ga4--> right after <head ...>.
Run from the repo root after adding or regenerating pages:  python3 tools/analytics_tag.py

Skipped: admin pages, the Google verification file and the /s/ share-redirect pages
(they forward to the real page, which is counted there).

Events sent besides page views (enhanced measurement adds scrolls, outbound clicks,
file downloads and form interactions on its own):
  book_consultation_click  any link to #consult
  phone_click              tel: links          (link_url = the number)
  line_click               line.me links
  facebook_click           facebook.com links
  form_sent                on the thanks page after a form was sent (form_name = which form)
  generate_lead            same moment, for the customer forms (consultation, installer-request)
Mark generate_lead (and phone_click / line_click if wanted) as Key events in GA:
Admin > Data display > Events.
"""
import glob, re

GA_ID = "G-46HG0JWSZV"
SKIP = {"members-admin.html", "vocab-admin.html", "googlef2e2bf45e07052f3.html"}

TAG = f"""<!--ga4--><script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA_ID}');
(function(){{var LEAD={{'consultation':1,'installer-request':1}};
function ev(n,p){{try{{gtag('event',n,p||{{}})}}catch(e){{}}}}
document.addEventListener('click',function(e){{var a=e.target.closest&&e.target.closest('a[href]');if(!a)return;var h=a.getAttribute('href')||'';
 if(/#consult$/.test(h))ev('book_consultation_click',{{link_text:(a.textContent||'').trim().slice(0,60),page_path:location.pathname}});
 else if(/^tel:/i.test(h))ev('phone_click',{{link_url:h.slice(4),page_path:location.pathname}});
 else if(/line\\.me/i.test(h))ev('line_click',{{page_path:location.pathname}});
 else if(/facebook\\.com/i.test(h))ev('facebook_click',{{page_path:location.pathname}});}},true);
document.addEventListener('submit',function(e){{var f=e.target;try{{sessionStorage.setItem('ga_form',f.getAttribute('name')||f.id||'form')}}catch(x){{}}}},true);
if(/\\/thanks\\.html$/.test(location.pathname)){{var n=null;try{{n=sessionStorage.getItem('ga_form');sessionStorage.removeItem('ga_form')}}catch(x){{}}
 if(n){{ev('form_sent',{{form_name:n}});if(LEAD[n])ev('generate_lead',{{form_name:n}})}}}}
}})();</script><!--/ga4-->"""

n = 0
for f in sorted(glob.glob("*.html") + glob.glob("th/*.html") + glob.glob("zh/*.html")):
    if f in SKIP:
        continue
    h = open(f, encoding="utf-8").read()
    h = re.sub(r"\n?<!--ga4-->.*?<!--/ga4-->\n?", "", h, flags=re.S)
    m = re.search(r"<head[^>]*>", h, flags=re.I)
    if not m:
        print("no <head>:", f); continue
    h = h[:m.end()] + "\n" + TAG + "\n" + h[m.end():]
    open(f, "w", encoding="utf-8").write(h); n += 1
print(n, "pages tagged with", GA_ID)
