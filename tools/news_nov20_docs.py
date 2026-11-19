# -*- coding: utf-8 -*-
"""News batch published 20 Nov 2026 (Kris's request, held from 19 Nov so they go out together):
  SolarEdge Duo power optimizer (bullet summary, no PDF) and five Solar ESS documents cleaned with
  tools/clean_quote_pdf.py (no prices, no customer names or details; watermark on every page):
  6 kW Solis hybrid + 16 kWh proposal (TH + EN), Growatt 25 kW / 30.375 kWp / 48 kWh proposal (TH),
  Growatt hybrid packages 6/10/15/50 kW (TH), 30 kW hybrid comparison GoodWe/Solis/Growatt (TH),
  plus the English PDF of the AIKO 675 W vs LONGi 650 W comparison (added to the 18 Nov article).
  The Mae Hong Son contract was NOT published (personal IDs, bank account, ID card copies).
1. News: articles at the top of /news.html and /th/news.html.
2. Quotation: three samples at the top of /quotation.html and /th/quotation.html (<!--q1120--> markers).
Idempotent. Run: python3 tools/news_nov20_docs.py, then tools/news_topics.py, tools/build_share.py, tools/site_search.py, tools/news_menu.py"""
import re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = "/downloads/"
P6T = D + "Solar-ESS-Sample-Proposal-Hybrid-6kW-Solis-16kWh-TH_Rev01_WM_20261120.pdf"
P6E = D + "Solar-ESS-Sample-Proposal-Hybrid-6kW-Solis-16kWh_Rev01_WM_20261120.pdf"
G25 = D + "Solar-ESS-Sample-Proposal-Hybrid-Growatt-25kW-30kWp-48kWh-TH_Rev01_WM_20261120.pdf"
PKG = D + "Solar-ESS-Sample-Packages-Growatt-Hybrid-6-10-15-50kW-TH_Rev01_WM_20261120.pdf"
C30 = D + "Solar-ESS-Comparison-30kW-Hybrid-GoodWe-Solis-Growatt-TH_Rev01_WM_20261120.pdf"
CMPEN = D + "Solar-ESS-PV-Module-Comparison-AIKO675-vs-LONGi650_Rev02_WM_20261120.pdf"
SEP = 'style="max-width:760px;margin-top:64px;padding-top:48px;border-top:1.5px solid var(--navy)"'
SE_SRC = [("POWER Magazine", "https://www.powermag.com/solaredge-debuts-duo-power-optimizer-for-ci-projects/"),
          ("Solar Builder", "https://solarbuildermag.com/products/solaredge-debuts-power-optimizer-for-commercial-projects/"),
          ("pv magazine", "https://www.pv-magazine.com/2026/11/19/solaredge-debuts-duo-power-optimizer-at-re/")]


def thumb(pdf):
    name = "doc-" + pdf.split("/downloads/Solar-ESS-")[1].split("_Rev")[0].lower().replace(".", "-")
    out = ROOT / "images" / f"{name}.jpg"
    if not out.exists():
        subprocess.run(["pdftoppm", "-r", "70", "-jpeg", "-jpegopt", "quality=85", "-f", "1", "-l", "1", "-singlefile",
                        str(ROOT / pdf.lstrip("/")), str(out.with_suffix(""))], check=True)
    return f"/images/{name}.jpg"


