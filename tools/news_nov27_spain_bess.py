# -*- coding: utf-8 -*-
"""News article (27 Nov 2026): Spain could reach 6-10 GW of batteries by 2030, but bankability is the challenge
(pv magazine roundtable at Genera 2026, Madrid, 25 Nov). Bullet summary, newest article on /news.html and /th/news.html
(id spain-batteries-10gw-bankability). Kris asked for it to go live with the other articles at the nightly publish.
Idempotent. Run: python3 tools/news_nov27_spain_bess.py, then tools/news_topics.py, tools/build_share.py,
tools/site_search.py, tools/news_menu.py"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ID = "spain-batteries-10gw-bankability"
SEP = 'style="max-width:760px;margin-top:64px;padding-top:48px;border-top:1.5px solid var(--navy)"'
SRCS = [("pv magazine", "https://www.pv-magazine.com/2026/11/26/spain-could-reach-10-gw-of-batteries-by-2030-but-bankability-remains-the-major-challenge/"),
        ("ESS News", "https://www.ess-news.com/2026/11/26/spain-could-reach-10-gw-of-batteries-by-2030-but-bankability-remains-the-major-challenge/")]
T = {
 "en": dict(eyebrow="27 November 2026 · Global Adoption",
  h2="Spain could reach 10 GW of batteries by 2030, but getting them financed is the big challenge",
  lede="At a pv magazine roundtable at the Genera 2026 fair in Madrid (25 November), Spain's storage association AEPIBAL, a lender, a battery maker and Wood Mackenzie discussed how to make battery projects bankable.",
  pts=[("How much", "6 to 10 GW of batteries by the end of 2030 (AEPIBAL: 6–8 GW; Wood Mackenzie: 10 GW, just under 40 GWh), and at least 30 GW by 2050."),
       ("Coming fast", "More than 10 GWh of battery equipment could arrive in Spain in 2027 alone; connection to the grid takes another 6–8 months after delivery."),
       ("Mostly with solar", "Most projects are hybrids added to solar farms; standalone batteries are only about 20% of the pipeline, and 4 hours is the usual size. Adding a battery is called the “technical rescue” for solar plants that earn too little at midday."),
       ("Where the money comes from", "Today about 60% from grid balancing services and 40% from arbitrage (charging when power is cheap, selling when it is dear). Over time arbitrage could reach about 80%, with price spreads of at least €70/MWh expected for 10 years."),
       ("Capacity market", "Spain's planned capacity payments may bring only 10–15% of battery revenue, much less than in Italy, so banks must accept more market risk."),
       ("Why banks hesitate", "No operating track record yet, real performance up to 15% off the business plan in some projects, interest rates above 3%, permits taking up to 48 months, and warranties and service contracts not yet standardised."),
       ("Longer life, lower cost", "Battery life rising from about 8,000 to 15,000 cycles could roughly halve the cost of each stored kWh."),
       ("Quality only", "Panelists said the market “leaves no room” for anything but Tier 1 equipment and suppliers – for safety, financing and public acceptance."),
       ("What it means in Thailand", "The same logic applies on a smaller scale: a battery adds most value next to solar, it pays back through daily use (charge from the sun, use at night), and quality equipment with a solid warranty and service matters more than the lowest price. Choose a hybrid inverter now so a battery can be added later.")],
  cta=("/#consult", "Talk to us about adding a battery"), src="Sources:", tail="Summary by Solar ESS Working Group."),
 "th": dict(eyebrow="27 พฤศจิกายน 2569 · การติดตั้งโซลาร์ทั่วโลก",
  h2="สเปนอาจมีแบตเตอรี่ 10 GW ภายในปี 2030 แต่การหาเงินกู้คือความท้าทายใหญ่",
  lede="ในวงเสวนาของ pv magazine ที่งาน Genera 2026 กรุงมาดริด (25 พ.ย.) สมาคมกักเก็บพลังงานสเปน (AEPIBAL) สถาบันการเงิน ผู้ผลิตแบตเตอรี่ และ Wood Mackenzie หารือกันว่าจะทำให้โครงการแบตเตอรี่ได้รับเงินกู้ได้อย่างไร",
  pts=[("ปริมาณ", "แบตเตอรี่ 6–10 GW ภายในสิ้นปี 2030 (AEPIBAL: 6–8 GW; Wood Mackenzie: 10 GW หรือเกือบ 40 GWh) และอย่างน้อย 30 GW ภายในปี 2050"),
       ("มาเร็ว", "อุปกรณ์แบตเตอรี่มากกว่า 10 GWh อาจเข้าสเปนในปี 2027 ปีเดียว และหลังส่งของยังต้องใช้เวลาอีก 6–8 เดือนกว่าจะเชื่อมต่อระบบไฟฟ้า"),
       ("ส่วนใหญ่คู่กับโซลาร์", "โครงการส่วนใหญ่เป็นแบบไฮบริดติดตั้งเพิ่มในโซลาร์ฟาร์ม แบตเตอรี่แบบแยกเดี่ยวมีเพียงประมาณ 20% ส่วนใหญ่ขนาด 4 ชั่วโมง การเพิ่มแบตเตอรี่ถูกเรียกว่า “การกู้ชีพทางเทคนิค” ของโซลาร์ฟาร์มที่ขายไฟตอนกลางวันได้ราคาต่ำ"),
       ("รายได้มาจากไหน", "ปัจจุบันประมาณ 60% มาจากบริการรักษาสมดุลระบบไฟฟ้า และ 40% จากการซื้อถูกขายแพง (ชาร์จตอนไฟถูก ขายตอนไฟแพง) ในระยะยาวส่วนหลังอาจเพิ่มเป็นประมาณ 80% โดยคาดว่าส่วนต่างราคาจะไม่ต่ำกว่า 70 ยูโร/MWh ไปอีก 10 ปี"),
       ("ตลาดกำลังการผลิต", "เงินค่าความพร้อมจ่ายที่สเปนกำลังจะมีอาจเป็นเพียง 10–15% ของรายได้แบตเตอรี่ น้อยกว่าอิตาลีมาก ธนาคารจึงต้องรับความเสี่ยงด้านตลาดมากขึ้น"),
       ("ทำไมธนาคารยังลังเล", "ยังไม่มีประวัติการทำงานจริง บางโครงการผลจริงต่างจากแผนธุรกิจถึง 15% ดอกเบี้ยสูงกว่า 3% ใบอนุญาตใช้เวลาถึง 48 เดือน และเงื่อนไขการรับประกันและสัญญาบริการยังไม่เป็นมาตรฐาน"),
       ("อายุยาวขึ้น ต้นทุนต่ำลง", "อายุแบตเตอรี่ที่เพิ่มจากประมาณ 8,000 เป็น 15,000 รอบ อาจทำให้ต้นทุนต่อหน่วยไฟที่เก็บลดลงราวครึ่งหนึ่ง"),
       ("คุณภาพเท่านั้น", "ผู้ร่วมเสวนาระบุว่าตลาด “ไม่มีที่ว่าง” สำหรับอุปกรณ์และผู้จำหน่ายที่ไม่ใช่ Tier 1 ด้วยเหตุผลด้านความปลอดภัย การขอสินเชื่อ และการยอมรับของสังคม"),
       ("ความหมายต่อประเทศไทย", "หลักการเดียวกันใช้ได้ในระดับบ้านและธุรกิจ: แบตเตอรี่คุ้มค่าที่สุดเมื่อใช้คู่กับโซลาร์ คืนทุนจากการใช้งานทุกวัน (ชาร์จจากแดด ใช้ตอนกลางคืน) และอุปกรณ์คุณภาพพร้อมการรับประกันและบริการที่ดีสำคัญกว่าราคาถูกที่สุด ควรเลือกอินเวอร์เตอร์ไฮบริดตั้งแต่วันนี้เพื่อเพิ่มแบตเตอรี่ได้ภายหลัง")],
  cta=("/th/#consult", "ปรึกษาเรื่องแบตเตอรี่"), src="ที่มา:", tail="สรุปโดย โซลาร์ เอสส์"),
}


def article(t):
    lis = "".join(f'<li style="margin-bottom:10px"><b>{a}:</b> {b}</li>' for a, b in t["pts"])
    srcs = " · ".join(f'{n} <a href="{u}" rel="noopener">↗</a>' for n, u in SRCS)
    return (f'<article id="{ID}" data-topics="adoption innovation" style="max-width:760px">\n'
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
