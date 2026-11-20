# -*- coding: utf-8 -*-
"""Jobs page 21 Nov 2026: crew wanted for the Mae Hong Son 15 kW hybrid project (contract Rev16):
certified electrician, solar installers, roof workers, labourers. Day rates, apply with CV/resume.
Public version: approximate location (Pang Mu area, Mueang Mae Hong Son), no customer name, no contract price.
Idempotent. Run: python3 tools/job_nov21_mhs_crew.py, then tools/job_links.py, tools/job_order.py,
tools/build_share.py, tools/site_search.py"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JID = "crew-maehongson-15kw-hybrid-32kwh"
JOB = "Crew wanted – Mae Hong Son 15 kW hybrid, 16.90 kWp + 32 kWh (electrician, solar installer, roof worker, labourer)"
MAP = "https://www.google.com/maps/search/?api=1&amp;query=Pang%20Mu%2C%20Mueang%20Mae%20Hong%20Son%2C%20Mae%20Hong%20Son%2C%20Thailand"
ICO = ('<div class="ico"><svg viewBox="0 0 30 30" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
       '<circle cx="15" cy="15" r="5"/><path d="M15 3v3M15 24v3M3 15h3M24 15h3M6.5 6.5l2 2M21.5 21.5l2 2M6.5 23.5l2-2M21.5 8.5l2-2"/></svg></div>')
PIN = ('<svg width="16" height="18" viewBox="0 0 16 18"><path d="M8 17s6-5.6 6-10A6 6 0 002 7c0 4.4 6 10 6 10z" fill="var(--c)"/>'
       '<circle cx="8" cy="7" r="2.3" fill="#fff"/></svg>')

T = {
    "en": dict(
        kind="Project based · day rate · 4 roles · about 2–3 weeks on site",
        h3="Crew wanted for a 15 kW hybrid solar + 32 kWh battery project near Mae Hong Son: electricians, solar installers, roof workers and labourers",
        where="Pang Mu area, Mueang Mae Hong Son, Mae Hong Son", maplbl="Area map (approx.) ↗",
        facts=[("16.90 kWp", "26 × 650 W anti-glare panels"), ("15 kW", "3-phase hybrid inverter"), ("2 × 16 kWh", "LiFePO4 batteries (32 kWh)"),
               ("฿1,000 / day", "Experienced certified electrician or solar installer, work-at-height certified"), ("฿900 / day", "Roof worker"), ("฿550 / day", "Labourer"),
               ("Dec 2026", "Start date confirmed once materials reach site")],
        fit=("Solar ESS has signed a turnkey contract to install a hybrid solar + battery system on the roof of a Buddhist meditation centre just outside Mae Hong Son town, "
             "and we are building the site crew. <b>Solar ESS supplies all equipment and materials and leads the work on site</b>; you join our team on a day rate. "
             "Crew: <b>1–2 certified electricians, 2 solar installers, 2 roof workers and 2–3 labourers.</b> The work is about 2–3 weeks on site, Monday–Saturday, 08:00–17:00. "
             "Safety first: work at height with harness and lifeline, follow the site lead’s instructions, and respect the temple grounds (quiet, modest dress, no alcohol or smoking on site). "
             "Workers from outside Mae Hong Son: tell us in your application if you need lodging."),
        roles=[
            ("Certified electrician", ["Experienced; hold an electrician certificate and a work-at-height certificate; 3-phase experience required",
                                       "Install the 15 kW 3-phase hybrid inverter, AC combiner, breakers, SPD and the earthing system",
                                       "Wire the 2 batteries with the BMS link, the PV strings to the inverter and the inverter to the building supply",
                                       "Test (insulation, polarity, Voc, earth resistance), start up with the Solar ESS team and record all readings"]),
            ("Solar installer", ["At least 1 year of rooftop PV experience (mounting, MC4, string wiring); work-at-height certificate required",
                                 "Fix rails and hooks to the roof structure and mount 26 panels on the southwest side of the roof",
                                 "Make up MC4 connectors, run PV cable in conduit, label strings and bond all frames and rails"]),
            ("Roof worker", ["Experience on tile / double-wave roofs; can work safely at height",
                             "Open and re-seal the roof at each hook so the roof stays watertight; replace any broken tiles",
                             "Set up ladders, roof walkways and lifelines; lift panels and rails safely"]),
            ("Labourer", ["Fit and willing; no experience needed – we train you on site",
                          "Unload and carry panels, batteries (heavy) and materials; help the installers on the ground and on the roof",
                          "Keep the site clean and tidy every day"]),
        ],
        rmk=("<b>Remark:</b> apply with the form below and attach your <b>resume (CV)</b>, plus your <b>certificates</b> if you have them (electrician licence, work-at-height). "
             "Choose this job in the form and write the role you apply for (electrician, solar installer, roof worker or labourer) and the days you are available. "
             "We will then contact you back to discuss the work. We apologize if your Facebook message has not been answered. "
             "<b>Please read every detail of this job carefully – do not ask questions by Facebook Messenger, apply with the form below.</b>"
             '<span class="tsia-req"><br><b>Electricians and solar installers:</b> every installer who works with Solar ESS must first <b>pass at least 1 Solar ESS installer test</b> '
             '(<a href="/installer-test.html">take a test</a>) and <b>register as a TSIA member</b> (<a href="/team.html#tsia-form">become a member</a>). '
             "Roof workers and labourers do not need the test.<br><b>Tell us where you are based:</b> give your approximate location (sub-district, district, province). "
             'People who live in or near Mae Hong Son are more likely to get the job. <a href="/location.html">Register or update your location</a> to be notified of jobs near you.</span>'),
        go="Apply for this job →", roles_lbl="Role",
    ),
    "th": dict(
        kind="งานรายโครงการ · ค่าแรงรายวัน · 4 ตำแหน่ง · ทำงานหน้างานประมาณ 2–3 สัปดาห์",
        h3="รับสมัครทีมงานโครงการโซลาร์ไฮบริด 15 kW พร้อมแบตเตอรี่ 32 kWh ใกล้ตัวเมืองแม่ฮ่องสอน: ช่างไฟฟ้า ช่างติดตั้งโซลาร์ ช่างหลังคา และคนงานทั่วไป",
        where="บริเวณ ต.ปางหมู อ.เมืองแม่ฮ่องสอน จ.แม่ฮ่องสอน", maplbl="แผนที่บริเวณ (โดยประมาณ) ↗",
        facts=[("16.90 kWp", "แผงกันแสงสะท้อน 650 W × 26"), ("15 kW", "อินเวอร์เตอร์ไฮบริด 3 เฟส"), ("2 × 16 kWh", "แบตเตอรี่ LiFePO4 (32 kWh)"),
               ("฿1,000 / วัน", "ช่างไฟฟ้ามีใบรับรองหรือช่างติดตั้งโซลาร์ที่มีประสบการณ์ มีใบรับรองการทำงานบนที่สูง"), ("฿900 / วัน", "ช่างหลังคา"), ("฿550 / วัน", "คนงานทั่วไป"),
               ("ธ.ค. 2569", "ยืนยันวันเริ่มงานเมื่ออุปกรณ์ถึงหน้างาน")],
        fit=("Solar ESS ลงนามสัญญาติดตั้งระบบโซลาร์ไฮบริดพร้อมแบตเตอรี่แบบเหมารวมบนหลังคาสถานปฏิบัติธรรมแห่งหนึ่งใกล้ตัวเมืองแม่ฮ่องสอน และกำลังรวมทีมหน้างาน "
             "<b>Solar ESS จัดหาอุปกรณ์และวัสดุทั้งหมด และเป็นผู้ควบคุมงานหน้างาน</b> ท่านเข้าร่วมทีมโดยรับค่าแรงรายวัน "
             "ทีมงาน: <b>ช่างไฟฟ้ามีใบรับรอง 1–2 คน ช่างติดตั้งโซลาร์ 2 คน ช่างหลังคา 2 คน และคนงานทั่วไป 2–3 คน</b> ทำงานหน้างานประมาณ 2–3 สัปดาห์ วันจันทร์–เสาร์ 08:00–17:00 น. "
             "ความปลอดภัยต้องมาก่อน: ทำงานบนที่สูงต้องใช้เข็มขัดนิรภัยและเชือกช่วยชีวิต ปฏิบัติตามหัวหน้างาน และเคารพสถานที่ปฏิบัติธรรม (สุภาพ แต่งกายเรียบร้อย ห้ามสุราและบุหรี่ในพื้นที่) "
             "ผู้สมัครจากนอกจังหวัดแม่ฮ่องสอน: หากต้องการที่พัก กรุณาแจ้งในใบสมัคร"),
        roles=[
            ("ช่างไฟฟ้ามีใบรับรอง", ["มีประสบการณ์ มีใบรับรองช่างไฟฟ้าและใบรับรองการทำงานบนที่สูง มีประสบการณ์งานไฟฟ้า 3 เฟส",
                                    "ติดตั้งอินเวอร์เตอร์ไฮบริด 15 kW 3 เฟส ตู้ AC combiner เบรกเกอร์ SPD และระบบสายดิน",
                                    "เดินสายแบตเตอรี่ 2 ชุดพร้อมสาย BMS สาย PV เข้าอินเวอร์เตอร์ และอินเวอร์เตอร์เข้าระบบไฟของอาคาร",
                                    "ทดสอบ (ความเป็นฉนวน ขั้ว Voc ค่าความต้านทานดิน) เปิดระบบร่วมกับทีม Solar ESS และบันทึกค่าทั้งหมด"]),
            ("ช่างติดตั้งโซลาร์", ["มีประสบการณ์ติดตั้งโซลาร์บนหลังคาอย่างน้อย 1 ปี (ระบบยึดแผง MC4 การเดินสายสตริง) ต้องมีใบรับรองการทำงานบนที่สูง",
                                  "ยึดรางและขอเข้ากับโครงหลังคา ติดตั้งแผง 26 แผงบนหลังคาฝั่งทิศตะวันตกเฉียงใต้",
                                  "เข้าหัว MC4 เดินสาย PV ในท่อ ติดป้ายสตริง และต่อฝากโครงแผงและรางทั้งหมด"]),
            ("ช่างหลังคา", ["มีประสบการณ์หลังคากระเบื้อง / ลอนคู่ ทำงานบนที่สูงได้อย่างปลอดภัย",
                           "เปิดและอุดกันซึมหลังคาทุกจุดที่ยึดขอ หลังคาต้องไม่รั่ว เปลี่ยนกระเบื้องที่แตก",
                           "ติดตั้งบันได ทางเดินบนหลังคา และเชือกช่วยชีวิต ยกแผงและรางขึ้นหลังคาอย่างปลอดภัย"]),
            ("คนงานทั่วไป", ["ร่างกายแข็งแรง ตั้งใจทำงาน ไม่ต้องมีประสบการณ์ – สอนงานหน้างาน",
                            "ขนถ่ายแผง แบตเตอรี่ (น้ำหนักมาก) และวัสดุ ช่วยช่างทั้งบนพื้นและบนหลังคา",
                            "ดูแลหน้างานให้สะอาดเรียบร้อยทุกวัน"]),
        ],
        rmk=("<b>หมายเหตุ:</b> สมัครผ่านแบบฟอร์มด้านล่าง แนบ<b>ประวัติส่วนตัว (Resume / CV)</b> และ<b>ใบรับรอง</b> (ถ้ามี เช่น ใบรับรองช่างไฟฟ้า ใบรับรองการทำงานบนที่สูง) "
             "เลือกงานนี้ในแบบฟอร์ม ระบุตำแหน่งที่สมัคร (ช่างไฟฟ้า ช่างติดตั้งโซลาร์ ช่างหลังคา หรือคนงานทั่วไป) และวันที่สะดวกทำงาน "
             "จากนั้นทางเราจะติดต่อกลับเพื่อพูดคุยรายละเอียดงาน ขออภัยหากข้อความทาง Facebook ของท่านยังไม่ได้รับการตอบกลับ "
             "<b>กรุณาอ่านรายละเอียดงานให้ครบถ้วน ไม่ต้องสอบถามทางข้อความ Facebook – กรุณาสมัครผ่านแบบฟอร์มด้านล่าง</b>"
             '<span class="tsia-req"><br><b>ช่างไฟฟ้าและช่างติดตั้งโซลาร์:</b> ช่างทุกคนที่จะทำงานกับ Solar ESS ต้อง<b>ผ่านแบบทดสอบช่างของ Solar ESS อย่างน้อย 1 ชุด</b> '
             '(<a href="/th/installer-test.html">ทำแบบทดสอบ</a>) และ<b>สมัครเป็นสมาชิก TSIA</b> (<a href="/th/team.html#tsia-form">สมัครสมาชิก</a>) ก่อน '
             "ช่างหลังคาและคนงานทั่วไปไม่ต้องทำแบบทดสอบ<br><b>แจ้งพื้นที่ที่อยู่ของท่าน:</b> ระบุตำแหน่งที่อยู่โดยประมาณ (ตำบล อำเภอ จังหวัด) "
             'ผู้ที่อยู่ในหรือใกล้แม่ฮ่องสอนจะมีโอกาสได้งานมากกว่า <a href="/th/location.html">ลงทะเบียนหรืออัปเดตตำแหน่ง</a>เพื่อรับแจ้งงานใกล้บ้าน</span>'),
        go="สมัครงานนี้ →", roles_lbl="ตำแหน่ง",
    ),
}


def card(lang):
    t = T[lang]
    facts = "".join(f'<div class="fact"><b>{a}</b>{b}</div>' for a, b in t["facts"])
    dl = "".join(f'<details class="dlv" open><summary>{t["roles_lbl"]}: {r} <span>({len(items)})</span></summary><ul>'
                 + "".join(f"<li>{i}</li>" for i in items) + "</ul></details>" for r, items in t["roles"])
    return (f'<article class="card p" id="{JID}" data-posted="2026-11-21" data-tags="project north" data-lat="19.33" data-lng="97.97" '
            f'data-work="electrical solar civil" data-q="pang mu, mueang mae hong son, mae hong son ต.ปางหมู อ.เมืองแม่ฮ่องสอน จ.แม่ฮ่องสอน '
            f'mae hong son แม่ฮ่องสอน electrician solar installer roof labourer ช่างไฟฟ้า ช่างติดตั้งโซลาร์ ช่างหลังคา คนงาน resume">'
            f'<div class="top">{ICO}<div><div class="kind">{t["kind"]}</div><h3>{t["h3"]}</h3></div></div>\n'
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
