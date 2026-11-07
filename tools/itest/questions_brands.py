# -*- coding: utf-8 -*-
"""Brand questions: what makes each panel / inverter brand Solar ESS installs different.
BRANDS2 (4, product knowledge) go into Level 2, BRANDS3 (2, used in diagnosis and wiring) into Level 3. Same format as questions_e.py: (section, th, en, [correct, wrong x3], explanation).
Facts checked against maker datasheets and press releases (Nov 2026). Never name the equipment supplier here."""

BRANDS2 = [
("A", "แผง LONGi Hi-MO X10 ใช้เทคโนโลยี HPBC 2.0 จุดเด่นของเซลล์แบบนี้คืออะไร",
 "LONGi Hi-MO X10 panels use HPBC 2.0 technology. What is special about this cell design?",
 [("ขั้วไฟฟ้าทั้งหมดอยู่ด้านหลังเซลล์ (back contact) ด้านหน้าไม่มีเส้นโลหะบังแสง ประสิทธิภาพสูงขึ้น",
   "All electrical contacts are on the back of the cell (back contact), so no metal lines shade the front and efficiency is higher"),
  ("เป็นแผงฟิล์มบางที่งอได้", "It is a flexible thin-film panel"),
  ("มีไมโครอินเวอร์เตอร์ติดมาในกล่องต่อสาย", "It has a microinverter built into the junction box"),
  ("ใช้เซลล์ชนิด P-type PERC รุ่นเก่า", "It uses older P-type PERC cells")],
 "HPBC = Hybrid Passivated Back Contact. With all contacts at the rear, the whole front surface collects light; Hi-MO X10 reaches about 24.8% module efficiency."),
("A", "แผง AIKO ซีรีส์ ABC (เช่น Neostar) มีจุดเด่นเรื่องใดเมื่อมีเงาบังบางส่วน",
 "What is AIKO's ABC panel series (e.g. Neostar) known for when part of the panel is shaded?",
 [("ออกแบบให้กำลังลดลงเฉพาะจุดที่ถูกบัง (partial shading optimisation) แผงที่เหลือยังผลิตไฟได้ดี",
   "Partial-shading optimisation: the loss stays near the shaded cells and the rest of the panel keeps producing well"),
  ("แผงจะตัดการทำงานทันทีเมื่อมีเงา", "The panel switches itself off as soon as it is shaded"),
  ("ต้องติดออปติไมเซอร์ทุกแผงจึงจะใช้งานได้", "It only works with an optimiser on every panel"),
  ("เงาไม่มีผลใดๆ เลย ผลิตไฟได้เต็ม 100%", "Shade has no effect at all; it still gives 100% power")],
 "ABC = All Back Contact. AIKO's Gen 2 ABC panels add a partial-shading optimisation; a TÜV Nord test with one cell fully shaded showed about 30% more power than conventional panels. Shade still costs energy."),
("A", "ฟังก์ชัน SafeDC ของ SolarEdge ทำอะไรเมื่อปิดอินเวอร์เตอร์หรือไฟ AC ดับ",
 "What does SolarEdge's SafeDC function do when the inverter or AC supply is switched off?",
 [("ออปติไมเซอร์แต่ละตัวลดแรงดันออกเหลือประมาณ 1 V ต่อแผง สาย DC จึงปลอดภัยต่อการสัมผัส",
   "Each optimiser drops its output to about 1 V per panel, so the DC cables become touch-safe"),
  ("แผงยังจ่ายแรงดันเต็มสตริงเหมือนเดิม", "The panels still give full string voltage"),
  ("ตัดเฉพาะฝั่ง AC ฝั่ง DC ไม่เปลี่ยน", "Only the AC side is cut; DC stays the same"),
  ("แผงจะลัดวงจรตัวเองจนฟิวส์ขาด", "The panels short themselves until the fuse blows")],
 "With SafeDC, a 20-panel string falls to about 20 V instead of several hundred volts, which protects installers and firefighters. A normal string inverter cannot lower roof DC voltage when switched off."),
("A", "Solar ESS เลือกอินเวอร์เตอร์ไฮบริด Solis สำหรับบ้าน เพราะรองรับแผงได้มากกว่ากำลังอินเวอร์เตอร์ (oversizing) สูงถึงประมาณเท่าใด",
 "Solar ESS often picks Solis hybrid inverters for homes. Up to roughly what PV oversizing (panel kWp vs inverter kW) do they support?",
 [("200%", "200%"), ("100% (ห้ามเกิน)", "100% (no oversizing)"), ("110%", "110%"), ("500%", "500%")],
 "Solis hybrids accept up to about 2x PV, so extra panels can charge the battery while the inverter's AC output is at its limit. Always check the model's datasheet for max DC input current and voltage."),
]

