# -*- coding: utf-8 -*-
"""News article (19 Nov 2026): data-centre batteries vs home batteries - how they compare and what it means in Thailand.
1. Builds the EN and TH PDFs (Solar ESS logo top-left, address top-right on every page; site colours, no pink/red accent).
2. Inserts the article as the newest on /news.html and /th/news.html (id datacentre-vs-home-batteries, topic datacenter).
Idempotent for the pages; never overwrites an existing PDF (bump REV instead).
Run: python3 tools/news_nov19_batteries.py, then tools/clean_quote_pdf.py (watermark, see WM below), tools/news_topics.py,
tools/build_share.py, tools/site_search.py, tools/news_menu.py"""
import base64, html, os, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ID = "datacentre-vs-home-batteries"
REV, DATE = "Rev01", "20261119"
RAW = {l: ROOT / f"tools/.pdf_tmp/{ID}-{l}.pdf" for l in ("en", "th")}
PDF = {"en": f"/downloads/Solar-ESS-News-Datacentre-vs-Home-Batteries_{REV}_WM_{DATE}.pdf",
       "th": f"/downloads/Solar-ESS-News-Datacentre-vs-Home-Batteries-TH_{REV}_WM_{DATE}.pdf"}
IMG = f"news-datacentre-vs-home-batteries-{DATE}.jpg"
SEP = 'style="max-width:760px;margin-top:64px;padding-top:48px;border-top:1.5px solid var(--navy)"'

SRC = [
 ("Schneider Electric – Design considerations for UPS systems in data centers (generator start 10–20 s; 1–2 / 5 / 10–15 min runtimes)", "https://blog.se.com/datacenter/2020/07/20/design-considerations-deployment-ups-systems-in-data-centers"),
 ("Schneider Electric – White Paper 229, Battery technology for data centers: VRLA vs. Li-ion", "https://www.datacenterdynamics.com/en/whitepapers/battery-technology-data-centers-vrla-vs-li-ion/"),
 ("Schneider Electric – White Paper 266, VRLA vs. Li-ion for UPS (10-year TCO 53% lower with Li-ion)", "https://go.schneider-electric.com/WW_201903_WP266-Battery-Technology-for-Single-Phase-UPS-Systems-VRLA-vs-Li-ion-A01983_EA-LP-EN.html"),
 ("Delta Power Solutions – Pros and cons of lithium-ion batteries for data centers (VRLA 3–6 years)", "https://www.deltapowersolutions.com"),
 ("pv magazine / ESS News – How competitive is BESS for data centers, really? (Volta Foundation, Sep 2026)", "https://www.ess-news.com/2026/09/10/how-competitive-is-bess-for-data-centers-really/"),
 ("PNNL-39627 – Storing Affordability: battery storage to reduce data center cost shifts (US DOE, June 2026)", "https://www.pnnl.gov/main/publications/external/technical_reports/PNNL-39627.pdf"),
 ("Introl – Backup power strategy for AI: UPS, generators and battery duration (BESS 4–8 h)", "https://introl.com/blog/backup-power-strategy-ai-ups-generator-battery-2025"),
 ("Battery-Tech Network – Why AI data centers are becoming battery storage's biggest new customer (Jul 2026)", "https://battery-tech.net/why-ai-data-centers-are-becoming-battery-storages-biggest-new-customer/"),
 ("FranklinWH – Home battery warranty basics (about 10 years, end-of-term capacity)", "https://www.franklinwh.com/blog/battery-warranty-everything-you-need-to-know-for-home-energy-storage"),
 ("LuxpowerTek – energy storage battery catalogue 2026 (LFP, 6,000 cycles, 10-year warranty, IEC 62619)", "https://luxpowertek.com/wp-content/uploads/2026/01/LuxpowerTek-Energy-Storage-Battery-Catalogue-20260109.pdf"),
]

