# -*- coding: utf-8 -*-
"""Technical page batch 27 Nov 2026 (Kris: "publish these articles on www.solaress.org"; skip any published before).
Nine PDFs cleaned with tools/clean_quote_pdf.py (no prices, no personal names, no customer details, no exact
locations; watermark on every page). The Solis design report is image-only: name, address, coordinates, site photo
and page headers painted over, then the pages flattened.
  System design: two-house shared hybrid, Chiang Rai (57100) - TH proposal 100 kWh Rev08, EN proposal 60 kWh Rev06,
                 SLD Rev08, Solis design report Rev08 (one entry, four PDFs).
                 Off-grid cafe new building, Mae Suai (57180) - 4-option comparison, energy graphs (new building and
                 new rooms), load and solar sizing TN-20261020-OG-01 (one entry, four PDFs).
  Safety: 50 kW off-grid hybrid safety brief (Solis S6-EH3P50K-H + FlexCore-ID 100 kWh).
NOT published: Main House load and battery report Rev03 (Rev02 already published on the News page on 21 Nov).
Idempotent (<!--t1127--> markers). Run, then tools/build_share.py, tools/site_search.py, tools/analytics_tag.py."""
import re, subprocess
from pathlib import Path
import pymupdf as fitz

ROOT = Path(__file__).resolve().parents[1]
D = "downloads/"
MK_TH = D + "Solar-ESS-Two-House-Shared-Hybrid-19.6kWp-100kWh-Proposal-TH_Rev08_WM_20261127.pdf"
MK_EN = D + "Solar-ESS-Two-House-Shared-Hybrid-19.6kWp-60kWh-Proposal_Rev06_WM_20261127.pdf"
MK_SLD = D + "Solar-ESS-Two-House-Shared-Hybrid-SLD_Rev08_WM_20261127.pdf"
MK_REP = D + "Solar-ESS-Two-House-Shared-Hybrid-Solis-Design-Report_Rev08_WM_20261127.pdf"
OG_CMP = D + "Solar-ESS-Offgrid-Cafe-New-Building-4-Option-Comparison-TH_Rev01_WM_20261127.pdf"
OG_GB = D + "Solar-ESS-Offgrid-Cafe-New-Building-Energy-Graphs-TH_Rev01_WM_20261127.pdf"
OG_GR = D + "Solar-ESS-Offgrid-Cafe-New-Rooms-Energy-Graphs-TH_Rev02_WM_20261127.pdf"
OG_LS = D + "Solar-ESS-Offgrid-Cafe-Load-and-Solar-Sizing-TH_Rev01_WM_20261127.pdf"
SAFE = D + "Solar-ESS-Safety-Brief-50kW-Offgrid-Solis-FlexCore-ID-100kWh_Rev01_WM_20261127.pdf"


def thumb(pdf, nid):
    out = ROOT / "images" / f"note-{nid}.jpg"
    if not out.exists():
        subprocess.run(["pdftoppm", "-r", "70", "-jpeg", "-jpegopt", "quality=85", "-f", "1", "-l", "1", "-singlefile",
                        str(ROOT / pdf), str(out.with_suffix(""))], check=True)
    r = fitz.open(ROOT / pdf)[0].rect
    return f"images/note-{nid}.jpg", round(r.width * 70 / 72), round(r.height * 70 / 72)


def pages(pdf):
    return len(fitz.open(ROOT / pdf))


