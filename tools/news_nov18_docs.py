# -*- coding: utf-8 -*-
"""Six Solar ESS documents published 18 Nov 2026 (Kris's request), cleaned with tools/clean_quote_pdf.py
(no prices, no personal names, no customer names or exact sites; Solar ESS watermark on every page):
  plant review (nursing home, Lampang, 12-18 Nov), two 5.4 kWp quotation reports (Solis hybrid / Huawei),
  AIKO 675 W vs LONGi 650 W comparison (TH), 14.5 kWp house package (TH), carbon credits briefing (TH, 17 Nov).
1. News: six articles at the top of /news.html and /th/news.html (ids below).
2. Quotation: the two quotations and the package at the top of /quotation.html and /th/quotation.html (<!--q1118--> markers).
The cleaned PDFs must already be in downloads/. Idempotent.
Run: python3 tools/news_nov18_docs.py, then tools/news_topics.py, tools/build_share.py, tools/site_search.py, tools/news_menu.py, tools/analytics_tag.py"""
import re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = "/downloads/"
KP = D + "Solar-ESS-Plant-Review-Nursing-Home-Lampang-12-18Nov2026_Rev01_WM_20261118.pdf"
SOL = D + "Solar-ESS-Sample-Quotation-5.4kWp-Solis6kW-Hybrid-AIKO675_Rev03_WM_20261118.pdf"
HUA = D + "Solar-ESS-Sample-Quotation-5.4kWp-Huawei5kW-AIKO675_Rev02_WM_20261118.pdf"
CMP = D + "Solar-ESS-PV-Module-Comparison-AIKO675-vs-LONGi650-TH_Rev02_WM_20261118.pdf"
PKG = D + "Solar-ESS-Sample-Package-House-Chiangrai-14.5kWp-10kW-TH_Rev37_WM_20261118.pdf"
CO2 = D + "Solar-ESS-Carbon-Credits-Solar-Briefing-TH_Rev02_WM_20261119.pdf"  # public version; the full internal Rev01 is admin-only
SEP = 'style="max-width:760px;margin-top:64px;padding-top:48px;border-top:1.5px solid var(--navy)"'


def thumb(pdf):
    name = "doc-" + pdf.split("/downloads/Solar-ESS-")[1].split("_Rev")[0].lower().replace(".", "-")
    out = ROOT / "images" / f"{name}.jpg"
    if not out.exists():
        subprocess.run(["pdftoppm", "-r", "70", "-jpeg", "-jpegopt", "quality=85", "-f", "1", "-l", "1", "-singlefile",
                        str(ROOT / pdf.lstrip("/")), str(out.with_suffix(""))], check=True)
    return f"/images/{name}.jpg"