C = {
 "en": dict(
  eyebrow="19 November 2026 · Data Center", h1="Data-centre batteries vs home batteries: same family, very different jobs",
  lede="Batteries are now one of the fastest-growing parts of data-centre power, and home batteries are the fastest-growing add-on to rooftop solar. They often use the same lithium chemistry, but they are built for completely different work.",
  kf=[("10–20 s", "for a data-centre generator to start and take the load"), ("1–15 min", "typical data-centre UPS battery runtime"),
      ("10–20 kWh", "typical home battery, for evening and night use"), ("~10 years", "home LFP warranty, about 6,000 cycles")],
  th=["", "Data centre", "Home with solar"],
  rows=[("Main job", "Keep servers running with no break: carry the load for seconds to minutes until generators start; newer site batteries also cut peaks and smooth AI load swings", "Store daytime solar for the evening and night, and back up chosen circuits in a power cut"),
        ("Size", "Hundreds of kW to many MW / MWh, in rooms or containers", "About 5–20 kWh, wall- or floor-mounted"),
        ("How long it runs", "UPS: 1–2 min (hyperscale), about 5 min (cloud), 10–15 min (banks). Site BESS: up to about 4–8 h", "A whole evening and night of normal use"),
        ("Power vs energy", "Power cells: very high current for a short time", "Energy cells: moderate current for many hours"),
        ("How often it works", "UPS: rarely, only in outages. BESS for peak shaving: every day", "Every day, one full cycle"),
        ("Chemistry", "Lithium-ion replacing lead-acid (VRLA); sodium-ion and other new types arriving", "Mostly lithium iron phosphate (LFP)"),
        ("Life", "Lead-acid 3–6 years; lithium-ion much longer", "LFP rated about 6,000 cycles, warranty about 10 years"),
        ("Safety and cooling", "Industrial air-conditioning, gas detection, fire suppression, multi-level BMS", "Sealed unit with its own BMS; safety depends on a certified product, a good location and correct installation")],
  secs=[
   ("1. What a data-centre battery does", [
    "When the grid fails, the UPS battery takes over instantly and carries the servers until the diesel generators start, usually in 10–20 seconds. Designers add margin: about 1–2 minutes in hyperscale sites, 5 minutes in cloud and colocation sites, and 10–15 minutes in banking.",
    "Lithium-ion is replacing lead-acid in UPS rooms. Lead-acid lasts about 3–6 years; lithium-ion lasts longer, is lighter and needs fewer replacements. Schneider Electric found a 10-year total cost about 53% lower with lithium-ion for single-phase UPS, despite the higher purchase price.",
    "AI is adding a second job. Large battery systems (BESS) now cut costly demand peaks, smooth sudden AI load swings and provide 'bridge power' while a site waits for its grid connection, which in busy markets can take years. A Volta Foundation report notes the battery wins where speed and daily cycling pay; where there are no demand charges, much of that advantage disappears."]),
   ("2. What a home battery does", [
    "At home the battery works every day: it charges from the panels at midday and runs the house in the evening and at night. In a power cut it keeps chosen circuits, or the whole house, running within the inverter's limit.",
    "Most home batteries are lithium iron phosphate (LFP), about 5–20 kWh, rated about 6,000 cycles with a warranty of about 10 years. A 10 kWh unit usually delivers about 3–5 kW continuously.",
    "In Thailand the money case is simple: a unit of solar you use yourself saves the full retail price of about 4–4.5 baht, while a unit sold back to PEA under net billing earns about 2.20 baht. Storing midday solar for the evening is worth about twice as much as selling it."]),
   ("3. What this means for you", [
    "Thailand's data-centre boom is adding load to the same grid that homes use, and the evening peak is where it hurts most. Every home battery that runs the house after sunset takes a little pressure off that peak.",
    "When you choose a home battery: size it to your evening and night use, not to the roof; choose LFP from the inverter's own brand or a model on its compatibility list so the BMS talks to the inverter; check the warranty's end-of-term capacity (often 60–70% after 10 years), not just the years; and insist on a certified product (IEC 62619, UN38.3) installed with proper DC protection.",
    "Solar ESS sizes batteries from your electricity bills and, where you already have solar, from your monitoring data. Ask for a free system check at www.solaress.org."]),
  ],
  src_h="Sources", end="Solar ESS Working Group", title="Data-centre vs home batteries – Solar ESS news summary",
  web=dict(lede="Data centres and homes both use lithium batteries, but for very different jobs: seconds to minutes of instant backup and peak-cutting at a data centre, a daily cycle of stored solar at home.",
   pts=[("Data centre", "The UPS battery carries the servers until generators start (usually 10–20 s); designs keep 1–15 minutes of runtime. Lithium-ion is replacing lead-acid, and large battery systems now also cut demand peaks and smooth AI load swings."),
        ("Home", "A 5–20 kWh LFP battery cycles every day, rated about 6,000 cycles with about a 10-year warranty, and backs up chosen circuits in a power cut."),
        ("In Thailand", "Solar you use yourself saves about 4–4.5 baht a unit; solar sold back under net billing earns about 2.20 baht. Storing midday solar for the evening is worth about twice as much."),
        ("Choosing one", "Size it to evening and night use, match it to the inverter, check end-of-warranty capacity, and insist on a certified product (IEC 62619, UN38.3) with proper DC protection.")],
   dl="Download the summary (PDF) ↓", other="ภาษาไทย (PDF)", srcl="Sources:", tail="Summary by Solar ESS.", alt="First page of the Solar ESS summary")),
 "th": dict(
  eyebrow="19 พฤศจิกายน 2569 · ดาต้าเซ็นเตอร์", h1="แบตเตอรี่ดาต้าเซ็นเตอร์ กับแบตเตอรี่บ้าน: ตระกูลเดียวกัน แต่ทำงานต่างกันมาก",
  lede="แบตเตอรี่กำลังเป็นส่วนที่เติบโตเร็วที่สุดส่วนหนึ่งของระบบไฟฟ้าในดาต้าเซ็นเตอร์ และแบตเตอรี่บ้านเป็นอุปกรณ์เสริมที่เติบโตเร็วที่สุดของโซลาร์บนหลังคา ทั้งสองมักใช้ลิเธียมเหมือนกัน แต่ออกแบบมาเพื่องานที่ต่างกันโดยสิ้นเชิง",
  kf=[("10–20 วินาที", "เวลาที่เครื่องปั่นไฟของดาต้าเซ็นเตอร์ติดและรับโหลด"), ("1–15 นาที", "เวลาสำรองไฟของแบตเตอรี่ UPS ในดาต้าเซ็นเตอร์"),
      ("10–20 kWh", "ขนาดแบตเตอรี่บ้านทั่วไป ใช้ช่วงเย็นและกลางคืน"), ("~10 ปี", "รับประกันแบตเตอรี่ LFP บ้าน ราว 6,000 รอบ")],
  th=["", "ดาต้าเซ็นเตอร์", "บ้านที่มีโซลาร์"],
  rows=[("หน้าที่หลัก", "ให้เซิร์ฟเวอร์ทำงานต่อเนื่องไม่สะดุด รับโหลดไม่กี่วินาทีถึงไม่กี่นาทีจนเครื่องปั่นไฟติด แบตเตอรี่รุ่นใหม่ยังช่วยตัดพีคและลดการกระชากของโหลด AI", "เก็บไฟโซลาร์กลางวันไว้ใช้ช่วงเย็นและกลางคืน และสำรองไฟวงจรที่เลือกเมื่อไฟดับ"),
        ("ขนาด", "หลายร้อย kW ถึงหลาย MW / MWh อยู่ในห้องหรือตู้คอนเทนเนอร์", "ประมาณ 5–20 kWh ติดผนังหรือวางพื้น"),
        ("สำรองได้นานเท่าไร", "UPS: 1–2 นาที (ไฮเปอร์สเกล) ราว 5 นาที (คลาวด์) 10–15 นาที (ธนาคาร) BESS ของไซต์: ได้ถึงราว 4–8 ชั่วโมง", "ตลอดช่วงเย็นและกลางคืนตามการใช้ไฟปกติ"),
        ("กำลัง กับ พลังงาน", "เซลล์กำลังสูง: จ่ายกระแสสูงมากในเวลาสั้น", "เซลล์พลังงาน: จ่ายกระแสปานกลางได้หลายชั่วโมง"),
        ("ใช้งานบ่อยแค่ไหน", "UPS: นาน ๆ ครั้ง เฉพาะตอนไฟดับ BESS ตัดพีค: ทุกวัน", "ทุกวัน วันละ 1 รอบเต็ม"),
        ("ชนิดแบตเตอรี่", "ลิเธียมไอออนกำลังแทนตะกั่วกรด (VRLA) และมีโซเดียมไอออนกับชนิดใหม่ ๆ เข้ามา", "ส่วนใหญ่เป็นลิเธียมไอรอนฟอสเฟต (LFP)"),
        ("อายุ", "ตะกั่วกรด 3–6 ปี ลิเธียมไอออนอยู่ได้นานกว่ามาก", "LFP ราว 6,000 รอบ รับประกันราว 10 ปี"),
        ("ความปลอดภัยและการระบายความร้อน", "แอร์อุตสาหกรรม ระบบตรวจจับแก๊ส ระบบดับเพลิง BMS หลายชั้น", "ตัวเครื่องปิดมิดชิดพร้อม BMS ความปลอดภัยขึ้นกับสินค้าที่ได้มาตรฐาน ตำแหน่งติดตั้ง และการติดตั้งที่ถูกต้อง")],
  secs=[
   ("1. แบตเตอรี่ในดาต้าเซ็นเตอร์ทำอะไร", [
    "เมื่อไฟจากการไฟฟ้าดับ แบตเตอรี่ UPS รับโหลดทันทีและจ่ายไฟให้เซิร์ฟเวอร์จนเครื่องปั่นไฟดีเซลติด ซึ่งปกติใช้เวลา 10–20 วินาที ผู้ออกแบบเผื่อเวลาไว้ ราว 1–2 นาทีในดาต้าเซ็นเตอร์ไฮเปอร์สเกล 5 นาทีในคลาวด์และโคโลเคชัน และ 10–15 นาทีในธนาคาร",
    "ลิเธียมไอออนกำลังแทนตะกั่วกรดในห้อง UPS ตะกั่วกรดอยู่ได้ราว 3–6 ปี ส่วนลิเธียมไอออนอยู่ได้นานกว่า เบากว่า และเปลี่ยนน้อยครั้งกว่า Schneider Electric พบว่าต้นทุนรวม 10 ปีของ UPS 1 เฟสที่ใช้ลิเธียมไอออนต่ำกว่าราว 53% แม้ราคาซื้อสูงกว่า",
    "AI เพิ่มงานที่สองให้แบตเตอรี่ ระบบแบตเตอรี่ขนาดใหญ่ (BESS) ใช้ตัดพีคที่มีค่าใช้จ่ายสูง ลดการกระชากของโหลด AI และจ่ายไฟชั่วคราวระหว่างรอการเชื่อมต่อกับการไฟฟ้า ซึ่งในตลาดที่แออัดอาจใช้เวลาหลายปี รายงานของ Volta Foundation ระบุว่าแบตเตอรี่ได้เปรียบเมื่อความเร็วและการใช้งานทุกวันสร้างรายได้ แต่ในพื้นที่ที่ไม่มีค่าความต้องการพลังไฟฟ้า (demand charge) ข้อได้เปรียบส่วนใหญ่ก็หายไป"]),
   ("2. แบตเตอรี่บ้านทำอะไร", [
    "แบตเตอรี่บ้านทำงานทุกวัน ชาร์จจากแผงช่วงเที่ยง แล้วจ่ายไฟให้บ้านช่วงเย็นและกลางคืน เมื่อไฟดับก็สำรองไฟให้วงจรที่เลือกหรือทั้งบ้านได้ ภายในกำลังของอินเวอร์เตอร์",
    "แบตเตอรี่บ้านส่วนใหญ่เป็นลิเธียมไอรอนฟอสเฟต (LFP) ขนาดราว 5–20 kWh ใช้งานได้ราว 6,000 รอบ รับประกันราว 10 ปี แบตเตอรี่ 10 kWh มักจ่ายไฟต่อเนื่องได้ราว 3–5 kW",
    "ในประเทศไทย ความคุ้มค่าเข้าใจง่าย ไฟโซลาร์ที่ใช้เองประหยัดได้เต็มราคาค่าไฟราว 4–4.5 บาทต่อหน่วย ส่วนไฟที่ขายคืน กฟภ. ตามโครงการ net billing ได้ราว 2.20 บาทต่อหน่วย การเก็บไฟช่วงเที่ยงไว้ใช้ตอนเย็นจึงมีค่าราวสองเท่าของการขาย"]),
   ("3. ความหมายสำหรับคุณ", [
    "การเติบโตของดาต้าเซ็นเตอร์ในไทยเพิ่มภาระให้กริดเดียวกับที่บ้านเราใช้ และช่วงพีคตอนเย็นคือช่วงที่หนักที่สุด แบตเตอรี่บ้านทุกชุดที่จ่ายไฟหลังพระอาทิตย์ตกช่วยลดภาระพีคนั้นลงได้บ้าง",
    "เมื่อเลือกแบตเตอรี่บ้าน: เลือกขนาดตามการใช้ไฟช่วงเย็นและกลางคืน ไม่ใช่ตามขนาดหลังคา เลือก LFP แบรนด์เดียวกับอินเวอร์เตอร์หรือรุ่นที่อยู่ในรายการรองรับ เพื่อให้ BMS สื่อสารกับอินเวอร์เตอร์ได้ ดูความจุที่รับประกันเมื่อสิ้นสุดประกัน (มักราว 60–70% หลัง 10 ปี) ไม่ใช่ดูแค่จำนวนปี และต้องเป็นสินค้าที่ได้มาตรฐาน (IEC 62619, UN38.3) ติดตั้งพร้อมอุปกรณ์ป้องกันฝั่ง DC ที่ถูกต้อง",
    "โซลาร์ เอสส์ เลือกขนาดแบตเตอรี่จากบิลค่าไฟของคุณ และจากข้อมูลมอนิเตอร์หากมีโซลาร์อยู่แล้ว ขอตรวจระบบฟรีได้ที่ www.solaress.org"]),
  ],
  src_h="แหล่งข้อมูล", end="คณะทำงาน Solar ESS", title="แบตเตอรี่ดาต้าเซ็นเตอร์ กับแบตเตอรี่บ้าน – สรุปข่าว Solar ESS",
  web=dict(lede="ดาต้าเซ็นเตอร์และบ้านต่างใช้แบตเตอรี่ลิเธียม แต่ทำงานต่างกันมาก ดาต้าเซ็นเตอร์ใช้สำรองไฟทันทีไม่กี่วินาทีถึงไม่กี่นาทีและตัดพีค ส่วนบ้านใช้เก็บไฟโซลาร์ไว้ใช้ทุกวัน",
   pts=[("ดาต้าเซ็นเตอร์", "แบตเตอรี่ UPS รับโหลดจนเครื่องปั่นไฟติด (ปกติ 10–20 วินาที) โดยออกแบบให้สำรองได้ 1–15 นาที ลิเธียมไอออนกำลังแทนตะกั่วกรด และระบบแบตเตอรี่ขนาดใหญ่ยังใช้ตัดพีคและลดการกระชากของโหลด AI"),
        ("บ้าน", "แบตเตอรี่ LFP ขนาด 5–20 kWh ทำงานทุกวัน ราว 6,000 รอบ รับประกันราว 10 ปี และสำรองไฟวงจรที่เลือกเมื่อไฟดับ"),
        ("ในประเทศไทย", "ไฟโซลาร์ที่ใช้เองประหยัดได้ราว 4–4.5 บาทต่อหน่วย ไฟที่ขายคืนตาม net billing ได้ราว 2.20 บาท การเก็บไว้ใช้ตอนเย็นจึงมีค่าราวสองเท่า"),
        ("วิธีเลือก", "เลือกขนาดตามการใช้ไฟช่วงเย็นและกลางคืน ให้เข้ากับอินเวอร์เตอร์ ดูความจุเมื่อสิ้นสุดประกัน และต้องเป็นสินค้าได้มาตรฐาน (IEC 62619, UN38.3) พร้อมอุปกรณ์ป้องกันฝั่ง DC")],
   dl="ดาวน์โหลดสรุป (PDF ภาษาไทย) ↓", other="English (PDF)", srcl="ที่มา:", tail="สรุปโดย โซลาร์ เอสส์", alt="หน้าแรกของสรุปโดย Solar ESS")),
}

