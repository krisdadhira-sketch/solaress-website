# -*- coding: utf-8 -*-
"""Technical page batch 25 Nov 2026 (Kris's request: "add post code and publish in the suitable heading").
Five PDFs cleaned with tools/clean_quote_pdf.py (no prices, no personal names, no customer details, no exact
locations; watermark on every page). Each entry shows the plant code or postcode area.
  Case study: Koh Samui resort ATS / grid failures (DH-84320-20-01), PEA units vs DeyeCloud at a chicken farm
              (DG-57270-20-01), ROLLER 600 cost-saving proposal (SG-57100-20-01).
  System design: 16.90 kWp / 10 kW hybrid design + BOM near Mae Hong Son (58000), AC combiner box labelled photo.
NOT published: the letter to the Samui resort (private correspondence, contract amounts) and the ATS job sheet
(already on the Jobs page since 24 Nov).
Idempotent (<!--t1125--> markers). Run, then tools/build_share.py, tools/site_search.py, tools/analytics_tag.py."""
import re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = "downloads/"
SAMUI = D + "Solar-ESS-Case-Study-Koh-Samui-Resort-When-The-Lights-Went-Out_Rev18_WM_20261125.pdf"
FARM = D + "Solar-ESS-Technical-Note-PEA-Units-vs-Solar-Data-Chicken-Farm_Rev01_WM_20261125.pdf"
ROLL = D + "Solar-ESS-Roller-600-Cost-Saving-Proposal-TH_Rev01_WM_20261125.pdf"
MHS = D + "Solar-ESS-Hybrid-16.9kWp-10kW-Design-BOM-Mae-Hong-Son-TH_Rev05_WM_20261125.pdf"
ACB = D + "Solar-ESS-AC-Combiner-Box-Labelled_Rev03_WM_20261125.pdf"


def thumb(pdf, nid):
    out = ROOT / "images" / f"note-{nid}.jpg"
    if not out.exists():
        subprocess.run(["pdftoppm", "-r", "70", "-jpeg", "-jpegopt", "quality=85", "-f", "1", "-l", "1", "-singlefile",
                        str(ROOT / pdf), str(out.with_suffix(""))], check=True)
    w, h = (819, 579) if pdf == ACB and False else (579, 819)
    return f"images/note-{nid}.jpg", w, h


def pages(pdf):
    out = subprocess.run(["pdfinfo", str(ROOT / pdf)], capture_output=True, text=True).stdout
    return int(re.search(r"Pages:\s+(\d+)", out).group(1))


