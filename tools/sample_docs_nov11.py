# -*- coding: utf-8 -*-
"""Sample documents added 11 Nov 2026 (cleaned with tools/clean_quote_pdf.py: no prices, names or exact sites).
- Quotation pages (EN/TH): 16.9 kWp hybrid + 32 kWh battery proposal (Mae Hong Son) and the general 10 kW hybrid
  package (7.8 kWp, 16 kWh, full-house MDB & ATS), at the top of the list, between <!--q1111--> markers.
- EV Charger pages (EN/TH): the "Sample" band becomes "Samples and drawings": EV 2nd circuit Option A/B (Rev15, Thai),
  and single-line diagrams + construction plan for four DC fast-charging stations.
Thumbnails: images/quote-sample-*.jpg / images/ev-sample-*.jpg from page 1 of each PDF. Idempotent.
Run from the repo root: python3 tools/sample_docs_nov11.py, then tools/analytics_tag.py, tools/build_share.py, tools/site_search.py"""
import re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = "/downloads/"
MHS = D + "Solar-ESS-Sample-Hybrid-16.9kWp-15kW-32kWh-Battery-Proposal-TH_Rev01_WM_20261111.pdf"
GEN = D + "Solar-ESS-Sample-General-Hybrid-Package-10kW-16kWh-7.8kWp-FullATS-TH_Rev01_WM_20261111.pdf"
EV2 = D + "Solar-ESS-Sample-EV-2nd-Circuit-Option-A-B-TH_Rev02_WM_20261111.pdf"
EV2_EN = D + "Solar-ESS-Sample-EV-2nd-Circuit-Option-A-B_Rev01_WM_20261111.pdf"
SLD = D + "Solar-ESS-EV-Stations-Single-Line-Diagrams-4-Sites_Rev01_WM_20261111.pdf"
PLAN = D + "Solar-ESS-EV-Stations-Construction-Plan-4-Sites_Rev01_WM_20261111.pdf"
THUMB = {MHS: "quote-sample-hybrid-16-9kwp-32kwh", GEN: "quote-sample-general-hybrid-10kw", EV2: "ev-sample-2nd-circuit-th",
         SLD: "ev-sample-stations-sld", PLAN: "ev-sample-stations-plan"}


def thumbs():
    for pdf, name in THUMB.items():
        out = ROOT / "images" / f"{name}.jpg"
        if not out.exists():
            subprocess.run(["pdftoppm", "-r", "70", "-jpeg", "-jpegopt", "quality=85", "-f", "1", "-l", "1", "-singlefile",
                            str(ROOT / pdf.lstrip("/")), str(out.with_suffix(""))], check=True)


def art(id_, pdf, alt, meta, h2, lead, pts, note, btns, alt_pdf=None, alt_label=""):
    lis = "".join(f"<li>{p}</li>" for p in pts)
    extra = f'<a class="btn ghost" href="{alt_pdf}">{alt_label}</a>' if alt_pdf else ""
    return (f'<article class="tnote" id="{id_}"><a href="{pdf}"><img src="/images/{THUMB[pdf]}.jpg" alt="{alt}" width="579" height="819" loading="lazy"></a>'
            f'<div><p class="meta">{meta}</p><h2>{h2}</h2><p>{lead}</p><ul>{lis}</ul><p class="meta" style="margin-top:12px">{note}</p>'
            f'<div class="acts"><a class="btn" href="{pdf}">{btns[0]}</a><a class="btn ghost" href="{pdf}" download>{btns[1]}</a>{extra}'
            f'<a class="btn ghost" href="{btns[3]}">{btns[2]}</a></div></div></article>\n')


