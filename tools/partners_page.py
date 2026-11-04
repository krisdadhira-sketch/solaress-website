#!/usr/bin/env python3
"""Builds /partners.html (EN) and /th/partners.html (TH): the Solar ESS installer-partner
directory (by region, no phone numbers) plus the registration and request forms.

The directory itself is filled in the browser from /data/installer-partners.json, so adding
an approved partner only needs a JSON edit, not a rebuild. Re-run this script only when the
page text or forms change:  python3 tools/partners_page.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REGIONS = [  # (key, EN, TH)
    ("north", "Northern", "ภาคเหนือ"),
    ("northeast", "Northeastern", "ภาคตะวันออกเฉียงเหนือ"),
    ("central", "Central", "ภาคกลาง"),
    ("bangkok", "Bangkok & vicinity", "กรุงเทพฯ และปริมณฑล"),
    ("east", "Eastern", "ภาคตะวันออก"),
    ("west", "Western", "ภาคตะวันตก"),
    ("south", "Southern", "ภาคใต้"),
]

SERVICES = [  # (value, EN, TH)
    ("res-ongrid", "Residential rooftop on-grid", "ระบบออนกริดบนหลังคาบ้าน"),
    ("hybrid", "Hybrid with battery", "ระบบไฮบริดพร้อมแบตเตอรี่"),
    ("offgrid", "Off-grid systems", "ระบบออฟกริด"),
    ("ci", "Commercial & industrial rooftop", "หลังคาอาคารพาณิชย์และโรงงาน"),
    ("ground", "Ground mount / carport", "ติดตั้งบนพื้น / โรงจอดรถ"),
    ("battery", "Battery add-on / retrofit", "เพิ่มแบตเตอรี่ระบบเดิม"),
    ("ev", "EV charger circuits", "วงจรเครื่องชาร์จรถไฟฟ้า"),
    ("electrical", "Electrical upgrade (meter, MDB, ATS)", "งานไฟฟ้า (มิเตอร์ ตู้ MDB ATS)"),
    ("structure", "Steel structure / welding", "งานโครงเหล็ก / งานเชื่อม"),
    ("cleaning", "PV cleaning", "ล้างแผงโซลาร์"),
    ("om", "Inspection & maintenance (O&M)", "ตรวจสอบและบำรุงรักษา (O&M)"),
    ("troubleshoot", "Troubleshooting & monitoring setup", "แก้ไขปัญหาและตั้งค่าระบบ Monitoring"),
]

BRANDS = ["Solis", "Huawei", "Deye", "GoodWe", "SAJ", "Growatt", "Sungrow", "SMA"]

TOOLS = [  # (value, EN, TH)
    ("insulation", "Insulation resistance tester", "เครื่องวัดความเป็นฉนวน"),
    ("earth", "Earth resistance tester", "เครื่องวัดความต้านทานดิน"),
    ("clamp", "DC clamp meter", "แคลมป์มิเตอร์ DC"),
    ("ivcurve", "I-V curve tracer", "เครื่องวัด I-V Curve"),
    ("thermal", "Thermal camera", "กล้องถ่ายภาพความร้อน"),
    ("drone", "Drone", "โดรน"),
    ("access", "Scaffolding / lift / roof safety gear", "นั่งร้าน / รถกระเช้า / อุปกรณ์กันตก"),
    ("vehicle", "Own pickup / transport", "มีรถกระบะ / รถขนส่งเอง"),
]

ENG = [  # Council of Engineers (COE) licence for professional practice
    ("associate", "Associate Engineer (ภาคีวิศวกร)", "ภาคีวิศวกร (Associate Engineer)"),
    ("professional", "Professional Engineer (สามัญวิศวกร)", "สามัญวิศวกร (Professional Engineer)"),
    ("senior", "Senior Professional Engineer (วุฒิวิศวกร)", "วุฒิวิศวกร (Senior Professional Engineer)"),
    ("adjunct", "Adjunct Engineer (ภาคีวิศวกรพิเศษ)", "ภาคีวิศวกรพิเศษ (Adjunct Engineer)"),
]

SAFETY = [  # จป. safety officer levels
    ("professional", "Safety Officer, Professional Level (จป.วิชาชีพ)", "จป.วิชาชีพ (Safety Officer, Professional Level)"),
    ("management", "Safety Officer, Management Level (จป.บริหาร)", "จป.บริหาร (Safety Officer, Management Level)"),
    ("adv-technical", "Safety Officer, Advanced Technical Level (จป.เทคนิคขั้นสูง)", "จป.เทคนิคขั้นสูง (Safety Officer, Advanced Technical Level)"),
    ("technical", "Safety Officer, Technical Level (จป.เทคนิค)", "จป.เทคนิค (Safety Officer, Technical Level)"),
    ("supervisory", "Safety Officer, Supervisory Level (จป.หัวหน้างาน)", "จป.หัวหน้างาน (Safety Officer, Supervisory Level)"),
]

SIZES = [  # (value, EN, TH)
    ("10", "Up to 10 kWp", "ไม่เกิน 10 kWp"),
    ("50", "Up to 50 kWp", "ไม่เกิน 50 kWp"),
    ("200", "Up to 200 kWp", "ไม่เกิน 200 kWp"),
    ("1000", "Up to 1 MWp", "ไม่เกิน 1 MWp"),
    ("1000+", "Above 1 MWp", "มากกว่า 1 MWp"),
]

T = {
"en": dict(
    lang="en", pre="", other="/th/partners.html",
    title="Installer Partners by Region · Solar ESS",
    desc="Solar ESS installer partners across Thailand, listed by region. Browse verified installation teams and book them through Solar ESS, or register your team as a subcontract partner.",
    eyebrow="Solar ESS · Installer partners",
    h1="Verified installers,<br>in every region.",
    lede="Solar ESS works with independent installation teams across Thailand as subcontract partners. Each team listed here has been screened by Solar ESS. Browse by region, then book a team through us: Solar ESS acts as main contractor, holds the payment and stands behind the work.",
    nav_dir="Find a partner", nav_reg="Register your team", nav_req="Request an installer",
    how_h="How outsourcing through Solar ESS works",
    how=[("1. Browse", "Pick a region and read each team’s profile: services, system sizes, experience and tools."),
         ("2. Request", "Send us your job with the team you prefer. Contact numbers are not published; every request comes to Solar ESS first."),
         ("3. We contract", "Solar ESS confirms scope and price, signs as main contractor and subcontracts the partner."),
         ("4. Protected", "Your payment is held by Solar ESS and released on completion. We check materials, workmanship and handover.")],
    dir_eyebrow="Directory", dir_h="Installer partners by region",
    dir_lede="Profiles show what each team does and where it works. Phone numbers, addresses and documents are kept private by Solar ESS.",
    filter_all="All regions", filter_svc="Any service",
    empty="No partners listed in this region yet.", empty_cta="Install solar here? Register your team",
    verified="Verified by Solar ESS", base="Base", serves="Also serves", max="Up to",
    yrs="years’ experience", team="installers", elec="certified electricians", proj="projects", kwp="kWp installed",
    brands_l="Inverters", tools_l="Tools", vat="Can issue tax invoice", ins="Insured", langs_l="Languages",
    req_btn="Request this team",
    reg_eyebrow="Register your team", reg_h="Become a Solar ESS installer partner",
    reg_lede="Installers, electricians and installation companies anywhere in Thailand can register. Approved teams are listed in their region and receive subcontract work from Solar ESS and from partners who outsource through us.",
    get_h="What partners get", get=["A public profile in your region, seen by homeowners, businesses and other installers looking to outsource", "Subcontract jobs from Solar ESS, with clear scope, materials list and fair, agreed prices", "Payment secured by Solar ESS before work starts and paid on completion", "Technical support, material supply in some cases, and help if a dispute arises"],
    rule_h="What we expect", rule=["Work done or supervised by a qualified electrician with a certificate", "Premium materials: copper cable, IMC/EMT conduit runs, well-matched breakers and cables", "Clear quotes: labour only, and labour & materials", "All jobs from the directory are contracted through Solar ESS"],
    priv_h="What we publish", priv="Only Sections 1 and 2 and the photos you mark for publication. Your phone number, email, LINE, address, ID and documents are never published.",
    s1="1. Public profile (published)", s2="2. Experience and capability (published)", s3="3. Private details (never published)", s4="4. Documents and photos", s5="5. Agreement",
    f_name="Team or business name as it should appear", f_type="Type", types=["Individual installer", "Installation team (not registered)", "Registered company / partnership"],
    f_region="Main region", f_prov="Base province", f_amphoe="Base district (amphoe)", f_serves="Other provinces you work in (optional)",
    f_svc="Services you offer", f_size="Largest single system you can install", f_bio="Short introduction (up to 400 characters): what you do best and the kind of jobs you want",
    f_years="Years installing solar", f_team="Installers in your team", f_elec="Certified electricians in your team", f_proj="Solar projects completed (approx.)", f_kwp="Total capacity installed (kWp, approx.)",
    f_brands="Inverter brands you have installed", f_other_brand="Other brands (optional)", f_batt="Battery brands you have installed (optional)", f_tools="Tools and equipment you own", f_eng_q="Can you provide a licensed engineer (COE licence for professional practice) on a job?", f_eng="If yes, which licence level(s)?", f_safety_q="Can you provide a qualified safety officer (จป.) on a job?", f_safety="If yes, which level(s)?", f_wah_q="Can you provide Work at Height certified workers on a job?", f_wah_n="Work at Height certified members in your team", wah_l="Work at height", av=["Yes, in our team", "Yes, we can arrange one for a job", "Not available"], av_short=["In team", "Can arrange", ""], f_lic="Copies of engineering licence, safety officer and Work at Height certificates (PDF, optional, kept private)", eng_l="Engineers", safety_l="Safety officers",
    f_vat="Can you issue a tax invoice (VAT registered)?", yes="Yes", no="No", f_ins="Do you carry work or liability insurance?",
    f_langs="Languages your team speaks", langs=["Thai", "English", "Chinese", "Burmese", "Lao"], f_avail="Availability", avails=["Full time", "Project based", "Weekends / part time"],
    f_legal="Legal name (person or company)", f_tax="Tax ID or national ID no.", f_cname="Contact person", f_phone="Phone", f_email="Email", f_line="LINE ID", f_addr="Address",
    f_rate="Typical labour rate, THB per kWp (optional, kept private)", f_ref="A past customer we may contact, with phone (optional)",
    docs_fine="All uploads are optional. PDF for documents; JPG or PNG for photos. Keep all files together under 8 MB. We may ask for your electrician certificate and ID before we approve your profile.",
    f_logo="Profile photo or logo (optional, published)", f_cert="Electrician certificate (PDF, optional)", f_id="Company registration, or ID card for individuals (PDF, optional)",
    f_port="Portfolio of past works (PDF, optional)", f_ph1="Project photo 1 (optional, published)", f_ph2="Project photo 2 (optional, published)", f_ph3="Project photo 3 (optional, published)",
    a_pub="I agree that Solar ESS may publish Sections 1 and 2 and the photos marked “published” on solaress.org. My contact details and documents stay private.",
    a_terms="I agree that jobs from this directory are contracted through Solar ESS as main contractor, and that I will use premium materials and have the work done by a qualified electrician.",
    a_true="I confirm the information is true, and Solar ESS may verify it, visit a site or contact past customers.",
    reg_btn="Send registration",
    reg_after="We review every registration and reply by phone or email. Approved profiles appear in the directory, usually within 7 days.",
    req_eyebrow="Request an installer", req_h="Tell us about your job",
    req_lede="Choose a team from the directory, or leave it blank and we will match the right partner in your area. Solar ESS replies with scope, price and the team assigned.",
    q_partner="Team you prefer", q_none="Any team: let Solar ESS choose", q_name="Your name", q_company="Company (optional)", q_phone="Phone", q_email="Email",
    q_prov="Project province", q_jtype="Type of job", q_size="System size (kWp, approx., optional)", q_start="Preferred start (optional)", q_msg="Job details: site, scope, materials, anything we should know",
    q_agree="I understand the job will be contracted with Solar ESS as main contractor, with payment held by Solar ESS until completion.",
    req_send="Send request",
),
"th": dict(
    lang="th", pre="/th", other="/partners.html",
    title="ทีมช่างพันธมิตรแยกตามภูมิภาค · Solar ESS",
    desc="ทีมช่างติดตั้งพันธมิตรของ Solar ESS ทั่วประเทศไทย แยกตามภูมิภาค เลือกทีมที่ผ่านการตรวจสอบและจ้างผ่าน Solar ESS หรือลงทะเบียนทีมของคุณเป็นพันธมิตรรับงานช่วง",
    eyebrow="Solar ESS · ทีมช่างพันธมิตร",
    h1="ทีมช่างที่ผ่านการตรวจสอบ<br>ในทุกภูมิภาค",
    lede="Solar ESS ร่วมงานกับทีมช่างติดตั้งอิสระทั่วประเทศในฐานะพันธมิตรรับงานช่วง ทุกทีมในหน้านี้ผ่านการคัดกรองโดย Solar ESS เลือกดูตามภูมิภาค แล้วจ้างทีมผ่านเรา โดย Solar ESS เป็นผู้รับเหมาหลัก ถือเงินค่างาน และรับผิดชอบคุณภาพงาน",
    nav_dir="ค้นหาทีมช่าง", nav_reg="ลงทะเบียนทีมของคุณ", nav_req="ขอใช้บริการทีมช่าง",
    how_h="การจ้างงานผ่าน Solar ESS",
    how=[("1. เลือกดู", "เลือกภูมิภาค แล้วอ่านโปรไฟล์ของแต่ละทีม: บริการ ขนาดระบบ ประสบการณ์ และเครื่องมือ"),
         ("2. ส่งคำขอ", "ส่งรายละเอียดงานพร้อมทีมที่ต้องการ เราไม่เผยแพร่เบอร์โทร ทุกคำขอส่งถึง Solar ESS ก่อน"),
         ("3. ทำสัญญา", "Solar ESS ยืนยันขอบเขตงานและราคา ลงนามเป็นผู้รับเหมาหลัก และจ้างช่วงทีมพันธมิตร"),
         ("4. คุ้มครอง", "Solar ESS ถือเงินค่างานไว้และจ่ายเมื่องานเสร็จ เราตรวจวัสดุ ฝีมือ และการส่งมอบงาน")],
    dir_eyebrow="รายชื่อทีมช่าง", dir_h="ทีมช่างพันธมิตรแยกตามภูมิภาค",
    dir_lede="โปรไฟล์แสดงบริการและพื้นที่ทำงานของแต่ละทีม เบอร์โทร ที่อยู่ และเอกสารต่าง ๆ Solar ESS เก็บเป็นความลับ",
    filter_all="ทุกภูมิภาค", filter_svc="ทุกบริการ",
    empty="ยังไม่มีทีมพันธมิตรในภูมิภาคนี้", empty_cta="ติดตั้งโซลาร์ในพื้นที่นี้? ลงทะเบียนทีมของคุณ",
    verified="ตรวจสอบโดย Solar ESS", base="ฐาน", serves="รับงานใน", max="สูงสุด",
    yrs="ปีประสบการณ์", team="ช่าง", elec="ช่างไฟฟ้ามีใบรับรอง", proj="โครงการ", kwp="kWp ที่ติดตั้ง",
    brands_l="อินเวอร์เตอร์", tools_l="เครื่องมือ", vat="ออกใบกำกับภาษีได้", ins="มีประกัน", langs_l="ภาษา",
    req_btn="ขอใช้บริการทีมนี้",
    reg_eyebrow="ลงทะเบียนทีมของคุณ", reg_h="ร่วมเป็นทีมช่างพันธมิตรของ Solar ESS",
    reg_lede="ช่างติดตั้ง ช่างไฟฟ้า และบริษัทติดตั้งทั่วประเทศลงทะเบียนได้ ทีมที่ผ่านการอนุมัติจะแสดงในภูมิภาคของตน และได้รับงานช่วงจาก Solar ESS และจากพันธมิตรที่จ้างงานผ่านเรา",
    get_h="สิ่งที่พันธมิตรได้รับ", get=["โปรไฟล์สาธารณะในภูมิภาคของคุณ ให้เจ้าของบ้าน ธุรกิจ และผู้ติดตั้งรายอื่นที่ต้องการจ้างงานเห็น", "งานช่วงจาก Solar ESS พร้อมขอบเขตงาน รายการวัสดุ และราคาที่ตกลงกันอย่างเป็นธรรม", "Solar ESS รับเงินค่างานไว้ก่อนเริ่มงาน และจ่ายเมื่องานเสร็จ", "การสนับสนุนด้านเทคนิค วัสดุในบางกรณี และความช่วยเหลือเมื่อมีข้อพิพาท"],
    rule_h="สิ่งที่เราคาดหวัง", rule=["งานทำหรือควบคุมโดยช่างไฟฟ้าที่มีใบรับรอง", "ใช้วัสดุคุณภาพ: สายทองแดง ท่อ IMC/EMT เบรกเกอร์และสายไฟที่เหมาะสมกัน", "เสนอราคาชัดเจน: ค่าแรงอย่างเดียว และค่าแรงพร้อมวัสดุ", "งานทุกงานจากหน้านี้ทำสัญญาผ่าน Solar ESS"],
    priv_h="ข้อมูลที่เราเผยแพร่", priv="เฉพาะส่วนที่ 1 และ 2 และรูปภาพที่ระบุว่าเผยแพร่ เบอร์โทร อีเมล LINE ที่อยู่ บัตรประชาชน และเอกสารของคุณจะไม่ถูกเผยแพร่",
    s1="1. โปรไฟล์สาธารณะ (เผยแพร่)", s2="2. ประสบการณ์และความสามารถ (เผยแพร่)", s3="3. ข้อมูลส่วนตัว (ไม่เผยแพร่)", s4="4. เอกสารและรูปภาพ", s5="5. ข้อตกลง",
    f_name="ชื่อทีมหรือชื่อธุรกิจที่ต้องการให้แสดง", f_type="ประเภท", types=["ช่างอิสระ", "ทีมช่าง (ยังไม่จดทะเบียน)", "บริษัท / ห้างหุ้นส่วนที่จดทะเบียน"],
    f_region="ภูมิภาคหลัก", f_prov="จังหวัดที่ตั้ง", f_amphoe="อำเภอที่ตั้ง", f_serves="จังหวัดอื่นที่รับงาน (ไม่บังคับ)",
    f_svc="บริการที่คุณให้", f_size="ขนาดระบบใหญ่ที่สุดต่อหนึ่งงานที่ติดตั้งได้", f_bio="แนะนำตัวสั้น ๆ (ไม่เกิน 400 ตัวอักษร): งานที่ถนัดและงานที่อยากรับ",
    f_years="ประสบการณ์ติดตั้งโซลาร์ (ปี)", f_team="จำนวนช่างในทีม", f_elec="ช่างไฟฟ้าที่มีใบรับรองในทีม", f_proj="โครงการโซลาร์ที่ทำเสร็จ (โดยประมาณ)", f_kwp="กำลังติดตั้งรวม (kWp โดยประมาณ)",
    f_brands="ยี่ห้ออินเวอร์เตอร์ที่เคยติดตั้ง", f_other_brand="ยี่ห้ออื่น (ไม่บังคับ)", f_batt="ยี่ห้อแบตเตอรี่ที่เคยติดตั้ง (ไม่บังคับ)", f_tools="เครื่องมือและอุปกรณ์ที่มี", f_eng_q="จัดหาวิศวกรที่มีใบอนุญาตประกอบวิชาชีพวิศวกรรมควบคุม (สภาวิศวกร) ประจำงานได้หรือไม่", f_eng="ถ้าได้ ระดับใบอนุญาต", f_safety_q="จัดหาเจ้าหน้าที่ความปลอดภัยในการทำงาน (จป.) ประจำงานได้หรือไม่", f_safety="ถ้าได้ ระดับ จป.", f_wah_q="จัดหาช่างที่ผ่านการอบรมการทำงานบนที่สูง (Work at Height) ประจำงานได้หรือไม่", f_wah_n="จำนวนช่างในทีมที่ผ่านการอบรมการทำงานบนที่สูง", wah_l="งานบนที่สูง", av=["ได้ มีในทีม", "ได้ จัดหามาประจำงานได้", "ไม่มี"], av_short=["มีในทีม", "จัดหาได้", ""], f_lic="สำเนาใบอนุญาตวิศวกร ใบรับรอง จป. และใบรับรองการทำงานบนที่สูง (PDF ไม่บังคับ เก็บเป็นความลับ)", eng_l="วิศวกร", safety_l="จป.",
    f_vat="ออกใบกำกับภาษีได้หรือไม่ (จดทะเบียนภาษีมูลค่าเพิ่ม)", yes="ได้", no="ไม่ได้", f_ins="มีประกันภัยงานหรือประกันความรับผิดหรือไม่",
    f_langs="ภาษาที่ทีมใช้ได้", langs=["ไทย", "อังกฤษ", "จีน", "พม่า", "ลาว"], f_avail="รูปแบบการรับงาน", avails=["เต็มเวลา", "รายโครงการ", "วันหยุด / พาร์ตไทม์"],
    f_legal="ชื่อตามกฎหมาย (บุคคลหรือบริษัท)", f_tax="เลขประจำตัวผู้เสียภาษีหรือเลขบัตรประชาชน", f_cname="ผู้ติดต่อ", f_phone="เบอร์โทร", f_email="อีเมล", f_line="LINE ID", f_addr="ที่อยู่",
    f_rate="ค่าแรงโดยทั่วไป บาทต่อ kWp (ไม่บังคับ เก็บเป็นความลับ)", f_ref="ลูกค้าเก่าที่เราติดต่อได้ พร้อมเบอร์โทร (ไม่บังคับ)",
    docs_fine="การแนบไฟล์ทั้งหมดไม่บังคับ เอกสารเป็น PDF รูปภาพเป็น JPG หรือ PNG ขนาดไฟล์รวมไม่เกิน 8 MB เราอาจขอใบรับรองช่างไฟฟ้าและบัตรประชาชนก่อนอนุมัติโปรไฟล์",
    f_logo="รูปโปรไฟล์หรือโลโก้ (ไม่บังคับ เผยแพร่)", f_cert="ใบรับรองช่างไฟฟ้า (PDF ไม่บังคับ)", f_id="หนังสือรับรองบริษัท หรือบัตรประชาชนสำหรับบุคคล (PDF ไม่บังคับ)",
    f_port="ผลงานที่ผ่านมา (PDF ไม่บังคับ)", f_ph1="รูปผลงาน 1 (ไม่บังคับ เผยแพร่)", f_ph2="รูปผลงาน 2 (ไม่บังคับ เผยแพร่)", f_ph3="รูปผลงาน 3 (ไม่บังคับ เผยแพร่)",
    a_pub="ข้าพเจ้ายินยอมให้ Solar ESS เผยแพร่ข้อมูลส่วนที่ 1 และ 2 และรูปภาพที่ระบุว่า “เผยแพร่” บน solaress.org โดยข้อมูลติดต่อและเอกสารของข้าพเจ้าจะไม่ถูกเผยแพร่",
    a_terms="ข้าพเจ้ายอมรับว่างานจากหน้านี้ทำสัญญาผ่าน Solar ESS ในฐานะผู้รับเหมาหลัก และจะใช้วัสดุคุณภาพ โดยให้ช่างไฟฟ้าที่มีใบรับรองเป็นผู้ทำงาน",
    a_true="ข้าพเจ้ายืนยันว่าข้อมูลเป็นความจริง และยินยอมให้ Solar ESS ตรวจสอบ เยี่ยมชมหน้างาน หรือติดต่อลูกค้าเก่า",
    reg_btn="ส่งใบลงทะเบียน",
    reg_after="เราตรวจสอบทุกใบลงทะเบียนและติดต่อกลับทางโทรศัพท์หรืออีเมล โปรไฟล์ที่ผ่านการอนุมัติจะแสดงในหน้านี้ โดยปกติภายใน 7 วัน",
    req_eyebrow="ขอใช้บริการทีมช่าง", req_h="บอกรายละเอียดงานของคุณ",
    req_lede="เลือกทีมจากรายชื่อ หรือเว้นว่างไว้ให้เราจับคู่ทีมพันธมิตรที่เหมาะสมในพื้นที่ของคุณ Solar ESS จะตอบกลับพร้อมขอบเขตงาน ราคา และทีมที่รับผิดชอบ",
    q_partner="ทีมที่ต้องการ", q_none="ทีมใดก็ได้: ให้ Solar ESS เลือก", q_name="ชื่อของคุณ", q_company="บริษัท (ไม่บังคับ)", q_phone="เบอร์โทร", q_email="อีเมล",
    q_prov="จังหวัดของโครงการ", q_jtype="ประเภทงาน", q_size="ขนาดระบบ (kWp โดยประมาณ ไม่บังคับ)", q_start="ช่วงเวลาที่ต้องการเริ่ม (ไม่บังคับ)", q_msg="รายละเอียดงาน: หน้างาน ขอบเขต วัสดุ และสิ่งที่เราควรทราบ",
    q_agree="ข้าพเจ้าเข้าใจว่างานนี้ทำสัญญากับ Solar ESS ในฐานะผู้รับเหมาหลัก โดย Solar ESS ถือเงินค่างานไว้จนงานเสร็จ",
    req_send="ส่งคำขอ",
),
}

CSS = """<style id="partners-css">
.pnav{display:flex;flex-wrap:wrap;gap:10px;margin-top:22px}
.how{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin-top:22px}
.how div{border:1px solid var(--line);border-radius:16px;padding:18px;background:#fff}
.how b{display:block;font-size:17px;margin-bottom:6px;color:var(--navy)}
.pfilters{display:flex;flex-wrap:wrap;gap:12px;margin:22px 0 6px}
.pfilters select{font:inherit;font-size:15px;padding:10px 14px;border:1.5px solid var(--line);border-radius:12px;background:#fff;color:var(--ink)}
.preg{margin-top:34px}.preg>h3{font-size:22px;border-bottom:2px solid var(--line);padding-bottom:8px;display:flex;justify-content:space-between;align-items:baseline;gap:12px}
.preg>h3 small{font-family:var(--mono);font-size:12px;color:var(--mute);letter-spacing:.1em}
.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:18px;margin-top:16px}
.pcard{border:1px solid var(--line);border-radius:18px;background:#fff;overflow:hidden;display:flex;flex-direction:column}
.pcard .ph{aspect-ratio:16/9;background:var(--sky) center/cover no-repeat}
.pcard .bd{padding:18px;display:grid;gap:10px;flex:1;text-align:left;align-content:start}
.pcard .hd{display:flex;gap:12px;align-items:center}.pcard .hd img{width:52px;height:52px;border-radius:50%;object-fit:cover;border:1px solid var(--line)}
.pcard h4{font-size:18px;margin:0}.pcard .loc{font-size:13px;color:var(--mute)}
.pcard .ver{display:inline-block;font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:#fff;background:var(--blue);border-radius:99px;padding:3px 9px;width:max-content}
.pcard .pstats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;font-size:12px;color:var(--mute)}.pcard .pstats div{background:var(--paper);border-radius:10px;padding:8px;margin:0}.pcard .pstats b{display:block;font-size:17px;color:var(--navy)}
.ptags{display:flex;flex-wrap:wrap;gap:6px}.ptags span{font-family:inherit;font-size:12px;color:var(--ink);background:var(--paper);border:1px solid var(--line);border-radius:99px;padding:3px 9px}
.pcard dl{display:grid;grid-template-columns:auto 1fr;gap:4px 10px;font-size:13px;margin:0}.pcard dt{color:var(--mute)}.pcard dd{margin:0}
.pcard .btn{margin-top:auto;text-align:center}
.pempty{border:1.5px dashed var(--line);border-radius:16px;padding:18px;color:var(--mute);margin-top:14px}.pempty a{font-weight:600}
.pform .apply{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);gap:48px}
.pform input,.pform form select,.pform form textarea{font:inherit;font-size:15px;letter-spacing:0;text-transform:none;color:var(--white);background:transparent;border:0;border-bottom:1.5px solid rgba(255,255,255,.4);padding:8px 0;border-radius:0;width:100%;min-width:0;box-sizing:border-box}
.pform form select option{color:#0A0E2E}
.pform input[type=file]{border-bottom:0;padding:6px 0;font-size:14px}
.pform .chks{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:8px 14px}.pform .chk{display:flex!important;gap:10px;align-items:flex-start;font-family:inherit!important;font-size:14px!important;letter-spacing:0!important;text-transform:none!important;line-height:1.45;opacity:.95!important}.pform .chk input{width:auto!important;margin-top:3px;border:0;flex:none;accent-color:var(--blue)}
.pform .grp{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;opacity:.8;margin:0 0 8px}
.pform .chks3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px 14px}
.pform .cnt{font-size:12px;opacity:.7;text-align:right}
@media (max-width:860px){.how{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}.pform .apply,.pform .two,.pform .chks,.pform .chks3{grid-template-columns:minmax(0,1fr)}}
@media (max-width:520px){.how{grid-template-columns:minmax(0,1fr)}}
</style>"""


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def chks(name, items, required_one=False, cols3=False):
    cls = "chks3" if cols3 else "chks"
    out = []
    for v, label in items:
        out.append(f'<label class="chk"><input type="checkbox" name="{name}" value="{esc(v)}"><span>{esc(label)}</span></label>')
    extra = f' data-need-one="{name}"' if required_one else ""
    return f'<div class="{cls}"{extra}>' + "".join(out) + "</div>"


def radios(name, items, required=True):
    out = []
    for i, (v, label) in enumerate(items):
        req = " required" if required and i == 0 else ""
        out.append(f'<label class="chk"><input type="radio" name="{name}" value="{esc(v)}"{req}><span>{esc(label)}</span></label>')
    return '<div class="chks">' + "".join(out) + "</div>"


def opts(items, placeholder):
    return f'<option value="">{esc(placeholder)}</option>' + "".join(f'<option value="{esc(v)}">{esc(l)}</option>' for v, l in items)


def build(lang):
    t = T[lang]
    th = lang == "th"
    li = 2 if th else 1
    regions = [(x[0], x[li]) for x in REGIONS]
    svcs = [(s[0], s[li]) for s in SERVICES]
    tools = [(s[0], s[li]) for s in TOOLS]
    sizes = [(s[0], s[li]) for s in SIZES]
    eng = [(s[0], s[li]) for s in ENG]
    safety = [(s[0], s[li]) for s in SAFETY]
    avail3 = list(zip(["in-team", "can-arrange", "no"], t["av"]))
    choose = "เลือก" if th else "Choose one"

    src = (ROOT / ("th/team.html" if th else "team.html")).read_text(encoding="utf-8")
    head_end = src.index('<section class="dark band"')
    head = src[:head_end]
    foot = re.sub(r'\n?<script src="/tsia\.js[^>]*></script>', "", src[src.index("<footer>"):])

    # page meta
    url = f"https://solaress.org{t['pre']}/partners"
    head = re.sub(r"<title>.*?</title>", f"<title>{esc(t['title'])}</title>", head, count=1)
    head = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + esc(t["desc"]), head, count=1)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + esc(t["title"]), head, count=1)
    head = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + esc(t["desc"]), head, count=1)
    head = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + url + ".html", head, count=1)
    head = re.sub(r'(<meta property="og:image" content=")[^"]*', lambda m: m.group(1) + "https://solaress.org/images/tsia-interwoven-dark.jpg", head, count=1)
    head = re.sub(r'(<meta property="og:image:width" content=")[^"]*', lambda m: m.group(1) + "1600", head, count=1)
    head = re.sub(r'(<meta property="og:image:height" content=")[^"]*', lambda m: m.group(1) + "900", head, count=1)
    head = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', head, count=1)
    head = re.sub(r'<link rel="alternate" hreflang="en" href="[^"]*">', '<link rel="alternate" hreflang="en" href="https://solaress.org/partners">', head, count=1)
    head = re.sub(r'<link rel="alternate" hreflang="th" href="[^"]*">', '<link rel="alternate" hreflang="th" href="https://solaress.org/th/partners">', head, count=1)
    head = re.sub(r'<link rel="alternate" hreflang="zh-Hans" href="[^"]*">\s*', "", head, count=1)
    head = re.sub(r'<link rel="alternate" hreflang="x-default" href="[^"]*">', '<link rel="alternate" hreflang="x-default" href="https://solaress.org/partners">', head, count=1)
    # language switch: EN / TH only for this page
    head = re.sub(r'<span class="langsw">.*?</span>(?=</nav>)',
                  '<span class="langsw"><a href="/partners.html" lang="en"' + ('' if th else ' aria-current="true"') + '>EN</a>'
                  '<a href="/th/partners.html" lang="th" style="font-family:var(--thai)"' + (' aria-current="true"' if th else '') + '>ไทย</a></span>',
                  head, count=1, flags=re.S)
    head = head.replace("</head>", CSS + "\n</head>", 1)

    how = "".join(f"<div><b>{esc(a)}</b>{esc(b)}</div>" for a, b in t["how"])
    hero = (f'<section class="dark band" style="padding-block:64px"><div class="wrap"><p class="eyebrow">{esc(t["eyebrow"])}</p>'
            f'<h1 style="font-size:clamp(36px,6vw,64px)">{t["h1"]}</h1><p class="lede" style="margin-top:18px">{esc(t["lede"])}</p>'
            f'<div class="faqnav"><a href="#directory">{esc(t["nav_dir"])}</a><a href="#request">{esc(t["nav_req"])}</a><a href="#register">{esc(t["nav_reg"])}</a></div></div></section>\n')
    howsec = (f'<section class="band light wide" style="padding-block:48px"><div class="wrap"><h2>{esc(t["how_h"])}</h2><div class="how">{how}</div></div></section>\n')

    region_opts = "".join(f'<option value="{k}">{esc(l)}</option>' for k, l in regions)
    svc_opts = "".join(f'<option value="{k}">{esc(l)}</option>' for k, l in svcs)
    directory = (f'<section class="band light wide" id="directory" style="background:var(--paper)"><div class="wrap"><p class="eyebrow">{esc(t["dir_eyebrow"])}</p>'
                 f'<h2>{esc(t["dir_h"])}</h2><p class="lede" style="margin-top:14px">{esc(t["dir_lede"])}</p>'
                 f'<div class="pfilters"><select id="pf-region" aria-label="{esc(t["f_region"])}"><option value="">{esc(t["filter_all"])}</option>{region_opts}</select>'
                 f'<select id="pf-svc" aria-label="{esc(t["f_svc"])}"><option value="">{esc(t["filter_svc"])}</option>{svc_opts}</select></div>'
                 f'<div id="pdir"></div></div></section>\n')

    # ---- request form
    jtypes = [(s[0], s[li]) for s in SERVICES]
    request = (f'<section class="band dark pform" id="request" style="padding-block:64px"><div class="wrap apply">'
               f'<div><p class="eyebrow">{esc(t["req_eyebrow"])}</p><h2>{esc(t["req_h"])}</h2><p class="lede" style="margin-top:18px">{esc(t["req_lede"])}</p></div>'
               f'<form name="installer-request" method="POST" data-netlify="true" netlify-honeypot="bot-field" action="{t["pre"]}/thanks.html">'
               f'<input type="hidden" name="form-name" value="installer-request"><input type="hidden" name="language" value="{"Thai" if th else "English"}"><p hidden><label>Leave empty <input name="bot-field"></label></p>'
               f'<label for="q-partner">{esc(t["q_partner"])}<select id="q-partner" name="partner"><option value="">{esc(t["q_none"])}</option></select></label>'
               f'<div class="two"><label for="q-name">{esc(t["q_name"])}<input id="q-name" name="name" required autocomplete="name"></label><label for="q-company">{esc(t["q_company"])}<input id="q-company" name="company" autocomplete="organization"></label></div>'
               f'<div class="two"><label for="q-phone">{esc(t["q_phone"])}<input id="q-phone" name="phone" type="tel" required autocomplete="tel"></label><label for="q-email">{esc(t["q_email"])}<input id="q-email" name="email" type="email" required autocomplete="email"></label></div>'
               f'<div class="two"><label for="q-prov">{esc(t["q_prov"])}<input id="q-prov" name="project-province" required></label><label for="q-jtype">{esc(t["q_jtype"])}<select id="q-jtype" name="job-type" required>{opts(jtypes, choose)}</select></label></div>'
               f'<div class="two"><label for="q-size">{esc(t["q_size"])}<input id="q-size" name="system-kwp" inputmode="decimal"></label><label for="q-start">{esc(t["q_start"])}<input id="q-start" name="preferred-start" type="month"></label></div>'
               f'<label for="q-msg">{esc(t["q_msg"])}<textarea id="q-msg" name="job-details" rows="4" required></textarea></label>'
               f'<label class="chk"><input type="checkbox" name="agree-contract" value="yes" required><span>{esc(t["q_agree"])}</span></label>'
               f'<button class="btn" type="submit">{esc(t["req_send"])}</button></form></div></section>\n')

    # ---- registration form
    get = "".join(f"<li>{esc(x)}</li>" for x in t["get"])
    rule = "".join(f"<li>{esc(x)}</li>" for x in t["rule"])
    types = [(x, x) for x in t["types"]]
    brand_items = [(b, b) for b in BRANDS]
    lang_items = [(x, x) for x in t["langs"]]
    avail_items = [(x, x) for x in t["avails"]]
    yn = [("yes", t["yes"]), ("no", t["no"])]
    reg = (f'<section class="band dark pform" id="register" style="padding-block:64px;border-top:1px solid rgba(255,255,255,.12)"><div class="wrap apply">'
           f'<div><p class="eyebrow">{esc(t["reg_eyebrow"])}</p><h2>{esc(t["reg_h"])}</h2><p class="lede" style="margin-top:18px">{esc(t["reg_lede"])}</p>'
           f'<div class="mediate"><h3>{esc(t["get_h"])}</h3><ul>{get}</ul></div>'
           f'<div class="mediate"><h3>{esc(t["rule_h"])}</h3><ul>{rule}</ul></div>'
           f'<div class="mediate"><h3>{esc(t["priv_h"])}</h3><p>{esc(t["priv"])}</p></div>'
           f'<p class="fine" style="margin-top:18px">{esc(t["reg_after"])}</p></div>'
           f'<form name="installer-partner" method="POST" data-netlify="true" netlify-honeypot="bot-field" enctype="multipart/form-data" action="{t["pre"]}/thanks.html">'
           f'<input type="hidden" name="form-name" value="installer-partner"><input type="hidden" name="language" value="{"Thai" if th else "English"}"><p hidden><label>Leave empty <input name="bot-field"></label></p>'
           # 1 public profile
           f'<fieldset><legend>{esc(t["s1"])}</legend>'
           f'<label for="r-name">{esc(t["f_name"])}<input id="r-name" name="display-name" required maxlength="80"></label>'
           f'<div><p class="grp">{esc(t["f_type"])}</p>{radios("partner-type", types)}</div>'
           f'<div class="two"><label for="r-region">{esc(t["f_region"])}<select id="r-region" name="region" required>{opts(regions, choose)}</select></label>'
           f'<label for="r-prov">{esc(t["f_prov"])}<input id="r-prov" name="base-province" required></label></div>'
           f'<div class="two"><label for="r-amphoe">{esc(t["f_amphoe"])}<input id="r-amphoe" name="base-district" required></label>'
           f'<label for="r-serves">{esc(t["f_serves"])}<input id="r-serves" name="provinces-served"></label></div>'
           f'<div><p class="grp">{esc(t["f_svc"])}</p>{chks("services", svcs, required_one=True)}</div>'
           f'<label for="r-size">{esc(t["f_size"])}<select id="r-size" name="max-system-size" required>{opts(sizes, choose)}</select></label>'
           f'<label for="r-bio">{esc(t["f_bio"])}<textarea id="r-bio" name="introduction" rows="3" maxlength="400" required></textarea></label><p class="cnt" data-count="r-bio">0 / 400</p>'
           f'</fieldset>'
           # 2 experience
           f'<fieldset><legend>{esc(t["s2"])}</legend>'
           f'<div class="two"><label for="r-years">{esc(t["f_years"])}<input id="r-years" name="years-experience" type="number" min="0" max="60" required></label>'
           f'<label for="r-team">{esc(t["f_team"])}<input id="r-team" name="team-size" type="number" min="1" required></label></div>'
           f'<div class="two"><label for="r-elec">{esc(t["f_elec"])}<input id="r-elec" name="certified-electricians" type="number" min="1" required></label>'
           f'<label for="r-proj">{esc(t["f_proj"])}<input id="r-proj" name="projects-completed" type="number" min="0" required></label></div>'
           f'<label for="r-kwp">{esc(t["f_kwp"])}<input id="r-kwp" name="total-kwp-installed" inputmode="decimal" required></label>'
           f'<div><p class="grp">{esc(t["f_brands"])}</p>{chks("inverter-brands", brand_items, cols3=True)}</div>'
           f'<div class="two"><label for="r-obrand">{esc(t["f_other_brand"])}<input id="r-obrand" name="other-inverter-brands"></label>'
           f'<label for="r-batt">{esc(t["f_batt"])}<input id="r-batt" name="battery-brands"></label></div>'
           f'<div><p class="grp">{esc(t["f_tools"])}</p>{chks("tools", tools)}</div>'
           f'<div><p class="grp">{esc(t["f_eng_q"])}</p>{radios("engineer-availability", avail3)}</div>'
           f'<div><p class="grp">{esc(t["f_eng"])}</p>{chks("engineering-licence", eng)}</div>'
           f'<div><p class="grp">{esc(t["f_safety_q"])}</p>{radios("safety-officer-availability", avail3)}</div>'
           f'<div><p class="grp">{esc(t["f_safety"])}</p>{chks("safety-officer", safety)}</div>'
           f'<div><p class="grp">{esc(t["f_wah_q"])}</p>{radios("work-at-height-availability", avail3)}</div>'
           f'<label for="r-wah">{esc(t["f_wah_n"])}<input id="r-wah" name="work-at-height-certified" type="number" min="0"></label>'
           f'<div><p class="grp">{esc(t["f_vat"])}</p>{radios("tax-invoice", yn)}</div>'
           f'<div><p class="grp">{esc(t["f_ins"])}</p>{radios("insurance", yn)}</div>'
           f'<div><p class="grp">{esc(t["f_langs"])}</p>{chks("languages", lang_items, required_one=True, cols3=True)}</div>'
           f'<div><p class="grp">{esc(t["f_avail"])}</p>{radios("availability", avail_items)}</div>'
           f'</fieldset>'
           # 3 private
           f'<fieldset><legend>{esc(t["s3"])}</legend>'
           f'<div class="two"><label for="r-legal">{esc(t["f_legal"])}<input id="r-legal" name="legal-name" required></label>'
           f'<label for="r-tax">{esc(t["f_tax"])}<input id="r-tax" name="tax-or-id-number" required inputmode="numeric" pattern="[0-9 \\-]{{13,17}}"></label></div>'
           f'<div class="two"><label for="r-cname">{esc(t["f_cname"])}<input id="r-cname" name="contact-name" required autocomplete="name"></label>'
           f'<label for="r-phone">{esc(t["f_phone"])}<input id="r-phone" name="phone" type="tel" required autocomplete="tel"></label></div>'
           f'<div class="two"><label for="r-email">{esc(t["f_email"])}<input id="r-email" name="email" type="email" required autocomplete="email"></label>'
           f'<label for="r-line">{esc(t["f_line"])}<input id="r-line" name="line-id" required></label></div>'
           f'<label for="r-addr">{esc(t["f_addr"])}<textarea id="r-addr" name="address" rows="2" required></textarea></label>'
           f'<div class="two"><label for="r-rate">{esc(t["f_rate"])}<input id="r-rate" name="labour-rate-thb-per-kwp" inputmode="decimal"></label>'
           f'<label for="r-ref">{esc(t["f_ref"])}<input id="r-ref" name="customer-reference"></label></div>'
           f'</fieldset>'
           # 4 documents
           f'<fieldset><legend>{esc(t["s4"])}</legend><p class="fine">{esc(t["docs_fine"])}</p>'
           f'<label for="r-logo">{esc(t["f_logo"])}<input id="r-logo" name="profile-photo" type="file" accept=".jpg,.jpeg,.png"></label>'
           f'<label for="r-cert">{esc(t["f_cert"])}<input id="r-cert" name="electrician-certificate" type="file" accept=".pdf"></label>'
           f'<label for="r-id">{esc(t["f_id"])}<input id="r-id" name="registration-or-id" type="file" accept=".pdf"></label>'
           f'<label for="r-lic">{esc(t["f_lic"])}<input id="r-lic" name="licences-certificates" type="file" accept=".pdf"></label>'
           f'<label for="r-port">{esc(t["f_port"])}<input id="r-port" name="portfolio" type="file" accept=".pdf"></label>'
           f'<label for="r-ph1">{esc(t["f_ph1"])}<input id="r-ph1" name="project-photo-1" type="file" accept=".jpg,.jpeg,.png"></label>'
           f'<label for="r-ph2">{esc(t["f_ph2"])}<input id="r-ph2" name="project-photo-2" type="file" accept=".jpg,.jpeg,.png"></label>'
           f'<label for="r-ph3">{esc(t["f_ph3"])}<input id="r-ph3" name="project-photo-3" type="file" accept=".jpg,.jpeg,.png"></label>'
           f'</fieldset>'
           # 5 agreement
           f'<fieldset><legend>{esc(t["s5"])}</legend>'
           f'<label class="chk"><input type="checkbox" name="agree-publish" value="yes" required><span>{esc(t["a_pub"])}</span></label>'
           f'<label class="chk"><input type="checkbox" name="agree-terms" value="yes" required><span>{esc(t["a_terms"])}</span></label>'
           f'<label class="chk"><input type="checkbox" name="agree-verification" value="yes" required><span>{esc(t["a_true"])}</span></label>'
           f'</fieldset>'
           f'<button class="btn" type="submit">{esc(t["reg_btn"])}</button></form></div></section>\n')

    labels = {k: t[k] for k in ["empty", "empty_cta", "verified", "base", "serves", "max", "yrs", "team", "elec", "proj", "kwp", "brands_l", "tools_l", "vat", "ins", "langs_l", "req_btn", "eng_l", "safety_l", "wah_l"]}
    import json
    script = ("<script>window.PARTNER_I18N=" + json.dumps({
        "lang": lang, "t": labels,
        "regions": dict(regions), "services": dict(svcs), "tools": dict(tools), "sizes": dict(sizes), "eng": dict(eng), "safety": dict(safety), "avail": {"in-team": t["av_short"][0], "can-arrange": t["av_short"][1]},
    }, ensure_ascii=False) + ";</script>\n<script src=\"/partners.js?v=6\" defer></script>\n")

    page = head + hero + howsec + directory + request + reg + script + foot
    out = ROOT / ("th/partners.html" if th else "partners.html")
    out.write_text(page, encoding="utf-8")
    print("wrote", out.relative_to(ROOT), len(page))


if __name__ == "__main__":
    build("en")
    build("th")