FONTS = ROOT / "tools/fonts"
ADDR = {"en": "<b>Solar ESS Co. Ltd.</b><br>53 Moo 2 Tambon Nanglae, Amphoe Muang, Chiang Rai 57100<br>Tel 063 151 6694, 089 632 5829 · LINE: solaress1<br>www.solaress.org · www.โซลาร์เอสส์.com",
        "th": "<b>บริษัท โซลาร์ เอสส์ จำกัด</b><br>53 หมู่ 2 ตำบลนางแล อำเภอเมือง จังหวัดเชียงราย 57100<br>โทร 063 151 6694, 089 632 5829 · LINE: solaress1<br>www.solaress.org · www.โซลาร์เอสส์.com"}


def doc(lang):
    c = C[lang]
    css = f"""@font-face{{font-family:'Sarabun';src:url('file://{FONTS}/Sarabun-Regular.ttf')}}
@font-face{{font-family:'Sarabun';font-weight:bold;src:url('file://{FONTS}/Sarabun-Bold.ttf')}}
body{{font-family:'Sarabun',sans-serif;font-size:10.5pt;line-height:1.55;color:#1b1f3a;margin:0}}
.eyebrow{{color:#4B4FD8;font-size:9pt;letter-spacing:.06em;text-transform:uppercase;margin:0 0 4px}}
h1{{font-size:22pt;line-height:1.2;margin:0 0 8px;color:#0B1736}} .lede{{font-size:11.5pt;margin:0 0 10px}}
h2{{font-size:13.5pt;margin:18px 0 6px;padding-top:8px;border-top:1.5px solid #0B1736;color:#0B1736;page-break-after:avoid}}
p{{margin:5px 0}} .kf{{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:12px 0}}
.kf div{{border:1px solid #D7DAEA;border-top:3px solid #4B4FD8;padding:7px 8px;background:#F5F6FC}} .kf b{{display:block;font-size:14pt;color:#0B1736}} .kf span{{font-size:8.5pt;color:#555}}
table{{width:100%;border-collapse:collapse;margin:8px 0 4px;font-size:9.2pt;page-break-inside:avoid}} th,td{{border:1px solid #D7DAEA;padding:5px 7px;text-align:left;vertical-align:top}}
th{{background:#0B1736;color:#fff}} td:first-child{{font-weight:bold;width:20%;background:#F5F6FC}}
ol.src{{font-size:8.3pt;padding-left:18px;color:#444}} ol.src a{{color:#444;word-break:break-all}} .end{{text-align:right;font-weight:bold;color:#0B1736;margin-top:16px}}"""
    b = [f'<p class="eyebrow">{c["eyebrow"]}</p><h1>{c["h1"]}</h1><p class="lede">{c["lede"]}</p>',
         '<div class="kf">' + "".join(f"<div><b>{a}</b><span>{s}</span></div>" for a, s in c["kf"]) + "</div>",
         "<table><tr>" + "".join(f"<th>{h}</th>" for h in c["th"]) + "</tr>" + "".join(f"<tr><td>{a}</td><td>{x}</td><td>{y}</td></tr>" for a, x, y in c["rows"]) + "</table>"]
    for h, ps in c["secs"]:
        b.append(f"<h2>{h}</h2>" + "".join(f"<p>{p}</p>" for p in ps))
    b.append(f'<h2>{c["src_h"]}</h2><ol class="src">' + "".join(f'<li>{html.escape(t)} – <a href="{u}">{u}</a></li>' for t, u in SRC) + "</ol>")
    b.append(f'<p class="end">{c["end"]}</p>')
    return f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><style>{css}</style></head><body>{"".join(b)}</body></html>'


