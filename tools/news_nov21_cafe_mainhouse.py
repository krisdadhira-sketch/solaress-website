# -*- coding: utf-8 -*-
"""21 Nov 2026: Main House battery sizing review for the off-grid café, plant DH-57180-12-01 (Mae Suai, Chiang Rai 57180).
1. News: plant-review article at the top of /news.html and /th/news.html with the watermarked public PDF
   (no prices, no customer name or details, approximate location only).
2. Jobs: project job for nearby installers - add 1 or 2 LiFePO4 batteries + generator connection (cites the plant code,
   so it is listed with the plant on the Plants by Province page and reaches installers registered near 57180).
Idempotent. Run, then tools/job_links.py, tools/job_order.py, tools/news_menu.py, tools/build_share.py, tools/site_search.py"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODE = "DH-57180-12-01"
PDF = "/downloads/Solar-ESS-Plant-Review-Offgrid-Cafe-Main-House-Battery-Sizing_Rev01_WM_20261121.pdf"
PDF_TH = "/downloads/Solar-ESS-Plant-Review-Offgrid-Cafe-Main-House-Battery-Sizing-TH_Rev01_WM_20261121.pdf"
IMG_TH = "/images/doc-plant-review-offgrid-cafe-main-house-battery-th.jpg"
IMG = "/images/doc-plant-review-offgrid-cafe-main-house-battery.jpg"
AID = "plant-review-offgrid-cafe-main-house-battery"
JID = "battery-addon-gen-maesuai-offgrid-cafe"
JOB = "Battery add-on + generator connection – off-grid café, Mae Suai (plant DH-57180-12-01)"
SEP = 'style="max-width:760px;margin-top:64px;padding-top:48px;border-top:1.5px solid var(--navy)"'
PCODE = lambda lang: f'<a class="pcode" href="{"/th" if lang == "th" else ""}/monthly-report.html#plant-{CODE}">{"รหัสโรงไฟฟ้า" if lang == "th" else "Plant code"} {CODE}</a>'

N = {
    "en": dict(eb="21 November 2026 · Plant review",
               h2="Off-grid café, Mae Suai: is the energy enough, and how much battery is needed?",
               lede="A review of the Main House system at plant DH-57180-12-01 (postcode 57180): 11.6 kWp, a Deye 10 kW off-grid inverter and 20.5 kWh of LiFePO4, with no grid and no generator.",
               pts=[("Normal days are covered", "In October solar supplied 100% of use (8–15 kWh a day). The battery was full by about 10:30 and only 15–47% was used at night."),
                    ("Cloudy spells are not", "The two batteries hold about one day of use. Two or three dull days in a row will run them empty."),
                    ("Peaks", "Kettles, hair dryers and the coffee machine together with the air-conditioners can pass the 10 kW inverter. Run them one at a time."),
                    ("How much battery", "One more battery (30.7 kWh) gives about 1.5 days without sun at today’s use; two more (41 kWh) only if guest-room night use grows."),
                    ("Backup", "A small generator on the inverter’s GEN input is the only thing that fully covers a long monsoon spell.")],
               btn="Open the PDF ↓ · English", foot="Prices, names and customer details removed. Solar ESS Working Group."),
    "th": dict(eb="21 พฤศจิกายน 2569 · รีวิวโรงไฟฟ้า",
               h2="คาเฟ่ออฟกริด แม่สรวย: ไฟพอไหม และต้องเพิ่มแบตเตอรี่เท่าไร?",
               lede="รีวิวระบบบ้านหลัก รหัสโรงไฟฟ้า DH-57180-12-01 (รหัสไปรษณีย์ 57180): แผง 11.6 kWp อินเวอร์เตอร์ออฟกริด Deye 10 kW และแบตเตอรี่ LiFePO4 20.5 kWh ไม่มีไฟการไฟฟ้าและไม่มีเครื่องปั่นไฟ",
               pts=[("วันปกติไฟพอ", "เดือนตุลาคมโซลาร์จ่ายไฟได้ 100% ของการใช้ (8–15 หน่วยต่อวัน) แบตเตอรี่เต็มประมาณ 10:30 น. และใช้กลางคืนเพียง 15–47%"),
                    ("ฟ้าครึ้มหลายวันไม่พอ", "แบตเตอรี่ 2 ลูกเก็บไฟได้ราว 1 วัน ถ้าฟ้าครึ้ม 2–3 วันติดกันแบตเตอรี่จะหมด"),
                    ("ไฟกระชาก", "กาต้มน้ำ ไดร์เป่าผม และเครื่องชงกาแฟ ใช้พร้อมแอร์อาจเกินอินเวอร์เตอร์ 10 kW ควรใช้ทีละเครื่อง"),
                    ("ต้องเพิ่มแบตเตอรี่เท่าไร", "เพิ่ม 1 ลูก (รวม 30.7 kWh) อยู่ได้ราว 1.5 วันไม่มีแดดที่การใช้ปัจจุบัน เพิ่ม 2 ลูก (41 kWh) เฉพาะเมื่อห้องพักใช้ไฟกลางคืนมากขึ้น"),
                    ("ไฟสำรอง", "เครื่องปั่นไฟขนาดเล็กต่อเข้าช่อง GEN ของอินเวอร์เตอร์ เป็นทางเดียวที่ครอบคลุมช่วงฝนตกยาวได้ทั้งหมด")],
               btn="เปิด PDF ↓ · ภาษาไทย", foot="ตัดราคา ชื่อ และข้อมูลลูกค้าออกแล้ว Solar ESS Working Group."),
}

ICO = ('<div class="ico"><svg viewBox="0 0 30 30" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
       '<rect x="6" y="9" width="18" height="15" rx="2"/><path d="M11 9V6h8v3M13 14l-2 4h5l-2 4"/></svg></div>')
PIN = ('<svg width="16" height="18" viewBox="0 0 16 18"><path d="M8 17s6-5.6 6-10A6 6 0 002 7c0 4.4 6 10 6 10z" fill="var(--c)"/>'
       '<circle cx="8" cy="7" r="2.3" fill="#fff"/></svg>')
MAP = "https://www.google.com/maps/search/?api=1&amp;query=Mae%20Suai%20Dam%2C%20Mae%20Suai%2C%20Chiang%20Rai%2C%20Thailand"
J = {
    "en": dict(kind="Project based · paid per job · 2 options", h3="Add 1 or 2 LiFePO4 batteries to an off-grid café system + connect a backup generator",
               where="Mae Suai Dam area, Mae Suai, Chiang Rai 57180", maplbl="Area map (approx.) ↗",
               facts=[("10 kW", "Deye off-grid inverter (existing)"), ("2 → 3 or 4", "51.2 V 200 Ah LiFePO4 batteries"), ("≈5 kVA", "Generator on the GEN input"),
                      ("฿4,500–6,000", "Pay guide · option A"), ("฿5,500–7,500", "Pay guide · option B")],
               fit=("An off-grid café and homestay (no grid) needs more storage and a backup source – read the plant review before you quote: "
                    f'<a href="{PDF}">Main House load &amp; battery report (PDF)</a> · {{PCODE}}. '
                    "<b>Solar ESS supplies</b> the battery(ies) – the same 51.2 V 200 Ah model as the existing two – the DC breaker, breaker box and busbar box. "
                    "<b>The installer supplies</b> DC cable and lugs, the generator cable to the GEN input, conduit and consumables. "
                    "The generator itself is supplied and installed by the generator company; you make the connection with them on site. "
                    "A certified electrician must do the electrical work. Use premium materials only (copper cable, IMC/EMT conduit, well-matched breakers and cables)."),
               opts=[("Option A – add 1 battery + generator connection", [
                          "Health check of the existing system first: cell balance, battery SOC and firmware, inverter standby draw – record everything",
                          "Install the new battery next to the existing two, balance the charge levels, connect through the new DC breaker and busbar box",
                          "Update the battery settings in the inverter so all batteries run as one bank under the BMS",
                          "Connect the generator to the inverter GEN input with the generator company; set auto-start below 25% SOC and stop at 60%, low-battery warning 25%, load shutdown 15%",
                          "Test charge, discharge and generator start; correct the PV capacity on DeyeCloud to 11.6 kWp; hand over with photos and the Solar ESS report form"]),
                     ("Option B – add 2 batteries + generator connection", ["Same as option A, with 2 new batteries (4 in total, 41 kWh)"])],
               rmk=("<b>Remark:</b> candidates must submit their <b>profile, certificate and quotation</b>. We will then contact you back to discuss the work. "
                    "We apologize if your Facebook message has not been answered. <b>Please read every detail of this job carefully and quote exactly for the scope, location and requirements shown. "
                    "Do not ask questions by Facebook Messenger – send your quotation with the form below.</b><br><b>Quote two prices for each option you take:</b> 1) Labour cost only; "
                    "2) Labour &amp; materials (the installer’s materials only – list every material by brand and size). Say which option(s) you quote for, how many people and how many days."
                    '<span class="tsia-req"><br><b>Before you quote:</b> every installer who works with Solar ESS must first <b>pass at least 1 Solar ESS installer test</b> '
                    '(<a href="/installer-test.html">take a test</a>) and <b>register as a TSIA member</b> (<a href="/team.html#tsia-form">become a member</a>). '
                    "Quotes from installers who have not done both cannot be accepted.<br><b>Tell us where you are based:</b> give your approximate location (sub-district, district, province) "
                    "with your quotation. Installers who live near Mae Suai are more likely to get the job. "
                    '<a href="/location.html">Register or update your location</a> to be notified of jobs near you.</span>'),
               go="Quote for this job →", olbl=""),
    "th": dict(kind="งานรายโครงการ · จ่ายเป็นรายงาน · 2 ทางเลือก", h3="เพิ่มแบตเตอรี่ LiFePO4 1 หรือ 2 ลูก ให้ระบบออฟกริดของคาเฟ่ + ต่อเครื่องปั่นไฟสำรอง",
               where="บริเวณเขื่อนแม่สรวย อ.แม่สรวย จ.เชียงราย 57180", maplbl="แผนที่บริเวณ (โดยประมาณ) ↗",
               facts=[("10 kW", "อินเวอร์เตอร์ออฟกริด Deye (เดิม)"), ("2 → 3 หรือ 4", "แบตเตอรี่ LiFePO4 51.2 V 200 Ah"), ("≈5 kVA", "เครื่องปั่นไฟต่อช่อง GEN"),
                      ("฿4,500–6,000", "ค่าแรงแนะนำ · ทางเลือก A"), ("฿5,500–7,500", "ค่าแรงแนะนำ · ทางเลือก B")],
               fit=("คาเฟ่และโฮมสเตย์ระบบออฟกริด (ไม่มีไฟการไฟฟ้า) ต้องการแบตเตอรี่เพิ่มและไฟสำรอง – กรุณาอ่านรีวิวโรงไฟฟ้าก่อนเสนอราคา: "
                    f'<a href="{PDF_TH}">รายงานโหลดและแบตเตอรี่บ้านหลัก (PDF)</a> · {{PCODE}} '
                    "<b>Solar ESS จัดหา</b>แบตเตอรี่ (รุ่น 51.2 V 200 Ah เดียวกับ 2 ลูกเดิม) เบรกเกอร์ DC กล่องเบรกเกอร์ และกล่องบัสบาร์ "
                    "<b>ผู้รับเหมาจัดหา</b>สาย DC และหางปลา สายจากเครื่องปั่นไฟเข้าช่อง GEN ท่อร้อยสาย และวัสดุสิ้นเปลือง "
                    "เครื่องปั่นไฟจัดหาและติดตั้งโดยบริษัทเครื่องปั่นไฟ ผู้รับเหมาต่อเชื่อมร่วมกับช่างของบริษัทที่หน้างาน "
                    "งานไฟฟ้าต้องทำโดยช่างไฟฟ้าที่มีใบรับรอง ใช้วัสดุคุณภาพดีเท่านั้น (สายทองแดง ท่อ IMC/EMT เบรกเกอร์และสายไฟที่เลือกขนาดเหมาะสม)"),
               opts=[("ทางเลือก A – เพิ่มแบตเตอรี่ 1 ลูก + ต่อเครื่องปั่นไฟ", [
                          "ตรวจสุขภาพระบบเดิมก่อน: ความสมดุลเซลล์ SOC และเฟิร์มแวร์แบตเตอรี่ การกินไฟขณะสแตนด์บายของอินเวอร์เตอร์ – บันทึกทุกค่า",
                          "ติดตั้งแบตเตอรี่ใหม่ข้าง 2 ลูกเดิม ปรับระดับประจุให้เท่ากัน ต่อผ่านเบรกเกอร์ DC และกล่องบัสบาร์ใหม่",
                          "ปรับค่าแบตเตอรี่ในอินเวอร์เตอร์ให้แบตเตอรี่ทุกลูกทำงานเป็นชุดเดียวภายใต้ BMS",
                          "ต่อเครื่องปั่นไฟเข้าช่อง GEN ร่วมกับบริษัทเครื่องปั่นไฟ ตั้งให้เครื่องติดเมื่อต่ำกว่า 25% SOC และดับที่ 60% เตือนแบตต่ำ 25% ตัดโหลด 15%",
                          "ทดสอบการชาร์จ คายประจุ และการสตาร์ทเครื่องปั่นไฟ แก้ขนาดแผงใน DeyeCloud เป็น 11.6 kWp ส่งมอบพร้อมภาพและแบบฟอร์มรายงานของ Solar ESS"]),
                     ("ทางเลือก B – เพิ่มแบตเตอรี่ 2 ลูก + ต่อเครื่องปั่นไฟ", ["เหมือนทางเลือก A แต่เพิ่มแบตเตอรี่ 2 ลูก (รวม 4 ลูก 41 kWh)"])],
               rmk=("<b>หมายเหตุ:</b> ผู้สมัครต้องส่ง<b>ประวัติ ใบรับรอง และใบเสนอราคา</b> จากนั้นทางเราจะติดต่อกลับเพื่อพูดคุยรายละเอียดงาน ขออภัยหากข้อความทาง Facebook ของท่านยังไม่ได้รับการตอบกลับ "
                    "<b>กรุณาอ่านรายละเอียดงานให้ครบถ้วนและเสนอราคาให้ตรงตามขอบเขตงาน สถานที่ และข้อกำหนดที่ระบุ ไม่ต้องสอบถามทางข้อความ Facebook – กรุณาส่งใบเสนอราคาผ่านแบบฟอร์มด้านล่าง</b>"
                    "<br><b>เสนอราคา 2 แบบสำหรับแต่ละทางเลือกที่เสนอ:</b> 1) ค่าแรงอย่างเดียว; 2) ค่าแรงและค่าวัสดุ (เฉพาะวัสดุที่ผู้รับเหมาจัดหา – ระบุยี่ห้อและขนาดวัสดุทุกรายการ) ระบุว่าเสนอทางเลือกใด จำนวนคน และจำนวนวัน"
                    '<span class="tsia-req"><br><b>ก่อนเสนอราคา:</b> ช่างทุกคนที่จะทำงานกับ Solar ESS ต้อง<b>ผ่านแบบทดสอบช่างของ Solar ESS อย่างน้อย 1 ชุด</b> '
                    '(<a href="/th/installer-test.html">ทำแบบทดสอบ</a>) และ<b>สมัครเป็นสมาชิก TSIA</b> (<a href="/th/team.html#tsia-form">สมัครสมาชิก</a>) ก่อน '
                    "ใบเสนอราคาจากช่างที่ยังไม่ได้ทำทั้งสองข้อจะไม่ได้รับการพิจารณา<br><b>แจ้งพื้นที่ที่อยู่ของท่าน:</b> ระบุตำแหน่งที่อยู่โดยประมาณ (ตำบล อำเภอ จังหวัด) มาพร้อมใบเสนอราคา "
                    'ช่างที่อยู่ใกล้แม่สรวยจะมีโอกาสได้งานมากกว่า <a href="/th/location.html">ลงทะเบียนหรืออัปเดตตำแหน่ง</a>เพื่อรับแจ้งงานใกล้บ้าน</span>'),
               go="เสนอราคางานนี้ →"),
}


def news(lang):
    t = N[lang]
    pdf, img = (PDF_TH, IMG_TH) if lang == "th" else (PDF, IMG)
    alt = (f'<a class="btn ghost" href="{PDF}" download>เปิด PDF ↓ · ภาษาอังกฤษ</a>' if lang == "th" else f'<a class="btn ghost" href="{PDF_TH}" download>Open the PDF ↓ · Thai</a>')
    lis = "".join(f'<li style="margin-bottom:10px"><b>{a}:</b> {b}</li>' for a, b in t["pts"])
    return (f'<article id="{AID}" style="max-width:760px">\n<p class="eyebrow">{t["eb"]}</p><h2 style="font-size:clamp(26px,3.6vw,40px)">{t["h2"]}</h2>\n'
            f'<p class="lede" style="margin-top:16px;opacity:1">{t["lede"]}</p>\n<ul style="margin-top:22px;padding-left:20px">{lis}</ul>\n'
            f'<p style="margin-top:14px">{PCODE(lang)}</p>\n'
            f'<p style="margin-top:22px"><a href="{pdf}"><img src="{img}" alt="{"หน้าแรกของเอกสาร Solar ESS" if lang == "th" else "First page of the Solar ESS document"}" width="579" height="819" loading="lazy" style="width:100%;max-width:360px;height:auto;border:1.5px solid var(--line)"></a></p>\n'
            f'<p style="margin-top:18px;display:flex;gap:10px;flex-wrap:wrap"><a class="btn" href="{pdf}" download>{t["btn"]}</a>{alt}</p>\n'
            f'<p style="margin-top:20px;font-size:14px;color:var(--mute)">{t["foot"]}</p>\n</article>\n')


def job(lang):
    t = J[lang]
    facts = "".join(f'<div class="fact"><b>{a}</b>{b}</div>' for a, b in t["facts"])
    dl = "".join(f'<details class="dlv" open><summary>{o} <span>({len(i)})</span></summary><ul>' + "".join(f"<li>{x}</li>" for x in i) + "</ul></details>" for o, i in t["opts"])
    return (f'<article class="card p" id="{JID}" data-posted="2026-11-21" data-tags="project north" data-lat="19.65" data-lng="99.54" data-work="electrical solar" '
            f'data-q="mae suai dam, mae suai, chiang rai 57180 เขื่อนแม่สรวย อ.แม่สรวย จ.เชียงราย chiang rai เชียงราย battery แบตเตอรี่ generator เครื่องปั่นไฟ off-grid {CODE}">'
            f'<div class="top">{ICO}<div><div class="kind">{t["kind"]}</div><h3>{t["h3"]}</h3></div></div>\n'
            f'<div class="body"><div class="where">{PIN}<span>{t["where"]} · <span style="white-space:nowrap"><a href="{MAP}" target="_blank" rel="noopener" style="color:var(--c);font-weight:600">{t["maplbl"]}</a></span></span></div>\n'
            f'<div class="facts">{facts}</div>\n<p class="fit">{t["fit"].replace("{PCODE}", PCODE(lang))}</p>\n{dl}\n'
            f'<p class="fit rmk" style="border-left-color:var(--c);margin-top:12px">{t["rmk"]}</p>\n'
            f'<div class="go"><a href="#apply" data-job="{JOB}">{t["go"]}</a></div></div></article>\n')


for lang, path in (("en", "news.html"), ("th", "th/news.html")):
    p = ROOT / path; s = p.read_text(encoding="utf-8")
    s = re.sub(rf'<article id="{AID}".*?</article>\n?', "", s, flags=re.S)
    m = re.search(r'<article id="([^"]+)"( data-topics="[^"]*")? style="[^"]*">', s)
    s = s[:m.start()] + news(lang) + re.sub(r'style="[^"]*"', SEP, m.group(0)) + s[m.end():]
    p.write_text(s, encoding="utf-8"); print(path, "news before", m.group(1))
for lang, path in (("en", "job.html"), ("th", "th/job.html")):
    p = ROOT / path; s = p.read_text(encoding="utf-8")
    s = re.sub(rf'<article class="card p" id="{JID}".*?</article>\n?', "", s, flags=re.S)
    m = re.search(r'<article class="card p" id="', s)
    s = s[:m.start()] + job(lang) + s[m.start():]
    p.write_text(s, encoding="utf-8"); print(path, "job inserted")
