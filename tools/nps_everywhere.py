# -*- coding: utf-8 -*-
"""Reader NPS band ("How likely are you to recommend Solar ESS…?") above the footer of almost every public page.
The home pages are handled by tools/home_search_nps.py (which also adds the blinking score in the hero).
Skipped: admin pages, noindex pages, share redirects (s/), tests in progress, forms that are one step of a flow.
Idempotent (markup between <!--nps--> markers; CSS <style id="nps-css">).
Run from the repo root after adding pages:  python3 tools/nps_everywhere.py"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from home_search_nps import T, NCSS, nps_html  # noqa: E402

SKIP = {"index.html", "th/index.html", "zh/index.html",            # home pages: home_search_nps.py
        "404.html", "thanks.html", "th/thanks.html", "zh/thanks.html", "googlef2e2bf45e07052f3.html",
        "installer-test.html", "th/installer-test.html",            # timed test
        "vocabulary.html", "certificate.html", "join.html", "th/join.html",
        "feedback.html", "th/feedback.html", "job-report.html", "th/job-report.html"}


def lang_of(rel):
    return "th" if rel.startswith("th/") else "zh" if rel.startswith("zh/") else "en"


def main():
    done = 0
    for p in sorted(ROOT.rglob("*.html")):
        rel = p.relative_to(ROOT).as_posix()
        if rel.split("/")[0] in {"s", "tools", "netlify", "node_modules", "data", "members", ".git"} or rel in SKIP or "admin" in rel:
            continue
        s = p.read_text(encoding="utf-8")
        if re.search(r'<meta[^>]+name="robots"[^>]+noindex', s) or "<footer" not in s:
            continue
        lg = lang_of(rel)
        s = re.sub(r"<!--nps-->.*?<!--/nps-->\n?", "", s, flags=re.S)
        s = re.sub(r'<style id="nps-css">.*?</style>', "", s, flags=re.S)
        s = s.replace("</head>", NCSS + "</head>", 1)
        i = s.rfind("<footer")
        s = s[:i] + nps_html(lg, T[lg]) + "\n" + s[i:]
        p.write_text(s, encoding="utf-8")
        done += 1
    print("NPS band on", done, "pages")


if __name__ == "__main__":
    main()