def header(lang):
    logo = "data:image/jpeg;base64," + base64.b64encode((ROOT / "images/solar-ess-report-logo.jpg").read_bytes()).decode()
    return (f'<div style="width:100%;padding:0 14mm;display:flex;justify-content:space-between;align-items:flex-start;font-family:Sarabun,sans-serif;font-size:7.5px;color:#0B1736">'
            f'<img src="{logo}" style="height:15mm"><div style="text-align:right;line-height:1.4">{ADDR[lang]}</div></div>')


def footer(lang):
    pg = ("Page" if lang == "en" else "หน้า") + ' <span class="pageNumber"></span> / <span class="totalPages"></span>'
    return f'<div style="width:100%;padding:0 14mm;font-family:Sarabun,sans-serif;font-size:7.5px;color:#666;display:flex;justify-content:space-between"><span>{C[lang]["title"]} · {REV} · 19 Nov 2026</span><span>{pg}</span></div>'


def build_pdfs():
    from playwright.sync_api import sync_playwright
    (ROOT / "tools/.pdf_tmp").mkdir(exist_ok=True)
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        for lang in ("en", "th"):
            f = ROOT / f"tools/.pdf_tmp/{ID}-{lang}.html"; f.write_text(doc(lang), encoding="utf-8")
            pg = br.new_page(); pg.goto("file://" + str(f)); pg.wait_for_timeout(500)
            pg.pdf(path=str(RAW[lang]), format="A4", print_background=True, display_header_footer=True,
                   header_template=header(lang), footer_template=footer(lang),
                   margin={"top": "32mm", "bottom": "16mm", "left": "14mm", "right": "14mm"})
            print("raw", RAW[lang])
        br.close()


