# -*- coding: utf-8 -*-
"""News 21 Nov 2026: upcoming project summary — 15 kW hybrid, 16.90 kWp, 32 kWh battery near Mae Hong Son town.
Summarised from the signed contract (Rev16). Public version only: no price, no payment terms, no names,
no ID numbers, approximate location only. The contract PDF itself is NOT published.
Idempotent. Run: python3 tools/news_nov21_mhs.py, then tools/news_topics.py, tools/build_share.py,
tools/site_search.py, tools/news_menu.py"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AID = "upcoming-mae-hong-son-15kw-hybrid-32kwh"
SEP = 'style="max-width:760px;margin-top:64px;padding-top:48px;border-top:1.5px solid var(--navy)"'

T = {
    "en": dict(
        eb="21 November 2026 · Upcoming project",
        h2="Upcoming: 15 kW three-phase hybrid with 32 kWh of storage near Mae Hong Son",
        lede="Contract signed for a turnkey solar + battery system on the roof of a Buddhist meditation centre just outside Mae Hong Son town. Work starts soon.",
        pts=[
            ("Equipment", "Solis S6-EH3P15K02-NV-YD-L 15 kW three-phase hybrid inverter, 26 × LONGi Hi-MO X10 Guardian Anti-Glare 650 W panels (16.90 kWp) and 2 × Solis IntelliHome 16 kWh LiFePO4 batteries (32 kWh)."),
            ("Roof", "Panels go on the southwest-facing side of the roof, using anti-glare glass."),
            ("Backup", "Daytime solar is stored for evening use, and the batteries keep power on during outages."),
            ("Timeline", "About 45 working days from start to handover (rain days not counted); the PEA grid-connection approval runs alongside."),
            ("Warranty", "Panels 15 years product / 30 years output, inverter and batteries 10 years each, installation workmanship 5 years."),
            ("Care", "Panel cleaning and a full safety check every year for 6 years."),
            ("Insured", "Covered from the first day on site by our Contractor All Risk (CAR) insurance."),
        ],
        foot="Customer details and prices are not published. Solar ESS Working Group.",
        cta=("Talk to us about solar + battery", "/#consult", "Ongoing projects", "/ongoing.html"),
    ),
    "th": dict(
        eb="21 พฤศจิกายน 2569 · โครงการที่กำลังจะเริ่ม",
        h2="เร็ว ๆ นี้: ไฮบริด 15 kW 3 เฟส พร้อมแบตเตอรี่ 32 kWh ใกล้ตัวเมืองแม่ฮ่องสอน",
        lede="ลงนามสัญญาแล้ว ติดตั้งระบบโซลาร์เซลล์พร้อมแบตเตอรี่แบบเหมารวม (Turnkey) บนหลังคาสถานปฏิบัติธรรมแห่งหนึ่งใกล้ตัวเมืองแม่ฮ่องสอน เตรียมเริ่มงานเร็ว ๆ นี้",
        pts=[
            ("อุปกรณ์", "อินเวอร์เตอร์ไฮบริด Solis S6-EH3P15K02-NV-YD-L 15 kW 3 เฟส แผง LONGi Hi-MO X10 Guardian Anti-Glare 650 W × 26 แผง (16.90 kWp) และแบตเตอรี่ Solis IntelliHome 16 kWh LiFePO4 × 2 ชุด (32 kWh)"),
            ("หลังคา", "ติดตั้งแผงบนหลังคาฝั่งทิศตะวันตกเฉียงใต้ ใช้แผงกระจกกันแสงสะท้อน"),
            ("ไฟสำรอง", "เก็บไฟจากแดดกลางวันไว้ใช้ช่วงค่ำ และสำรองไฟเมื่อไฟดับ"),
            ("ระยะเวลา", "ประมาณ 45 วันทำการตั้งแต่เริ่มงานจนส่งมอบ (ไม่นับวันฝนตก) ส่วนการขออนุญาตเชื่อมต่อกับ กฟภ. ดำเนินการคู่กัน"),
            ("การรับประกัน", "แผงรับประกันสินค้า 15 ปี กำลังผลิต 30 ปี อินเวอร์เตอร์และแบตเตอรี่ 10 ปี งานติดตั้ง 5 ปี"),
            ("ดูแลหลังการขาย", "ล้างแผงและตรวจความปลอดภัยของระบบปีละครั้ง ตลอด 6 ปี"),
            ("ประกันภัย", "คุ้มครองด้วยประกันภัยความเสี่ยงทุกชนิดของผู้รับเหมา (CAR) ตั้งแต่วันแรกที่เข้าหน้างาน"),
        ],
        foot="ไม่เผยแพร่ข้อมูลลูกค้าและราคา Solar ESS Working Group.",
        cta=("ปรึกษาเรื่องโซลาร์ + แบตเตอรี่", "/th/#consult", "โครงการที่กำลังดำเนินการ", "/th/ongoing.html"),
    ),
}


def article(lang):
    t = T[lang]
    lis = "".join(f'<li style="margin-bottom:10px"><b>{a}:</b> {b}</li>' for a, b in t["pts"])
    c = t["cta"]
    return (f'<article id="{AID}" style="max-width:760px">\n'
            f'<p class="eyebrow">{t["eb"]}</p><h2 style="font-size:clamp(26px,3.6vw,40px)">{t["h2"]}</h2>\n'
            f'<p class="lede" style="margin-top:16px;opacity:1">{t["lede"]}</p>\n'
            f'<ul style="margin-top:22px;padding-left:20px">{lis}</ul>\n'
            f'<p style="margin-top:22px;display:flex;gap:10px;flex-wrap:wrap"><a class="btn" href="{c[1]}">{c[0]}</a><a class="btn ghost" href="{c[3]}">{c[2]}</a></p>\n'
            f'<p style="margin-top:20px;font-size:14px;color:var(--mute)">{t["foot"]}</p>\n</article>\n')


for lang, path in (("en", "news.html"), ("th", "th/news.html")):
    p = ROOT / path
    s = p.read_text(encoding="utf-8")
    s = re.sub(rf'<article id="{AID}".*?</article>\n?', "", s, flags=re.S)
    m = re.search(r'<article id="([^"]+)"( data-topics="[^"]*")? style="[^"]*">', s)
    old_first = re.sub(r'style="[^"]*"', SEP, m.group(0))
    s = s[:m.start()] + article(lang) + old_first + s[m.end():]
    p.write_text(s, encoding="utf-8")
    print(path, "inserted before", m.group(1))