BRANDS3 = [
("A", "อินเวอร์เตอร์ Huawei SUN2000 มีฟังก์ชัน Smart I-V Curve Diagnosis ใช้ทำอะไร",
 "Huawei SUN2000 inverters have Smart I-V Curve Diagnosis. What is it used for?",
 [("สแกนเส้นโค้ง I-V ของทุกสตริงจากระยะไกล เพื่อหาสตริงหรือแผงที่ผิดปกติ เช่น เงา ไดโอดลัด สตริงไม่สมดุล โดยไม่ต้องขึ้นหลังคา",
   "Remotely scans the I-V curve of every string to find faults such as shading, shorted diodes or mismatched strings, without climbing on the roof"),
  ("ใช้ตั้งค่าแรงดันกริด", "It sets the grid voltage"),
  ("ใช้ชาร์จแบตเตอรี่จากเครื่องปั่นไฟ", "It charges the battery from a generator"),
  ("ใช้วัดความต้านทานดิน", "It measures earth resistance")],
 "The scan takes under a second per string and compares curves across strings. Huawei also adds AI-based arc-fault protection (AFCI). The I-V scan is not available when optimisers are fitted."),
("A", "อินเวอร์เตอร์ไฮบริด Deye มีพอร์ต GEN แยก พอร์ตนี้ใช้งานได้แบบใดบ้าง",
 "Deye hybrid inverters have a separate GEN port. How can this port be used?",
 [("ต่อเครื่องปั่นไฟเพื่อชาร์จแบต หรือตั้งเป็น Smart Load จ่ายโหลดที่เลือก หรือรับไฟจากไมโคร/สตริงอินเวอร์เตอร์ (AC coupling)",
   "Connect a generator to charge the battery, set it as a Smart Load output, or take power from a micro or string inverter (AC coupling)"),
  ("ใช้ต่อแผงโซลาร์เพิ่มได้โดยตรง", "Connect extra solar panels directly"),
  ("ใช้ต่อสายดินเท่านั้น", "It is only for the earth wire"),
  ("ใช้ต่อแบตเตอรี่ก้อนที่สอง", "Connect a second battery")],
 "The GEN port is AC. Deye hybrids can also run up to 16 units in parallel, on-grid or off-grid."),
]

# Brand-specific question sets, kept out of the five levels (Nov 2026). Ready for a brand test of their own.
SIGENERGY = [
("A", "ระบบ Sigenergy SigenStor เรียกว่า '5-in-1' เพราะรวมอะไรไว้ในเครื่องเดียว",
 "Sigenergy's SigenStor is called '5-in-1'. What does it combine in one system?",
 [("อินเวอร์เตอร์โซลาร์, PCS แบตเตอรี่, แบตเตอรี่, เครื่องชาร์จรถ EV แบบ DC และระบบจัดการพลังงาน (EMS)",
   "Solar inverter, battery PCS, battery, DC EV charger and energy management system (EMS)"),
  ("แผงโซลาร์, ราง, น็อต, สายไฟ และเบรกเกอร์", "Panels, rails, bolts, cables and breakers"),
  ("มิเตอร์ 5 ตัวสำหรับ 5 เฟส", "Five meters for five phases"),
  ("อินเวอร์เตอร์ 5 ตัวต่อขนาน", "Five inverters in parallel")],
 "Fewer separate boxes means a cleaner install. The battery modules stack, so capacity can be added later."),
]

ENPHASE = [
("A", "ระบบ Enphase แตกต่างจากอินเวอร์เตอร์แบบสตริงอย่างไร",
 "How does an Enphase system differ from a string inverter system?",
 [("ใช้ไมโครอินเวอร์เตอร์ 1 ตัวต่อแผง แปลงเป็นไฟ AC ที่แผงเลย ไม่มีสาย DC แรงดันสูงบนหลังคา และแผงหนึ่งเสียไม่ทำให้แผงอื่นหยุด",
   "One microinverter per panel converts to AC at the panel: no high-voltage DC on the roof, and one faulty panel does not stop the others"),
  ("ใช้อินเวอร์เตอร์ตัวเดียวต่อสตริงยาว 1,000 V", "It uses one inverter on a long 1,000 V string"),
  ("ต้องมีแบตเตอรี่เสมอจึงจะผลิตไฟได้", "It always needs a battery to produce power"),
  ("ไม่มีระบบมอนิเตอร์รายแผง", "It has no per-panel monitoring")],
 "Microinverters work panel by panel, so each panel has its own MPPT and monitoring, and roof wiring is low-voltage AC."),
]
