# -*- coding: utf-8 -*-
"""Blinking "NEW" badge on the top-menu News link of every page.

1. Reads the newest article date on news.html, th/news.html and zh/news.html (first article's eyebrow)
   and writes data/news-latest.json  {"en": "YYYY-MM-DD", "th": ..., "zh": ..., "days": 7}.
2. Adds <script src="/js/news-menu.js"> to every public page (idempotent, between <!--newsmenu--> markers).
js/news-menu.js shows the badge on the News menu link while the newest article is at most `days` old.
Run after publishing news:  python3 tools/news_menu.py"""
import json, re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN = "january february march april may june july august september october november december".split()
TH = ["มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"]
SKIP = {"admin.html", "members-admin.html", "vocab-admin.html", "feedback-admin.html", "itest-admin.html", "googlef2e2bf45e07052f3.html"}
TAG = '<!--newsmenu--><script src="/js/news-menu.js?v=1" defer></script><!--/newsmenu-->'


def parse(t):
    t = t.strip()
    m = re.match(r"(\d{4})年(\d{1,2})月(\d{1,2})日", t)
    if m:
        return date(int(m[1]), int(m[2]), int(m[3]))
    m = re.match(r"(\d{1,2})\s+(\S+)\s+(\d{4})", t)
    if not m:
        return None
    mo = m[2].lower()
    mi = EN.index(mo) if mo in EN else (TH.index(m[2]) if m[2] in TH else -1)
    if mi < 0:
        return None
    y = int(m[3]); y = y - 543 if y > 2400 else y
    return date(y, mi + 1, int(m[1]))


latest = {}
for lang, path in (("en", "news.html"), ("th", "th/news.html"), ("zh", "zh/news.html")):
    s = (ROOT / path).read_text(encoding="utf-8")
    ds = [d for d in (parse(x) for x in re.findall(r'<article id="[^"]+"[^>]*>\s*<p class="eyebrow">([^<]+)', s)) if d]
    latest[lang] = max(ds).isoformat() if ds else None
latest["days"] = 7
(ROOT / "data/news-latest.json").write_text(json.dumps(latest), encoding="utf-8")
print("news-latest:", latest)

n = 0
for p in ROOT.rglob("*.html"):
    rel = p.relative_to(ROOT).as_posix()
    if rel.startswith(("s/", "tools/", "node_modules/", "netlify/")) or p.name in SKIP or "admin" in p.name:
        continue
    s = p.read_text(encoding="utf-8")
    if "</body>" not in s or 'class="dd"' not in s:
        continue
    s2 = re.sub(r"<!--newsmenu-->.*?<!--/newsmenu-->", "", s, flags=re.S)
    s2 = s2.replace("</body>", TAG + "\n</body>", 1)
    if s2 != s:
        p.write_text(s2, encoding="utf-8"); n += 1
print("pages with news-menu script:", n)