# (id, [(pdf, lang)], {lang: (eyebrow, h2, lede, [(label, text)])})
A = [
 ("solaredge-duo-power-optimizer", [], {
  "en": ("19 November 2026 · Innovation", "SolarEdge Duo: one power optimizer for two panels, with arc sensing built in",
         "SolarEdge launched the Duo Power Optimizer for commercial and industrial (C&I) solar in the U.S. on 16 November, ahead of RE+ in Las Vegas (17–19 Nov).",
         [("Half the units", "One optimizer connects two panels and, SolarEdge says, harvests as much as one optimizer per panel, with 50% fewer units to specify, wire and install."),
          ("Own MPPT per panel", "Each of the two panels keeps its own maximum power point tracker, so shade or mismatch on one panel does not pull down the other."),
          ("Arc detection in the array", "Every optimizer acts as an arc sensor, so detection is spread across the array instead of only at the inverter; if one misses an arc, its neighbour can catch it."),
          ("Hot-connector warning", "Sense Connect watches the temperature of every input and output connector and flags a developing fault before an overheating connector can cause an arc."),
          ("Dual-tilt roofs", "One optimizer can take two panels facing different directions, which suits east–west and dual-tilt racking."),
          ("Availability", "Made in Florida and on order now in the U.S. only; not yet sold in Thailand."),
          ("What it means here", "Panel-level arc and connector-heat detection is becoming a standard safety feature for roofs. On factory and warehouse roofs, ask your installer how arcs and hot connectors are detected and how the DC side is protected.")]),
  "th": ("19 พฤศจิกายน 2569 · นวัตกรรม", "SolarEdge Duo: ออปติไมเซอร์ 1 ตัวต่อ 2 แผง พร้อมตรวจจับอาร์กในตัว",
         "SolarEdge เปิดตัว Duo Power Optimizer สำหรับโซลาร์เชิงพาณิชย์และอุตสาหกรรม (C&I) ในสหรัฐฯ เมื่อวันที่ 16 พ.ย. ก่อนงาน RE+ ที่ลาสเวกัส (17–19 พ.ย.)",
         [("ใช้อุปกรณ์ครึ่งเดียว", "ออปติไมเซอร์ 1 ตัวต่อแผงได้ 2 แผง SolarEdge ระบุว่าได้พลังงานเท่ากับแบบ 1 ตัวต่อ 1 แผง แต่จำนวนอุปกรณ์ที่ต้องออกแบบ เดินสาย และติดตั้งลดลง 50%"),
          ("MPPT แยกทุกแผง", "แต่ละแผงมีตัวติดตามจุดกำลังสูงสุด (MPPT) ของตัวเอง เงาหรือแผงที่ไม่เท่ากันจึงไม่ดึงอีกแผงลง"),
          ("ตรวจจับอาร์กทั่วทั้งแผง", "ออปติไมเซอร์ทุกตัวทำหน้าที่ตรวจจับอาร์ก การตรวจจับจึงกระจายทั่วทั้งชุดแผง ไม่ได้อยู่ที่อินเวอร์เตอร์จุดเดียว ถ้าตัวหนึ่งพลาด ตัวข้าง ๆ ก็ตรวจจับได้"),
          ("เตือนขั้วต่อร้อน", "Sense Connect วัดอุณหภูมิขั้วต่อเข้าและออกทุกจุด เตือนความผิดปกติก่อนขั้วต่อที่ร้อนเกินจะทำให้เกิดอาร์ก"),
          ("หลังคาสองทิศ", "ออปติไมเซอร์ 1 ตัวต่อแผงที่หันคนละทิศได้ เหมาะกับโครงแบบตะวันออก–ตะวันตกหรือสองระดับเอียง"),
          ("การวางจำหน่าย", "ผลิตในรัฐฟลอริดา สั่งซื้อได้แล้วเฉพาะในสหรัฐฯ ยังไม่มีขายในประเทศไทย"),
          ("ความหมายสำหรับเรา", "การตรวจจับอาร์กและความร้อนที่ขั้วต่อระดับแผงกำลังเป็นมาตรฐานความปลอดภัยของงานหลังคา สำหรับหลังคาโรงงานและโกดัง ควรถามผู้ติดตั้งว่าระบบตรวจจับอาร์กและขั้วต่อร้อนอย่างไร และป้องกันฝั่ง DC อย่างไร")])}),
 ("proposal-hybrid-6kw-solis-16kwh", [(P6T, "th"), (P6E, "en")], {
  "en": ("20 November 2026 · Sample proposal", "6 kW hybrid with whole-house backup: Solis 6 kW, 5.85 kWp, 16 kWh battery",
         "A single-phase project proposal for a business customer, in Thai and English. Customer details and prices removed.",
         [("Equipment", "Solis S6-EH1P6K-L-PLUS 6 kW hybrid inverter, 9 × LONGi Hi-MO X10 650 W panels (5.85 kWp) and a Solis IntelliHome 16 kWh LiFePO4 battery from the same brand."),
          ("Backup", "An MDB & ATS board switches the whole building to backup in a power cut, up to 6 kW of combined load."),
          ("Output", "About 7,900 kWh a year (1,350 kWh per kWp)."),
          ("Included", "Full bill of materials by category, turnkey installation, SolisCloud monitoring and 5-year maintenance.")]),
  "th": ("20 พฤศจิกายน 2569 · ตัวอย่างข้อเสนอโครงการ", "ไฮบริด 6 kW พร้อมไฟสำรองทั้งบ้าน: Solis 6 kW แผง 5.85 kWp แบตเตอรี่ 16 kWh",
         "ข้อเสนอโครงการระบบ 1 เฟสสำหรับลูกค้าธุรกิจ ภาษาไทยและภาษาอังกฤษ ตัดข้อมูลลูกค้าและราคาออกแล้ว",
         [("อุปกรณ์", "อินเวอร์เตอร์ไฮบริด Solis S6-EH1P6K-L-PLUS 6 kW แผง LONGi Hi-MO X10 650 W × 9 แผง (5.85 kWp) และแบตเตอรี่ Solis IntelliHome 16 kWh LiFePO4 แบรนด์เดียวกัน"),
          ("ไฟสำรอง", "ตู้ MDB & ATS สลับไฟทั้งอาคารไปใช้ไฟสำรองเมื่อไฟดับ ใช้ไฟรวมกันได้ไม่เกิน 6 kW"),
          ("ผลผลิต", "ประมาณ 7,900 หน่วยต่อปี (1,350 หน่วยต่อ kWp)"),
          ("รวมในงาน", "รายการวัสดุครบตามหมวด งานติดตั้งแบบเหมา ระบบดูผล SolisCloud และบำรุงรักษา 5 ปี")])}),
 ("proposal-growatt-25kw-30kwp-48kwh", [(G25, "th")], {
  "en": ("20 November 2026 · Sample proposal", "Growatt 25 kW hybrid on a ground mount: 30.375 kWp with 48 kWh of storage",
         "A three-phase project proposal with ground-mount structure drawings, compared with two other Growatt layouts (Thai PDF). Prices removed.",
         [("Equipment", "1 × Growatt WIT25K-HU 25 kW three-phase hybrid inverter, 45 × AIKO 675 W back-contact panels (30.375 kWp) and 3 × Growatt HOPE 16 kWh LiFePO4 batteries (48 kWh)."),
          ("Structure", "One ground-mounted table on screw piles with a gravel floor; layout, sections and pile details are in the appendix."),
          ("Output", "About 41,000 kWh a year."),
          ("Compared", "Against 3 × 10 kW inverters and against 2 × 25 kW with 50 kWh: one 25 kW inverter is the simplest and lowest-cost way to reach about 30 kWp.")]),
  "th": ("20 พฤศจิกายน 2569 · ตัวอย่างข้อเสนอโครงการ", "ไฮบริด Growatt 25 kW ติดตั้งบนพื้นดิน: แผง 30.375 kWp แบตเตอรี่ 48 kWh",
         "ข้อเสนอโครงการระบบ 3 เฟส พร้อมแบบโครงสร้างติดตั้งบนพื้นดิน และเปรียบเทียบกับ Growatt อีก 2 แบบ ตัดราคาออกแล้ว",
         [("อุปกรณ์", "อินเวอร์เตอร์ไฮบริด Growatt WIT25K-HU 25 kW 3 เฟส 1 เครื่อง แผง AIKO 675 W × 45 แผง (30.375 kWp) และแบตเตอรี่ Growatt HOPE 16 kWh × 3 ชุด (48 kWh)"),
          ("โครงสร้าง", "โต๊ะแผงชุดเดียวบนเสาเข็มเกลียวพร้อมพื้นหินกรวด แบบผัง รูปตัด และรายละเอียดเสาอยู่ในภาคผนวก"),
          ("ผลผลิต", "ประมาณ 41,000 หน่วยต่อปี"),
          ("เปรียบเทียบ", "เทียบกับอินเวอร์เตอร์ 10 kW 3 เครื่อง และ 25 kW 2 เครื่องกับแบตเตอรี่ 50 kWh: อินเวอร์เตอร์ 25 kW เครื่องเดียวง่ายที่สุดและประหยัดที่สุดสำหรับขนาดราว 30 kWp")])}),
 ("packages-growatt-hybrid-6-10-15-50kw", [(PKG, "th")], {
  "en": ("20 November 2026 · Packages", "Growatt hybrid packages 2026: 6, 10, 15 and 50 kW with battery",
         "Four ready-to-quote packages, each with battery, balance of system, the PEA application and 5-year maintenance (Thai PDF). Prices removed.",
         [("6 kW single-phase", "Growatt SPM6000TL-HU, 9 × LONGi 650 W (5.85 kWp), 16 kWh battery; about 7,900 kWh a year, for homes paying about 2,500–4,000 baht a month."),
          ("10 kW single-phase", "Growatt SPM10000TL-HU, 16 panels (10.40 kWp), 16 kWh; about 14,000 kWh a year, for larger homes paying about 4,000–7,000 baht a month."),
          ("15 kW three-phase", "Growatt WIT15K-HU, 24 panels (15.60 kWp), 32 kWh; about 21,100 kWh a year, for large homes, offices and shops."),
          ("50 kW three-phase", "2 × Growatt WIT25K-HU, 78 panels (50.70 kWp), 64 kWh; about 68,400 kWh a year, for hotels, resorts and small factories.")]),
  "th": ("20 พฤศจิกายน 2569 · แพ็กเกจ", "แพ็กเกจไฮบริด Growatt 2026: 6, 10, 15 และ 50 kW พร้อมแบตเตอรี่",
         "4 แพ็กเกจพร้อมเสนอราคา ทุกแพ็กเกจรวมแบตเตอรี่ อุปกรณ์ประกอบระบบ การยื่นขออนุญาต กฟภ. และบำรุงรักษา 5 ปี ตัดราคาออกแล้ว",
         [("6 kW 1 เฟส", "Growatt SPM6000TL-HU แผง LONGi 650 W × 9 (5.85 kWp) แบตเตอรี่ 16 kWh ผลิตราว 7,900 หน่วยต่อปี เหมาะกับบ้านค่าไฟราว 2,500–4,000 บาทต่อเดือน"),
          ("10 kW 1 เฟส", "Growatt SPM10000TL-HU แผง 16 แผง (10.40 kWp) แบตเตอรี่ 16 kWh ผลิตราว 14,000 หน่วยต่อปี เหมาะกับบ้านค่าไฟราว 4,000–7,000 บาทต่อเดือน"),
          ("15 kW 3 เฟส", "Growatt WIT15K-HU แผง 24 แผง (15.60 kWp) แบตเตอรี่ 32 kWh ผลิตราว 21,100 หน่วยต่อปี เหมาะกับบ้านใหญ่ สำนักงาน ร้านค้า"),
          ("50 kW 3 เฟส", "Growatt WIT25K-HU × 2 แผง 78 แผง (50.70 kWp) แบตเตอรี่ 64 kWh ผลิตราว 68,400 หน่วยต่อปี เหมาะกับโรงแรม รีสอร์ต โรงงานขนาดเล็ก")])}),
 ("comparison-30kw-hybrid-goodwe-solis-growatt", [(C30, "th")], {
  "en": ("20 November 2026 · Technical comparison", "30 kW hybrid, three ways: GoodWe, Solis or Growatt (3 × 10 kW)",
         "The same 29.70 kWp array and about 48 kWh of storage on three inverter brands, with the ground-mount structure design (Thai PDF). Prices removed.",
         [("Same on all three", "44 × AIKO 675 W panels (29.70 kWp), about 48 kWh of low-voltage LiFePO4 batteries and the same screw-pile ground mount with gravel floor."),
          ("A: GoodWe", "3 × GW10K-ET 10 kW with 3 × Lynx A G4 16.1 kWh; the lowest total of the three, monitored in the SEMS app."),
          ("B: Solis", "3 × S6-EH3P10K 10 kW with 3 × IntelliHome 16 kWh; the brand Solar ESS installs and services most, with SolisCloud."),
          ("C: Growatt", "3 × WIT10K-HU 10 kW with 3 × HOPE 16 kWh; the highest total here, with ShinePhone monitoring."),
          ("Why three inverters", "If one inverter stops, the other two keep about two-thirds of the system running.")]),
  "th": ("20 พฤศจิกายน 2569 · เปรียบเทียบทางเทคนิค", "ไฮบริด 30 kW สามทางเลือก: GoodWe, Solis หรือ Growatt (10 kW × 3)",
         "แผงชุดเดียวกัน 29.70 kWp และแบตเตอรี่ราว 48 kWh บนอินเวอร์เตอร์ 3 แบรนด์ พร้อมแบบโครงสร้างติดตั้งบนพื้นดิน ตัดราคาออกแล้ว",
         [("เหมือนกันทุกทางเลือก", "แผง AIKO 675 W × 44 แผง (29.70 kWp) แบตเตอรี่ LiFePO4 แรงดันต่ำราว 48 kWh และโครงสร้างเสาเข็มเกลียวกับพื้นหินกรวดแบบเดียวกัน"),
          ("A: GoodWe", "GW10K-ET 10 kW × 3 กับ Lynx A G4 16.1 kWh × 3 ราคารวมต่ำที่สุดในสามทางเลือก ดูผลผ่านแอป SEMS"),
          ("B: Solis", "S6-EH3P10K 10 kW × 3 กับ IntelliHome 16 kWh × 3 แบรนด์ที่ Solar ESS ติดตั้งและดูแลมากที่สุด พร้อม SolisCloud"),
          ("C: Growatt", "WIT10K-HU 10 kW × 3 กับ HOPE 16 kWh × 3 ราคารวมสูงที่สุดในชุดนี้ ดูผลผ่าน ShinePhone"),
          ("ทำไมใช้ 3 เครื่อง", "หากอินเวอร์เตอร์ขัดข้อง 1 เครื่อง อีก 2 เครื่องยังทำงานต่อได้ราวสองในสามของระบบ")])}),
]

