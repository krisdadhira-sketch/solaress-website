# -*- coding: utf-8 -*-
"""Ongoing projects page (EN /ongoing.html, TH /th/ongoing.html), linked first in the News dropdown on every page.
- Overview of the current projects (taken from the News article #upcoming-projects-nov2026) + the Starbucks @ My Park
  CAR-insurance section that used to sit on the profile page (#ongoing).
- The profile page keeps a short #ongoing band pointing here, so old links still work; links to profile#ongoing
  across the site now point to /ongoing.html; "Ongoing project" is removed from the Solar ESS dropdown.
Idempotent. Run:  python3 tools/ongoing_page.py   (then tools/accessibility.py, tools/site_search.py)"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
T = {
    "en": dict(base="", title="Ongoing Projects – Solar ESS Co. Ltd.", menu="Ongoing Projects",
               desc="Solar ESS projects in progress: off-grid systems in Chiang Rai and a commercial on-grid rooftop in Chonburi, covered by Contractor All Risk insurance.",
               eyebrow="News · Ongoing projects", h1="Ongoing projects", lede="What our team is building right now, across Thailand.",
               upd="Updated 9 November 2026", mp="Starbucks @ My Park: project details and insurance",
               moved="Our ongoing projects now have their own page.", go="See ongoing projects →",
               cta="Plan your own project", cta2="Installers: open jobs", locale="en_US"),
    "th": dict(base="/th", title="โครงการที่กำลังดำเนินการ – บริษัท โซลาร์ เอสส์ จำกัด", menu="โครงการที่กำลังดำเนินการ",
               desc="โครงการของโซลาร์ เอสส์ ที่กำลังดำเนินการ: ระบบออฟกริดในเชียงราย และระบบออนกริดบนหลังคาเชิงพาณิชย์ในชลบุรี คุ้มครองด้วยประกันภัย CAR",
               eyebrow="ข่าวสาร · โครงการที่กำลังดำเนินการ", h1="โครงการที่กำลังดำเนินการ", lede="งานที่ทีมของเรากำลังติดตั้งอยู่ในขณะนี้ ทั่วประเทศไทย",
               upd="อัปเดต 9 พฤศจิกายน 2569", mp="Starbucks @ My Park: รายละเอียดโครงการและประกันภัย",
               moved="โครงการที่กำลังดำเนินการย้ายไปอยู่ในหน้าของตัวเองแล้ว", go="ดูโครงการที่กำลังดำเนินการ →",
               cta="วางแผนโครงการของคุณ", cta2="ช่างติดตั้ง: งานที่เปิดรับ", locale="th_TH"),
}
ZH_MENU = "在建项目"


def news_projects(lang):
    s = (ROOT / ("th/news.html" if lang == "th" else "news.html")).read_text(encoding="utf-8")
    a = re.search(r'<article id="upcoming-projects-nov2026".*?</article>', s, re.S).group(0)
    body = a[a.index('<h3'): a.index('<p style="margin-top:24px">')]
    # each project gets an anchor
    ids = iter(["akao-phase-2", "m-harmony-resort", "my-park"])
    body = re.sub(r"<h3 ", lambda _: f'<h3 id="{next(ids)}" ', body)
    return body


def profile_section(lang):
    p = ROOT / ("th/profile.html" if lang == "th" else "profile.html")
    s = p.read_text(encoding="utf-8")
    m = re.search(r'<section class="band light" id="ongoing">.*?</section>', s, re.S)
    if m and "<!--ongoing-moved-->" not in m.group(0):
        sec = m.group(0)
        (ROOT / "data").mkdir(exist_ok=True)
        (ROOT / "data" / f"ongoing-mypark-{lang}.html").write_text(sec, encoding="utf-8")  # keep the original for re-runs
    sec = (ROOT / "data" / f"ongoing-mypark-{lang}.html").read_text(encoding="utf-8")
    sec = sec.replace('id="ongoing"', 'id="my-park-insurance"').replace('href="#insurance"', f'href="{T[lang]["base"]}/profile.html#insurance"')
    return sec


def build(lang):
    t = T[lang]
    shell = (ROOT / ("th/statement.html" if lang == "th" else "statement.html")).read_text(encoding="utf-8")
    url = f"https://solaress.org{t['base']}/ongoing"
    h = shell
    h = re.sub(r"<title>[^<]*</title>", f"<title>{t['title']}</title>", h, count=1)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{t["desc"]}">', h, count=1)
    h = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{t["title"]}">', h, count=1)
    h = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{t["desc"]}">', h, count=1)
    h = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', h, count=1)
    h = re.sub(r'<meta property="og:image" content="[^"]*">', '<meta property="og:image" content="https://solaress.org/images/job-maesuai-pv-roof.jpg">', h, count=1)
    h = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', h, count=1)
    h = re.sub(r'<link rel="alternate" hreflang="zh-Hans"[^>]*>\n?', "", h)
    h = h.replace('href="https://solaress.org/statement"', 'href="https://solaress.org/ongoing"').replace('href="https://solaress.org/th/statement"', 'href="https://solaress.org/th/ongoing"')
    # language switcher: EN <-> TH; 中文 goes to the Chinese home page (no Chinese version of this page)
    def sw(m):
        x = m.group(0)
        x = re.sub(r'(<a href=")[^"]*(" lang="en")', r'\1/ongoing.html\2', x)
        x = re.sub(r'(<a href=")[^"]*(" lang="th")', r'\1/th/ongoing.html\2', x)
        x = re.sub(r'(<a href=")[^"]*(" lang="zh-Hans")', r'\1/zh/\2', x)
        return x
    h = re.sub(r'<span class="langsw">.*?</span>', sw, h, count=1, flags=re.S)
    main = (f'<section class="dark band" style="padding-block:64px"><div class="wrap"><p class="eyebrow">{t["eyebrow"]}</p>'
            f'<h1 style="font-size:clamp(36px,6vw,60px)">{t["h1"]}</h1><p class="lede" style="margin-top:18px">{t["lede"]}</p>'
            f'<p class="fine" style="margin-top:10px;opacity:.85">{t["upd"]}</p></div></section>\n'
            f'<section class="band light" id="projects-now"><div class="wrap"><article style="max-width:760px">{news_projects(lang)}'
            f'<p style="margin-top:26px;display:flex;gap:10px;flex-wrap:wrap"><a class="btn" href="{t["base"]}/#consult">{t["cta"]}</a>'
            f'<a class="btn ghost" href="{t["base"]}/job.html">{t["cta2"]}</a></p></article></div></section>\n'
            + profile_section(lang) + "\n")
    h = re.sub(r"(<main[^>]*><!--main-->).*?(<!--/main--></main>)", lambda m: m.group(1) + main + m.group(2), h, count=1, flags=re.S)
    # the My Park link in the overview goes to the insurance section on this page
    h = h.replace(f'href="{t["base"]}/profile.html#ongoing"', 'href="#my-park-insurance"')
    (ROOT / (f"th/ongoing.html" if lang == "th" else "ongoing.html")).write_text(h, encoding="utf-8")


for lg in ("en", "th"):
    profile_section(lg)  # saves the original section before the profile is changed
    build(lg)
    # profile: short pointer band keeps the #ongoing anchor
    p = ROOT / ("th/profile.html" if lg == "th" else "profile.html")
    s = p.read_text(encoding="utf-8")
    band = (f'<section class="band light" id="ongoing"><!--ongoing-moved--><div class="wrap" style="display:flex;gap:16px;align-items:center;flex-wrap:wrap;justify-content:space-between">'
            f'<p style="margin:0;font-size:18px"><b>{T[lg]["moved"]}</b></p><a class="btn" href="{T[lg]["base"]}/ongoing.html">{T[lg]["go"]}</a></div></section>')
    s = re.sub(r'<section class="band light" id="ongoing">.*?</section>', lambda _: band, s, count=1, flags=re.S)
    p.write_text(s, encoding="utf-8")

# menus and links on every page
n = 0
for f in sorted(ROOT.glob("*.html")) + sorted((ROOT / "th").glob("*.html")) + sorted((ROOT / "zh").glob("*.html")):
    s = f.read_text(encoding="utf-8"); o = s
    s = re.sub(r'<a href="(/th|/zh)?/profile\.html#ongoing">[^<]*</a>(?=<a href="[^"]*/statement\.html">)', "", s)  # Solar ESS dropdown item
    lang = "th" if f.parent.name == "th" else "zh" if f.parent.name == "zh" else "en"
    href = "/th/ongoing.html" if lang == "th" else "/ongoing.html"
    label = T["th"]["menu"] if lang == "th" else ZH_MENU if lang == "zh" else T["en"]["menu"]
    m = re.search(r'(<span class="dd"><a href="(?:/th/|/zh/|/)news\.html">[^<]*</a><span class="ddm">)(<!--ogm-->.*?<!--/ogm-->)?', s)
    if m:
        s = s[: m.end(1)] + f'<!--ogm--><a href="{href}">{label}</a><!--/ogm-->' + s[m.end():]
    if f.name != "ongoing.html":
        s = s.replace('href="/profile.html#ongoing"', 'href="/ongoing.html"').replace('href="/th/profile.html#ongoing"', 'href="/th/ongoing.html"')
    if s != o:
        f.write_text(s, encoding="utf-8"); n += 1
print("ongoing pages built; menus/links updated on", n, "pages")

# sitemap
sm = ROOT / "sitemap.xml"
x = sm.read_text(encoding="utf-8")
if "/ongoing</loc>" not in x:
    entry = ("  <url>\n    <loc>https://solaress.org/ongoing</loc>\n    <lastmod>2026-11-09</lastmod>\n"
             '    <xhtml:link rel="alternate" hreflang="en" href="https://solaress.org/ongoing"/>\n'
             '    <xhtml:link rel="alternate" hreflang="th" href="https://solaress.org/th/ongoing"/>\n'
             '    <xhtml:link rel="alternate" hreflang="x-default" href="https://solaress.org/ongoing"/>\n  </url>\n'
             "  <url>\n    <loc>https://solaress.org/th/ongoing</loc>\n    <lastmod>2026-11-09</lastmod>\n"
             '    <xhtml:link rel="alternate" hreflang="en" href="https://solaress.org/ongoing"/>\n'
             '    <xhtml:link rel="alternate" hreflang="th" href="https://solaress.org/th/ongoing"/>\n'
             '    <xhtml:link rel="alternate" hreflang="x-default" href="https://solaress.org/ongoing"/>\n  </url>\n')
    x = x.replace("</urlset>", entry + "</urlset>")
    sm.write_text(x, encoding="utf-8")
