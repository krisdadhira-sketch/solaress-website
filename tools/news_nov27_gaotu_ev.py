# -*- coding: utf-8 -*-
"""News article (27 Nov 2026): Gaotu GT-EV16-PB-FD foldable roof-mounted off-grid solar EV charger (pv magazine,
24 Nov). Bullet summary, newest article on /news.html and /th/news.html (id gaotu-foldable-solar-ev-charger), published
with the other articles at the nightly publish. Idempotent. Run after tools/news_nov27_spain_bess.py, then
tools/news_topics.py, tools/build_share.py, tools/site_search.py, tools/news_menu.py"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ID = "gaotu-foldable-solar-ev-charger"
SEP = 'style="max-width:760px;margin-top:64px;padding-top:48px;border-top:1.5px solid var(--navy)"'
SRCS = [("pv magazine", "https://www.pv-magazine.com/2026/11/24/gaotu-unveils-foldable-off-grid-solar-ev-charger/"),
        ("pv magazine Australia", "https://www.pv-magazine-australia.com/2026/11/24/gaotu-unveils-foldable-off-grid-solar-ev-charger/")]
T = {
 "en": dict(eyebrow="27 November 2026 · Innovation",
  h2="Gaotu unveils a foldable solar EV charger that rides on the car roof",
  lede="Chinese maker Gaotu Innovation has launched the GT-EV16-PB-FD, an off-grid charger for electric cars aimed at drivers in Australia's rural and outback areas, where public chargers are far apart.",
  pts=[("What it is", "A roof-mounted box that unfolds into a 1,600 W solar array, with a built-in 2.5 kWh LiFePO4 battery that smooths the solar power and feeds regulated AC power to the car's charging inlet."),
       ("Claimed range", "Up to 80 km of driving a day from sunlight alone, with no grid."),
       ("Electronics", "Two independent MPPT trackers (800 W each, up to 99.9% efficient), 25% efficient solar cells, and a UPS function that switches over within 10 ms if mains power drops."),
       ("Built for the road", "IP68 solar enclosure, aerodynamic shape rated for winds up to 160 km/h, works from −20 °C to +55 °C, app control by Bluetooth and Wi-Fi."),
       ("Warranty", "Five years on workmanship, two years on power output; about 1% degradation in year one, then at most 0.4% a year."),
       ("Not stated", "Charging power in kW, plug type, weight, price and launch date. It is sold through local distributors, with OEM/ODM versions offered."),
       ("Our reality check", "1.6 kW of panels gives roughly 5–7 kWh on a good sunny day in Thailand, which is about 30–45 km for a typical EV – useful for camping or remote trips, but well short of daily commuting."),
       ("What it means in Thailand", "For everyday charging, rooftop solar at home or at work with a proper EV charger circuit gives many times more energy for the money. Ask us about an EV charger circuit and a free inspection.")],
  cta=("/ev.html", "EV charger circuit – free inspection"), src="Sources:", tail="Summary by Solar ESS Working Group."),
 "th": dict(eyebrow="27 พฤศจิกายน 2569 · นวัตกรรม",
  h2="Gaotu เปิดตัวเครื่องชาร์จรถ EV พลังแสงอาทิตย์แบบพับได้ ติดบนหลังคารถ",
  lede="Gaotu Innovation ผู้ผลิตจากจีน เปิดตัว GT-EV16-PB-FD เครื่องชาร์จรถยนต์ไฟฟ้าแบบไม่ใช้ไฟการไฟฟ้า สำหรับผู้ขับขี่ในพื้นที่ชนบทและเขตห่างไกลของออสเตรเลีย ซึ่งสถานีชาร์จอยู่ห่างกันมาก",
  pts=[("คืออะไร", "กล่องติดบนหลังคารถที่กางออกเป็นแผงโซลาร์ 1,600 W พร้อมแบตเตอรี่ LiFePO4 2.5 kWh ในตัว ช่วยปรับไฟจากแผงให้นิ่งและจ่ายไฟ AC เข้าช่องชาร์จของรถ"),
       ("ระยะทางที่อ้าง", "ขับได้สูงสุด 80 กม. ต่อวันจากแสงแดดอย่างเดียว ไม่ต้องใช้ไฟการไฟฟ้า"),
       ("อุปกรณ์ภายใน", "MPPT อิสระ 2 ชุด (ชุดละ 800 W ประสิทธิภาพสูงสุด 99.9%) เซลล์แสงอาทิตย์ประสิทธิภาพ 25% และฟังก์ชัน UPS สลับไฟภายใน 10 มิลลิวินาทีเมื่อไฟการไฟฟ้าดับ"),
       ("ออกแบบมาเพื่อการเดินทาง", "กล่องแผงกันน้ำกันฝุ่น IP68 รูปทรงลู่ลม ทนลมได้ถึง 160 กม./ชม. ทำงานที่ −20 °C ถึง +55 °C ควบคุมผ่านแอปด้วย Bluetooth และ Wi-Fi"),
       ("การรับประกัน", "งานประกอบ 5 ปี กำลังผลิต 2 ปี กำลังลดลงประมาณ 1% ในปีแรก จากนั้นไม่เกิน 0.4% ต่อปี"),
       ("ข้อมูลที่ยังไม่เปิดเผย", "กำลังชาร์จ (kW) ชนิดหัวชาร์จ น้ำหนัก ราคา และวันวางจำหน่าย ขายผ่านตัวแทนจำหน่ายในพื้นที่ และรับผลิตแบบ OEM/ODM"),
       ("มุมมองของเรา", "แผง 1.6 kW ในวันแดดดีในประเทศไทยผลิตไฟได้ประมาณ 5–7 หน่วย หรือราว 30–45 กม. สำหรับรถ EV ทั่วไป เหมาะกับการเดินทางไกลหรือแคมปิ้ง แต่ไม่พอสำหรับการใช้รถทุกวัน"),
       ("ความหมายต่อประเทศไทย", "สำหรับการชาร์จประจำวัน โซลาร์บนหลังคาบ้านหรือที่ทำงาน คู่กับวงจรชาร์จ EV ที่ติดตั้งถูกต้อง ให้พลังงานต่อเงินที่จ่ายมากกว่าหลายเท่า สอบถามเรื่องวงจรชาร์จ EV และนัดตรวจหน้างานฟรีได้")],
  cta=("/th/ev.html", "วงจรชาร์จ EV – ตรวจหน้างานฟรี"), src="ที่มา:", tail="สรุปโดย โซลาร์ เอสส์"),
}


def article(t):
    lis = "".join(f'<li style="margin-bottom:10px"><b>{a}:</b> {b}</li>' for a, b in t["pts"])
    srcs = " · ".join(f'{n} <a href="{u}" rel="noopener">↗</a>' for n, u in SRCS)
    return (f'<article id="{ID}" data-topics="innovation" style="max-width:760px">\n'
            f'<p class="eyebrow">{t["eyebrow"]}</p><h2 style="font-size:clamp(26px,3.6vw,40px)">{t["h2"]}</h2>\n'
            f'<p class="lede" style="margin-top:16px;opacity:1">{t["lede"]}</p>\n'
            f'<ul style="margin-top:22px;padding-left:20px">{lis}</ul>\n'
            f'<p style="margin-top:22px;display:flex;gap:10px;flex-wrap:wrap"><a class="btn" href="{t["cta"][0]}">{t["cta"][1]}</a></p>\n'
            f'<p style="margin-top:28px;font-size:14px;color:var(--mute)">{t["src"]} {srcs}. {t["tail"]}</p>\n</article>\n')


for lang, path in (("en", "news.html"), ("th", "th/news.html")):
    p = ROOT / path
    s = p.read_text(encoding="utf-8")
    s = re.sub(rf'<article id="{ID}".*?</article>\n?', "", s, flags=re.S)
    m = re.search(r'<article id="([^"]+)"( data-topics="[^"]*")? style="[^"]*">', s)
    first = re.sub(r'style="[^"]*"', SEP, m.group(0))
    s = s[:m.start()] + article(T[lang]) + first + s[m.end():]
    p.write_text(s, encoding="utf-8")
    print("article on", path, "before", m.group(1))