# (id, pdf, pdf language, {lang: (eyebrow, h2, lede, [(label, text)])})
A = [
 ("plant-review-nursing-home-lampang-nov2026", KP, "en", {
  "en": ("18 November 2026 · Plant review", "Nursing home, Lampang: what cleaning and a panel removal did to output",
         "A 25 kWp zero-export system, reviewed on SolisCloud for the three days before and after our 15 November site work.",
         [("The week", "509 kWh of solar in 7 days (42–99 kWh a day), covering about 38% of the site's use, an estimated saving of about 2,130 baht at 4.18 baht per unit."),
          ("Cleaning helped", "Peak output on clear days rose from about 17.1–18.1 kW before cleaning to 18.2 kW on 16 Nov and 18.6 kW on 18 Nov, with one panel fewer."),
          ("Cracked panel", "Removing the impact-damaged panel made no noticeable drop; low days were rain and cloud. Zero export works: only 0.06–0.35 kWh a day went to the grid."),
          ("Next steps", "Confirm a 40-minute stop on 18 Nov, check leakage with a clamp meter after the air-conditioner repair, and update the PV capacity on SolisCloud.")]),
  "th": ("18 พฤศจิกายน 2569 · รีวิวระบบ", "บ้านพักผู้สูงอายุ ลำปาง: ผลของการล้างแผงและการถอดแผงที่แตก",
         "ระบบ 25 kWp แบบไม่ขายไฟคืน (zero export) ตรวจข้อมูลจาก SolisCloud 3 วันก่อนและหลังงานหน้างานวันที่ 15 พ.ย.",
         [("สัปดาห์นี้", "ผลิตไฟจากโซลาร์ 509 kWh ใน 7 วัน (42–99 kWh ต่อวัน) คิดเป็นราว 38% ของไฟที่ใช้ ประหยัดได้ประมาณ 2,130 บาท ที่หน่วยละ 4.18 บาท"),
          ("ล้างแผงแล้วดีขึ้น", "กำลังผลิตสูงสุดในวันแดดดีเพิ่มจากราว 17.1–18.1 kW ก่อนล้าง เป็น 18.2 kW (16 พ.ย.) และ 18.6 kW (18 พ.ย.) แม้แผงน้อยลง 1 แผง"),
          ("แผงที่แตก", "ถอดแผงที่แตกจากแรงกระแทกแล้วไม่เห็นผลผลิตลดลงชัดเจน วันที่ผลิตน้อยเป็นเพราะฝนและเมฆ zero export ทำงานปกติ ไหลกลับกริดเพียง 0.06–0.35 kWh ต่อวัน"),
          ("ขั้นต่อไป", "ยืนยันสาเหตุที่ระบบหยุด 40 นาทีวันที่ 18 พ.ย. วัดไฟรั่วด้วยแคลมป์มิเตอร์หลังซ่อมแอร์ และแก้ขนาดแผงใน SolisCloud")])}),
 ("quotation-5-4kwp-solis-hybrid-aiko", SOL, "en", {
  "en": ("18 November 2026 · Sample quotation", "5.4 kWp hybrid: Solis 6 kW with AIKO 675 W panels",
         "A turnkey single-phase system that is ready for a battery later. Prices removed; ask us for a quote for your home.",
         [("Equipment", "8 × AIKO ABC 675 W back-contact panels (5.40 kWp), Solis S6-EH1P6K-L-PLUS 6 kW hybrid inverter, smart meter for zero export and WiFi monitoring."),
          ("Output", "About 7,100–7,900 kWh a year."),
          ("Included", "DC cable, AC/DC combiner box with surge protection, earthing, mounting, installation, 5-year maintenance and the PEA application."),
          ("Options", "Two more panels to reach 6.75 kWp, or a 16 kWh LV battery for backup and night use.")]),
  "th": ("18 พฤศจิกายน 2569 · ตัวอย่างใบเสนอราคา", "ไฮบริด 5.4 kWp: Solis 6 kW กับแผง AIKO 675 W",
         "ระบบ 1 เฟสแบบเหมาครบ พร้อมเพิ่มแบตเตอรี่ภายหลัง ตัดราคาออกแล้ว ขอใบเสนอราคาสำหรับบ้านของคุณได้",
         [("อุปกรณ์", "แผง AIKO ABC 675 W × 8 แผง (5.40 kWp) อินเวอร์เตอร์ไฮบริด Solis S6-EH1P6K-L-PLUS 6 kW สมาร์ทมิเตอร์สำหรับ zero export และ WiFi ดูผลผลิต"),
          ("ผลผลิต", "ประมาณ 7,100–7,900 kWh ต่อปี"),
          ("รวมในงาน", "สาย DC ตู้ AC/DC พร้อมกันฟ้าผ่า ระบบดิน โครงยึด ค่าติดตั้ง บำรุงรักษา 5 ปี และการยื่นขออนุญาต กฟภ."),
          ("ทางเลือก", "เพิ่มแผง 2 แผงเป็น 6.75 kWp หรือเพิ่มแบตเตอรี่ 16 kWh สำหรับไฟสำรองและใช้กลางคืน")])}),
 ("quotation-5-4kwp-huawei-aiko", HUA, "en", {
  "en": ("18 November 2026 · Sample quotation", "5.4 kWp on-grid: Huawei 5 kW with AIKO 675 W panels",
         "The same 5.4 kWp array with a Huawei single-phase inverter with arc-fault protection. Prices removed.",
         [("Equipment", "8 × AIKO ABC 675 W panels (5.40 kWp), Huawei SUN2000-5K-LB0 5 kW inverter with AFCI, battery-ready, and a DDSU666-H power sensor for zero export."),
          ("Output", "About 7,100–7,900 kWh a year."),
          ("Included", "DC cable, AC/DC combiner box with surge protection, earthing, mounting, installation, 5-year maintenance and the PEA application."),
          ("Option", "A WiFi dongle if the site needs it for monitoring.")]),
  "th": ("18 พฤศจิกายน 2569 · ตัวอย่างใบเสนอราคา", "ออนกริด 5.4 kWp: Huawei 5 kW กับแผง AIKO 675 W",
         "แผงชุดเดียวกัน 5.4 kWp กับอินเวอร์เตอร์ Huawei 1 เฟสที่มีระบบป้องกันอาร์ก ตัดราคาออกแล้ว",
         [("อุปกรณ์", "แผง AIKO ABC 675 W × 8 แผง (5.40 kWp) อินเวอร์เตอร์ Huawei SUN2000-5K-LB0 5 kW มี AFCI รองรับแบตเตอรี่ และเซนเซอร์ DDSU666-H สำหรับ zero export"),
          ("ผลผลิต", "ประมาณ 7,100–7,900 kWh ต่อปี"),
          ("รวมในงาน", "สาย DC ตู้ AC/DC พร้อมกันฟ้าผ่า ระบบดิน โครงยึด ค่าติดตั้ง บำรุงรักษา 5 ปี และการยื่นขออนุญาต กฟภ."),
          ("ทางเลือก", "WiFi dongle หากหน้างานต้องใช้ดูผลผลิต")])}),
 ("pv-module-comparison-aiko675-longi650", CMP, "th", {
  "en": ("18 November 2026 · Technical comparison", "Panel comparison: AIKO 675 W vs LONGi Hi-MO X10 Guardian Anti-Glare 650 W",
         "A datasheet comparison of two Tier 1 back-contact panels, checked against our 14.5 kWp house package (Thai PDF).",
         [("AIKO 675 W", "About 3.8% more power from the same panel size, 25.0% efficiency, and about 4 kg lighter per panel (28.2 vs 32.5 kg)."),
          ("LONGi Guardian 650 W", "Anti-glare glass, glass-glass build and some rear-side gain (bifacial), though on a tiled house roof that adds only about 0–5%."),
          ("Same on both", "Size, temperature coefficient, degradation, load and hail ratings, and a 30-year linear power warranty. Both fit the 10 kW Solis package without changes."),
          ("Our advice", "Glare-sensitive sites: LONGi Guardian. Small or weak roofs: AIKO. Otherwise choose on price per watt.")]),
  "th": ("18 พฤศจิกายน 2569 · เปรียบเทียบทางเทคนิค", "เปรียบเทียบแผง AIKO 675 W กับ LONGi Hi-MO X10 Guardian Anti-Glare 650 W",
         "เปรียบเทียบจาก datasheet ของแผง Tier 1 ชนิดขั้วไฟฟ้าด้านหลัง 2 รุ่น และตรวจความเหมาะสมกับแพ็กเกจบ้าน 14.5 kWp",
         [("AIKO 675 W", "กำลังผลิตต่อแผงสูงกว่าประมาณ 3.8% ในขนาดเท่ากัน ประสิทธิภาพ 25.0% และเบากว่าแผงละประมาณ 4 กก. (28.2 กับ 32.5 กก.)"),
          ("LONGi Guardian 650 W", "กระจกป้องกันแสงสะท้อน กระจก 2 ชั้น และรับแสงด้านหลังได้ แต่บนหลังคากระเบื้องของบ้านได้เพิ่มเพียงราว 0–5%"),
          ("ที่เท่ากัน", "ขนาด สัมประสิทธิ์อุณหภูมิ การเสื่อมสภาพ การรับแรงกดและลูกเห็บ และรับประกันกำลังผลิตเชิงเส้น 30 ปี ใช้กับแพ็กเกจ Solis 10 kW ได้ทั้งคู่"),
          ("คำแนะนำ", "หน้างานที่ต้องระวังแสงสะท้อน: LONGi Guardian · หลังคาเล็กหรือโครงรับน้ำหนักได้น้อย: AIKO · กรณีอื่น: เลือกตามราคาต่อวัตต์")])}),
 ("package-house-chiangrai-14-5kwp", PKG, "th", {
  "en": ("18 November 2026 · Package", "Small-medium package for a house in Chiang Rai: 14.5 kWp, two choices",
         "A 14.5 kWp system with a 10 kW single-phase hybrid inverter, with or without a battery (Thai PDF, prices removed).",
         [("Package 1", "16 kWh LiFePO4 battery, MDB & ATS board: the whole house keeps power in a cut (up to 10 kW). Uses about 90% of its own solar; payback about 7.9 years."),
          ("Package 2", "No battery or ATS, with a battery addable later. Payback about 8.0 years."),
          ("Equipment", "Tier 1 anti-glare panels (LONGi, AIKO or equal), Solis 10 kW hybrid or equal, Suntree DC box, Yazaki and PV1-F cable, IMC conduit and copper-clad earth rods."),
          ("Included", "5-year installation warranty, yearly panel cleaning and maintenance for 5 years, and the PEA sell-back application with an engineer-certified single-line diagram.")]),
  "th": ("18 พฤศจิกายน 2569 · แพ็กเกจ", "แพ็กเกจขนาดเล็ก–กลาง สำหรับบ้านในเชียงราย 14.5 kWp มี 2 แบบให้เลือก",
         "ระบบ 14.5 kWp อินเวอร์เตอร์ไฮบริด 10 kW 1 เฟส แบบมีและไม่มีแบตเตอรี่ (ตัดราคาออกแล้ว)",
         [("แพ็กเกจ 1", "แบตเตอรี่ LiFePO4 16 kWh ตู้ MDB & ATS ไฟดับยังมีไฟใช้ทั้งบ้าน (ไม่เกิน 10 kW) ใช้ไฟจากระบบเองราว 90% คืนทุนประมาณ 7.9 ปี"),
          ("แพ็กเกจ 2", "ไม่มีแบตเตอรี่และ ATS เพิ่มแบตเตอรี่ภายหลังได้ คืนทุนประมาณ 8.0 ปี"),
          ("อุปกรณ์", "แผง Tier 1 ป้องกันแสงสะท้อน (LONGi, AIKO หรือเทียบเท่า) Solis ไฮบริด 10 kW หรือเทียบเท่า ตู้ DC Suntree สาย Yazaki และ PV1-F ท่อ IMC หลักดินหุ้มทองแดง"),
          ("รวมในราคา", "รับประกันงานติดตั้ง 5 ปี ล้างแผงและบำรุงรักษาปีละครั้ง 5 ปี และยื่นขอขายไฟ กฟภ. พร้อมแบบ Single-line diagram รับรองโดยวิศวกร")])}),
 ("carbon-credits-norway-solar", CO2, "th", {
  "en": ("17 November 2026 · Global Adoption", "Carbon credits and solar: Norway's new deals and what they mean in Thailand",
         "At COP in November 2026 Norway signed Article 6.2 deals to pay for emission cuts abroad, including solar. Our briefing looks at Thailand's position (Thai PDF).",
         [("The deals", "Norway may buy up to 12 million tonnes of CO₂ cuts from Indonesia and 8.78 million from Morocco over 10 years, and plans about US$2.7 billion for Article 6 in 2027."),
          ("Thailand", "Thailand has already sold credits to Switzerland under Article 6, signed a deal with Singapore, and runs its own T-VER scheme through TGO."),
          ("Prices", "Credits from Thai solar sell for only about 45–250 baht per tonne, so small rooftop systems earn little on their own; bundling many sites (PoA) is the route."),
          ("For customers", "Business customers facing ETS and the EU's CBAM can use yearly CO₂ and clean-energy reports from their solar for ESG reporting.")]),
  "th": ("17 พฤศจิกายน 2569 · การติดตั้งโซลาร์ทั่วโลก", "คาร์บอนเครดิตกับพลังงานแสงอาทิตย์: ข้อตกลงใหม่ของนอร์เวย์ และความหมายต่อประเทศไทย",
         "ในการประชุม COP เดือนพฤศจิกายน 2569 นอร์เวย์ลงนามข้อตกลงตาม Article 6.2 เพื่อซื้อผลการลดก๊าซจากต่างประเทศ รวมถึงโครงการโซลาร์",
         [("ข้อตกลง", "นอร์เวย์อาจซื้อผลการลด CO₂ สูงสุด 12 ล้านตันจากอินโดนีเซีย และ 8.78 ล้านตันจากโมร็อกโกใน 10 ปี และวางงบ Article 6 ราว 2,700 ล้านดอลลาร์ในปี 2570"),
          ("ประเทศไทย", "ไทยขายคาร์บอนเครดิตให้สวิตเซอร์แลนด์แล้วภายใต้ Article 6 มีข้อตกลงกับสิงคโปร์ และมีระบบ T-VER ของ อบก."),
          ("ราคา", "เครดิตจากโซลาร์ในไทยราคาเพียงราว 45–250 บาทต่อตัน ระบบหลังคาขนาดเล็กได้ไม่มาก ต้องรวมกลุ่มหลายระบบ (PoA)"),
          ("สำหรับลูกค้า", "ลูกค้าธุรกิจที่ต้องเจอ ETS และ CBAM ของสหภาพยุโรป ใช้รายงาน CO₂ และพลังงานสะอาดรายปีจากโซลาร์ประกอบรายงาน ESG ได้")])}),
]