Q = {
 "en": [
  art("hybrid-16-9kwp-32kwh", MHS, "First page of the sample 16.9 kWp hybrid proposal with 32 kWh battery", "Sample proposal · 2 pages · PDF · Thai",
      "16.9 kWp hybrid with a 32 kWh battery, three-phase",
      "A two-storey building near Mae Hong Son on a three-phase supply. Twenty-six anti-glare panels, a 15 kW three-phase hybrid inverter and two 16 kWh batteries in parallel, with an ATS that switches the backed-up loads.",
      ["26 × 650 W anti-glare panels (16.90 kWp), Solis 15 kW 3-phase hybrid inverter (room to grow to 24 kWp), 2 × Solis 16 kWh LiFePO4 batteries (32 kWh)",
       "Itemised scope in 14 lines: products, battery breaker and cables, DC combiner, AC combiner + ATS, cabling, mounting, KCE grounding, transport, PEA application, installation",
       "Six years of panel cleaning and safety checks, plus project administration with Contractor All Risk insurance",
       "One lump-sum price for the whole project (removed here)"],
      "Customer details and prices have been removed from this sample.", ["Open the PDF", "Download", "Ask for a price", "/#consult"]),
  art("general-hybrid-10kw-16kwh", GEN, "First page of the general 10 kW hybrid home package", "Package · 8 pages · PDF · Thai",
      "General home package: 10 kW hybrid, 16 kWh battery, 7.8 kWp, whole-house backup",
      "Our standard package for single-phase homes anywhere in Thailand using about 400–900 kWh a month. The inverter is sized so the roof can grow later, and the MDB &amp; ATS cabinet backs up the whole house, not just a few circuits.",
      ["12 × 650 W anti-glare panels (7.80 kWp) in 2 strings, Solis 10 kW 1-phase hybrid inverter (up to 20 kW of panels), Solis IntelliHome 16 kWh battery",
       "Assembled MDB &amp; ATS cabinet: whole-house backup, and the ATS returns the house to PEA power if the inverter stops",
       "Single-line diagram, design values, why each component was chosen, and Option B without a battery (add one later)",
       "Savings and payback for an example home using 600 kWh a month, with and without PEA sell-back approval"],
      "Prices have been removed from this sample.", ["Open the PDF", "Download", "Ask for a price", "/#consult"]),
 ],
 "th": [
  art("hybrid-16-9kwp-32kwh", MHS, "หน้าแรกของตัวอย่างข้อเสนอระบบไฮบริด 16.9 kWp แบตเตอรี่ 32 kWh", "ตัวอย่างข้อเสนอ · 2 หน้า · PDF · ภาษาไทย",
      "ระบบไฮบริด 16.9 kWp พร้อมแบตเตอรี่ 32 kWh ไฟ 3 เฟส",
      "อาคารสองชั้นใกล้แม่ฮ่องสอน ใช้ไฟ 3 เฟส แผงป้องกันแสงสะท้อน 26 แผง อินเวอร์เตอร์ไฮบริด 15 kW 3 เฟส และแบตเตอรี่ 16 kWh 2 ชุดต่อขนาน พร้อม ATS สลับแหล่งจ่ายโหลดสำรอง",
      ["แผง 650 W ป้องกันแสงสะท้อน 26 แผง (16.90 kWp) อินเวอร์เตอร์ไฮบริด Solis 15 kW 3 เฟส (ขยายแผงได้ถึง 24 kWp) แบตเตอรี่ Solis 16 kWh LiFePO4 2 ชุด (32 kWh)",
       "แยกรายการ 14 ข้อ: อุปกรณ์หลัก เบรกเกอร์และสายแบตเตอรี่ ตู้ DC ตู้ AC + ATS สายไฟ ระบบยึดแผง สายดิน KCE ค่าขนส่ง ยื่นขออนุญาต กฟภ. และค่าติดตั้ง",
       "ล้างแผงและตรวจสอบความปลอดภัย 6 ปี และค่าบริหารโครงการรวมประกันภัย Contractor All Risk",
       "ราคาเหมารวมทั้งโครงการ (ตัดออกจากตัวอย่างนี้)"],
      "ตัดข้อมูลลูกค้าและราคาออกจากตัวอย่างนี้แล้ว", ["เปิด PDF", "ดาวน์โหลด", "ขอราคา", "/th/#consult"]),
  art("general-hybrid-10kw-16kwh", GEN, "หน้าแรกของแพ็กเกจไฮบริด 10 kW สำหรับบ้านทั่วไป", "แพ็กเกจ · 8 หน้า · PDF · ภาษาไทย",
      "แพ็กเกจบ้านทั่วไป: ไฮบริด 10 kW แบตเตอรี่ 16 kWh แผง 7.8 kWp สำรองไฟทั้งบ้าน",
      "แพ็กเกจมาตรฐานสำหรับบ้านไฟ 1 เฟสทั่วประเทศ ใช้ไฟประมาณ 400–900 หน่วยต่อเดือน อินเวอร์เตอร์เผื่อขยายแผงในอนาคต และตู้ MDB &amp; ATS สำรองไฟทั้งบ้าน ไม่ใช่เพียงบางวงจร",
      ["แผง 650 W ป้องกันแสงสะท้อน 12 แผง (7.80 kWp) 2 สตริง อินเวอร์เตอร์ไฮบริด Solis 10 kW 1 เฟส (รองรับแผงถึง 20 kW) แบตเตอรี่ Solis IntelliHome 16 kWh",
       "ตู้ MDB &amp; ATS ประกอบสำเร็จ สำรองไฟทั้งบ้าน และ ATS สลับกลับไฟการไฟฟ้าเมื่ออินเวอร์เตอร์หยุด",
       "แผนภาพเส้นเดี่ยว ค่าออกแบบ เหตุผลในการเลือกอุปกรณ์ และทางเลือก B ไม่มีแบตเตอรี่ (เพิ่มภายหลังได้)",
       "ตัวอย่างการประหยัดและระยะคืนทุนสำหรับบ้านที่ใช้ไฟ 600 หน่วยต่อเดือน ทั้งกรณีได้และไม่ได้รับอนุมัติขายไฟ"],
      "ตัดราคาออกจากตัวอย่างนี้แล้ว", ["เปิด PDF", "ดาวน์โหลด", "ขอราคา", "/th/#consult"]),
 ],
}

