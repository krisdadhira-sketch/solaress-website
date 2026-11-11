# -*- coding: utf-8 -*-
"""Second batch of samples, 11 Nov 2026: latest quotations found in Kris's Downloads that were not yet on the site,
cleaned with tools/clean_quote_pdf.py (no prices, customer names, signatures, bank accounts or exact sites).
Inserted at the top of the Quotation pages (EN/TH) between <!--q1111b--> markers. Idempotent.
Run from the repo root: python3 tools/sample_docs_nov11b.py, then tools/analytics_tag.py, tools/build_share.py, tools/site_search.py"""
import re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
W = "_Rev01_WM_20261111.pdf"
P = lambda s: f"/downloads/Solar-ESS-Sample-{s}{W}"
VFD, VFD_TH = P("VFD-Peak-Control-Heat-Press-Proposal"), P("VFD-Peak-Control-Heat-Press-Proposal-TH")
MUN, MUN_TH = P("OnGrid-15kWp-Municipal-Office-Proposal"), P("OnGrid-15kWp-Municipal-Office-Proposal-TH")
MUN2 = P("OnGrid-2x15kW-Parallel-Municipal-Office-Proposal")
PKG20 = P("Hybrid-Package-20kW-18.9kWp-48kWh")
STR = P("Offgrid-29kWp-Structure-Options-A-Frame-vs-Ground")
ABC = P("Quotation-Backup-Upgrade-Options-ABC")
PNL = P("Quotation-600W-Bifacial-Panels-TH")
CAFE = P("Offgrid-Cafe-Battery-Upgrade-Proposal-TH")
SUB = P("Quotation-Submeter-Installation-TH")


def thumb(pdf):
    name = "quote-sample-" + pdf.split("Sample-")[1].replace(W, "").lower()
    out = ROOT / "images" / f"{name}.jpg"
    if not out.exists():
        subprocess.run(["pdftoppm", "-r", "70", "-jpeg", "-jpegopt", "quality=85", "-f", "1", "-l", "1", "-singlefile",
                        str(ROOT / pdf.lstrip("/")), str(out.with_suffix(""))], check=True)
    return f"/images/{name}.jpg"


def art(id_, pdf, meta, h2, lead, pts, note, b, alt=None):
    lis = "".join(f"<li>{p}</li>" for p in pts)
    extra = f'<a class="btn ghost" href="{alt[0]}">{alt[1]}</a>' if alt else ""
    return (f'<article class="tnote" id="{id_}"><a href="{pdf}"><img src="{thumb(pdf)}" alt="{h2}" width="579" height="819" loading="lazy"></a>'
            f'<div><p class="meta">{meta}</p><h2>{h2}</h2><p>{lead}</p><ul>{lis}</ul><p class="meta" style="margin-top:12px">{note}</p>'
            f'<div class="acts"><a class="btn" href="{pdf}">{b[0]}</a><a class="btn ghost" href="{pdf}" download>{b[1]}</a>{extra}'
            f'<a class="btn ghost" href="{b[3]}">{b[2]}</a></div></div></article>\n')


