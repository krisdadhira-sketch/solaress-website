# -*- coding: utf-8 -*-
"""Free System Check pages: "Example report" section (EN /system-check.html, TH /th/system-check.html), Nov 2026.
A real check (6.48 kWp hybrid + 16 kWh battery, eastern Bangkok) with the customer's name and address removed.
PDFs: downloads/Solar-ESS-Free-System-Check-Example-Report[_TH]_Rev03_WM_20261111.pdf; previews images/system-check-example[-th].jpg.
Inserted before the request form (#check) between <!--scex--> markers. Idempotent. Run: python3 tools/system_check_example.py"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_PDF = "/downloads/Solar-ESS-Free-System-Check-Example-Report_Rev03_WM_20261111.pdf"
TH_PDF = "/downloads/Solar-ESS-Free-System-Check-Example-Report-TH_Rev03_WM_20261111.pdf"
T = {
    "en": dict(path=ROOT / "system-check.html", img="/images/system-check-example.jpg", pdf=EN_PDF, alt_pdf=TH_PDF,
               eyebrow="Example", h2="What you get: a real report",
               lead="This is the report we sent after a free check of a 6.48 kWp hybrid system with a 16 kWh battery in eastern Bangkok (customer details removed). The panels were fine; the battery reading was not, and the home was buying power from the grid before dawn while the battery still had energy.",
               pts=["Production checked against what the roof should give: ≈3.7 kWh/kWp/day, normal for Bangkok",
                    "Battery reading drops to 0% overnight at 49.8 V: about 15–20% of the battery unused",
                    "This year against last year, month by month, to separate weather from real faults",
                    "Clear actions: BMS and capacity settings, whether more panels fit the inverter, when to run big loads"],
               btn="Open the example report (PDF)", alt="ภาษาไทย", cta="Start my free check ↓"),
    "th": dict(path=ROOT / "th" / "system-check.html", img="/images/system-check-example-th.jpg", pdf=TH_PDF, alt_pdf=EN_PDF,
               eyebrow="ตัวอย่าง", h2="สิ่งที่คุณจะได้รับ: รายงานจริง",
               lead="นี่คือรายงานที่เราส่งให้ลูกค้าหลังตรวจระบบฟรี ระบบไฮบริด 6.48 kWp พร้อมแบตเตอรี่ 16 kWh ในกรุงเทพฯ ฝั่งตะวันออก (ปิดข้อมูลลูกค้าแล้ว) แผงโซลาร์ทำงานปกติ แต่ค่าแบตเตอรี่ผิดพลาด ทำให้บ้านซื้อไฟจากการไฟฟ้าช่วงก่อนเช้า ทั้งที่แบตเตอรี่ยังมีพลังงานเหลือ",
               pts=["เทียบการผลิตไฟกับที่หลังคาควรผลิตได้: ≈3.7 kWh/kWp/วัน ปกติสำหรับกรุงเทพฯ",
                    "ค่าแบตเตอรี่ลดเป็น 0% กลางดึกทั้งที่แรงดันยัง 49.8 V: ใช้แบตเตอรี่ไม่ได้ราว 15–20%",
                    "เทียบปีนี้กับปีที่แล้วรายเดือน เพื่อแยกผลจากสภาพอากาศกับความผิดปกติจริง",
                    "ข้อแนะนำที่ทำได้ทันที: ตั้งค่า BMS และความจุ เพิ่มแผงได้หรือไม่ ควรใช้เครื่องใช้ไฟฟ้ากำลังสูงช่วงใด"],
               btn="เปิดรายงานตัวอย่าง (PDF)", alt="English", cta="ขอตรวจระบบฟรี ↓"),
}
CSS = """<style id="scex-css">
.scex{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,340px);gap:32px;align-items:start;margin-top:22px}
.scex ul{margin:14px 0 18px;padding-left:20px;line-height:1.6}.scex li{margin:5px 0}
.scex a.thumb{display:block;border:1.5px solid var(--line);box-shadow:0 8px 24px rgba(10,18,48,.12);background:#fff}
.scex a.thumb img{display:block;width:100%;height:auto}
.scex .acts{display:flex;flex-wrap:wrap;gap:10px;align-items:center}
@media(max-width:760px){.scex{grid-template-columns:1fr}.scex a.thumb{max-width:340px}}
</style>"""

for lang, t in T.items():
    s = t["path"].read_text(encoding="utf-8")
    s = re.sub(r"<!--scex-->.*?<!--/scex-->\n?", "", s, flags=re.S)
    lis = "".join(f"<li>{p}</li>" for p in t["pts"])
    sec = (f'<!--scex--><section class="band" id="example" style="padding-block:64px"><div class="wrap"><p class="eyebrow">{t["eyebrow"]}</p>'
           f'<h2>{t["h2"]}</h2><div class="scex"><div><p class="lede">{t["lead"]}</p><ul>{lis}</ul>'
           f'<div class="acts"><a class="btn" href="{t["pdf"]}" target="_blank" rel="noopener">{t["btn"]}</a>'
           f'<a href="{t["alt_pdf"]}" target="_blank" rel="noopener">{t["alt"]} (PDF)</a> · <a href="#check">{t["cta"]}</a></div></div>'
           f'<a class="thumb" href="{t["pdf"]}" target="_blank" rel="noopener"><img src="{t["img"]}" alt="{t["btn"]}" width="744" height="1052" loading="lazy"></a>'
           f'</div></div></section><!--/scex-->\n')
    i = s.index('<section class="band light" id="check"')
    s = s[:i] + sec + s[i:]
    if 'id="scex-css"' not in s:
        s = s.replace("</head>", CSS + "\n</head>", 1)
    t["path"].write_text(s, encoding="utf-8")
    print("updated", t["path"].relative_to(ROOT))