EVS = {
 "en": dict(eyebrow="Samples and drawings", h2="EV circuits for homes, DC charging stations for business",
    lead="Real documents with customer names, sites and prices removed. Click a cover to open the PDF.",
    arts=[art("ev-2nd-circuit", EV2, "First page of the EV second-circuit proposal, Option A and B", "Home EV circuit · 6 pages · PDF · Thai",
              "Second circuit for a home EV charger: Option A or B",
              "Why a 7 kW home charger works best on a single-phase 30(100) A PEA meter, and two ways to wire it: A taps straight off the meter to a weatherproof EV box; B adds a steel MCCB board with a 100 A main, a 50 A house breaker, a 40 A EV breaker and surge protection (our recommendation).",
              ["Single-line diagram and wiring drawing for each option", "Fire-resistant CV-FR 2 × 16 mm² cable in HDPE and IMC conduit, separate earth rod for the EV (TT)",
               "Bill of materials: what the package includes and what may be added on site", "Meets the PEA/MEA home EV charging standard MPESTD-001:2563"],
              "Customer details and prices have been removed.", ["Open the PDF", "Download", "Call for a free inspection", "tel:+66631516694"], EV2_EN, "English (earlier version)"),
          art("ev-stations-sld", SLD, "First page of the single-line diagrams for four DC EV charging stations", "DC charging stations · 5 pages · PDF · English",
              "Single-line diagrams: four DC fast-charging stations",
              "The electrical design basis for four stations in Lamphun, Mukdahan, Ubon Ratchathani and Nakhon Ratchasima, from 240 kW to 540 kW: PEA 22 kV supply, a new transformer per site and an outdoor main board.",
              ["Transformers 315 to 630 kVA, main breakers MCCB 630 A to ACB 1,000 A", "One MCCB with shunt trip per charger, wired to an island emergency stop",
               "SPD Type 1+2, PEA TOU metering and a multifunction meter on Modbus", "Cable sizes for grouping in ducts at 40 °C and ≤ 3 % voltage drop"],
              "Site and customer names have been removed.", ["Open the PDF", "Download", "Talk to us about a station", "/#consult"]),
          art("ev-stations-plan", PLAN, "First page of the construction plan for four DC EV charging stations", "DC charging stations · 8 pages · PDF · English",
              "Construction plan: four DC fast-charging stations",
              "Site plans in millimetres for 4 to 8 charging bays per site: charger islands, canopy, drive aisles, cable trench and the fenced transformer yard.",
              ["EV bays 2,600 × 5,500 mm, one dual-gun charger for every 2 bays", "Chargers on a raised island with plinths and bollards, canopy ≥ 3.2 m clear",
               "HDPE ducts in a trench under the driveway, TN-S earthing ≤ 5 Ω", "Site notes per location: setbacks, levels, drainage and safe distance from fuel stations"],
              "Site and customer names have been removed.", ["Open the PDF", "Download", "Talk to us about a station", "/#consult"])]),
 "th": dict(eyebrow="ตัวอย่างและแบบ", h2="วงจร EV สำหรับบ้าน และสถานีชาร์จ DC สำหรับธุรกิจ",
    lead="เอกสารจริงที่ตัดชื่อลูกค้า สถานที่ และราคาออกแล้ว คลิกที่ปกเพื่อเปิด PDF",
    arts=[art("ev-2nd-circuit", EV2, "หน้าแรกของข้อเสนอวงจรที่ 2 สำหรับเครื่องชาร์จ EV ทางเลือก A และ B", "วงจร EV ในบ้าน · 6 หน้า · PDF · ภาษาไทย",
              "วงจรที่ 2 สำหรับเครื่องชาร์จรถยนต์ไฟฟ้าที่บ้าน: ทางเลือก A หรือ B",
              "ทำไมเครื่องชาร์จบ้าน 7 kW จึงควรใช้มิเตอร์ กฟภ. 1 เฟส 30(100) A และวิธีเดินสาย 2 แบบ: A ต่อแยกตรงจากมิเตอร์ไปกล่อง EV กันน้ำ; B เพิ่มตู้เหล็ก MCCB เมน 100 A เบรกเกอร์บ้าน 50 A เบรกเกอร์ EV 40 A และอุปกรณ์กันฟ้าผ่า (แนะนำ)",
              ["ไดอะแกรมเส้นเดียวและแบบเดินสายของแต่ละทางเลือก", "สายทนไฟ CV-FR 2 × 16 ตร.มม. ร้อยท่อ HDPE และ IMC หลักดินแยกสำหรับ EV (TT)",
               "รายการวัสดุ: สิ่งที่รวมในแพ็กเกจ และค่าใช้จ่ายที่อาจเพิ่มหน้างาน", "เป็นไปตามมาตรฐาน กฟภ./กฟน. MPESTD-001:2563 สำหรับการชาร์จ EV ในบ้าน"],
              "ตัดข้อมูลลูกค้าและราคาออกแล้ว", ["เปิด PDF", "ดาวน์โหลด", "โทรขอตรวจหน้างานฟรี", "tel:+66631516694"], EV2_EN, "English (ฉบับก่อน)"),
          art("ev-stations-sld", SLD, "หน้าแรกของไดอะแกรมเส้นเดียว สถานีชาร์จ EV แบบ DC 4 แห่ง", "สถานีชาร์จ DC · 5 หน้า · PDF · English",
              "ไดอะแกรมเส้นเดียว: สถานีชาร์จเร็ว DC 4 แห่ง",
              "เกณฑ์ออกแบบระบบไฟฟ้าของสถานี 4 แห่งในลำพูน มุกดาหาร อุบลราชธานี และนครราชสีมา ขนาด 240 ถึง 540 kW: รับไฟ กฟภ. 22 kV หม้อแปลงใหม่ทุกแห่ง และตู้ MDB กลางแจ้ง",
              ["หม้อแปลง 315 ถึง 630 kVA เมนเบรกเกอร์ MCCB 630 A ถึง ACB 1,000 A", "MCCB พร้อม shunt trip ทุกเครื่องชาร์จ ต่อเข้าปุ่มหยุดฉุกเฉิน",
               "SPD Type 1+2 มิเตอร์ TOU ของ กฟภ. และมิเตอร์วัดพลังงานผ่าน Modbus", "ขนาดสายคิดการรวมกลุ่มในท่อที่ 40 °C แรงดันตกไม่เกิน 3%"],
              "ตัดชื่อสถานที่และลูกค้าออกแล้ว", ["เปิด PDF", "ดาวน์โหลด", "ปรึกษาเรื่องสถานีชาร์จ", "/th/#consult"]),
          art("ev-stations-plan", PLAN, "หน้าแรกของแผนก่อสร้างสถานีชาร์จ EV แบบ DC 4 แห่ง", "สถานีชาร์จ DC · 8 หน้า · PDF · English",
              "แผนก่อสร้าง: สถานีชาร์จเร็ว DC 4 แห่ง",
              "ผังพื้นที่หน่วยมิลลิเมตร 4 ถึง 8 ช่องจอดต่อแห่ง: เกาะเครื่องชาร์จ หลังคา ช่องทางวิ่ง รางเดินสาย และลานหม้อแปลงพร้อมรั้ว",
              ["ช่องจอด EV 2,600 × 5,500 มม. เครื่องชาร์จหัวคู่ 1 เครื่องต่อ 2 ช่อง", "เครื่องชาร์จบนเกาะยกสูง มีฐานและเสากันชน หลังคาสูงโล่งอย่างน้อย 3.2 ม.",
               "ท่อ HDPE ในรางใต้ถนน ระบบกราวด์ TN-S ไม่เกิน 5 Ω", "หมายเหตุหน้างานแต่ละแห่ง: ระยะร่น ระดับพื้น การระบายน้ำ และระยะห่างจากปั๊มน้ำมัน"],
              "ตัดชื่อสถานที่และลูกค้าออกแล้ว", ["เปิด PDF", "ดาวน์โหลด", "ปรึกษาเรื่องสถานีชาร์จ", "/th/#consult"])]),
}