# (section, id, pdf, pdf_lang, code, {lang: (kind, h2, p, [li])})
N = [
 ("cases", "koh-samui-resort-lights-went-out", SAMUI, "en", "DH-84320-20-01", {
  "en": ("Case study", "DH-84320-20-01 · When the lights went out: a Koh Samui resort and its solar backup",
         "A 20 kW Deye hybrid with 20.48 kWp and three batteries (postcode area 84320, Koh Samui) was built to cut the PEA bill for about 40 kWh a day. The resort now uses 150–180 kWh a day in high season, the standby generator was removed, and in November repeated grid failures left the ATS stuck on backup and the resort in the dark.",
         ["What the plant was designed for, and what it can and cannot do", "Monitoring data: daily load, peaks up to 28.6 kW and night use against the battery", "The 9–23 November timeline: brownouts, the ATS failure and the blackout", "What full standalone backup would need: about double the system", "Four ways forward, from an essential-loads board to an auto-start generator"]),
  "th": ("กรณีศึกษา", "DH-84320-20-01 · เมื่อไฟดับ: รีสอร์ทบนเกาะสมุยกับระบบไฟสำรองโซลาร์",
         "ระบบไฮบริด Deye 20 kW แผง 20.48 kWp และแบตเตอรี่ 3 ชุด (รหัสไปรษณีย์ 84320 เกาะสมุย) ออกแบบมาเพื่อลดค่าไฟ กฟภ. สำหรับการใช้ไฟประมาณ 40 หน่วยต่อวัน ปัจจุบันรีสอร์ทใช้ไฟ 150–180 หน่วยต่อวันในช่วงไฮซีซั่น เครื่องปั่นไฟสำรองถูกถอดออก และในเดือนพฤศจิกายน ไฟการไฟฟ้าตกและดับซ้ำหลายครั้งจน ATS ค้างอยู่ฝั่งไฟสำรองและรีสอร์ทไฟดับ",
         ["ระบบออกแบบมาเพื่ออะไร ทำอะไรได้และทำอะไรไม่ได้", "ข้อมูลจากระบบติดตาม: โหลดรายวัน พีคสูงสุด 28.6 kW และการใช้ไฟกลางคืนเทียบกับแบตเตอรี่", "ลำดับเหตุการณ์ 9–23 พ.ย.: ไฟตก ATS เสีย และไฟดับทั้งรีสอร์ท", "ถ้าจะสำรองไฟได้ทั้งรีสอร์ทต้องขยายระบบประมาณเท่าตัว", "สี่ทางเลือก ตั้งแต่ตู้แยกโหลดสำคัญจนถึงเครื่องปั่นไฟสตาร์ทอัตโนมัติ (เอกสารภาษาอังกฤษ)"])}),
 ("cases", "pea-units-vs-solar-data-chicken-farm", FARM, "en", "DG-57270-20-01", {
  "en": ("Technical note", "DG-57270-20-01 · Why the PEA meter bills 1,100–2,000 more units than the solar data",
         "At a chicken farm in Chiang Rai (postcode area 57270), the PEA bill is 1,100–2,000 units a month higher than what DeyeCloud records as bought from the grid. The solar production is measured correctly; the inverter's CT is most likely not seeing the whole farm.",
         ["The gap in numbers: 37–67 kWh a day of unseen use", "Most likely first: loads wired between the PEA meter and the CT", "A reversed CT or a CT on the wrong phase, and the fingerprint it leaves", "How to find the real cause on site"]),
  "th": ("บันทึกทางเทคนิค", "DG-57270-20-01 · ทำไมมิเตอร์ กฟภ. คิดหน่วยมากกว่าข้อมูลโซลาร์ 1,100–2,000 หน่วย",
         "ฟาร์มไก่แห่งหนึ่งในเชียงราย (รหัสไปรษณีย์ 57270) บิล กฟภ. สูงกว่าหน่วยที่ DeyeCloud บันทึกว่าซื้อจากการไฟฟ้า 1,100–2,000 หน่วยต่อเดือน การวัดไฟที่แผงผลิตได้ถูกต้อง แต่ CT ของอินเวอร์เตอร์น่าจะวัดไม่ครบทั้งฟาร์ม",
         ["ส่วนต่างเป็นตัวเลข: ใช้ไฟที่มองไม่เห็นวันละ 37–67 หน่วย", "สาเหตุที่น่าจะเป็นที่สุด: โหลดที่ต่ออยู่ระหว่างมิเตอร์ กฟภ. กับ CT", "CT กลับด้านหรืออยู่ผิดเฟส และร่องรอยที่เห็นในข้อมูล", "วิธีหาสาเหตุจริงที่หน้างาน (เอกสารภาษาอังกฤษ)"])}),
 ("cases", "roller-600-cost-saving", ROLL, "th", "SG-57100-20-01", {
  "en": ("Proposal", "SG-57100-20-01 · ROLLER 600: cutting the heat press bill by almost half",
         "A follow-up to the heat press case study at the same Chiang Rai factory (postcode area 57100): the most cost-effective way to cut the machine's electricity bill of about 42,000 THB a month. Thai PDF; prices removed.",
         ["Reduce the energy the machine needs first, then generate it", "Three measures together: about −46% on the bill at 8 hours a day", "30 kWp on-grid solar without a battery pays back in about 5.4 years", "Why the 60 kWh battery in the earlier proposal is not recommended (about 16 years payback)"]),
  "th": ("ข้อเสนอ", "SG-57100-20-01 · ROLLER 600: ลดค่าไฟเครื่องรีดร้อนเกือบครึ่งหนึ่ง",
         "ต่อยอดจากกรณีศึกษาเครื่องรีดร้อนที่โรงงานเดียวกันในเชียงราย (รหัสไปรษณีย์ 57100) หาวิธีที่คุ้มค่าที่สุดในการลดค่าไฟของเครื่อง ซึ่งอยู่ที่ประมาณ 42,000 บาทต่อเดือน ตัดราคาออกแล้ว",
         ["ลดพลังงานที่เครื่องต้องใช้ก่อน แล้วจึงผลิตไฟเอง", "สามมาตรการรวมกัน ลดค่าไฟได้ประมาณ 46% เมื่อเดินเครื่อง 8 ชั่วโมงต่อวัน", "โซลาร์ออนกริด 30 kWp ไม่มีแบตเตอรี่ คืนทุนประมาณ 5.4 ปี", "ทำไมไม่แนะนำแบตเตอรี่ 60 kWh ตามข้อเสนอเดิม (คืนทุนประมาณ 16 ปี)"])}),
 ("design", "hybrid-16-9kwp-10kw-mae-hong-son", MHS, "th", "58000", {
  "en": ("System design", "Postcode 58000 · 16.90 kWp hybrid with 10 kW and 16 kWh: roof design and bill of materials",
         "Rooftop design for a two-storey building near Mae Hong Son town (postcode area 58000): 26 LONGi Hi-MO X10 Anti-Glare 650 W panels in two rows on the southwest-facing roof, a Solis 10 kW three-phase hybrid and a 16 kWh battery. Thai PDF.",
         ["Roof layout: 2 rows of 13 panels, out of sight from the guest balconies", "About 55–58 kWh a day, 20,500 kWh a year", "Selected circuits stay on when the PEA grid fails", "Full bill of materials by category"]),
  "th": ("ออกแบบระบบ", "รหัสไปรษณีย์ 58000 · ไฮบริด 16.90 kWp อินเวอร์เตอร์ 10 kW แบตเตอรี่ 16 kWh: แบบติดตั้งบนหลังคาและรายการวัสดุ",
         "แบบติดตั้งบนหลังคาอาคาร 2 ชั้นใกล้ตัวเมืองแม่ฮ่องสอน (รหัสไปรษณีย์ 58000) แผง LONGi Hi-MO X10 Anti-Glare 650 W × 26 แผง 2 แถว บนหลังคาด้านทิศตะวันตกเฉียงใต้ ไฮบริดอินเวอร์เตอร์ Solis 10 kW 3 เฟส และแบตเตอรี่ 16 kWh",
         ["ผังหลังคา: 2 แถว แถวละ 13 แผ่น มองไม่เห็นจากระเบียงห้องพัก", "ผลิตไฟประมาณ 55–58 หน่วยต่อวัน หรือ 20,500 หน่วยต่อปี", "วงจรที่เลือกไว้มีไฟใช้ต่อเมื่อไฟ กฟภ. ดับ", "รายการวัสดุครบตามหมวด"])}),
 ("design", "ac-combiner-box-labelled", ACB, "en", None, {
  "en": ("Reference photo", "AC combiner box with ATS: every device labelled",
         "A real AC combiner box from a single-phase hybrid installation with an automatic transfer switch. Each of the nine devices is numbered and described, and the grid connections are marked.",
         ["MCB, CT, main MCCB and RCBO with their ratings", "The dual-power ATS: normal and standby sides, Auto/Manual and the selector", "Type 2 SPD values (Uc, In, Imax, Up) and the earth bar", "Where the PEA grid, the inverter's grid port and the load connect"]),
  "th": ("ภาพอ้างอิง", "ตู้ AC Combiner พร้อม ATS: ระบุชื่อทุกอุปกรณ์",
         "ตู้ AC Combiner จากงานติดตั้งไฮบริด 1 เฟส พร้อมสวิตช์สลับไฟอัตโนมัติ (ATS) อุปกรณ์ทั้ง 9 รายการมีหมายเลขและคำอธิบาย พร้อมจุดต่อไฟการไฟฟ้า",
         ["MCB, CT, เมน MCCB และ RCBO พร้อมพิกัด", "ATS แบบ dual power: ฝั่งไฟหลักและไฟสำรอง Auto/Manual และตัวเลือก", "ค่าของ SPD Type 2 (Uc, In, Imax, Up) และบาร์กราวด์", "จุดต่อไฟ กฟภ. พอร์ตกริดของอินเวอร์เตอร์ และโหลด (เอกสารภาษาอังกฤษ)"])}),
]