def items(lang):
    en = lang == "en"
    B = ["Open the PDF", "Download", "Ask for a price", "/#consult"] if en else ["เปิด PDF", "ดาวน์โหลด", "ขอราคา", "/th/#consult"]
    N = "Customer details and prices have been removed." if en else "ตัดข้อมูลลูกค้าและราคาออกแล้ว"
    TH, ENL = "ภาษาไทย", "English"
    if en:
        return [
         art("vfd-peak-control", VFD, "Proposal · 5 pages · PDF · English", "Cutting a factory's demand charge: VFD and heater control",
             "A heat-press machine on a TOU/demand tariff was setting a 55–62 kW peak. Five-minute monitoring data showed the peak came from the drum heaters, not the motor, so the proposal targets the heaters.",
             ["Evidence from the solar monitoring data and six PEA bills", "A small VFD for the drum motor plus an SCR heater controller with PID and a new warm-up schedule",
              "Billed peak from about 61.5 kW down to 32–38 kW, with monthly and yearly savings worked out", "Option A (schedule only, no cost) and package B, with payback"],
             N, B, (VFD_TH, TH)),
         art("ongrid-15kwp-municipal", MUN, "Proposal · 6 pages · PDF · English", "15 kWp on-grid rooftop for a municipal office",
             "A turnkey proposal written to a public-sector TOR for a 15 kWp rooftop system on a local government office building.",
             ["24 × LONGi Hi-MO X10 650 W panels (15.6 kWp), Huawei SUN2000-15KTL-M5 three-phase inverter",
              "Single-line diagram, roof layout and itemised bill of materials", "About 20,850 kWh in year 1, payback in about 4.7 years",
              "Warranty, maintenance and what is and is not included"], N, B, (MUN_TH, TH)),
         art("ongrid-2x15kw-municipal", MUN2, "Proposal · 6 pages · PDF · English", "31.2 kWp on-grid: two 15 kW inverters in parallel",
             "The larger option for the same office building: double the panels and two inverters working in parallel.",
             ["48 × 650 W panels (31.2 kWp), 2 × Huawei SUN2000-15KTL-M5 in parallel", "About 41,700 kWh in year 1, payback in about 4.2 years",
              "Itemised bill of materials and 25-year return on investment", "Running costs including an inverter replacement in year 13"], N, B),
         art("hybrid-package-20kw-48kwh", PKG20, "Package · 3 pages · PDF · English", "20 kW hybrid package: 18.9 kWp, 48 kWh, generator-ready",
             "A three-phase package for homes, resorts, shops and small businesses with a big evening load or frequent power cuts.",
             ["30 × 630 W n-type bifacial panels in 3 strings of 10", "20 kW three-phase hybrid inverter and 3 × 16 kWh LFP batteries (48 kWh)",
              "Keeps backed-up circuits running from solar and battery when PEA power is cut; generator input", "What is included, timeline and terms"], N, B),
         art("offgrid-29kwp-structure-options", STR, "Proposal · 7 pages · PDF · English", "29.25 kWp off-grid: A-frame or low ground mount?",
             "One off-grid system (29.25 kWp of bifacial panels, 60 kWh of battery) with two choices for the structure underneath. Everything else is the same.",
             ["Option A: new A-shape frames with adjustable tilt on concrete ballast blocks, higher and neater, a little more bifacial gain",
              "Option B: the proven low ground-mounted structure, simpler and more economical", "Side-by-side comparison and full bill of materials",
              "How we agree the plan, lock the price at signing and then talk discount"], N, B),
         art("backup-upgrade-abc", ABC, "Quotation · 3 pages · PDF · English", "Backup power upgrade for a lodge: options A, B and C",
             "An existing 10 kWp, 10 kW hybrid system with about 15 kWh of battery: how to keep the whole lodge, the water pump and hot water running in a power cut.",
             ["Part 1, in every option: rewiring the backup circuits and inverter settings",
              "Option A (recommended): heat-pump water heater with a 300 L tank, about one-third of the electricity of the old heater",
              "Options B and C: keep electric heating with a smaller heater, or double the inverter power", "Customer acceptance section to pick A, B or C"], N, B),
         art("bifacial-600w-panels", PNL, "Quotation · 2 pages · PDF · Thai", "Quotation for 600 W N-type bifacial panels",
             "A sample quotation for a customer buying panels only, with the panel specification and sales terms.",
             ["Mono half-cell N-type bifacial 600 W, 23.23% efficiency", "2,278 × 1,134 × 30 mm, IP68 junction box, MC4 connectors, TÜV / CE / MCS / IEC",
              "Vmp/Imp 44.30 V / 13.55 A, Voc/Isc 51.30 V / 14.30 A", "Price valid 30 days from the quotation date"], N, B),
         art("offgrid-cafe-battery-upgrade", CAFE, "Proposal · 4 pages · PDF · Thai", "Off-grid café upgrade: power through the rainy season",
             "Keep the existing panels and inverter, add battery so the café runs on solar all year and the generator is only a backup.",
             ["Existing 11.6 kWp of panels is enough: no new panels", "30.7 kWh of battery in total, about 1.5 days of backup on cloudy days",
              "Overview of the proposed system and how it works with the generator", "Solar as the main source, 100%"], N, B),
         art("submeter-installation", SUB, "Quotation · 2 pages · PDF · Thai", "Quotation: installing two sub-meters",
             "Sub-metering for a house in a mountain area, with protection devices and earthing.",
             ["Electronic meters with calibration", "LT switch and fuse set", "Lightning arrester with earth rod and cable",
              "Optional: three-phase cabling to the house and a three-phase main board"], N, B),
        ]
    return [
     art("vfd-peak-control", VFD_TH, "ข้อเสนอ · 4 หน้า · PDF · ภาษาไทย", "ลดค่าความต้องการพลังไฟฟ้าของโรงงาน: VFD และระบบควบคุมฮีตเตอร์",
         "เครื่องรีดร้อนในอัตรา TOU ทำให้เกิดพีค 55–62 kW ข้อมูลราย 5 นาทีจากระบบโซลาร์ยืนยันว่าพีคมาจากฮีตเตอร์ลูกกลิ้ง ไม่ใช่มอเตอร์ ข้อเสนอจึงควบคุมที่ฮีตเตอร์",
         ["หลักฐานจากข้อมูลมอนิเตอร์ และบิล กฟภ.", "VFD ขนาดเล็กสำหรับมอเตอร์ลูกกลิ้ง และชุดควบคุมฮีตเตอร์ SCR + PID พร้อมตารางอุ่นเครื่องใหม่",
          "ลดพีคที่ถูกเรียกเก็บจาก ≈ 61.5 kW เหลือ 32–38 kW พร้อมคำนวณการประหยัด", "ทางเลือก A (ปรับตารางอย่างเดียว ไม่มีค่าใช้จ่าย) และชุด ข. พร้อมระยะคืนทุน"],
         N, B, (VFD, ENL)),
     art("ongrid-15kwp-municipal", MUN_TH, "ข้อเสนอ · 6 หน้า · PDF · ภาษาไทย", "โซลาร์รูฟท็อปออนกริด 15 kWp สำหรับอาคารสำนักงานเทศบาล",
         "ข้อเสนอแบบเหมาครบวงจรตามข้อกำหนด TOR ของหน่วยงานภาครัฐ สำหรับระบบ 15 kWp บนหลังคาอาคารสำนักงานองค์กรปกครองส่วนท้องถิ่น",
         ["แผง LONGi Hi-MO X10 650 W × 24 แผง (15.6 kWp) อินเวอร์เตอร์ Huawei SUN2000-15KTL-M5 3 เฟส", "แผนภาพเส้นเดียว ผังหลังคา และรายการวัสดุแยกรายการ",
          "ผลิตไฟปีแรกประมาณ 20,850 kWh คืนทุนประมาณ 4.7 ปี", "การรับประกัน การบำรุงรักษา และสิ่งที่รวม/ไม่รวมในงาน"], N, B, (MUN, ENL)),
     art("ongrid-2x15kw-municipal", MUN2, "ข้อเสนอ · 6 หน้า · PDF · English", "ออนกริด 31.2 kWp: อินเวอร์เตอร์ 15 kW 2 เครื่องทำงานขนาน",
         "ทางเลือกขนาดใหญ่สำหรับอาคารเดียวกัน: แผงเพิ่มเป็นสองเท่าและอินเวอร์เตอร์ 2 เครื่องทำงานขนานกัน",
         ["แผง 650 W × 48 แผง (31.2 kWp) Huawei SUN2000-15KTL-M5 × 2 เครื่องขนาน", "ผลิตไฟปีแรกประมาณ 41,700 kWh คืนทุนประมาณ 4.2 ปี",
          "รายการวัสดุแยกรายการ และผลตอบแทน 25 ปี", "ค่าใช้จ่ายระหว่างใช้งาน รวมการเปลี่ยนอินเวอร์เตอร์ปีที่ 13"], N, B),
     art("hybrid-package-20kw-48kwh", PKG20, "แพ็กเกจ · 3 หน้า · PDF · English", "แพ็กเกจไฮบริด 20 kW: แผง 18.9 kWp แบตเตอรี่ 48 kWh รองรับเครื่องปั่นไฟ",
         "แพ็กเกจไฟ 3 เฟส สำหรับบ้าน รีสอร์ต ร้านค้า และธุรกิจขนาดเล็กที่ใช้ไฟช่วงเย็นมาก หรือไฟดับบ่อย",
         ["แผง n-type สองหน้า 630 W × 30 แผง 3 สตริง", "อินเวอร์เตอร์ไฮบริด 20 kW 3 เฟส และแบตเตอรี่ LFP 16 kWh × 3 (48 kWh)",
          "ไฟดับยังมีไฟใช้ในวงจรสำรองจากแผงและแบตเตอรี่ ต่อเครื่องปั่นไฟได้", "รายการที่รวม ระยะเวลาดำเนินงาน และเงื่อนไข"], N, B),
     art("offgrid-29kwp-structure-options", STR, "ข้อเสนอ · 7 หน้า · PDF · English", "ออฟกริด 29.25 kWp: โครงทรง A หรือโครงติดพื้นแบบเตี้ย?",
         "ระบบออฟกริดชุดเดียว (แผงสองหน้า 29.25 kWp แบตเตอรี่ 60 kWh) มีโครงสร้างให้เลือก 2 แบบ ส่วนอื่นเหมือนกันทุกอย่าง",
         ["ทางเลือก A: โครงทรง A ปรับมุมได้ วางบนแท่งคอนกรีตถ่วง สูงและเรียบร้อย ได้ประโยชน์จากแผงสองหน้ามากขึ้น",
          "ทางเลือก B: โครงติดพื้นแบบเตี้ยที่พิสูจน์แล้ว เรียบง่ายและประหยัดกว่า", "ตารางเปรียบเทียบและรายการวัสดุครบ",
          "ขั้นตอนตกลงแผน ล็อกราคาเมื่อเซ็นสัญญา แล้วจึงคุยเรื่องส่วนลด"], N, B),
     art("backup-upgrade-abc", ABC, "ใบเสนอราคา · 3 หน้า · PDF · English", "ปรับปรุงระบบไฟสำรองของที่พัก: ทางเลือก A, B และ C",
         "ระบบไฮบริดเดิม 10 kWp อินเวอร์เตอร์ 10 kW แบตเตอรี่ประมาณ 15 kWh: ทำอย่างไรให้ทั้งที่พัก ปั๊มน้ำ และน้ำร้อนใช้ได้เมื่อไฟดับ",
         ["ส่วนที่ 1 (ทุกทางเลือก): เดินวงจรสำรองใหม่และตั้งค่าอินเวอร์เตอร์", "ทางเลือก A (แนะนำ): เครื่องทำน้ำร้อนฮีตปั๊มพร้อมถัง 300 ลิตร ใช้ไฟประมาณ 1 ใน 3 ของเครื่องเดิม",
          "ทางเลือก B และ C: ใช้ฮีตเตอร์ไฟฟ้าขนาดเล็กลง หรือเพิ่มกำลังอินเวอร์เตอร์เป็นสองเท่า", "ส่วนยืนยันการเลือกทางเลือกของลูกค้า"], N, B),
     art("bifacial-600w-panels", PNL, "ใบเสนอราคา · 2 หน้า · PDF · ภาษาไทย", "ใบเสนอราคาขายแผงโซลาร์ N-Type Bifacial 600 W",
         "ตัวอย่างใบเสนอราคาสำหรับลูกค้าที่ซื้อแผงอย่างเดียว พร้อมสเปกแผงและเงื่อนไขการขาย",
         ["แผง Mono Half Cell N-Type Bifacial 600 W ประสิทธิภาพ 23.23%", "สเปก: ขนาด 2,278 × 1,134 × 30 มม. กล่องต่อสาย IP68 คอนเนกเตอร์ MC4 มาตรฐาน TÜV CE MCS IEC",
          "ค่าไฟฟ้า: Vmp/Imp 44.30 V / 13.55 A, Voc/Isc 51.30 V / 14.30 A", "ยืนราคา 30 วันนับจากวันที่เสนอ"], N, B),
     art("offgrid-cafe-battery-upgrade", CAFE, "ข้อเสนอ · 4 หน้า · PDF · ภาษาไทย", "ปรับปรุงระบบออฟกริดของคาเฟ่ ให้มีไฟใช้แม้ฤดูฝน",
         "ใช้แผงและอินเวอร์เตอร์เดิมต่อไป เพิ่มแบตเตอรี่เพื่อให้คาเฟ่มีไฟใช้ตลอด และใช้เครื่องปั่นไฟเป็นสำรองเท่านั้น",
         ["แผงเดิม 11.6 kWp เพียงพอแล้ว ไม่ต้องเพิ่มแผง", "ความจุแบตเตอรี่รวม 30.7 kWh สำรองไฟได้ราว 1.5 วันในวันที่มีเมฆมาก",
          "ภาพรวมระบบที่เสนอและการทำงานร่วมกับเครื่องปั่นไฟ", "ใช้โซลาร์เป็นหลัก 100%"], N, B),
     art("submeter-installation", SUB, "ใบเสนอราคา · 2 หน้า · PDF · ภาษาไทย", "ใบเสนอราคาติดตั้งมิเตอร์ย่อย 2 ชุด",
         "งานติดตั้งมิเตอร์ย่อยสำหรับบ้านบนพื้นที่ภูเขา พร้อมอุปกรณ์ป้องกันและระบบสายดิน",
         ["มิเตอร์อิเล็กทรอนิกส์ พร้อมสอบเทียบ", "ชุดสวิตช์และฟิวส์แรงต่ำ (LT switch / fuse)", "ชุดกันฟ้าผ่าพร้อมหลักดินและสายดิน",
          "ทางเลือก: เดินสาย 3 เฟสเข้าบ้านและติดตั้งตู้ MDB 3 เฟส"], N, B),
    ]


def run(lang):
    p = ROOT / ("th/quotation.html" if lang == "th" else "quotation.html")
    s = p.read_text(encoding="utf-8")
    s = re.sub(r"<!--q1111b-->.*?<!--/q1111b-->\n?", "", s, flags=re.S)
    i = s.index('<article class="tnote"')
    s = s[:i] + "<!--q1111b-->" + "".join(items(lang)) + "<!--/q1111b-->\n" + s[i:]
    p.write_text(s, encoding="utf-8")
    print("quotation", lang, len(items(lang)))


if __name__ == "__main__":
    run("en"); run("th")
