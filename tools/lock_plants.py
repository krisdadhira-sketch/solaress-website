"""Make the "Plants by Province" pages admin-only.

The full pages built by tools/plants_page.py (plants.html, th/plants.html) and data/plant-index.json are moved
into the private docs function (netlify/functions/docs/plants-pages.json). The public files are replaced by a
small sign-in page; after the admin password is accepted, /api/docs?a=plants-page&l=en|th returns the full page.
Same password as all admin pages. Run after tools/plants_page.py (it calls this automatically).
"""
import json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
MARK = "<!--admin-locked-->"
OUT = ROOT / "netlify/functions/docs/plants-pages.json"

SCROLL = ('<script>(function(){function g(){var h=location.hash;if(h.length>1){var e=document.getElementById(h.slice(1));'
          'if(e)e.scrollIntoView({block:"start"})}}if(document.readyState!=="loading")setTimeout(g,60);'
          'else document.addEventListener("DOMContentLoaded",function(){setTimeout(g,60)})})();</script>')

T = {
    "en": dict(lang="en", title="Plants by Province | Solar ESS Admin", h="Solar ESS Admin", p="Plants by Province is for Solar ESS staff only. Same password as all admin pages.",
               ph="Admin password", btn="Sign in", bad="Password is not right.", load="Loading…", l="en"),
    "th": dict(lang="th", title="โรงไฟฟ้าตามจังหวัด | Solar ESS Admin", h="Solar ESS Admin", p="หน้าโรงไฟฟ้าตามจังหวัดสำหรับเจ้าหน้าที่ Solar ESS เท่านั้น ใช้รหัสผ่านเดียวกับหน้าผู้ดูแลระบบทุกหน้า",
               ph="รหัสผ่านผู้ดูแลระบบ", btn="เข้าสู่ระบบ", bad="รหัสผ่านไม่ถูกต้อง", load="กำลังโหลด…", l="th"),
}


def shell(t):
    return f"""<!DOCTYPE html>{MARK}
<html lang="{t['lang']}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>{t['title']}</title>
<style>:root{{--navy:#0B1736;--violet:#4B4FD8;--line:#D7DAEA}}*{{box-sizing:border-box}}
body{{margin:0;font-family:"IBM Plex Sans Thai","Sarabun",system-ui,-apple-system,"Segoe UI",sans-serif;background:#F5F6FB;color:#1d2333}}
header{{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:14px 22px;background:#fff;border-bottom:3px solid var(--navy)}}
header img{{height:54px}}.addr{{text-align:right;font-size:12.5px;line-height:1.45;color:#5A6275}}.addr b{{color:var(--navy)}}
.login{{max-width:380px;margin:12vh auto;background:#fff;border:1px solid var(--line);border-radius:16px;padding:26px 26px 20px;box-shadow:0 10px 30px rgba(11,23,54,.08)}}
h1{{margin:0 0 6px;font-size:22px;color:var(--navy)}}p{{margin:0 0 12px;color:#5A6275;font-size:14px;line-height:1.5}}
input{{width:100%;padding:11px 12px;border:1.5px solid var(--line);border-radius:10px;font:inherit;margin:4px 0 12px}}
button{{width:100%;padding:11px;border:0;border-radius:10px;background:var(--violet);color:#fff;font:600 15px/1 inherit;cursor:pointer}}
.err{{color:#B42318;min-height:20px;margin:10px 0 0;font-size:13.5px}}</style></head>
<body><header><img src="/images/solar-ess-report-logo.jpg" alt="Solar ESS"><div class="addr"><b>Solar ESS Co. Ltd.</b><br>53 Moo 2, Tambon Nanglae, Amphoe Muang, Chiang Rai 57100<br>Tel 063 151 6694 · www.solaress.org · www.โซลาร์เอสส์.com</div></header>
<main id="main"><div class="login"><h1>{t['h']}</h1><p>{t['p']}</p>
<form id="lf"><input type="password" id="pw" placeholder="{t['ph']}" autocomplete="current-password" aria-label="{t['ph']}"><button type="submit">{t['btn']}</button></form>
<p class="err" id="lerr" role="status"></p></div></main>
<script>(function(){{var K='members-admin-pw',PW='',e=document.getElementById('lerr');try{{PW=sessionStorage.getItem(K)||''}}catch(x){{}}
function go(){{if(!PW)return;e.textContent='{t['load']}';fetch('/api/docs?a=plants-page&l={t['l']}',{{headers:{{'x-admin-password':PW}},cache:'no-store'}})
.then(function(r){{if(r.status===401)throw new Error('401');if(!r.ok)throw new Error(r.status);return r.text()}})
.then(function(h){{try{{sessionStorage.setItem(K,PW)}}catch(x){{}}document.open();document.write(h);document.close()}})
.catch(function(x){{try{{sessionStorage.removeItem(K)}}catch(y){{}}e.textContent=x.message==='401'?'{t['bad']}':x.message;PW=''}})}}
document.getElementById('lf').addEventListener('submit',function(v){{v.preventDefault();PW=document.getElementById('pw').value.trim();go()}});go()}})();</script>
</body></html>
"""


def lock():
    pages = json.load(open(OUT, encoding="utf-8")) if OUT.exists() else {}
    for lang, f in (("en", "plants.html"), ("th", "th/plants.html")):
        p = ROOT / f
        s = p.read_text(encoding="utf-8")
        if MARK not in s:  # a freshly built full page: move it into the private store
            s = re.sub(r'<meta name="robots"[^>]*>\n?', "", s)
            s = s.replace("<head>", '<head><meta name="robots" content="noindex,nofollow">', 1)
            s = s.replace("</body>", SCROLL + "</body>", 1)
            pages[lang] = s
        p.write_text(shell(T[lang]), encoding="utf-8")
    pages["index"] = json.load(open(ROOT / "data/plant-index.json", encoding="utf-8"))
    json.dump(pages, open(OUT, "w", encoding="utf-8"), ensure_ascii=False)
    print("plants pages locked:", {k: len(v) if isinstance(v, str) else "json" for k, v in pages.items()})


if __name__ == "__main__":
    lock()