# extra documents: (pdf, pdf_lang, {lang: label})
N = [
 ("design", "two-house-shared-hybrid-chiang-rai", MK_TH, "th", "57100", [
    (MK_EN, "en", {"en": "Proposal, 60 kWh option (Rev06)", "th": "ข้อเสนอ ทางเลือกแบตเตอรี่ 60 kWh (Rev06)"}),
    (MK_SLD, "en", {"en": "Single-line diagram (Rev08)", "th": "Single Line Diagram (Rev08)"}),
    (MK_REP, "en", {"en": "Solis design report (Rev08)", "th": "รายงานออกแบบ Solis (Rev08)"})], {
  "en": ("System design", "Postcode 57100 · One hybrid system for two houses: 19.575 kWp, 20 kW + 10 kW and 100 kWh",
         "Two neighbouring houses in Chiang Rai (postcode area 57100) use about 1,850 kWh a month together and cannot sell surplus solar to PEA. One zero-export system serves both: 29 AIKO 675 W panels on House B's roof, a Solis 20 kW three-phase hybrid with a 100 kWh high-voltage battery at House B, and the existing Huawei 10 kW on-grid inverter AC-coupled into the Solis. Thai proposal (100 kWh), English proposal (60 kWh option), single-line diagram and Solis design report.",
         ["Monthly PEA use of both houses and what the system covers: about 93% of the yearly bill, 76–90% in the wettest months",
          "Why zero export, and how AC coupling lets the Huawei inverter keep working during a power cut",
          "Two ATS units: House B is fed from the Solis backup output, House A falls back to its own PEA meter; the two meters are never joined",
          "TN-C-S earthing: one N-G link at each service main, all feeders with separate N and PE",
          "Solis side: 2 strings of 7 panels, about 13,400 kWh a year from the 9.45 kWp on the Solis",
          "60 kWh or 100 kWh: the bigger battery adds backup time during outages more than savings"]),
  "th": ("ออกแบบระบบ", "รหัสไปรษณีย์ 57100 · ระบบไฮบริดเดียวสำหรับบ้าน 2 หลัง: 19.575 kWp อินเวอร์เตอร์ 20 + 10 kW แบตเตอรี่ 100 kWh",
         "บ้าน 2 หลังที่อยู่ติดกันในเชียงราย (รหัสไปรษณีย์ 57100) ใช้ไฟรวมกันประมาณ 1,850 หน่วยต่อเดือน และขายไฟส่วนเกินคืน กฟภ. ไม่ได้ จึงออกแบบระบบไม่ส่งไฟย้อน (Zero Export) ระบบเดียวจ่ายไฟทั้ง 2 หลัง: แผง AIKO 675 W 29 แผงบนหลังคาบ้าน B ไฮบริดอินเวอร์เตอร์ Solis 20 kW 3 เฟส กับแบตเตอรี่แรงดันสูง 100 kWh ที่บ้าน B และอินเวอร์เตอร์ออนกริด Huawei 10 kW เดิมต่อแบบ AC-coupled เข้า Solis มีข้อเสนอภาษาไทย (100 kWh) ข้อเสนอภาษาอังกฤษ (ทางเลือก 60 kWh) Single Line Diagram และรายงานออกแบบ Solis",
         ["การใช้ไฟของบ้านทั้ง 2 หลังจากบันทึก กฟภ. และระบบครอบคลุมได้เท่าไร: ประมาณ 93% ของค่าไฟทั้งปี และ 76–90% ในเดือนที่ฝนตกชุก",
          "ทำไมต้อง Zero Export และ AC coupling ทำให้อินเวอร์เตอร์ Huawei ยังทำงานได้ตอนไฟดับอย่างไร",
          "ATS 2 ชุด: บ้าน B รับไฟจากช่อง Backup ของ Solis บ้าน A สลับกลับไปใช้มิเตอร์ กฟภ. ของตัวเอง มิเตอร์ 2 ลูกไม่ต่อถึงกัน",
          "ระบบกราวด์ TN-C-S: ต่อ N-G จุดเดียวที่เมนของแต่ละหลัง สายป้อนทุกเส้นแยก N และ PE",
          "ฝั่ง Solis: 2 สตริง สตริงละ 7 แผง ผลิตไฟประมาณ 13,400 หน่วยต่อปีจาก 9.45 kWp",
          "60 kWh หรือ 100 kWh: แบตเตอรี่ใหญ่ขึ้นช่วยเรื่องเวลาสำรองไฟตอนไฟดับมากกว่าค่าไฟที่ประหยัดเพิ่ม"])}),
 ("design", "offgrid-cafe-new-building-mae-suai", OG_CMP, "th", "57180", [
    (OG_GB, "th", {"en": "How the system works each day: new building (Rev01)", "th": "ระบบทำงานอย่างไรในแต่ละวัน: บ้านหลังใหม่ (Rev01)"}),
    (OG_GR, "th", {"en": "How the system works each day: 4 new rooms (Rev02)", "th": "ระบบทำงานอย่างไรในแต่ละวัน: ห้องพักใหม่ 4 หลัง (Rev02)"}),
    (OG_LS, "th", {"en": "Load list and off-grid sizing (TN-20261020-OG-01)", "th": "ตารางโหลดและการออกแบบระบบออฟกริด (TN-20261020-OG-01)"})], {
  "en": ("System design", "Postcode 57180 · Off-grid café new building, Mae Suai: four options compared, and how the system runs each day",
         "A new building at an off-grid café and homestay near Mae Suai (postcode area 57180) with four guest rooms, a staff room and storage, and no grid. All options use a Solis 16 kW single-phase hybrid; they differ in batteries (3 or 4 × 16 kWh) and panels (24 or 32 × 650 W). Thai PDFs; prices removed.",
         ["Load: about 38 kWh a day, 32 kWh of it at night; 43.7 kWh a day with system losses",
          "24 panels give 47–59 kWh a day (108–135% of need); 32 panels 63–79 kWh",
          "Generator energy needed after 1 very cloudy day and after 3 part-cloudy days, option by option",
          "How many days the battery needs to refill after a cloudy spell",
          "Daily graphs: solar vs load, battery state of charge over 3 days, and how long the battery lasts with no sun",
          "The original load list and sizing for the whole site (20 Oct 2026)"]),
  "th": ("ออกแบบระบบ", "รหัสไปรษณีย์ 57180 · บ้านหลังใหม่ คาเฟ่ออฟกริด แม่สรวย: เปรียบเทียบ 4 ทางเลือก และระบบทำงานอย่างไรในแต่ละวัน",
         "อาคารใหม่ของคาเฟ่และโฮมสเตย์ระบบออฟกริดใกล้แม่สรวย (รหัสไปรษณีย์ 57180) มีห้องพัก 4 หลัง ห้องพนักงาน และห้องเก็บของ ไม่มีไฟการไฟฟ้า ทุกทางเลือกใช้ไฮบริดอินเวอร์เตอร์ Solis 16 kW 1 เฟส ต่างกันที่แบตเตอรี่ (16 kWh 3 หรือ 4 ก้อน) และแผง (650 W 24 หรือ 32 แผง) ตัดราคาออกแล้ว",
         ["โหลดประมาณ 38 หน่วยต่อวัน ใช้กลางคืน 32 หน่วย รวมการสูญเสียของระบบ 43.7 หน่วยต่อวัน",
          "แผง 24 แผงผลิตได้ 47–59 หน่วยต่อวัน (108–135% ของความต้องการ) แผง 32 แผง 63–79 หน่วย",
          "พลังงานที่ต้องใช้จากเครื่องปั่นไฟหลังฟ้าครึ้มมาก 1 วัน และฟ้าครึ้มบางส่วน 3 วัน แยกตามทางเลือก",
          "แบตเตอรี่ใช้เวลากี่วันจึงกลับมาเต็มหลังช่วงฟ้าครึ้ม",
          "กราฟรายวัน: ไฟจากแผงเทียบโหลด ระดับแบตเตอรี่ 3 วัน และแบตเตอรี่อยู่ได้นานเท่าไรเมื่อไม่มีแดด",
          "ตารางโหลดและการออกแบบเดิมของทั้งพื้นที่ (20 ต.ค. 2569)"])}),
 ("safety", "safety-brief-50kw-offgrid-flexcore", SAFE, "en", None, [], {
  "en": ("Safety brief", "Safety brief: 50 kW off-grid hybrid with a 100 kWh battery for remote resorts and hotels",
         "A Solis S6-EH3P50K-H with a Solis FlexCore-ID 100 kWh LFP battery is suitable and certified for off-grid use. The main risks are on site: the battery is IP20, limited to 85% humidity and weighs about 830 kg, so heat, damp, floods, animals, lightning and slow emergency response at a remote Thai resort must be designed for.",
         ["Battery datasheet: 5 × 20 kWh packs at about 320 V, 157 A recommended, ≥ 8,000 cycles, aerosol fire suppression in every pack",
          "Inverter match: both battery ports are needed for 50 kW; one port alone limits power to about 25 kW",
          "Phase loading: about 16.5 kW per phase at most, so resort loads must be balanced",
          "Standards: EIT codes, IEC 62485-5, IEC 62619 / 63056, NFPA 855 as best practice, ERC notification",
          "Battery room checklist: walls and door, air-conditioning, floor load and flood level, clearances, ventilation, fire detection"]),
  "th": ("สรุปความปลอดภัย", "สรุปความปลอดภัย: ระบบไฮบริดออฟกริด 50 kW แบตเตอรี่ 100 kWh สำหรับรีสอร์ทและโรงแรมที่ไม่มีไฟการไฟฟ้า",
         "Solis S6-EH3P50K-H กับแบตเตอรี่ LFP Solis FlexCore-ID 100 kWh เหมาะและได้รับการรับรองสำหรับระบบออฟกริด ความเสี่ยงหลักอยู่ที่หน้างาน: แบตเตอรี่เป็น IP20 รับความชื้นได้ไม่เกิน 85% และหนักประมาณ 830 กก. รีสอร์ทที่อยู่ห่างไกลต้องออกแบบรับความร้อน ความชื้น น้ำท่วม สัตว์ ฟ้าผ่า และการเข้าช่วยเหลือฉุกเฉินที่ช้า",
         ["ข้อมูลแบตเตอรี่: 20 kWh 5 แพ็ก แรงดันประมาณ 320 V กระแสแนะนำ 157 A อายุ ≥ 8,000 รอบ มีระบบดับเพลิงแบบละอองในทุกแพ็ก",
          "การจับคู่กับอินเวอร์เตอร์: ต้องใช้ช่องแบตเตอรี่ทั้ง 2 ช่องจึงได้ 50 kW ใช้ช่องเดียวได้ประมาณ 25 kW",
          "โหลดต่อเฟส: สูงสุดประมาณ 16.5 kW ต่อเฟส ต้องแบ่งโหลดของรีสอร์ทให้สมดุล",
          "มาตรฐาน: มาตรฐาน วสท. IEC 62485-5, IEC 62619 / 63056, NFPA 855 เป็นแนวปฏิบัติ และการแจ้ง กกพ.",
          "รายการตรวจห้องแบตเตอรี่: ผนังและประตู แอร์ น้ำหนักพื้นและระดับน้ำท่วม ระยะห่าง การระบายอากาศ ระบบตรวจจับไฟ (เอกสารภาษาอังกฤษ)"])}),
]

