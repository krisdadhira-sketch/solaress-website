# -*- coding: utf-8 -*-
"""Jobs page 27 Nov 2026: Solar installer assistant on a daily wage (800 THB/day, set by Kris) - 3 jobs, one per
project area: Hat Yai, Trang, Krabi - PV cleaning, preventive maintenance and general help; each job takes a few hours to one day.
Fixed wage, so the remark asks for availability instead of a two-price quotation.
Idempotent. Run: python3 tools/job_nov27_assistant_south.py, then tools/job_links.py, tools/job_search.py,
tools/pv_clean_photo.py, tools/job_order.py, tools/site_search.py, tools/analytics_tag.py"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# one job per project area: (id suffix, EN name, TH name, map query, lat, lng, search words)
AREAS = [
 ("hatyai", "Hat Yai, Songkhla", "หาดใหญ่ สงขลา", "Hat%20Yai%2C%20Songkhla", 7.007, 100.474, "hat yai, songkhla หาดใหญ่ สงขลา"),
 ("trang", "Mueang Trang, Trang", "อ.เมืองตรัง จ.ตรัง", "Mueang%20Trang%2C%20Trang", 7.556, 99.611, "trang ตรัง mueang trang เมืองตรัง"),
 ("krabi", "Mueang Krabi, Krabi", "อ.เมืองกระบี่ จ.กระบี่", "Mueang%20Krabi%2C%20Krabi", 8.086, 98.906, "krabi กระบี่ mueang krabi เมืองกระบี่"),
]
SVG = ('<svg viewBox="0 0 30 30" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
       '<circle cx="15" cy="15" r="5"/><path d="M15 3v3M15 24v3M3 15h3M24 15h3M6.5 6.5l2 2M21.5 21.5l2 2M6.5 23.5l2-2M21.5 8.5l2-2"/></svg>')
PIN = ('<svg width="16" height="18" viewBox="0 0 16 18"><path d="M8 17s6-5.6 6-10A6 6 0 002 7c0 4.4 6 10 6 10z" fill="var(--c)"/>'
       '<circle cx="8" cy="7" r="2.3" fill="#fff"/></svg>')
FORM = "/downloads/Solar-ESS-PV-Cleaning-Maintenance-Report-Form-{}_Rev{}_WM_20261111.pdf"

T = {
 "en": dict(
  kind="Project based · daily wage", posted="Posted 27 Nov 2026", 
  h3="Solar installer assistant, {A}: daily wage for PV cleaning, preventive maintenance and site help",
  maplbl="Area map (approx.) ↗",
  facts=[("฿800 / day", "Daily wage, fixed"), ("Hours – 1 day", "Most jobs take a few hours or one day"),
         ("Near you", "Work at plants in and around {A}"), ("On call", "Paid for each day you work")],
  fit=('We are looking for assistants who live in or near <b>{A}</b> to help at solar plants that Solar ESS looks after there. Solar ESS is hiring the same role in Hat Yai, Trang and Krabi. '
       'You work with a Solar ESS technician or a TSIA installer team, or on your own for simple cleaning jobs. Most visits are short: a few hours or one day. '
       'Good for people who are new to solar and want to learn, or installers with free days between jobs. '
       '<b>Safety:</b> roof work needs safe work-at-height practice (harness where needed); never open inverter, battery or DC equipment unless the technician in charge has isolated it and tells you to.'),
  scope_t="Typical work", scope=[
   "PV panel cleaning with a soft brush and clean water (no hard brushes, no detergent, no high-pressure jet)",
   "Preventive maintenance help: visual checks of panels, mounting, cables, conduit and connectors; tightening and labelling",
   "Photos before and after, and filling in the Solar ESS PV cleaning and maintenance report form",
   "Carrying tools and materials, keeping the site clean and safe, helping the technician with readings",
   "Other site help on installation or service days as assigned"],
  req_t="What we look for", req=[
   "Live in or near {A}; own transport (motorbike is fine)",
   "Comfortable working on roofs and in the sun; careful and honest",
   "Basic electrical knowledge is a plus; a certificate or electrical training is an advantage, not a must",
   "Smartphone with LINE for photos and job alerts"],
  frm="<b>PV cleaning report form:</b> download it before you apply. Fill it in on site and send it back with your photos.",
  rmk=('<b>Remark:</b> candidates must submit their <b>profile, certificate and quotation</b>. We will then contact you back to discuss the work. We apologize if your Facebook message has not been answered. '
       '<b>Please read every detail of this job carefully. Do not ask questions by Facebook Messenger – apply with the form below.</b><br>'
       '<b>The wage for this job is fixed at 800 THB a day</b>, so instead of a price tell us <b>which days</b> you can work, and any solar or electrical experience you have.'
       '<span class="tsia-req"><br><b>Before you apply:</b> every installer who works with Solar ESS must first <b>pass at least 1 Solar ESS installer test</b> (<a href="/installer-test.html">take a test</a>) '
       'and <b>register as a TSIA member</b> (<a href="/team.html#tsia-form">become a member</a>). Applications from people who have not done both cannot be accepted.<br>'
       '<b>Tell us where you are based:</b> give your approximate location (sub-district, district, province). Applicants who live near {A} are more likely to get the work. '
       '<a href="/location.html">Register or update your location</a> to be notified of jobs near you.</span>'),
  go="Apply for this job →"),
 "th": dict(
  kind="งานรายโครงการ · ค่าแรงรายวัน", posted="ลงประกาศ 27 พ.ย. 2569", 
  h3="ผู้ช่วยช่างติดตั้งโซลาร์ {A}: ค่าแรงรายวัน ล้างแผงโซลาร์ บำรุงรักษาเชิงป้องกัน และช่วยงานหน้างาน",
  maplbl="แผนที่บริเวณ (โดยประมาณ) ↗",
  facts=[("฿800 / วัน", "ค่าแรงรายวัน อัตราคงที่"), ("ไม่กี่ชั่วโมง – 1 วัน", "งานส่วนใหญ่เสร็จภายในไม่กี่ชั่วโมงหรือ 1 วัน"),
         ("ใกล้บ้าน", "งานที่โรงไฟฟ้าใน{A}และพื้นที่ใกล้เคียง"), ("เรียกตามงาน", "จ่ายตามวันที่ทำงาน")],
  fit=('เรากำลังหาผู้ช่วยที่อยู่ใน<b>{A}</b> หรือใกล้เคียง เพื่อช่วยงานที่โรงไฟฟ้าโซลาร์ที่ Solar ESS ดูแลในพื้นที่ (Solar ESS เปิดรับตำแหน่งเดียวกันที่หาดใหญ่ ตรัง และกระบี่) '
       'ทำงานร่วมกับช่างของ Solar ESS หรือทีมช่างสมาชิก TSIA หรือทำเองสำหรับงานล้างแผงทั่วไป งานส่วนใหญ่ใช้เวลาไม่กี่ชั่วโมงหรือ 1 วัน '
       'เหมาะสำหรับผู้ที่เพิ่งเริ่มงานโซลาร์และอยากเรียนรู้ หรือช่างที่มีวันว่างระหว่างงาน '
       '<b>ความปลอดภัย:</b> งานบนหลังคาต้องปฏิบัติตามหลักการทำงานบนที่สูง (ใช้เข็มขัดนิรภัยเมื่อจำเป็น) ห้ามเปิดอินเวอร์เตอร์ แบตเตอรี่ หรืออุปกรณ์ DC เว้นแต่ช่างผู้รับผิดชอบตัดระบบแล้วและสั่งให้ทำ'),
  scope_t="ลักษณะงาน", scope=[
   "ล้างแผงโซลาร์ด้วยแปรงขนนุ่มและน้ำสะอาด (ห้ามใช้แปรงแข็ง น้ำยาทำความสะอาด หรือเครื่องฉีดน้ำแรงดันสูง)",
   "ช่วยงานบำรุงรักษาเชิงป้องกัน: ตรวจดูแผง โครงยึด สายไฟ ท่อร้อยสาย และขั้วต่อ ขันแน่นและติดป้าย",
   "ถ่ายรูปก่อนและหลัง และกรอกแบบฟอร์มรายงานการล้างแผงและบำรุงรักษาของ Solar ESS",
   "ขนเครื่องมือและวัสดุ ดูแลหน้างานให้สะอาดและปลอดภัย ช่วยช่างวัดค่าต่าง ๆ",
   "ช่วยงานอื่นหน้างานในวันติดตั้งหรือบริการตามที่ได้รับมอบหมาย"],
  req_t="คุณสมบัติที่ต้องการ", req=[
   "อยู่ใน{A}หรือใกล้เคียง มีพาหนะของตัวเอง (มอเตอร์ไซค์ได้)",
   "ทำงานบนหลังคาและกลางแดดได้ ละเอียดรอบคอบและซื่อสัตย์",
   "มีความรู้ไฟฟ้าเบื้องต้นจะพิจารณาเป็นพิเศษ มีใบรับรองหรือผ่านการอบรมไฟฟ้าเป็นข้อได้เปรียบ แต่ไม่บังคับ",
   "มีสมาร์ทโฟนและ LINE สำหรับส่งรูปและรับแจ้งงาน"],
  frm="<b>แบบฟอร์มรายงานการล้างแผง:</b> ดาวน์โหลดก่อนสมัคร กรอกที่หน้างานและส่งกลับพร้อมรูปถ่าย",
  rmk=('<b>หมายเหตุ:</b> ผู้สมัครต้องส่ง<b>ประวัติ ใบรับรอง และใบเสนอราคา</b> จากนั้นทางเราจะติดต่อกลับเพื่อพูดคุยรายละเอียดงาน ขออภัยหากข้อความทาง Facebook ของท่านยังไม่ได้รับการตอบกลับ '
       '<b>กรุณาอ่านรายละเอียดงานให้ครบถ้วน ไม่ต้องสอบถามทางข้อความ Facebook – กรุณาสมัครผ่านแบบฟอร์มด้านล่าง</b><br>'
       '<b>งานนี้ค่าแรงคงที่วันละ 800 บาท</b> จึงไม่ต้องเสนอราคา แต่ให้แจ้ง<b>วันที่ทำงานได้</b> พร้อมประสบการณ์ด้านโซลาร์หรือไฟฟ้าที่มี'
       '<span class="tsia-req"><br><b>ก่อนสมัคร:</b> ช่างทุกคนที่จะทำงานกับ Solar ESS ต้อง<b>ผ่านแบบทดสอบช่างของ Solar ESS อย่างน้อย 1 ชุด</b> (<a href="/th/installer-test.html">ทำแบบทดสอบ</a>) '
       'และ<b>สมัครเป็นสมาชิก TSIA</b> (<a href="/th/team.html#tsia-form">สมัครสมาชิก</a>) ใบสมัครจากผู้ที่ยังไม่ได้ทำทั้งสองอย่างจะไม่ได้รับการพิจารณา<br>'
       '<b>แจ้งพื้นที่ที่อยู่ของท่าน:</b> ระบุตำแหน่งที่อยู่โดยประมาณ (ตำบล อำเภอ จังหวัด) ผู้ที่อยู่ใกล้{A}จะมีโอกาสได้งานมากกว่า '
       '<a href="/th/location.html">ลงทะเบียนหรืออัปเดตตำแหน่ง</a>เพื่อรับแจ้งงานใกล้บ้าน</span>'),
  go="สมัครงานนี้ →"),
}


def card(lang, area):
    sid, en, th, mq, lat, lng, q = area
    A = en if lang == "en" else th
    t = {k: (v.replace("{A}", A) if isinstance(v, str) else [x.replace("{A}", A) for x in v] if isinstance(v, list) and v and isinstance(v[0], str)
             else [(a.replace("{A}", A), b.replace("{A}", A)) for a, b in v] if isinstance(v, list) else v) for k, v in T[lang].items()}
    jid = f"assistant-daily-{sid}"
    job = f"Solar installer assistant – daily wage 800 THB, {en} (PV cleaning, preventive maintenance)"
    mp = (f'<a href="https://www.google.com/maps/search/?api=1&amp;query={mq}%2C%20Thailand" target="_blank" rel="noopener" '
          f'style="color:var(--c);font-weight:600">{t["maplbl"]}</a>')
    facts = "".join(f'<div class="fact"><b>{a}</b>{b}</div>' for a, b in t["facts"])
    dl = (f'<details class="dlv" open><summary>{t["scope_t"]} <span>({len(t["scope"])})</span></summary><ul>' + "".join(f"<li>{i}</li>" for i in t["scope"]) + "</ul></details>"
          f'<details class="dlv" open><summary>{t["req_t"]} <span>({len(t["req"])})</span></summary><ul>' + "".join(f"<li>{i}</li>" for i in t["req"]) + "</ul></details>")
    frm = (f'<div class="frm"><p>{t["frm"]}</p><div class="frmdl"><a href="{FORM.format("EN", "07")}" download>Report form EN ↓</a>'
           f'<a href="{FORM.format("TH", "02")}" download>Report form TH ↓</a></div></div>')
    return (f'<article class="card p" id="{jid}" data-posted="2026-11-27" data-tags="project south" data-lat="{lat}" data-lng="{lng}" '
            f'data-work="cleaning" data-q="{q} assistant ผู้ช่วยช่าง daily wage ค่าแรงรายวัน pv cleaning ล้างแผง preventive maintenance บำรุงรักษา">'
            f'<div class="thumb ph" aria-hidden="true">{SVG}<span>{A}</span></div>'
            f'<div class="top"><div class="ico">{SVG}</div><div><div class="kind">{t["kind"]}<span class="posted"> · {t["posted"]}</span></div><h3>{t["h3"]}</h3></div></div>\n'
            f'<div class="body"><div class="where">{PIN}<span>{A} · <span style="white-space:nowrap">{mp}</span></span></div>\n'
            f'<div class="facts">{facts}</div>\n<p class="fit">{t["fit"]}</p>\n{dl}{frm}\n'
            f'<p class="fit rmk" style="border-left-color:var(--c);margin-top:12px">{t["rmk"]}</p>\n'
            f'<div class="go"><a href="#apply" data-job="{job}">{t["go"]}</a></div></div></article>\n')


for lang, path in (("en", "job.html"), ("th", "th/job.html")):
    p = ROOT / path
    s = p.read_text(encoding="utf-8")
    s = re.sub(r'<article class="card p[^"]*" id="assistant-daily-[a-z-]+".*?</article>\n?', "", s, flags=re.S)
    m = re.search(r'<article class="card p[^"]*" id="', s)
    s = s[:m.start()] + "".join(card(lang, a) for a in AREAS) + s[m.start():]
    p.write_text(s, encoding="utf-8")
    print(path, "inserted", len(AREAS))