L = {"en": dict(open="Open the PDF ↓", lang={"en": "English", "th": "Thai"}, alt="First page of the Solar ESS document", note="Prices, names and customer details removed.", src="Sources:", tail="Summary by Solar ESS."),
     "th": dict(open="เปิด PDF ↓", lang={"en": "ภาษาอังกฤษ", "th": "ภาษาไทย"}, alt="หน้าแรกของเอกสาร Solar ESS", note="ตัดราคา ชื่อ และข้อมูลลูกค้าออกแล้ว", src="ที่มา:", tail="สรุปโดย โซลาร์ เอสส์")}


def article(aid, pdfs, lang, t, first):
    eb, h2, lede, pts = t
    lis = "".join(f'<li style="margin-bottom:10px"><b>{a}:</b> {b}</li>' for a, b in pts)
    style = 'style="max-width:760px"' if first else SEP
    out = (f'<article id="{aid}" {style}>\n<p class="eyebrow">{eb}</p><h2 style="font-size:clamp(26px,3.6vw,40px)">{h2}</h2>\n'
           f'<p class="lede" style="margin-top:16px;opacity:1">{lede}</p>\n<ul style="margin-top:22px;padding-left:20px">{lis}</ul>\n')
    if pdfs:
        main = next((p for p, l in pdfs if l == lang), pdfs[0][0])
        btns = "".join(f'<a class="btn{"" if p == main else " ghost"}" href="{p}" download>{L[lang]["open"]} · {L[lang]["lang"][l]}</a>' for p, l in sorted(pdfs, key=lambda x: x[0] != main))
        out += (f'<p style="margin-top:22px"><a href="{main}"><img src="{thumb(main)}" alt="{L[lang]["alt"]}" width="579" height="819" loading="lazy" '
                f'style="width:100%;max-width:360px;height:auto;border:1.5px solid var(--line)"></a></p>\n'
                f'<p style="margin-top:18px;display:flex;gap:10px;flex-wrap:wrap">{btns}</p>\n'
                f'<p style="margin-top:20px;font-size:14px;color:var(--mute)">{L[lang]["note"]} Solar ESS Working Group.</p>\n')
    else:
        src = " · ".join(f'{n} <a href="{u}" rel="noopener">↗</a>' for n, u in SE_SRC)
        out += f'<p style="margin-top:28px;font-size:14px;color:var(--mute)">{L[lang]["src"]} {src}. {L[lang]["tail"]}</p>\n'
    return out + "</article>\n"


