# -*- coding: utf-8 -*-
"""16 Nov 2026: raise every job pay amount on the Jobs pages by 25% (rounded to the nearest 50 THB).
Touches only pay: the ฿ amounts in job cards, the day rates in the pay guide (technician, helper, crew,
minimum per visit) and the Roi Et helper day rate. Platform fees (3-5%, minimum 300 THB) are not changed.
Run once:  python3 tools/job_pay_raise_nov16.py"""
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
F = 1.25
def up(n): return int(round(n * F / 50.0) * 50)
def fmt(n): return f"{n:,}"
def baht(m):
    return "฿" + "–".join(fmt(up(int(x.replace(",", "")))) for x in m.group(1).split("–"))
for path in ("job.html", "th/job.html"):
    p = ROOT / path; s = p.read_text(encoding="utf-8"); before = s
    s = re.sub(r"฿([0-9][0-9,]*(?:–[0-9][0-9,]*)?)", baht, s)
    if path == "job.html":
        s = s.replace("1,000 THB a day for a certified technician and 600 THB a day for a helper</b> (1,600 THB a day for a crew of two)",
                      "1,250 THB a day for a certified technician and 750 THB a day for a helper</b> (2,000 THB a day for a crew of two)")
        s = s.replace("Minimum 1,000 THB per visit", "Minimum 1,250 THB per visit")
        s = s.replace("Fixed day rate: 600 THB per day.", "Fixed day rate: 750 THB per day.")
        s = s.replace("(600 THB/day)", "(750 THB/day)").replace("%28600%20THB/day%29", "%28750%20THB/day%29")
    else:
        s = s.replace("วันละ 1,000 บาท", "วันละ 1,250 บาท").replace("วันละ 600 บาท", "วันละ 750 บาท").replace("วันละ 1,600 บาท", "วันละ 2,000 บาท")
        s = s.replace("1,000 บาท รวมค่าเดินทางในพื้น", "1,250 บาท รวมค่าเดินทางในพื้น")
        s = s.replace("600 บาท/วัน", "750 บาท/วัน")
    p.write_text(s, encoding="utf-8")
    print(path, "changed" if s != before else "unchanged")