def article(lang, first):
    w = C[lang]["web"]; c = C[lang]
    lis = "".join(f'<li style="margin-bottom:10px"><b>{a}:</b> {b}</li>' for a, b in w["pts"])
    other = PDF["th" if lang == "en" else "en"]; ostyle = ' lang="th" style="font-family:var(--thai)"' if lang == "en" else ' lang="en"'
    style = 'style="max-width:760px"' if first else SEP
    src = " · ".join(f'{n} <a href="{u}" rel="noopener">↗</a>' for n, u in (("Schneider Electric", SRC[0][1]), ("ESS News / Volta Foundation", SRC[4][1]), ("PNNL", SRC[5][1]), ("FranklinWH", SRC[8][1])))
    return (f'<article id="{ID}" {style}>\n<p class="eyebrow">{c["eyebrow"]}</p><h2 style="font-size:clamp(26px,3.6vw,40px)">{c["h1"]}</h2>\n'
            f'<p class="lede" style="margin-top:16px;opacity:1">{w["lede"]}</p>\n<ul style="margin-top:22px;padding-left:20px">{lis}</ul>\n'
            f'<p style="margin-top:22px"><a href="{PDF[lang]}"><img src="/images/{IMG}" alt="{w["alt"]}" width="579" height="819" loading="lazy" style="width:100%;max-width:360px;height:auto;border:1.5px solid var(--line)"></a></p>\n'
            f'<p style="margin-top:18px;display:flex;gap:10px;flex-wrap:wrap"><a class="btn" href="{PDF[lang]}" download>{w["dl"]}</a><a class="btn ghost" href="{other}"{ostyle}>{w["other"]}</a></p>\n'
            f'<p style="margin-top:28px;font-size:14px;color:var(--mute)">{w["srcl"]} {src}. {w["tail"]}</p>\n</article>\n')


def pages():
    for lang, path in (("en", "news.html"), ("th", "th/news.html")):
        p = ROOT / path; s = p.read_text(encoding="utf-8")
        s = re.sub(rf'<article id="{ID}".*?</article>\n?', "", s, flags=re.S)
        m = re.search(r'<article id="([^"]+)"( data-topics="[^"]*")? style="[^"]*">', s)
        s = s[:m.start()] + article(lang, True) + re.sub(r'style="[^"]*"', SEP, m.group(0)) + s[m.end():]
        p.write_text(s, encoding="utf-8"); print(path, "article before", m.group(1))


if __name__ == "__main__":
    if "--pdf" in sys.argv:
        build_pdfs()
    else:
        pages()