EN_BTN = {"en": f'<a class="btn ghost" href="{CMPEN}" download>Open the PDF ↓ · English</a>',
          "th": f'<a class="btn ghost" href="{CMPEN}" download>เปิด PDF ↓ · ภาษาอังกฤษ</a>'}

for lang, path in (("en", "news.html"), ("th", "th/news.html")):
    p = ROOT / path
    s = p.read_text(encoding="utf-8")
    for aid, *_ in A:
        s = re.sub(rf'<article id="{aid}".*?</article>\n?', "", s, flags=re.S)
    m = re.search(r'<article id="([^"]+)"( data-topics="[^"]*")? style="[^"]*">', s)
    old_first = re.sub(r'style="[^"]*"', SEP, m.group(0))
    block = "".join(article(aid, pdfs, lang, d[lang], i == 0) for i, (aid, pdfs, d) in enumerate(A))
    s = s[:m.start()] + block + old_first + s[m.end():]
    # English PDF of the AIKO vs LONGi comparison (18 Nov article)
    m2 = re.search(r'(<article id="pv-module-comparison-aiko675-longi650".*?<a class="btn" href="[^"]+" download>[^<]*</a>)(.*?</article>)', s, flags=re.S)
    if m2 and CMPEN not in m2.group(0):
        s = s[:m2.start()] + m2.group(1) + EN_BTN[lang] + m2.group(2) + s[m2.end():]
    p.write_text(s, encoding="utf-8")
    print(path, len(A), "articles before", m.group(1), "| EN comparison button", bool(m2))

