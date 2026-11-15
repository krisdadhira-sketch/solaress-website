# -*- coding: utf-8 -*-
"""News articles (15 Nov 2026): 7 news briefs + the electrical-leakage safety guide, each with downloadable
watermarked PDFs (EN + TH). Inserted as the newest articles on /news.html and /th/news.html. Idempotent.
Run: python3 tools/news_nov15_briefs.py, then tools/news_topics.py, tools/build_share.py, tools/site_search.py, tools/analytics_tag.py"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = "/downloads/"
SEP = 'style="max-width:760px;margin-top:64px;padding-top:48px;border-top:1.5px solid var(--navy)"'

# (id, topics, slug-for-pdf, image, {lang: dict(eyebrow,h2,lede,pts,src)})
A = [
 ("electrical-leakage-guide", "", None, "electrical-leakage-guide-th-20261115.jpg", {
  "en": dict(eyebrow="15 November 2026 · Safety guide", h2="Electrical leakage: how deadly it is, how to test it, and how to prevent it",
   lede="A Thai-language guide for homeowners, installers and our team: what leakage current is, why about 40 mA can stop a heart, the tests that find it, and the protection every home needs.",
   pts=[("Why it kills", "Current of about 40 mA flowing through the body for more than 2 seconds can stop the heart. A wet hand touching 230 V can pass several times that."),
        ("What protects you", "A 30 mA RCD/RCBO installed with an earth wire, and tested with its test button every 6 months. An ordinary breaker (MCB) does not protect people from shock."),
        ("Common causes", "Water in outdoor boxes and conduit, UV-cracked or rodent-bitten cable, loose joints, failing water heaters and pumps, wet MC4 connectors on solar arrays, and flooding."),
        ("How to test", "A leakage clamp meter on L and N together (power on), a 500 V insulation test of at least 1 MΩ (power off), and an RCD trip-time test.")],
   btn="Download the guide (PDF, Thai) ↓", btn2=None, src=None),
  "th": dict(eyebrow="15 พฤศจิกายน 2569 · คู่มือความปลอดภัย", h2="ไฟฟ้ารั่ว: อันตรายถึงชีวิตแค่ไหน วิธีทดสอบ และวิธีป้องกัน",
   lede="คู่มือภาษาไทยสำหรับเจ้าของบ้าน ช่างติดตั้ง และทีมงาน: ไฟรั่วคืออะไร ทำไมกระแสเพียงราว 40 mA หยุดหัวใจได้ วิธีทดสอบหาไฟรั่ว และการป้องกันที่ทุกบ้านต้องมี",
   pts=[("ทำไมถึงตาย", "กระแสประมาณ 40 mA ผ่านร่างกายนานเกิน 2 วินาทีอาจทำให้หัวใจหยุดเต้นได้ มือเปียกแตะไฟ 230 V มีกระแสผ่านได้มากกว่านั้นหลายเท่า"),
        ("อะไรช่วยชีวิต", "เครื่องตัดไฟรั่ว RCD/RCBO 30 mA ที่ติดตั้งร่วมกับสายดิน และกดปุ่มทดสอบทุก 6 เดือน เบรกเกอร์ธรรมดา (MCB) ไม่ได้ป้องกันคนจากไฟดูด"),
        ("สาเหตุที่พบบ่อย", "น้ำเข้ากล่องและท่อนอกอาคาร สายไฟแตกจากแดดหรือหนูกัด จุดต่อหลวม เครื่องทำน้ำอุ่นและปั๊มที่ฉนวนเสื่อม ขั้ว MC4 ของแผงโซลาร์เปียก และน้ำท่วม"),
        ("วิธีทดสอบ", "แคลมป์วัดกระแสรั่วคล้อง L และ N พร้อมกัน (มีไฟ) ทดสอบฉนวนที่ 500 V ต้องได้ไม่ต่ำกว่า 1 MΩ (ตัดไฟ) และทดสอบเวลาตัดของ RCD")],
   btn="ดาวน์โหลดคู่มือ (PDF) ↓", btn2=None, src=None)}),
 ("topcon-cell-prices-nov2026", "adoption", "topcon-cell-prices", "news-topcon-cell-prices-20261115.jpg", {
  "en": dict(eyebrow="15 November 2026 · Prices", h2="China's TOPCon cell prices slip as the export rush fades",
   lede="TOPCon M10 cells fell 1.13% in a week to $0.0439/W (FOB China, OPIS, 10 Nov); 210R cells held at $0.0459/W.",
   pts=[("Why", "The buying rush ahead of the US Section 232 measures (from 4 Dec) is over, and demand inside China is weak under market-based power pricing."),
        ("Supply", "Most wafer makers run at about 50% of capacity; November cell output is expected at about 52–53 GW."),
        ("Outlook", "More downward pressure on cell prices, but production cuts and proposed module price floors make a levelling off more likely than a crash."),
        ("For customers", "Panel prices are moving only a little now; starting your savings sooner is worth more than waiting for small price drops.")],
   src=[("pv magazine / OPIS, 13 Nov 2026", "https://www.pv-magazine.com/2026/11/13/chinas-topcon-m10-cell-prices-slip-as-export-rush-fades-domestic-demand-weakens/")]),
  "th": dict(eyebrow="15 พฤศจิกายน 2569 · ราคา", h2="ราคาเซลล์ TOPCon ของจีนอ่อนตัว เมื่อกระแสเร่งส่งออกจบลง",
   lede="เซลล์ TOPCon M10 ลดลง 1.13% ในหนึ่งสัปดาห์ เหลือ $0.0439/W (FOB จีน, OPIS 10 พ.ย.) ส่วน 210R ทรงตัวที่ $0.0459/W",
   pts=[("สาเหตุ", "การเร่งซื้อก่อนมาตรการ Section 232 ของสหรัฐ (มีผล 4 ธ.ค.) จบลง และความต้องการในจีนอ่อนตัวจากการปฏิรูปราคาไฟฟ้าตามกลไกตลาด"),
        ("ฝั่งการผลิต", "โรงงานเวเฟอร์ส่วนใหญ่เดินเครื่องราว 50% คาดว่าการผลิตเซลล์เดือน พ.ย. ราว 52–53 GW"),
        ("แนวโน้ม", "ราคาเซลล์ยังมีแรงกดดันขาลง แต่การลดกำลังผลิตและราคาขั้นต่ำของแผงที่เสนอ ทำให้น่าจะทรงตัวมากกว่าดิ่งลง"),
        ("สำหรับลูกค้า", "ราคาแผงเปลี่ยนแปลงเพียงเล็กน้อย การเริ่มประหยัดค่าไฟเร็วขึ้นคุ้มกว่าการรอราคาลดอีกนิด")],
   src=[("pv magazine / OPIS, 13 พ.ย. 2569", "https://www.pv-magazine.com/2026/11/13/chinas-topcon-m10-cell-prices-slip-as-export-rush-fades-domestic-demand-weakens/")])}),
 ("huawei-luterra-s2-all-in-one", "innovation", "huawei-luterra-s2", "news-huawei-luterra-s2-20261115.jpg", {
  "en": dict(eyebrow="15 November 2026 · Products", h2="Huawei launches LUTERRA S2, a 20 kW all-in-one home energy system",
   lede="Inverter, battery and AI energy management in one stackable unit, launched in Europe on 11 November 2026.",
   pts=[("Power", "Single-phase 3–10 kW and three-phase 5–20 kW; up to three units in parallel for 60 kW."),
        ("Storage", "5 or 7 kWh battery packs, up to 48 packs (336 kWh)."),
        ("Design", "Full silicon-carbide electronics, up to 99% efficiency, no fans, below 29 dB, -25 to +60 °C, IP66; backup switchover under 10 ms."),
        ("In Thailand", "Price, warranty and local availability are not announced yet, so we will not quote it until they are confirmed.")],
   src=[("pv magazine, 11 Nov 2026", "https://www.pv-magazine.com/2026/11/11/huawei-unveils-20-kw-all-in-one-residential-energy-storage-system/")]),
  "th": dict(eyebrow="15 พฤศจิกายน 2569 · ผลิตภัณฑ์", h2="Huawei เปิดตัว LUTERRA S2 ระบบพลังงานบ้านแบบรวมเครื่องเดียว 20 kW",
   lede="รวมอินเวอร์เตอร์ แบตเตอรี่ และระบบจัดการพลังงานด้วย AI ในเครื่องเดียวแบบซ้อนต่อได้ เปิดตัวที่ยุโรปเมื่อ 11 พฤศจิกายน 2569",
   pts=[("กำลังไฟ", "เฟสเดียว 3–10 kW และสามเฟส 5–20 kW ต่อขนานได้ 3 เครื่อง รวม 60 kW"),
        ("แบตเตอรี่", "ชุดละ 5 หรือ 7 kWh ต่อได้ถึง 48 ชุด (336 kWh)"),
        ("การออกแบบ", "อิเล็กทรอนิกส์ซิลิคอนคาร์ไบด์ทั้งระบบ ประสิทธิภาพสูงสุด 99% ไม่มีพัดลม เสียงต่ำกว่า 29 dB ทำงาน -25 ถึง +60 °C มาตรฐาน IP66 สลับไปไฟสำรองภายใน 10 ms"),
        ("ในประเทศไทย", "ยังไม่ประกาศราคา การรับประกัน และการวางขายในไทย เราจึงยังไม่เสนอราคาจนกว่าจะยืนยันได้")],
   src=[("pv magazine, 11 พ.ย. 2569", "https://www.pv-magazine.com/2026/11/11/huawei-unveils-20-kw-all-in-one-residential-energy-storage-system/")])}),
 ("grid-forming-ai-renewables", "innovation", "grid-forming-ai", "news-grid-forming-ai-20261115.jpg", {
  "en": dict(eyebrow="15 November 2026 · Technology", h2="How grid-forming batteries and AI help more renewables onto the grid",
   lede="Grid-forming storage holds voltage and frequency steady on weak grids; AI energy management forecasts solar and load to run the battery better. (Vendor-sponsored article, figures not independently verified.)",
   pts=[("Weak grids", "Frequency change held within 0.5 Hz/s on a very weak grid; example: 30 MW of PV with a 6 MW / 24 MWh grid-forming battery in Ngari, China."),
        ("Smarter batteries", "Forecast-based peak shaving and valley filling; lifecycle returns more than 10% better."),
        ("Remote sites", "Factory-tested microgrids cost 40–60% less than diesel; more than 90% of common faults fixed remotely."),
        ("For our customers", "Most useful at off-grid and end-of-line sites such as mountain homestays, resorts and farms.")],
   src=[("pv magazine, 21 Sep 2026 (sponsored by Huawei Digital Power)", "https://www.pv-magazine.com/2026/09/21/how-grid-forming-and-ai-technologies-are-helping-overcome-barriers-to-renewable-growth/")]),
  "th": dict(eyebrow="15 พฤศจิกายน 2569 · เทคโนโลยี", h2="แบตเตอรี่แบบสร้างกริดและ AI ช่วยให้กริดรับพลังงานหมุนเวียนได้มากขึ้น",
   lede="แบตเตอรี่แบบสร้างกริด (Grid-forming) ช่วยคุมแรงดันและความถี่บนกริดที่อ่อน ส่วน AI พยากรณ์การผลิตโซลาร์และการใช้ไฟเพื่อสั่งงานแบตเตอรี่ให้ดีขึ้น (เนื้อหาสนับสนุนโดยผู้ผลิต ตัวเลขยังไม่ได้ตรวจสอบอิสระ)",
   pts=[("กริดอ่อน", "คุมอัตราเปลี่ยนความถี่ได้ภายใน 0.5 Hz/s ตัวอย่าง: โซลาร์ 30 MW กับแบตเตอรี่สร้างกริด 6 MW / 24 MWh ที่ Ngari ประเทศจีน"),
        ("แบตเตอรี่ฉลาดขึ้น", "Peak shaving และ valley filling ตามการพยากรณ์ ผลตอบแทนตลอดอายุโครงการดีขึ้นกว่า 10%"),
        ("พื้นที่ห่างไกล", "ไมโครกริดทดสอบจากโรงงานถูกกว่าดีเซล 40–60% และแก้ปัญหาทั่วไปจากระยะไกลได้กว่า 90%"),
        ("สำหรับลูกค้าของเรา", "มีประโยชน์ที่สุดกับพื้นที่นอกกริดและปลายสาย เช่น โฮมสเตย์บนเขา รีสอร์ท และฟาร์ม")],
   src=[("pv magazine, 21 ก.ย. 2569 (สนับสนุนโดย Huawei Digital Power)", "https://www.pv-magazine.com/2026/09/21/how-grid-forming-and-ai-technologies-are-helping-overcome-barriers-to-renewable-growth/")])}),
 ("thailand-solar-market-2031", "adoption", "thailand-solar-market-2031", "news-thailand-solar-market-2031-20261115.jpg", {
  "en": dict(eyebrow="15 November 2026 · Thailand", h2="Thailand's solar market: 5.2 GW to 7.7 GW by 2031",
   lede="Mordor Intelligence expects Thailand's installed solar to grow about 6.8% a year, with homes and off-grid systems growing fastest.",
   pts=[("Growth", "5.20 GW in 2025 and 5.55 GW in 2026, rising to 7.71 GW in 2031."),
        ("Fastest segments", "Residential at 10.25% a year and off-grid at 9.22%, while utility-scale plants still hold about half of capacity."),
        ("Drivers and brakes", "Rising grid tariffs, cheaper modules and the direct PPA pilot push growth; slow grid approvals and saturated feeders hold it back."),
        ("Policy", "Home surplus buyback at 2.20 baht/kWh from 1 July 2026, and a personal income tax deduction of up to 200,000 baht for qualifying rooftop systems.")],
   src=[("Mordor Intelligence, report page updated 23 Jul 2026", "https://www.mordorintelligence.com/industry-reports/thailand-solar-energy-market")]),
  "th": dict(eyebrow="15 พฤศจิกายน 2569 · ประเทศไทย", h2="ตลาดโซลาร์ไทย: 5.2 GW สู่ 7.7 GW ภายในปี 2574",
   lede="Mordor Intelligence คาดว่ากำลังผลิตโซลาร์ที่ติดตั้งในไทยจะโตราว 6.8% ต่อปี โดยกลุ่มบ้านและระบบนอกกริดโตเร็วที่สุด",
   pts=[("การเติบโต", "5.20 GW ในปี 2568 และ 5.55 GW ในปี 2569 เพิ่มเป็น 7.71 GW ในปี 2574"),
        ("กลุ่มที่โตเร็วที่สุด", "ที่อยู่อาศัยโต 10.25% ต่อปี นอกกริด 9.22% ขณะที่โรงไฟฟ้าขนาดใหญ่ยังมีสัดส่วนราวครึ่งหนึ่ง"),
        ("ปัจจัยหนุนและฉุด", "ค่าไฟสูงขึ้น แผงถูกลง และโครงการนำร่อง Direct PPA หนุนการเติบโต ส่วนการอนุมัติเชื่อมกริดที่ช้าและสายป้อนที่เต็มเป็นตัวฉุด"),
        ("นโยบาย", "รับซื้อไฟส่วนเกินจากบ้าน 2.20 บาท/หน่วย ตั้งแต่ 1 ก.ค. 2569 และลดหย่อนภาษีเงินได้สูงสุด 200,000 บาทสำหรับโซลาร์บนหลังคาที่เข้าเงื่อนไข")],
   src=[("Mordor Intelligence ปรับปรุง 23 ก.ค. 2569", "https://www.mordorintelligence.com/industry-reports/thailand-solar-energy-market")])}),
 ("hyperscalers-utility-monopoly", "datacenter", "hyperscalers-utility-monopoly", "news-hyperscalers-utility-monopoly-20261115.jpg", {
  "en": dict(eyebrow="15 November 2026 · Data Center", h2="Big tech's own power plants challenge the utility monopoly",
   lede="In the US, AI data-centre owners are building onsite generation at a scale utilities have never faced, and they have the money to shape the rules.",
   pts=[("Scale", "10+ onsite plants for data centres filed in Ohio since 2025, a 350 MW off-grid microgrid with a 430 MWh battery, and projects of 2–2.45 GW elsewhere."),
        ("Outlook", "Enverus expects 62 GW of new US data-centre capacity by 2030, about 40% of it behind the meter."),
        ("Money gap", "The seven biggest US tech companies are worth about 15–16 times all 31 US listed utilities."),
        ("The lesson", "Every big project pairs generation with batteries; the same logic of self-generation applies to homes, factories and resorts.")],
   src=[("Energy Changemakers, 9 Aug 2026", "https://energychangemakers.com/hyperscalers-threaten-utility-monopoly-with-onsite-energy/")]),
  "th": dict(eyebrow="15 พฤศจิกายน 2569 · ดาต้าเซ็นเตอร์", h2="โรงไฟฟ้าของบริษัทเทคยักษ์ใหญ่ ท้าทายการผูกขาดของการไฟฟ้า",
   lede="ในสหรัฐ เจ้าของดาต้าเซ็นเตอร์ AI สร้างโรงไฟฟ้าในพื้นที่ของตัวเองในขนาดที่การไฟฟ้าไม่เคยเจอ และมีเงินพอจะกำหนดกติกา",
   pts=[("ขนาด", "โรงไฟฟ้าในพื้นที่ของดาต้าเซ็นเตอร์ยื่นขออนุมัติในโอไฮโอกว่า 10 แห่งตั้งแต่ปี 2568 ไมโครกริดนอกกริด 350 MW กับแบตเตอรี่ 430 MWh และโครงการ 2–2.45 GW ในรัฐอื่น"),
        ("แนวโน้ม", "Enverus คาดว่าดาต้าเซ็นเตอร์ใหม่ในสหรัฐจะเพิ่ม 62 GW ภายในปี 2573 ราว 40% ผลิตไฟเองหลังมิเตอร์"),
        ("ช่องว่างด้านเงิน", "บริษัทเทคใหญ่ที่สุด 7 แห่งของสหรัฐมีมูลค่าราว 15–16 เท่าของการไฟฟ้า 31 แห่งในตลาดหุ้นสหรัฐรวมกัน"),
        ("บทเรียน", "ทุกโครงการใหญ่จับคู่การผลิตกับแบตเตอรี่ ตรรกะการผลิตไฟใช้เองแบบเดียวกันใช้ได้กับบ้าน โรงงาน และรีสอร์ท")],
   src=[("Energy Changemakers, 9 ส.ค. 2569", "https://energychangemakers.com/hyperscalers-threaten-utility-monopoly-with-onsite-energy/")])}),
 ("ilsr-solar-equity-monopoly", "consumption", "ilsr-solar-equity-monopoly", "news-ilsr-solar-equity-monopoly-20261115.jpg", {
  "en": dict(eyebrow="15 November 2026 · Opinion (US, 2020)", h2="Solar, equity and monopoly power",
   lede="A US advocacy article argues that rooftop and local solar shift profit and influence away from monopoly utilities, and that the cheapest clean path puts local solar first.",
   pts=[("The argument", "More solar owners means a smaller utility market share, profit and political influence."),
        ("Cost", "A 2020 study cited by the author finds local solar first is the lowest-cost clean path for all grid customers, including people without solar."),
        ("Utility spending", "A few US Southeast utilities spent over $40 billion on risky projects in a decade, paid for by their customers."),
        ("In Thailand", "Self-generation lets homes and businesses produce their own power instead of buying every unit from the grid.")],
   src=[("Institute for Local Self-Reliance, 22 Dec 2020", "https://ilsr.org/article/energy-democracy/lets-talk-about-solar-equity-and-monopoly-power-in-2021/")]),
  "th": dict(eyebrow="15 พฤศจิกายน 2569 · บทความความคิดเห็น (สหรัฐ, 2563)", h2="โซลาร์ ความเป็นธรรม และอำนาจผูกขาด",
   lede="บทความเชิงรณรงค์ในสหรัฐเสนอว่าโซลาร์บนหลังคาและโซลาร์ท้องถิ่นย้ายกำไรและอิทธิพลออกจากการไฟฟ้าผูกขาด และเส้นทางพลังงานสะอาดที่ถูกที่สุดคือให้โซลาร์ท้องถิ่นมาก่อน",
   pts=[("ข้อโต้แย้ง", "ยิ่งมีเจ้าของโซลาร์มาก ส่วนแบ่งตลาด กำไร และอิทธิพลทางการเมืองของการไฟฟ้ายิ่งลดลง"),
        ("ต้นทุน", "งานศึกษาปี 2563 ที่ผู้เขียนอ้างพบว่าการให้โซลาร์ท้องถิ่นมาก่อนเป็นเส้นทางที่ถูกที่สุดสำหรับผู้ใช้ไฟทุกคน รวมถึงคนที่ไม่มีโซลาร์"),
        ("การใช้เงินของการไฟฟ้า", "การไฟฟ้าไม่กี่แห่งทางตะวันออกเฉียงใต้ของสหรัฐใช้เงินกว่า 40,000 ล้านดอลลาร์กับโครงการเสี่ยงใน 10 ปี โดยผู้ใช้ไฟเป็นคนจ่าย"),
        ("ในประเทศไทย", "การผลิตไฟใช้เองทำให้บ้านและธุรกิจผลิตไฟเองได้ แทนการซื้อทุกหน่วยจากการไฟฟ้า")],
   src=[("Institute for Local Self-Reliance, 22 ธ.ค. 2563", "https://ilsr.org/article/energy-democracy/lets-talk-about-solar-equity-and-monopoly-power-in-2021/")])}),
 ("cato-natural-monopoly-distribution", "consumption", "cato-natural-monopoly", "news-cato-natural-monopoly-20261115.jpg", {
  "en": dict(eyebrow="15 November 2026 · Opinion (US, 2016)", h2="Will the natural monopoly in energy distribution end?",
   lede="A 2016 free-market blog post argued that solar and home batteries could break the utilities' hold on distribution. Ten years on, how did it hold up?",
   pts=[("The flaw", "Under cost-plus pricing, utilities earn their costs plus a margin, so they have no reason to cut costs and a reason to spend more."),
        ("The competitor", "Rooftop solar and home batteries could let houses rely far less on the grid, forcing utilities to compete."),
        ("The risk", "If customers leave, fixed grid costs fall on those who stay, raising their bills and pushing more to leave."),
        ("In Thailand", "PEA and MEA run distribution as state monopolies, so generating your own power is the main way to control energy costs.")],
   src=[("Cato Institute blog, 6 Jan 2016", "https://www.cato.org/blog/will-natural-monopoly-energy-distribution-come-end-heres-hoping")]),
  "th": dict(eyebrow="15 พฤศจิกายน 2569 · บทความความคิดเห็น (สหรัฐ, 2559)", h2="การผูกขาดโดยธรรมชาติในระบบจำหน่ายไฟฟ้าจะสิ้นสุดหรือไม่",
   lede="บล็อกฝ่ายตลาดเสรีปี 2559 เสนอว่าโซลาร์และแบตเตอรี่บ้านอาจทำลายการผูกขาดระบบจำหน่ายของการไฟฟ้า ผ่านไป 10 ปี เป็นอย่างไรบ้าง",
   pts=[("จุดอ่อน", "ระบบราคาแบบต้นทุนบวกกำไร ทำให้การไฟฟ้าไม่มีเหตุผลให้ลดต้นทุน และมีแรงจูงใจให้ใช้เงินมากขึ้น"),
        ("คู่แข่ง", "โซลาร์บนหลังคาและแบตเตอรี่บ้านทำให้บ้านพึ่งกริดน้อยลงมาก บังคับให้การไฟฟ้าต้องแข่งขัน"),
        ("ความเสี่ยง", "ถ้าลูกค้าออกจากกริด ต้นทุนคงที่จะตกกับคนที่เหลือ ค่าไฟของพวกเขาสูงขึ้นและผลักให้คนออกมากขึ้น"),
        ("ในประเทศไทย", "กฟภ. และ กฟน. ดูแลระบบจำหน่ายแบบผูกขาดของรัฐ การผลิตไฟใช้เองจึงเป็นทางหลักในการควบคุมค่าไฟ")],
   src=[("Cato Institute, 6 ม.ค. 2559", "https://www.cato.org/blog/will-natural-monopoly-energy-distribution-come-end-heres-hoping")])}),
]

L = {"en": dict(dl="Download the summary (PDF) ↓", th="ภาษาไทย (PDF)", srcl="Source:", tail="Summary by Solar ESS.", alt="First page of the Solar ESS summary"),
     "th": dict(dl="ดาวน์โหลดสรุป (PDF ภาษาไทย) ↓", en="English (PDF)", srcl="ที่มา:", tail="สรุปโดย โซลาร์ เอสส์", alt="หน้าแรกของสรุปโดย Solar ESS")}


def links(lang, slug, t):
    if slug is None:
        pdf = D + "Solar-ESS-Electrical-Leakage-Guide-TH_Rev01_WM_20261115.pdf"
        return pdf, f'<a class="btn" href="{pdf}" download>{t["btn"]}</a>'
    en = D + f"Solar-ESS-News-{slug}_Rev01_WM_20261115.pdf"; th = D + f"Solar-ESS-News-{slug}-TH_Rev01_WM_20261115.pdf"
    if lang == "en":
        return en, (f'<a class="btn" href="{en}" download>{L["en"]["dl"]}</a>'
                    f'<a class="btn ghost" href="{th}" lang="th" style="font-family:var(--thai)">{L["en"]["th"]}</a>')
    return th, f'<a class="btn" href="{th}" download>{L["th"]["dl"]}</a><a class="btn ghost" href="{en}" lang="en">{L["th"]["en"]}</a>'


def article(aid, topics, slug, img, lang, t, first):
    pdf, btns = links(lang, slug, t)
    lis = "".join(f'<li style="margin-bottom:10px"><b>{a}:</b> {b}</li>' for a, b in t["pts"])
    style = 'style="max-width:760px"' if first else SEP
    src = ""
    if t.get("src"):
        src = (f'<p style="margin-top:28px;font-size:14px;color:var(--mute)">{L[lang]["srcl"]} ' +
               " · ".join(f'{n} <a href="{u}" rel="noopener">↗</a>' for n, u in t["src"]) + f'. {L[lang]["tail"]}</p>\n')
    return (f'<article id="{aid}" data-topics="{topics}" {style}>\n'
            f'<p class="eyebrow">{t["eyebrow"]}</p><h2 style="font-size:clamp(26px,3.6vw,40px)">{t["h2"]}</h2>\n'
            f'<p class="lede" style="margin-top:16px;opacity:1">{t["lede"]}</p>\n'
            f'<ul style="margin-top:22px;padding-left:20px">{lis}</ul>\n'
            f'<p style="margin-top:22px"><a href="{pdf}"><img src="/images/{img}" alt="{L[lang]["alt"]}" width="579" height="819" loading="lazy" '
            f'style="width:100%;max-width:360px;height:auto;border:1.5px solid var(--line)"></a></p>\n'
            f'<p style="margin-top:18px;display:flex;gap:10px;flex-wrap:wrap">{btns}</p>\n' + src + '</article>\n')


for lang, path in (("en", "news.html"), ("th", "th/news.html")):
    p = ROOT / path
    s = p.read_text(encoding="utf-8")
    for aid, *_ in A:
        s = re.sub(rf'<article id="{aid}".*?</article>\n?', "", s, flags=re.S)
    m = re.search(r'<article id="([^"]+)" data-topics="[^"]*" style="[^"]*">', s)
    old_first = re.sub(r'style="[^"]*"', SEP, m.group(0))
    block = "".join(article(aid, tp, slug, img, lang, d[lang], i == 0) for i, (aid, tp, slug, img, d) in enumerate(A))
    s = s[:m.start()] + block + old_first + s[m.end():]
    p.write_text(s, encoding="utf-8")
    print(path, "8 articles before", m.group(1))