L = {"en": dict(open="Open the PDF ↓", lang={"en": "English", "th": "Thai"}, alt="First page of the Solar ESS document", note="Prices, names and customer details removed."),
     "th": dict(open="เปิด PDF ↓", lang={"en": "ภาษาอังกฤษ", "th": "ภาษาไทย"}, alt="หน้าแรกของเอกสาร Solar ESS", note="ตัดราคา ชื่อ และข้อมูลลูกค้าออกแล้ว")}


def article(aid, pdf, plang, lang, t, first):
    eb, h2, lede, pts = t
    lis = "".join(f'<li style="margin-bottom:10px"><b>{a}:</b> {b}</li>' for a, b in pts)
    style = 'style="max-width:760px"' if first else SEP
    return (f'<article id="{aid}" {style}>\n'
            f'<p class="eyebrow">{eb}</p><h2 style="font-size:clamp(26px,3.6vw,40px)">{h2}</h2>\n'
            f'<p class="lede" style="margin-top:16px;opacity:1">{lede}</p>\n'
            f'<ul style="margin-top:22px;padding-left:20px">{lis}</ul>\n'
            f'<p style="margin-top:22px"><a href="{pdf}"><img src="{thumb(pdf)}" alt="{L[lang]["alt"]}" width="579" height="819" loading="lazy" '
            f'style="width:100%;max-width:360px;height:auto;border:1.5px solid var(--line)"></a></p>\n'
            f'<p style="margin-top:18px;display:flex;gap:10px;flex-wrap:wrap"><a class="btn" href="{pdf}" download>{L[lang]["open"]} · {L[lang]["lang"][plang]}</a></p>\n'
            f'<p style="margin-top:20px;font-size:14px;color:var(--mute)">{L[lang]["note"]} Solar ESS Working Group.</p>\n</article>\n')


