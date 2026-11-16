"""Make the Monthly Report admin-only (17 Nov 2026).

The "Monthly Report" topic section is moved out of technical-notes.html / th/technical-notes.html into
monthly-report.html / th/monthly-report.html. Those pages, the Monthly Report PDFs (/downloads/Solar-ESS-Monthly-Report-*)
and their preview images (/images/note-monthly-*) are served only with the admin sign-in cookie
(netlify/edge-functions/admin-gate.js, /api/admin-session). Public menus, search and share stubs no longer point to them.

Run again after any tool adds new monthly notes to technical-notes.html: the section is moved again
(the private page is rebuilt from the latest public page that still has it).
"""
import json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SEC = '<section class="topicsec" id="topic-monthly"'
LANGS = {"en": ("technical-notes.html", "monthly-report.html", "/"), "th": ("th/technical-notes.html", "th/monthly-report.html", "/th/")}
TITLE = {"en": "Monthly Report (admin only) | Solar ESS", "th": "รายงานประจำเดือน (เฉพาะผู้ดูแล) | Solar ESS"}
BANNER = {"en": "Admin only – not shown on the public website.", "th": "เฉพาะผู้ดูแลระบบ – ไม่แสดงบนเว็บไซต์สาธารณะ"}


HASHJS = '<script>(function(){var h=location.hash;if(/^#(monthly-|plant-|topic-monthly)/.test(h))location.replace((location.pathname.indexOf("/th/")===0?"/th/":"/")+"monthly-report.html"+h)})();</script>'


def cut(s):
    a = s.find(SEC)
    if a < 0:
        return None, s
    b = s.find('<section class="topicsec"', a + 10)
    return s[a:b], s[:a] + s[b:]


def private_page(full, sec, lang, pre):
    p = full
    # keep only the monthly section in the topic area
    a = p.find('<section class="topicsec"'); ls = p.rfind('<section class="topicsec"')
    z = p.find('</section>', ls) + len('</section>')
    p = p[:a] + f'<p style="background:#EEF0FB;border-left:4px solid #4B4FD8;padding:8px 12px;border-radius:8px;font-weight:600">{BANNER[lang]}</p>' + sec + p[z:]
    p = re.sub(r"<title>.*?</title>", f"<title>{TITLE[lang]}</title>", p, count=1, flags=re.S)
    p = re.sub(r'<meta name="robots"[^>]*>', "", p)
    p = p.replace("<head>", '<head><meta name="robots" content="noindex,nofollow">', 1)
    p = re.sub(r'<link rel="canonical"[^>]*>', "", p)
    p = re.sub(r'<link rel="alternate" hreflang[^>]*>\n?', "", p)
    p = re.sub(r'<script type="application/ld\+json">.*?</script>', "", p, flags=re.S)
    # in-page topic links to other topics go back to the public page
    p = re.sub(r'href="#topic-(?!monthly|top)([a-z-]+)"', lambda m: f'href="{pre}technical-notes.html#topic-{m.group(1)}"', p)
    p = re.sub(r'href="(?:https://solaress\.org)?' + re.escape(pre) + r'technical-notes\.html#(monthly-[^"]*|plant-[^"]*|topic-monthly)"', r'href="#\1"', p)
    return p


def public_fix(s, lang, pre):
    # topic menus / chips inside the technical notes page; "All topics" count drops by the monthly count
    mc = re.search(r'<a href="#topic-monthly">[^<]*<span>(\d+)</span></a>', s)
    k = int(mc.group(1)) if mc else 0
    s = re.sub(r'<a href="#topic-monthly">[^<]*(?:<span>\d+</span>)?</a>', "", s)
    if k:
        s = re.sub(r'(<a href="#topic-top">[^<]*<span>)(\d+)(</span>)', lambda m: f"{m.group(1)}{int(m.group(2)) - k}{m.group(3)}", s)
    s = s.replace("Solar Technical Notes &amp; Monthly Plant Reports", "Solar Technical Notes")
    if "monthly-report.html\"+h" not in s:
        s = s.replace("</head>", HASHJS + "</head>", 1)
    s = re.sub(r'(<meta (?:property="og:image"|name="twitter:image") content="https://solaress.org/images/)note-monthly-[^"]*"', r'\1solar-ess-report-logo.jpg"', s)
    return s


def link_fix(s):
    for pre in ("/", "/th/"):
        s = re.sub(r'<a href="' + re.escape(pre) + r'technical-notes\.html#topic-monthly">[^<]*</a>', "", s)
    s = re.sub(r'<a href="/technical-notes\.html#topic-monthly">[^<]*</a>', "", s)
    s = re.sub(r'href="(?:https://solaress\.org)?(/th/|/)technical-notes\.html#((?:monthly-|plant-)[^"]*|plant-codes)"', r'href="\1monthly-report.html#\2"', s)
    return s


def lock():
    for lang, (src, dst, pre) in LANGS.items():
        f = ROOT / src
        s = f.read_text(encoding="utf-8")
        sec, rest = cut(s)
        if sec:
            pv = link_fix(private_page(s, sec, lang, pre))
            pv = re.sub(r'(<span class="langsw">.*?</span>)', lambda m: m.group(1).replace('/th/technical-notes.html"', '/th/monthly-report.html"').replace('/technical-notes.html"', '/monthly-report.html"').replace('/zh/monthly-report.html"', '/zh/technical-notes.html"'), pv, count=1, flags=re.S)
            (ROOT / dst).write_text(pv, encoding="utf-8")
            f.write_text(public_fix(rest, lang, pre), encoding="utf-8")
            print("moved monthly section:", src, "->", dst, len(sec))
    n = 0
    files = [p for p in ROOT.rglob("*.html") if ".git" not in p.parts and "node_modules" not in p.parts and not p.name.startswith("monthly-report")]
    for p in files:
        if p.parts[len(ROOT.parts)] == "s":
            continue
        s = p.read_text(encoding="utf-8")
        if "<!--admin-locked-->" in s:
            continue
        t = link_fix(s)
        if t != s:
            p.write_text(t, encoding="utf-8"); n += 1
    # plants page (private store) links to reports
    pp = ROOT / "netlify/functions/docs/plants-pages.json"
    if pp.exists():
        d = json.load(open(pp, encoding="utf-8"))
        for k in ("en", "th"):
            if isinstance(d.get(k), str):
                d[k] = link_fix(d[k])
        json.dump(d, open(pp, "w", encoding="utf-8"), ensure_ascii=False)
    # share stubs for monthly notes
    gone = [p for p in ROOT.glob("s/*/technical-notes/monthly-*.html")]
    for p in gone:
        p.unlink()
    # site search
    for l in ("en", "th", "zh"):
        sp = ROOT / f"data/search-{l}.json"
        if sp.exists():
            d = json.load(open(sp, encoding="utf-8"))
            d["items"] = [i for i in d["items"] if not re.search(r"#(monthly-|plant-|topic-monthly)|monthly-report|Monthly-Report", i.get("u", ""))]
            json.dump(d, open(sp, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print("pages relinked:", n, "| share stubs removed:", len(gone))


if __name__ == "__main__":
    lock()