# Quotation pages
Q = [("sample-6kw-solis-hybrid-16kwh", P6T, P6E, A[1]), ("sample-growatt-25kw-30kwp-48kwh", G25, None, A[2]), ("sample-growatt-packages-6-10-15-50kw", PKG, None, A[3])]
META = {"en": {P6T: "Project proposal · 3 pages · PDF · Thai and English", G25: "Project proposal · 7 pages · PDF · Thai", PKG: "Package brochure · 6 pages · PDF · Thai"},
        "th": {P6T: "ข้อเสนอโครงการ · 3 หน้า · PDF · ภาษาไทยและอังกฤษ", G25: "ข้อเสนอโครงการ · 7 หน้า · PDF · ภาษาไทย", PKG: "แพ็กเกจ · 6 หน้า · PDF · ภาษาไทย"}}
for lang, path in (("en", "quotation.html"), ("th", "th/quotation.html")):
    B = ["Open the PDF", "Download", "Ask for a price", "/#consult", "English PDF"] if lang == "en" else ["เปิด PDF", "ดาวน์โหลด", "ขอราคา", "/th/#consult", "PDF ภาษาอังกฤษ"]
    N = "Customer details and prices have been removed." if lang == "en" else "ตัดข้อมูลลูกค้าและราคาออกแล้ว"
    out = ""
    for qid, pdf, pen, a in Q:
        eb, h2, lede, pts = a[2][lang]
        lis = "".join(f"<li>{x}: {y}</li>" for x, y in pts)
        main = pen if (lang == "en" and pen) else pdf
        extra = f'<a class="btn ghost" href="{pen}">{B[4]}</a>' if (pen and lang == "th") else (f'<a class="btn ghost" href="{pdf}" lang="th">ภาษาไทย (PDF)</a>' if pen else "")
        out += (f'<article class="tnote" id="{qid}"><a href="{main}"><img src="{thumb(main)}" alt="{h2}" width="579" height="819" loading="lazy"></a>'
                f'<div><p class="meta">{META[lang][pdf]}</p><h2>{h2}</h2><p>{lede}</p><ul>{lis}</ul><p class="meta" style="margin-top:12px">{N}</p>'
                f'<div class="acts"><a class="btn" href="{main}">{B[0]}</a><a class="btn ghost" href="{main}" download>{B[1]}</a>{extra}'
                f'<a class="btn ghost" href="{B[3]}">{B[2]}</a></div></div></article>\n')
    p = ROOT / path
    s = p.read_text(encoding="utf-8")
    s = re.sub(r"<!--q1120-->.*?<!--/q1120-->\n?", "", s, flags=re.S)
    i = s.index('<article class="tnote"')
    s = s[:i] + "<!--q1120-->" + out + "<!--/q1120-->\n" + s[i:]
    p.write_text(s, encoding="utf-8")
    print(path, len(Q), "samples")