def quotation(lang):
    p = ROOT / ("th/quotation.html" if lang == "th" else "quotation.html")
    s = p.read_text(encoding="utf-8")
    s = re.sub(r"<!--q1111-->.*?<!--/q1111-->\n?", "", s, flags=re.S)
    i = s.index('<article class="tnote"')
    s = s[:i] + "<!--q1111-->" + "".join(Q[lang]) + "<!--/q1111-->\n" + s[i:]
    # the older EV sample also gets the new Thai revision
    s = s.replace(EV2_EN.replace(".pdf", "") + '.pdf" download>', EV2_EN + '" download>', 1)
    p.write_text(s, encoding="utf-8")
    print("quotation", lang)


def ev(lang):
    p = ROOT / ("th/ev.html" if lang == "th" else "ev.html")
    s = p.read_text(encoding="utf-8")
    t = EVS[lang]
    new = (f'<!--evdocs--><section class="band light" id="samples" style="padding-block:56px"><div class="wrap"><p class="eyebrow">{t["eyebrow"]}</p>'
           f'<h2 class="evh2">{t["h2"]}</h2><p class="lede" style="margin-top:10px">{t["lead"]}</p><div class="notes" style="margin-top:26px;display:grid;gap:40px">'
           + "".join(t["arts"]) + '</div></div></section><!--/evdocs-->')
    if "<!--evdocs-->" in s:
        s = re.sub(r"<!--evdocs-->.*?<!--/evdocs-->", lambda m: new, s, flags=re.S)
    else:
        m = re.search(r'<section class="band light" style="padding-block:48px"><div class="wrap"><p class="eyebrow">[^<]*</p><h2 class="evh2">.*?</section>', s, flags=re.S)
        s = s[:m.start()] + new + s[m.end():]
    p.write_text(s, encoding="utf-8")
    print("ev", lang)


if __name__ == "__main__":
    thumbs()
    for lang in ("en", "th"):
        quotation(lang); ev(lang)
