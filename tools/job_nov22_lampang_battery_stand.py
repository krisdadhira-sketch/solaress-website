# -*- coding: utf-8 -*-
"""Jobs page 22 Nov 2026: fabricate and install a steel stand for 3 LiFePO4 batteries, bolted to an existing
equipment frame, Ban Ueam, Mueang Lampang. Drawings: downloads/Solar-ESS-Battery-Stand-3-LiFePO4-Drawings_Rev02_WM_20261122.pdf
(sheets D1-D5 at 1:25 / 1:10 / 1:5). Public version: approximate location only, no customer name.
Idempotent. Run: python3 tools/job_nov22_lampang_battery_stand.py, then tools/job_links.py, tools/job_search.py,
tools/job_order.py, tools/site_search.py"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JID = "battery-stand-banueam-lampang"
JOB = "Battery stand – Ban Ueam, Lampang: fabricate + install a 1600 × 420 mm steel stand for 3 LiFePO4 batteries"
PDF = "/downloads/Solar-ESS-Battery-Stand-3-LiFePO4-Drawings_Rev02_WM_20261122.pdf"
IMG3D, IMGF = "images/job-battery-stand-lampang-3d_Rev01_20261122.jpg", "images/job-battery-stand-lampang-front_Rev01_20261122.jpg"
MAP = "https://www.google.com/maps/search/?api=1&amp;query=Ban%20Ueam%2C%20Mueang%20Lampang%2C%20Lampang%2C%20Thailand"
ICO = ('<div class="ico"><svg viewBox="0 0 30 30" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
       '<rect x="6" y="9" width="18" height="15" rx="2"/><path d="M11 9V6h8v3M13 14l-2 4h5l-2 4"/></svg></div>')
PIN = ('<svg width="16" height="18" viewBox="0 0 16 18"><path d="M8 17s6-5.6 6-10A6 6 0 002 7c0 4.4 6 10 6 10z" fill="var(--c)"/>'
       '<circle cx="8" cy="7" r="2.3" fill="#fff"/></svg>')

BOM = {
 "en": [
  "Steel RHS 50×50×2.3: 3 × 6 m lengths (≈15.5 m used, ≈52 kg) – cut list: A front/rear rail 2 × 1600; B middle rail 6 × 208; C cross member 7 × 320; D leg 8 × 191; E rear post 4 × 753; F horizontal bar 2 × 1600; G tie arm 4 × 150; H side arm 4 × ≈115 (cut to fit)",
  "Base plate 100×100×6 flat, 2 × Ø12 holes – 8 pcs",
  "End plate 50×130×10 flat, 2 × Ø11 holes 90 c/c – 4 pcs; shims 50×130, 1–3 mm – 4 pcs (if needed)",
  "Box mounting rail L40×40×4 × 600 – 2 pcs; removable kerb L40×40×4: 1 × 420 + 2 × 460 – 3 pcs",
  "Clamp bracket flat 40×4, bent L ≈120 + 110, slotted 30 mm, rubber pad – 6 pcs",
  "Deck plate 3 mm galvanised 1600 × 420, notched 52×52 at 4 posts – 1 pc; rubber battery pad 3 mm (1 × 460×230, 2 × 500×230) – 3 pcs",
  "M10 floor anchor (through-bolt/wedge, ≥ 60 mm embed) – 16; M10 × 100 bolt set with 2 washers + nyloc – 8",
  "M8 × 70 countersunk DIN 7991 + nyloc (deck) – 20; M8 × 25 bolt sets – 14; M8 rivet nut + M8 × 16 (kerbs) – 6",
  "Cable glands to suit cable OD – 8; hot-dip galvanising, or zinc-rich primer on welds + top coat",
 ],
 "th": [
  "เหล็กกล่อง RHS 50×50×2.3 มม. ยาว 6 ม. 3 เส้น (ใช้จริง ≈15.5 ม. ≈52 กก.) – รายการตัด: A รางหน้า/หลัง 2 × 1600; B รางกลาง 6 × 208; C คานขวาง 7 × 320; D ขา 8 × 191; E เสาหลัง 4 × 753; F คานนอน 2 × 1600; G แขนยึด 4 × 150; H แขนข้าง 4 × ≈115 (ตัดตามหน้างาน)",
  "เพลทฐาน เหล็กแผ่น 100×100×6 มม. เจาะ Ø12 2 รู – 8 ชิ้น",
  "เพลทปลาย 50×130×10 มม. เจาะ Ø11 2 รู ระยะ 90 มม. – 4 ชิ้น; แผ่นรองหนุน 50×130 หนา 1–3 มม. – 4 ชิ้น (ถ้าจำเป็น)",
  "เหล็กฉาก L40×40×4 ยาว 600 สำหรับยึดกล่องบัสบาร์ – 2 ชิ้น; ขอบกันตกถอดได้ L40×40×4: 1 × 420 + 2 × 460 – 3 ชิ้น",
  "ตัวกดแบตเตอรี่ เหล็กแบน 40×4 ดัดฉาก ≈120 + 110 เจาะร่อง 30 มม. พร้อมยางรอง – 6 ชิ้น",
  "แผ่นพื้นเหล็กชุบกัลวาไนซ์ 3 มม. 1600 × 420 บากมุม 52×52 ที่เสา 4 ต้น – 1 แผ่น; ยางรองแบตเตอรี่ 3 มม. (1 × 460×230, 2 × 500×230) – 3 แผ่น",
  "พุกยึดพื้น M10 (ฝังลึก ≥ 60 มม.) – 16 ตัว; ชุดน็อต M10 × 100 พร้อมแหวน 2 ตัว + น็อตล็อกไนลอน – 8 ชุด",
  "สกรูหัวเรียบ M8 × 70 DIN 7991 + น็อตล็อก (ยึดพื้น) – 20; ชุดน็อต M8 × 25 – 14; รีเวทนัท M8 + สกรู M8 × 16 (ขอบกันตก) – 6",
  "เคเบิลแกลนด์ตามขนาดสาย – 8 ตัว; ชุบกัลวาไนซ์แบบจุ่มร้อน หรือทาสีรองพื้นซิงค์ริชที่รอยเชื่อม + สีทับหน้า",
 ],
}

T = {
 "en": dict(
  kind="Project based · paid per job · fabricate + install", posted="Posted 22 Nov 2026",
  h3="Weld and install a steel stand for 3 LiFePO4 batteries, bolted to an existing equipment frame",
  where="Ban Ueam, Mueang Lampang, Lampang", maplbl="Area map (approx.) ↗",
  cap3d="3D view: stand centred between the existing frame legs", capf="Front elevation, sheet D2 (scale 1:10)",
  facts=[("1600 × 420 mm", "Stand, deck 250 mm high, 50 mm between batteries"), ("RHS 50×50×2.3", "≈15.5 m, ≈75 kg of steel in total"),
         ("3 batteries", "1 × 460×230×810 + 2 × 500×230×780 mm, on castors"), ("8 × M10", "Bolted ties to the existing frame legs – nothing fixed to the wall"),
         ("฿7,500–9,500", "Pay guide · labour only")],
  fit=('A home hybrid system (Solis inverter) needs a proper stand for its 3 LiFePO4 batteries. The stand sits 200 mm from the wall, centred between the existing frame legs (125 mm clear each end), '
       'and is tied to both legs with bolted tie arms. <b>Read the full drawing set before you quote:</b> '
       f'<a href="{PDF}">Battery stand drawings, sheets D1–D5 to scale, cut list and fixings (PDF)</a>. All dimensions are in mm; print on A4 at 100%. '
       '<b>Safety:</b> a qualified electrician shuts the system down and isolates the batteries before anything is moved; no welding next to the batteries – fabricate off site or well away, then bolt up on site. '
       'Batteries are heavy: use a ramp at least 1 m long or lift with 2 people. Use premium materials only.'),
  scope_t="Scope of work", scope=[
   "Check the site dimensions and the existing frame leg section (taken as 50 × 50 – confirm before drilling)",
   "Cut, weld and square the stand to the drawings (diagonals within 2 mm); drill all holes and vent holes before galvanising",
   "Hot-dip galvanise, or zinc-rich primer on welds plus top coat",
   "With the system isolated: set the stand 200 mm from the wall, shim level, fix 16 × M10 floor anchors",
   "Cut the side arms to the measured gap, weld to the tie arms and end plates, drill through the legs and bolt up 8 × M10",
   "Bolt the L40 rails and the existing bus bar box behind the middle posts; lay the pads, roll the batteries in, lock castors, fit kerbs and clamp brackets",
   "Electrician re-routes the battery cables into the box glands, re-energises and tests; hand over with photos and the Solar ESS report form"],
  bom_t="Bill of materials (BOM)",
  rmk=('<b>Remark:</b> candidates must submit their <b>profile, certificate and quotation</b>. We will then contact you back to discuss the work. We apologize if your Facebook message has not been answered. '
       '<b>Please read every detail of this job carefully and quote exactly for the scope, location and requirements shown. Do not ask questions by Facebook Messenger – send your quotation with the form below.</b><br>'
       '<b>Quote two prices:</b> 1) Labour cost only; 2) Labour &amp; materials (materials as in the BOM – list every material by brand and size). Say how many people and how many days, and whether you galvanise or paint.'
       '<span class="tsia-req"><br><b>Before you quote:</b> every installer who works with Solar ESS must first <b>pass at least 1 Solar ESS installer test</b> (<a href="/installer-test.html">take a test</a>) '
       'and <b>register as a TSIA member</b> (<a href="/team.html#tsia-form">become a member</a>). Quotes from installers who have not done both cannot be accepted.<br>'
       '<b>Tell us where you are based:</b> give your approximate location (sub-district, district, province) with your quotation. Installers who live near Lampang are more likely to get the job. '
       '<a href="/location.html">Register or update your location</a> to be notified of jobs near you.</span>'),
  go="Quote for this job →"),
 "th": dict(
  kind="งานรายโครงการ · จ่ายเป็นรายงาน · ผลิต + ติดตั้ง", posted="ลงประกาศ 22 พ.ย. 2569",
  h3="เชื่อมและติดตั้งโครงขาตั้งเหล็กสำหรับแบตเตอรี่ LiFePO4 3 ก้อน ยึดด้วยน็อตกับโครงอุปกรณ์เดิม",
  where="ต.บ้านเอื้อม อ.เมืองลำปาง จ.ลำปาง", maplbl="แผนที่บริเวณ (โดยประมาณ) ↗",
  cap3d="ภาพ 3 มิติ: โครงขาตั้งอยู่กึ่งกลางระหว่างขาโครงเดิม", capf="รูปด้านหน้า แผ่น D2 (มาตราส่วน 1:10)",
  facts=[("1600 × 420 มม.", "โครงขาตั้ง พื้นสูง 250 มม. ระยะห่างแบตเตอรี่ 50 มม."), ("RHS 50×50×2.3", "≈15.5 ม. เหล็กรวม ≈75 กก."),
         ("แบตเตอรี่ 3 ก้อน", "1 × 460×230×810 + 2 × 500×230×780 มม. มีล้อ"), ("8 × M10", "ยึดน็อตกับขาโครงเดิม – ไม่ยึดกับผนัง"),
         ("฿7,500–9,500", "ค่าแรงแนะนำ · ค่าแรงอย่างเดียว")],
  fit=('ระบบโซลาร์ไฮบริดของบ้าน (อินเวอร์เตอร์ Solis) ต้องการโครงขาตั้งที่แข็งแรงสำหรับแบตเตอรี่ LiFePO4 3 ก้อน โครงตั้งห่างผนัง 200 มม. อยู่กึ่งกลางระหว่างขาโครงเดิม (เว้นปลายละ 125 มม.) '
       'และยึดกับขาโครงทั้งสองข้างด้วยแขนยึดแบบขันน็อต <b>กรุณาอ่านแบบทั้งชุดก่อนเสนอราคา:</b> '
       f'<a href="{PDF}">แบบโครงขาตั้งแบตเตอรี่ แผ่น D1–D5 ตามมาตราส่วน รายการตัดเหล็ก และอุปกรณ์ยึด (PDF)</a> ทุกขนาดเป็นมิลลิเมตร พิมพ์บนกระดาษ A4 ขนาด 100% '
       '<b>ความปลอดภัย:</b> ช่างไฟฟ้าที่มีคุณวุฒิต้องปิดระบบและตัดแบตเตอรี่ออกก่อนเคลื่อนย้ายอุปกรณ์ใด ๆ ห้ามเชื่อมใกล้แบตเตอรี่ – ผลิตนอกสถานที่หรือห่างออกไป แล้วนำมาประกอบด้วยน็อตที่หน้างาน '
       'แบตเตอรี่มีน้ำหนักมาก: ใช้ทางลาดยาวอย่างน้อย 1 ม. หรือยก 2 คน ใช้วัสดุคุณภาพดีเท่านั้น'),
  scope_t="ขอบเขตงาน", scope=[
   "ตรวจวัดขนาดหน้างานและหน้าตัดขาโครงเดิม (ในแบบใช้ 50 × 50 – ยืนยันก่อนเจาะ)",
   "ตัด เชื่อม และจัดฉากโครงตามแบบ (ทแยงต่างกันไม่เกิน 2 มม.) เจาะรูทั้งหมดและรูระบายก่อนชุบ",
   "ชุบกัลวาไนซ์แบบจุ่มร้อน หรือทาสีรองพื้นซิงค์ริชที่รอยเชื่อม + สีทับหน้า",
   "เมื่อตัดระบบแล้ว: วางโครงห่างผนัง 200 มม. หนุนให้ได้ระดับ ยึดพุก M10 16 ตัว",
   "ตัดแขนข้างตามระยะจริง เชื่อมกับแขนยึดและเพลทปลาย เจาะทะลุขาโครงและขันน็อต M10 8 ตัว",
   "ยึดเหล็กฉาก L40 และกล่องบัสบาร์เดิมหลังเสากลาง ปูยางรอง เข็นแบตเตอรี่เข้า ล็อกล้อ ใส่ขอบกันตกและตัวกด",
   "ช่างไฟฟ้าเดินสายแบตเตอรี่เข้าเคเบิลแกลนด์ของกล่อง เปิดระบบและทดสอบ ส่งมอบพร้อมรูปถ่ายและแบบฟอร์มรายงานของ Solar ESS"],
  bom_t="รายการวัสดุ (BOM)",
  rmk=('<b>หมายเหตุ:</b> ผู้สมัครต้องส่ง<b>ประวัติ ใบรับรอง และใบเสนอราคา</b> จากนั้นทางเราจะติดต่อกลับเพื่อพูดคุยรายละเอียดงาน ขออภัยหากข้อความทาง Facebook ของท่านยังไม่ได้รับการตอบกลับ '
       '<b>กรุณาอ่านรายละเอียดงานให้ครบถ้วนและเสนอราคาให้ตรงตามขอบเขตงาน สถานที่ และข้อกำหนดที่ระบุ ไม่ต้องสอบถามทางข้อความ Facebook – กรุณาส่งใบเสนอราคาผ่านแบบฟอร์มด้านล่าง</b><br>'
       '<b>เสนอราคา 2 แบบ:</b> 1) ค่าแรงอย่างเดียว; 2) ค่าแรงและค่าวัสดุ (วัสดุตาม BOM – ระบุยี่ห้อและขนาดทุกรายการ) ระบุจำนวนคน จำนวนวัน และจะชุบกัลวาไนซ์หรือทาสี'
       '<span class="tsia-req"><br><b>ก่อนเสนอราคา:</b> ช่างทุกคนที่จะทำงานกับ Solar ESS ต้อง<b>ผ่านแบบทดสอบช่างของ Solar ESS อย่างน้อย 1 ชุด</b> (<a href="/th/installer-test.html">ทำแบบทดสอบ</a>) '
       'และ<b>สมัครเป็นสมาชิก TSIA</b> (<a href="/th/team.html#tsia-form">สมัครสมาชิก</a>) ใบเสนอราคาจากช่างที่ยังไม่ได้ทำทั้งสองอย่างจะไม่ได้รับการพิจารณา<br>'
       '<b>แจ้งพื้นที่ที่อยู่ของท่าน:</b> ระบุตำแหน่งที่อยู่โดยประมาณ (ตำบล อำเภอ จังหวัด) พร้อมใบเสนอราคา ช่างที่อยู่ใกล้ลำปางจะมีโอกาสได้งานมากกว่า '
       '<a href="/th/location.html">ลงทะเบียนหรืออัปเดตตำแหน่ง</a>เพื่อรับแจ้งงานใกล้บ้าน</span>'),
  go="เสนอราคางานนี้ →"),
}


def card(lang):
    t = T[lang]
    pics = (f'<div class="thumb"><div class="pics" style="grid-template-columns:1fr 1fr">'
            f'<figure style="margin:0"><img src="/{IMG3D}" alt="{t["cap3d"]}" loading="lazy" style="width:100%;height:190px;object-fit:contain;background:#fff;display:block"><figcaption>{t["cap3d"]}</figcaption></figure>'
            f'<figure style="margin:0"><img src="/{IMGF}" alt="{t["capf"]}" loading="lazy" style="width:100%;height:190px;object-fit:contain;background:#fff;display:block"><figcaption>{t["capf"]}</figcaption></figure></div></div>')
    facts = "".join(f'<div class="fact"><b>{a}</b>{b}</div>' for a, b in t["facts"])
    dl = (f'<details class="dlv" open><summary>{t["scope_t"]} <span>({len(t["scope"])})</span></summary><ul>' + "".join(f"<li>{i}</li>" for i in t["scope"]) + "</ul></details>"
          f'<details class="dlv"><summary>{t["bom_t"]} <span>({len(BOM[lang])})</span></summary><ul>' + "".join(f"<li>{i}</li>" for i in BOM[lang]) + "</ul></details>")
    return (f'<article class="card p" id="{JID}" data-posted="2026-11-22" data-tags="project north" data-lat="18.37" data-lng="99.42" '
            f'data-work="civil electrical" data-q="ban ueam, mueang lampang, lampang 52100 ต.บ้านเอื้อม อ.เมืองลำปาง จ.ลำปาง lampang ลำปาง '
            f'battery stand โครงแบตเตอรี่ welding welder ช่างเชื่อม steel เหล็ก">'
            f'{pics}<div class="top">{ICO}<div><div class="kind">{t["kind"]}<span class="posted"> · {t["posted"]}</span></div><h3>{t["h3"]}</h3></div></div>\n'
            f'<div class="body"><div class="where">{PIN}<span>{t["where"]} · <span style="white-space:nowrap"><a href="{MAP}" target="_blank" rel="noopener" '
            f'style="color:var(--c);font-weight:600">{t["maplbl"]}</a></span></span></div>\n'
            f'<div class="facts">{facts}</div>\n<p class="fit">{t["fit"]}</p>\n{dl}\n'
            f'<p class="fit rmk" style="border-left-color:var(--c);margin-top:12px">{t["rmk"]}</p>\n'
            f'<div class="go"><a href="#apply" data-job="{JOB}">{t["go"]}</a></div></div></article>\n')


for lang, path in (("en", "job.html"), ("th", "th/job.html")):
    p = ROOT / path
    s = p.read_text(encoding="utf-8")
    s = re.sub(rf'<article class="card p" id="{JID}".*?</article>\n?', "", s, flags=re.S)
    m = re.search(r'<article class="card p" id="', s)
    s = s[:m.start()] + card(lang) + s[m.start():]
    p.write_text(s, encoding="utf-8")
    print(path, "inserted")
