# -*- coding: utf-8 -*-
"""Form boxes are white with black text on every page, so typing is easy to read (also on dark sections).
Idempotent: replaces the <style id="form-ink"> block in each page's <head>.
Run from the repo root after regenerating any page:  python3 tools/form_ink.py"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = ('<style id="form-ink">'
       'form input:not([type=radio]):not([type=checkbox]):not([type=submit]):not([type=button]):not([type=hidden]):not([type=file]),'
       'form select,form textarea{background:#FFFFFF!important;color:#0A0E2E!important;-webkit-text-fill-color:#0A0E2E!important;caret-color:#2563EB}'
       'form input::placeholder,form textarea::placeholder{color:#6B7280!important;-webkit-text-fill-color:#6B7280!important;opacity:1}'
       'form select option,form select optgroup{color:#0A0E2E;background:#FFFFFF}'
       'form input:-webkit-autofill{-webkit-box-shadow:0 0 0 1000px #FFFFFF inset!important;-webkit-text-fill-color:#0A0E2E!important}'
       '</style>')
n = 0
for f in ROOT.rglob("*.html"):
    if ".git" in f.parts or "node_modules" in f.parts:
        continue
    s = f.read_text(encoding="utf-8")
    if "<form" not in s or "</head>" not in s:
        continue
    new = re.sub(r'<style id="form-ink">.*?</style>', "", s, flags=re.S).replace("</head>", CSS + "</head>", 1)
    if new != s:
        f.write_text(new, encoding="utf-8"); n += 1
print("form-ink:", n, "pages")
