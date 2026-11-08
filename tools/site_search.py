# -*- coding: utf-8 -*-
"""Site search for www.solaress.org.
Builds data/search-index.json from every public page (EN, /th/, /zh/): one entry per page, one per section or
card that has an id and a heading (news articles, job posts, technical notes, FAQ ...), and one per linked PDF.
Pages marked noindex (admin, forms with codes, members) are left out. The home pages carry the search box
(markup between <!--sitesearch--> markers, script /js/site-search.js).
Re-run after adding or editing pages:  python3 tools/site_search.py"""
import json, re
from pathlib import Path
from urllib.parse import unquote
from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = Path(__file__).resolve().parents[1]
SKIP = {"404.html", "thanks.html", "admin.html"}
HEAD = {"h1", "h2", "h3", "h4"}
WS = re.compile(r"\s+")
MAXTXT = 600


def clean(s):
    return WS.sub(" ", s or "").strip()


def pages():
    for p in sorted(ROOT.glob("*.html")) + sorted((ROOT / "th").glob("*.html")) + sorted((ROOT / "zh").glob("*.html")):
        if p.name in SKIP or p.name.startswith("google"):
            continue
        yield p


def url_of(p):
    rel = p.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def lang_of(p):
    rel = p.relative_to(ROOT).as_posix()
    return "th" if rel.startswith("th/") else "zh" if rel.startswith("zh/") else "en"


def first_heading(el):
    h = el.find(lambda t: isinstance(t, Tag) and t.name in HEAD)
    return clean(h.get_text(" ")) if h else ""


def text_of(el, skip):
    """Text of el, leaving out descendants that are their own index entries."""
    out = []
    for c in el.children:
        if isinstance(c, NavigableString):
            out.append(str(c))
        elif isinstance(c, Tag):
            if id(c) in skip:
                continue
            out.append(text_of(c, skip))
            if c.name in ("p", "li", "div", "h1", "h2", "h3", "h4", "td", "br", "section", "article"):
                out.append(" ")
    return "".join(out)


items, seen_pdf = [], set()
for p in pages():
    html = p.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "lxml")
    rob = soup.find("meta", attrs={"name": "robots"})
    if rob and "noindex" in (rob.get("content") or "").lower():
        continue
    u, lg = url_of(p), lang_of(p)
    title = clean(soup.title.get_text()) if soup.title else u
    title = re.sub(r"\s*[|·–-]\s*Solar ESS.*$", "", title) or title
    md = soup.find("meta", attrs={"name": "description"})
    desc = clean(md.get("content")) if md else ""
    for t in soup(["script", "style", "noscript", "svg", "template", "iframe", "select", "option", "button"]):
        t.decompose()
    for t in soup.select("header.nav, footer, .fab, .share, .mnav-btn, #sitesearch, #nps"):
        t.decompose()
    body = soup.body or soup
    # PDFs linked from the page (before forms are removed: some download links sit next to forms)
    for a in body.find_all("a", href=True):
        h = a["href"].split("#")[0]
        if not h.lower().endswith(".pdf") or h.startswith("http") and "solaress.org" not in h:
            continue
        h = "/" + h.split("solaress.org/")[-1].lstrip("/") if h.startswith("http") else ("/" + h.lstrip("/") if not h.startswith("/") and lg == "en" else h)
        key = (h, lg)
        if key in seen_pdf:
            continue
        seen_pdf.add(key)
        sec = a.find_parent(lambda t: isinstance(t, Tag) and t.get("id") and first_heading(t))
        name = clean(a.get_text(" ")) or unquote(h.rsplit("/", 1)[-1])
        ctx = first_heading(sec) if sec else title
        items.append({"u": h, "t": (ctx + " · " + name) if ctx and ctx != name else name, "s": unquote(h.rsplit("/", 1)[-1]).replace("_", " "), "l": lg, "k": "pdf"})
    for t in body.find_all("form"):
        t.decompose()
    cands = [el for el in body.find_all(lambda t: isinstance(t, Tag) and t.get("id") and t.name in ("section", "article", "div", "li", "details", "aside")) if first_heading(el)]
    skip = {id(c) for c in cands}
    page_txt = clean(text_of(body, skip))
    items.append({"u": u, "t": title, "s": clean((desc + " " + page_txt))[:MAXTXT], "l": lg, "k": "page"})
    for el in cands:
        txt = clean(text_of(el, skip - {id(el)}))
        if len(txt) < 25:
            continue
        hd = first_heading(el)
        items.append({"u": f"{u}#{el['id']}", "t": f"{hd} — {title}" if hd != title else hd, "s": txt[:MAXTXT], "l": lg, "k": "sec"})

old = ROOT / "data" / "search-index.json"
if old.exists():
    old.unlink()
for lg in ("en", "th", "zh"):  # one file per language: the box loads its own language first, the others only if needed
    sub = [{k: v for k, v in i.items() if k != "l"} for i in items if i["l"] == lg]
    out = ROOT / "data" / f"search-{lg}.json"
    out.write_text(json.dumps({"v": 1, "items": sub}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"search index {lg}: {len(sub)} entries, {out.stat().st_size // 1024} KB")