UI = {"en": dict(open="Open the PDF", dl="Download", more="More documents", post="Postcode area", lang={"en": "English", "th": "Thai"}, pg="pages", pg1="page",
                 note="Prices, names and customer details removed.", alt="First page of"),
      "th": dict(open="เปิด PDF", dl="ดาวน์โหลด", more="เอกสารเพิ่มเติม", post="รหัสไปรษณีย์", lang={"en": "ภาษาอังกฤษ", "th": "ภาษาไทย"}, pg="หน้า", pg1="หน้า",
                 note="ตัดราคา ชื่อ และข้อมูลลูกค้าออกแล้ว", alt="หน้าแรกของ")}


def entry(lang, nid, pdf, plang, code, extra, t):
    u = UI[lang]
    kind, h2, p, lis = t[lang]
    pre = "" if lang == "en" else "/"
    img, w, h = thumb(pdf, nid)
    n = pages(pdf)
    tag = f' <span class="pcode">{u["post"]} {code}</span>' if code else ""
    meta = f'{kind} · {n} {u["pg"] if n > 1 else u["pg1"]} · PDF · {u["lang"][plang]}{tag}'
    li = "".join(f"<li>{x}</li>" for x in lis)
    more = ""
    if extra:
        items = "".join(f'<li><a href="{pre}{x}">{lab[lang]}</a> · PDF · {u["lang"][xl]}</li>' for x, xl, lab in extra)
        more = f'<p class="meta" style="margin-top:10px"><b>{u["more"]}</b></p>\n<ul>{items}</ul>\n'
    return (f'<article class="tnote" id="{nid}"><a href="{pre}{pdf}"><img src="{pre}{img}" alt="{u["alt"]} {h2}" width="{w}" height="{h}" loading="lazy"></a>\n'
            f'<div><p class="meta">{meta}</p><h2>{h2}</h2>\n<p>{p}</p>\n<ul>{li}</ul>\n{more}'
            f'<p class="meta" style="margin-top:10px">{u["note"]} Solar ESS Working Group.</p>\n'
            f'<div class="acts"><a class="btn" href="{pre}{pdf}">{u["open"]}</a><a class="btn ghost" href="{pre}{pdf}" download>{u["dl"]}</a></div></div></article>\n')


for lang, path in (("en", "technical-notes.html"), ("th", "th/technical-notes.html")):
    f = ROOT / path
    s = f.read_text(encoding="utf-8")
    s = re.sub(r"<!--t1127-->.*?<!--/t1127-->\n?", "", s, flags=re.S)
    for sec in ("design", "safety"):
        block = "".join(entry(lang, nid, pdf, pl, code, ex, t) for se, nid, pdf, pl, code, ex, t in N if se == sec)
        m = re.search(rf'(<section class="topicsec" id="topic-{sec}"><h2 class="th">[^<]*<small>)(\d+)( [^<]*</small></h2><div class="notes">\n?)', s)
        body_end = s.index("</section>", m.end())
        count = s[m.end():body_end].count('class="tnote"') + block.count('class="tnote"')
        s = s[:m.start()] + m.group(1) + str(count) + m.group(3) + "<!--t1127-->" + block + "<!--/t1127-->\n" + s[m.end():]
        print(path, sec, "now", count)
    f.write_text(s, encoding="utf-8")