for lang, path in (("en", "news.html"), ("th", "th/news.html")):
    p = ROOT / path
    s = p.read_text(encoding="utf-8")
    for aid, *_ in A:
        s = re.sub(rf'<article id="{aid}".*?</article>\n?', "", s, flags=re.S)
    m = re.search(r'<article id="([^"]+)"( data-topics="[^"]*")? style="[^"]*">', s)
    old_first = re.sub(r'style="[^"]*"', SEP, m.group(0))
    block = "".join(article(aid, pdf, pl, lang, d[lang], i == 0) for i, (aid, pdf, pl, d) in enumerate(A))
    s = s[:m.start()] + block + old_first + s[m.end():]
    p.write_text(s, encoding="utf-8")
    print(path, len(A), "articles before", m.group(1))

# Quotation pages
Q = [("sample-5-4kwp-solis-hybrid-aiko", SOL, A[1]), ("sample-5-4kwp-huawei-aiko", HUA, A[2]), ("sample-14-5kwp-house-package", PKG, A[4])]
META = {"en": {SOL: "Quotation report · 2 pages · PDF · English", HUA: "Quotation report · 2 pages · PDF · English", PKG: "Package proposal · 6 pages · PDF · Thai"},
        "th": {SOL: "ใบเสนอราคา · 2 หน้า · PDF · ภาษาอังกฤษ", HUA: "ใบเสนอราคา · 2 หน้า · PDF · ภาษาอังกฤษ", PKG: "ข้อเสนอแพ็กเกจ · 6 หน้า · PDF · ภาษาไทย"}}
