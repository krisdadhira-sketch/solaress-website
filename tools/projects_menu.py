# -*- coding: utf-8 -*-
"""Projects dropdown on every page (EN/TH/ZH), Nov 2026:
Solar Package (Quotation indented under it), EV Charger, Preventive Maintenance, Consultation (FAQ indented), Solar ESS Care.
Idempotent: rewrites the list inside the Projects dropdown.  Run from the repo root:  python3 tools/projects_menu.py"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IND = ' style="padding-left:30px;font-size:.92em"'
M = {
 "en": [("/package.html", "Solar Package", 0), ("/quotation.html", "Quotation", 1), ("/ev.html", "EV Charger", 0),
        ("/maintenance.html", "Preventive Maintenance", 0), ("/#consult", "Consultation", 0), ("/faq.html", "FAQ", 1), ("/care.html", "Solar ESS Care", 0)],
 "th": [("/th/package.html", "แพ็กเกจโซลาร์", 0), ("/th/quotation.html", "ใบเสนอราคา", 1), ("/th/ev.html", "ที่ชาร์จรถ EV", 0),
        ("/th/maintenance.html", "บำรุงรักษาเชิงป้องกัน", 0), ("/th/#consult", "ขอคำปรึกษา", 0), ("/th/faq.html", "คำถามที่พบบ่อย", 1), ("/th/care.html", "Solar ESS Care", 0)],
 "zh": [("/package.html", "太阳能套餐（英文）", 0), ("/zh/quotation.html", "报价单", 1), ("/ev.html", "电动车充电（英文）", 0),
        ("/maintenance.html", "预防性维护（英文）", 0), ("/zh/#consult", "预约咨询", 0), ("/zh/faq.html", "常见问题", 1), ("/zh/care.html", "Solar ESS Care", 0)],
}
DD = re.compile(r'(<a href="(?:/th/|/zh/|/)#projects">[^<]*</a><span class="ddm">)(.*?)(</span>)', re.S)
n = 0
for f in sorted(ROOT.rglob("*.html")):
    s = f.read_text(encoding="utf-8")
    m = DD.search(s)
    if not m:
        continue
    lang = "th" if "/th/#projects" in m.group(1) else "zh" if "/zh/#projects" in m.group(1) else "en"
    items = "".join(f'<a href="{u}"{IND if i else ""}>{t}</a>' for u, t, i in M[lang])
    new = s[:m.start(2)] + items + s[m.end(2):]
    if new != s:
        f.write_text(new, encoding="utf-8"); n += 1
print("updated", n, "pages")