UI = {"en": dict(open="Open the PDF", dl="Download", pc="Plant code", post="Postcode area", lang={"en": "English", "th": "Thai"}, pg="pages", pg1="page",
                 note="Prices, names and customer details removed.", alt="First page of"),
      "th": dict(open="เปิด PDF", dl="ดาวน์โหลด", pc="รหัสโรงไฟฟ้า", post="รหัสไปรษณีย์", lang={"en": "ภาษาอังกฤษ", "th": "ภาษาไทย"}, pg="หน้า", pg1="หน้า",
                 note="ตัดราคา ชื่อ และข้อมูลลูกค้าออกแล้ว", alt="หน้าแรกของ")}


def entry(lang, nid, pdf, plang, code, t):
    u = UI[lang]
    kind, h2, p, lis = t[lang]
    pre = "" if lang == "en" else "/"
    img, w, h = thumb(pdf, nid)
    n = pages(pdf)
    if code and "-" in code:
        tag = f' <a class="pcode" href="#plant-{code}">{u["pc"]} {code}</a>'
    elif code:
        tag = f' <span class="pcode">{u["post"]} {code}</span>'
    else:
        tag = ""
    meta = f'{kind} · {n} {u["pg"] if n > 1 else u["pg1"]} · PDF · {u["lang"][plang]}{tag}'
    li = "".join(f"<li>{x}</li>" for x in lis)
    return (f'<article class="tnote" id="{nid}"><a href="{pre}{pdf}"><img src="{pre}{img}" alt="{u["alt"]} {h2}" width="{w}" height="{h}" loading="lazy"></a>\n'
            f'<div><p class="meta">{meta}</p><h2>{h2}</h2>\n<p>{p}</p>\n<ul>{li}</ul>\n'
            f'<p class="meta" style="margin-top:10px">{u["note"]} Solar ESS Working Group.</p>\n'
            f'<div class="acts"><a class="btn" href="{pre}{pdf}">{u["open"]}</a><a class="btn ghost" href="{pre}{pdf}" download>{u["dl"]}</a></div></div></article>\n')


for lang, path in (("en", "technical-notes.html"), ("th", "th/technical-notes.html")):
    f = ROOT / path
    s = f.read_text(encoding="utf-8")
    s = re.sub(r"<!--t1125-->.*?<!--/t1125-->\n?", "", s, flags=re.S)
    for sec in ("design", "cases"):
        block = "".join(entry(lang, nid, pdf, pl, code, t) for se, nid, pdf, pl, code, t in N if se == sec)
        m = re.search(rf'(<section class="topicsec" id="topic-{sec}"><h2 class="th">[^<]*<small>)(\d+)( [^<]*</small></h2><div class="notes">\n?)', s)
        body_end = s.index("</section>", m.end())
        count = s[m.end():body_end].count('class="tnote"') + block.count('class="tnote"')
        s = s[:m.start()] + m.group(1) + str(count) + m.group(3) + "<!--t1125-->" + block + "<!--/t1125-->\n" + s[m.end():]
        print(path, sec, "now", count)
    f.write_text(s, encoding="utf-8")