for lang, path in (("en", "quotation.html"), ("th", "th/quotation.html")):
    B = ["Open the PDF", "Download", "Ask for a price", "/#consult"] if lang == "en" else ["เปิด PDF", "ดาวน์โหลด", "ขอราคา", "/th/#consult"]
    N = "Customer details and prices have been removed." if lang == "en" else "ตัดข้อมูลลูกค้าและราคาออกแล้ว"
    out = ""
    for qid, pdf, a in Q:
        eb, h2, lede, pts = a[3][lang]
        lis = "".join(f"<li>{x}: {y}</li>" for x, y in pts)
        out += (f'<article class="tnote" id="{qid}"><a href="{pdf}"><img src="{thumb(pdf)}" alt="{h2}" width="579" height="819" loading="lazy"></a>'
                f'<div><p class="meta">{META[lang][pdf]}</p><h2>{h2}</h2><p>{lede}</p><ul>{lis}</ul><p class="meta" style="margin-top:12px">{N}</p>'
                f'<div class="acts"><a class="btn" href="{pdf}">{B[0]}</a><a class="btn ghost" href="{pdf}" download>{B[1]}</a>'
                f'<a class="btn ghost" href="{B[3]}">{B[2]}</a></div></div></article>\n')
    p = ROOT / path
    s = p.read_text(encoding="utf-8")
    s = re.sub(r"<!--q1118-->.*?<!--/q1118-->\n?", "", s, flags=re.S)
    i = s.index('<article class="tnote"')
    s = s[:i] + "<!--q1118-->" + out + "<!--/q1118-->\n" + s[i:]
    p.write_text(s, encoding="utf-8")
    print(path, len(Q), "samples")
