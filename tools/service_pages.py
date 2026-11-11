# -*- coding: utf-8 -*-
"""Build the Solar Package page (package.html, th/package.html) and the Preventive Maintenance page
(maintenance.html, th/maintenance.html) from the quotation page shell (same header, menu and footer).
No prices on these pages: prices are sent on request (consultation / LINE / phone).
Run from the repo root:  python3 tools/service_pages.py   then  python3 tools/projects_menu.py  and  python3 tools/analytics_tag.py"""
import re

CSS = """<style>
.svg{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:20px;margin-top:28px}
.svc{position:relative;background:var(--white);border:1.5px solid var(--line);padding:24px 22px 22px;display:flex;flex-direction:column;gap:6px}
.svc.hl{background:var(--navy);border-color:var(--navy);color:var(--white)}
.svc .lv{font-family:var(--mono);font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--mute)}
.svc.hl .lv,.svc.hl .br{color:var(--sky)}
.svc h3{font-size:clamp(22px,2.4vw,28px);margin:0}
.svc .br{color:var(--mute);font-size:15px;margin:0}
.svc .sz{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0 4px}
.svc .sz span{font-family:var(--mono);font-size:12px;border:1.5px solid currentColor;padding:4px 8px;opacity:.85}
.svc ul,.svinc{list-style:none;margin:6px 0 0;padding:0;display:grid;gap:8px}
.svc li,.svinc li{position:relative;padding-left:28px;line-height:1.45}
.svc li::before,.svinc li::before{content:"";position:absolute;left:0;top:3px;width:18px;height:18px;border-radius:50%;background:var(--navy) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 18 18'%3E%3Cpath d='M5.2 9.2l2.5 2.4 5-5.2' stroke='%23fff' stroke-width='2' fill='none' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center/18px no-repeat}
.svc.hl li::before{background-color:#fff;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 18 18'%3E%3Cpath d='M5.2 9.2l2.5 2.4 5-5.2' stroke='%230A1230' stroke-width='2' fill='none' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E")}
.svc .go{margin-top:auto;padding-top:14px}
.svinc{grid-template-columns:repeat(2,minmax(0,1fr));column-gap:32px;margin-top:16px}
.svh2{font-size:clamp(28px,3.4vw,40px);margin:0}
.svsub{color:var(--mute);margin-top:8px;max-width:820px}
.svnote{margin-top:24px;background:var(--sky);padding:18px 22px}
.svsteps{counter-reset:s;list-style:none;padding:0;margin:24px 0 0;display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px}
.svsteps li{counter-increment:s;border-top:3px solid var(--navy);padding-top:12px}
.svsteps li::before{content:counter(s,decimal-leading-zero);font-family:var(--mono);font-size:12px;color:var(--mute);display:block;margin-bottom:4px}
@media(max-width:820px){.svinc{grid-template-columns:minmax(0,1fr)}}
</style>
"""
PHONE = '<a class="btn" href="tel:+66631516694">{call} · 063 151 6694</a><a class="btn ghost" href="https://line.me/ti/p/~solaress1" target="_blank" rel="noopener">LINE: solaress1</a>'


def li(xs):
    return "".join(f"<li>{x}</li>" for x in xs)


def card(c):
    sz = "".join(f"<span>{s}</span>" for s in c.get("sz", []))
    go = f'<div class="go"><a class="btn{" ghost" if not c.get("hl") else ""}" href="{c["href"]}">{c["btn"]}</a></div>' if c.get("btn") else ""
    return (f'<div class="svc{" hl" if c.get("hl") else ""}"><span class="lv">{c["lv"]}</span><h3>{c["name"]}</h3><p class="br">{c["br"]}</p>'
            + (f'<div class="sz">{sz}</div>' if sz else "") + f'<ul>{li(c["items"])}</ul>{go}</div>')


def hero(eyebrow, h1, lede, call, extra=""):
    return (f'<section class="dark band" style="padding-block:64px"><div class="wrap"><p class="eyebrow">{eyebrow}</p>'
            f'<h1 style="font-size:clamp(36px,6vw,64px)">{h1}</h1><p class="lede" style="margin-top:18px;max-width:820px">{lede}</p>'
            f'<div class="cta" style="margin-top:26px;display:flex;gap:12px;flex-wrap:wrap">{PHONE.format(call=call)}{extra}</div></div></section>')


def section(eyebrow, h2, sub, inner, paper=False):
    bg = ' style="padding-block:64px;background:var(--paper)"' if paper else ' style="padding-block:64px"'
    return (f'<section class="band{"" if paper else " light"}"{bg}><div class="wrap"><p class="eyebrow">{eyebrow}</p><h2 class="svh2">{h2}</h2>'
            + (f'<p class="svsub">{sub}</p>' if sub else "") + inner + "</div></section>")


def cta(h, p, buttons):
    return (f'<section class="dark band" style="padding-block:56px"><div class="wrap"><h2 class="svh2">{h}</h2><p class="lede" style="margin-top:10px">{p}</p>'
            f'<div style="margin-top:22px;display:flex;gap:12px;flex-wrap:wrap">{buttons}</div></div></section>')


# ------------------------------------------------------------------ Solar Package
PKG = {
 "en": dict(
  title="Solar Packages: On-grid, Hybrid and Off-grid Systems | Solar ESS",
  desc="Solar ESS solar packages for homes, businesses and farms: on-grid, hybrid with battery, off-grid and commercial systems, installed to standard across Thailand. Ask for a package price.",
  body=lambda: hero("Services · Solar Package", "Solar packages,<br>sized for your site.",
      "Four ways to go solar, from a small on-grid roof to a fully off-grid site. Every package is sized from your electricity bill and roof, built with quality, well-matched materials and installed by a qualified team. Prices are sent on request, worked out for your site.",
      "Ask for a package price", '<a class="btn ghost" href="/quotation.html">See sample quotations</a>')
   + "\n" + section("Packages", "Choose the system that fits how you use power", "Sizes are a guide; we confirm the right size after looking at 3–12 months of your bills and photos of your roof and main board.",
      '<div class="svg">' + "".join(card(c) for c in [
        dict(lv="Daytime savings", name="On-grid", br="Homes, shops and offices that use most power in the day.", sz=["3 kWp", "5 kWp", "10 kWp", "20 kWp"],
             items=["Panels and grid-tie inverter, no battery", "Zero export setting so no power is fed back to the grid", "Lowest cost per kWp and fastest payback", "Monitoring app on your phone"], btn="Ask for a price", href="/#consult"),
        dict(hl=True, lv="Most popular", name="Hybrid with battery", br="Save day and night, and keep key loads on during power cuts.", sz=["5 kW + 10 kWh", "10 kW + 16 kWh", "3-phase"],
             items=["Hybrid inverter with lithium (LFP) battery", "Backup circuit for lights, fridge, Wi-Fi and pumps", "Battery schedule set to your tariff and habits", "Add more battery later"], btn="Ask for a price", href="/#consult"),
        dict(lv="No grid", name="Off-grid", br="Farms, resorts and homes far from the grid, or where the grid is weak.", sz=["5–30 kW", "single or 3-phase"],
             items=["Sized for your full daily use and cloudy days", "Battery bank and backup generator input", "ATS and load planning for pumps and air conditioners", "Remote monitoring where there is signal"], btn="Ask for a price", href="/#consult"),
        dict(lv="Business", name="Commercial & factory", br="Factories, hotels, hospitals, schools and farms.", sz=["30–100+ kWp", "rooftop", "carport", "ground"],
             items=["Load study from your meter data", "Rooftop, carport or ground-mount structure", "PEA / MEA paperwork and grid connection", "Engineer-signed drawings and handover file"], btn="Ask for a price", href="/#consult"),
      ]) + "</div>")
   + "\n" + section("In every package", "What is included", "",
      '<ul class="svinc">' + li(["Site survey and system design from your bills", "Tier-1 solar panels and a matched inverter",
        "Mounting structure, rails and clamps for your roof type", "Copper DC/AC cables in conduit, labelled",
        "DC and AC protection: breakers, fuses and surge protection (SPD)", "Earthing to standard",
        "Grid-connection paperwork with PEA / MEA (on-grid and hybrid)", "Monitoring set-up on your phone",
        "Testing, commissioning and a handover report", "Manufacturer warranties plus Solar ESS workmanship warranty",
        "Full e-Tax Invoice", "Preventive maintenance plans available after handover"]) + "</ul>"
      + '<div class="svnote"><b>Want to see the detail first?</b> Our <a href="/quotation.html">sample quotations</a> show real scopes, terms and drawings with customer names removed, and the <a href="/picks.html">Products</a> page explains the materials we pick and why.</div>', paper=True)
   + "\n" + section("How it works", "From your bill to a working system", "",
      '<ol class="svsteps">' + li(["<b>Send your bill and photos</b><br>3–12 months of bills, roof and main board photos.", "<b>Get a package and price</b><br>We size the system and send a written quotation.",
        "<b>Install and connect</b><br>Our team installs, tests and handles the grid paperwork.", "<b>Monitor and maintain</b><br>Watch it on your phone; book preventive maintenance."]) + "</ol>")
   + "\n" + cta("Ask for your package price", "Send us your electricity bill and a few photos of your roof and main board, and we will reply with the right package and price.",
      PHONE.format(call="Call") + '<a class="btn ghost" href="/#consult">Book a consultation</a><a class="btn ghost" href="/quotation.html">Sample quotations</a>')),
 "th": dict(
  title="แพ็กเกจโซลาร์เซลล์: ออนกริด ไฮบริด และออฟกริด | Solar ESS",
  desc="แพ็กเกจโซลาร์เซลล์ Solar ESS สำหรับบ้าน ธุรกิจ และฟาร์ม: ออนกริด ไฮบริดพร้อมแบตเตอรี่ ออฟกริด และระบบเชิงพาณิชย์ ติดตั้งได้มาตรฐานทั่วประเทศไทย สอบถามราคาแพ็กเกจได้",
  body=lambda: hero("บริการ · แพ็กเกจโซลาร์", "แพ็กเกจโซลาร์<br>ออกแบบตามหน้างานของคุณ",
      "4 แบบให้เลือก ตั้งแต่ระบบออนกริดบนหลังคาขนาดเล็ก จนถึงระบบออฟกริดเต็มรูปแบบ ทุกแพ็กเกจคำนวณขนาดจากบิลค่าไฟและหลังคาของคุณ ใช้วัสดุคุณภาพที่เข้ากันอย่างถูกต้อง และติดตั้งโดยทีมช่างที่มีคุณวุฒิ ราคาแจ้งตามคำขอ คำนวณเฉพาะหน้างานของคุณ",
      "สอบถามราคาแพ็กเกจ", '<a class="btn ghost" href="/th/quotation.html">ดูตัวอย่างใบเสนอราคา</a>')
   + "\n" + section("แพ็กเกจ", "เลือกระบบที่เหมาะกับการใช้ไฟของคุณ", "ขนาดเป็นเพียงแนวทาง เราจะยืนยันขนาดที่เหมาะสมหลังดูบิลค่าไฟ 3–12 เดือน และรูปหลังคากับตู้ไฟหลัก",
      '<div class="svg">' + "".join(card(c) for c in [
        dict(lv="ประหยัดกลางวัน", name="ออนกริด", br="บ้าน ร้านค้า และสำนักงานที่ใช้ไฟกลางวันเป็นหลัก", sz=["3 kWp", "5 kWp", "10 kWp", "20 kWp"],
             items=["แผงโซลาร์และอินเวอร์เตอร์ออนกริด ไม่มีแบตเตอรี่", "ตั้งค่าไม่ส่งไฟย้อนเข้าสายส่ง (Zero export)", "ต้นทุนต่อ kWp ต่ำที่สุด คืนทุนเร็ว", "ดูการผลิตไฟผ่านแอปบนมือถือ"], btn="สอบถามราคา", href="/th/#consult"),
        dict(hl=True, lv="ยอดนิยม", name="ไฮบริดพร้อมแบตเตอรี่", br="ประหยัดทั้งกลางวันและกลางคืน และมีไฟสำรองเมื่อไฟดับ", sz=["5 kW + 10 kWh", "10 kW + 16 kWh", "3 เฟส"],
             items=["อินเวอร์เตอร์ไฮบริดพร้อมแบตเตอรี่ลิเธียม (LFP)", "วงจรไฟสำรองสำหรับไฟแสงสว่าง ตู้เย็น Wi-Fi และปั๊มน้ำ", "ตั้งเวลาชาร์จ/จ่ายแบตตามอัตราค่าไฟและการใช้งาน", "เพิ่มแบตเตอรี่ภายหลังได้"], btn="สอบถามราคา", href="/th/#consult"),
        dict(lv="ไม่มีไฟการไฟฟ้า", name="ออฟกริด", br="ฟาร์ม รีสอร์ต และบ้านที่ห่างไกลสายส่ง หรือไฟการไฟฟ้าไม่เสถียร", sz=["5–30 kW", "1 เฟส หรือ 3 เฟส"],
             items=["ออกแบบให้พอกับการใช้ไฟทั้งวันและวันที่ฟ้าครึ้ม", "ชุดแบตเตอรี่และช่องต่อเครื่องปั่นไฟสำรอง", "ATS และวางแผนโหลดสำหรับปั๊มน้ำและแอร์", "ติดตามระบบระยะไกลในพื้นที่ที่มีสัญญาณ"], btn="สอบถามราคา", href="/th/#consult"),
        dict(lv="ธุรกิจ", name="เชิงพาณิชย์และโรงงาน", br="โรงงาน โรงแรม โรงพยาบาล โรงเรียน และฟาร์ม", sz=["30–100+ kWp", "หลังคา", "โรงจอดรถ", "บนพื้นดิน"],
             items=["วิเคราะห์โหลดจากข้อมูลมิเตอร์", "โครงสร้างบนหลังคา โรงจอดรถ หรือบนพื้นดิน", "เอกสารและการขอเชื่อมต่อกับ กฟภ. / กฟน.", "แบบลงนามโดยวิศวกรและแฟ้มส่งมอบงาน"], btn="สอบถามราคา", href="/th/#consult"),
      ]) + "</div>")
   + "\n" + section("รวมในทุกแพ็กเกจ", "สิ่งที่ได้รับ", "",
      '<ul class="svinc">' + li(["สำรวจหน้างานและออกแบบระบบจากบิลค่าไฟ", "แผงโซลาร์ Tier-1 และอินเวอร์เตอร์ที่เข้ากัน",
        "โครงสร้าง ราง และตัวยึดที่เหมาะกับหลังคา", "สายไฟทองแดง DC/AC เดินในท่อ ติดป้ายครบ",
        "อุปกรณ์ป้องกัน DC และ AC: เบรกเกอร์ ฟิวส์ และอุปกรณ์ป้องกันฟ้าผ่า (SPD)", "ระบบสายดินตามมาตรฐาน",
        "เอกสารขอเชื่อมต่อกับ กฟภ. / กฟน. (ออนกริดและไฮบริด)", "ตั้งค่าระบบติดตามบนมือถือ",
        "ทดสอบ เดินระบบ และรายงานส่งมอบงาน", "รับประกันจากผู้ผลิต และรับประกันงานติดตั้งจาก Solar ESS",
        "ใบกำกับภาษีอิเล็กทรอนิกส์ (e-Tax Invoice) เต็มรูปแบบ", "มีแผนบำรุงรักษาเชิงป้องกันหลังส่งมอบงาน"]) + "</ul>"
      + '<div class="svnote"><b>อยากดูรายละเอียดก่อน?</b> <a href="/th/quotation.html">ตัวอย่างใบเสนอราคา</a> แสดงขอบเขตงาน เงื่อนไข และแบบจริง (ตัดชื่อลูกค้าออกแล้ว) และหน้า <a href="/th/picks.html">ผลิตภัณฑ์</a> อธิบายวัสดุที่เราเลือกและเหตุผล</div>', paper=True)
   + "\n" + section("ขั้นตอน", "จากบิลค่าไฟ สู่ระบบที่ใช้งานได้จริง", "",
      '<ol class="svsteps">' + li(["<b>ส่งบิลและรูปถ่าย</b><br>บิลค่าไฟ 3–12 เดือน รูปหลังคาและตู้ไฟหลัก", "<b>รับแพ็กเกจและราคา</b><br>เราคำนวณขนาดระบบและส่งใบเสนอราคา",
        "<b>ติดตั้งและเชื่อมต่อ</b><br>ทีมงานติดตั้ง ทดสอบ และดำเนินเอกสารกับการไฟฟ้า", "<b>ติดตามและบำรุงรักษา</b><br>ดูระบบผ่านมือถือ และนัดบำรุงรักษาเชิงป้องกัน"]) + "</ol>")
   + "\n" + cta("สอบถามราคาแพ็กเกจของคุณ", "ส่งบิลค่าไฟและรูปหลังคากับตู้ไฟหลักมาให้เรา แล้วเราจะแนะนำแพ็กเกจและราคาที่เหมาะสม",
      PHONE.format(call="โทร") + '<a class="btn ghost" href="/th/#consult">นัดขอคำปรึกษา</a><a class="btn ghost" href="/th/quotation.html">ตัวอย่างใบเสนอราคา</a>')),
}

# ------------------------------------------------------------------ Preventive Maintenance
PM_FORM_EN = "/downloads/Solar-ESS-PV-Cleaning-Maintenance-Report-Form-EN_Rev07_WM_20261111.pdf"
PM_FORM_TH = "/downloads/Solar-ESS-PV-Cleaning-Maintenance-Report-Form-TH_Rev02_WM_20261111.pdf"
PM = {
 "en": dict(
  title="Preventive Maintenance for Solar PV Systems | Solar ESS",
  desc="Solar ESS preventive maintenance plans: PV cleaning, string measurements, thermal scan, connection and breaker checks, inverter and battery health, earthing and SPD, with a written report.",
  body=lambda: hero("Services · Preventive Maintenance", "Keep your solar<br>safe and producing.",
      "Dust, loose connections, wrong settings and tired batteries quietly cut output and can become a fire risk. Our preventive maintenance finds them early: we clean, measure, tighten, check the settings and send you a written report with photos.",
      "Book a maintenance visit", '<a class="btn ghost" href="/technical-notes.html#topic-monthly">See our Monthly Report</a>')
   + "\n" + section("Plans", "Choose how often we visit", "For systems installed by Solar ESS or by others. Prices depend on system size, access and location and are sent on request.",
      '<div class="svg">' + "".join(card(c) for c in [
        dict(lv="Once a year", name="Basic", br="Small homes in clean areas.", items=["PV panel cleaning", "Visual check of panels, roof fixings and cables", "Inverter alarm log and settings check", "Photo report before and after"], btn="Book Basic", href="/#consult"),
        dict(hl=True, lv="Twice a year · recommended", name="Standard", br="Most homes and businesses; dusty or farm areas.", items=["Everything in Basic", "String voltage and current, before and after", "Thermal scan of panels and boards", "Tighten DC/AC connections, MC4 and breakers", "Earthing and surge protection (SPD) check", "Written report with findings and advice"], btn="Book Standard", href="/#consult"),
        dict(lv="Every 3 months", name="Plus", br="Factories, hotels, farms and systems with batteries.", items=["Everything in Standard", "Battery health: charge level, BMS link, terminals", "Monthly monitoring review and alerts", "Settings tuned to your tariff and loads", "Priority call-out for faults"], btn="Book Plus", href="/#consult"),
      ]) + "</div>")
   + "\n" + section("Every visit", "What we check", "",
      '<ul class="svinc">' + li(["Panels cleaned with soft brushes and clean water, no harsh chemicals", "Cracks, hot spots, discoloured cells and broken glass",
        "Roof fixings, rails, clamps and water-tightness", "Cables, conduit, glands and MC4 connectors",
        "DC isolators, fuses, breakers and terminal torque", "Inverter: alarms, settings, firmware, ventilation",
        "Battery (where fitted): charge level, BMS communication, terminals", "Earthing and surge protection devices (SPD)",
        "Monitoring and data logger online", "Production compared with what the system should give"]) + "</ul>"
      + f'<div class="svnote"><b>The report you get:</b> photos before and after, string readings, findings and advice on the Solar ESS report form. <a href="{PM_FORM_EN}" download>English form ↓</a> · <a href="{PM_FORM_TH}" download>Thai form ↓</a></div>', paper=True)
   + "\n" + section("Why it matters", "Small checks, big savings", "",
      '<ol class="svsteps">' + li(["<b>More output</b><br>Dirty panels can lose a noticeable share of their production, more in dry and farm areas.", "<b>Safer system</b><br>Loose DC connections and burnt MC4 connectors are a common cause of solar fires.",
        "<b>Longer life</b><br>Correct battery and inverter settings protect the most expensive parts.", "<b>Warranty ready</b><br>Dated reports help when you need to claim a warranty."]) + "</ol>")
   + "\n" + cta("Book preventive maintenance", "Tell us your system size, location and monitoring app, and we will plan a visit. Solar ESS installers work across Thailand.",
      PHONE.format(call="Call") + '<a class="btn ghost" href="/#consult">Book a consultation</a><a class="btn ghost" href="/care.html">Solar ESS Care</a>')),
 "th": dict(
  title="บำรุงรักษาเชิงป้องกันระบบโซลาร์เซลล์ | Solar ESS",
  desc="แผนบำรุงรักษาเชิงป้องกันจาก Solar ESS: ล้างแผง วัดค่าสตริง สแกนความร้อน ตรวจจุดต่อและเบรกเกอร์ ตรวจอินเวอร์เตอร์และแบตเตอรี่ สายดินและ SPD พร้อมรายงานเป็นลายลักษณ์อักษร",
  body=lambda: hero("บริการ · บำรุงรักษาเชิงป้องกัน", "ดูแลโซลาร์ให้ปลอดภัย<br>และผลิตไฟเต็มที่",
      "ฝุ่น จุดต่อหลวม การตั้งค่าผิด และแบตเตอรี่เสื่อม ทำให้ผลิตไฟได้น้อยลงโดยไม่รู้ตัว และอาจเสี่ยงไฟไหม้ การบำรุงรักษาเชิงป้องกันช่วยพบปัญหาตั้งแต่เนิ่น ๆ เราล้าง วัดค่า ขันจุดต่อ ตรวจการตั้งค่า และส่งรายงานพร้อมรูปถ่ายให้คุณ",
      "นัดบำรุงรักษา", '<a class="btn ghost" href="/th/technical-notes.html#topic-monthly">ดูรายงานประจำเดือน</a>')
   + "\n" + section("แผนบริการ", "เลือกความถี่ในการเข้าดูแล", "สำหรับระบบที่ติดตั้งโดย Solar ESS หรือผู้ติดตั้งรายอื่น ราคาขึ้นกับขนาดระบบ การเข้าถึง และพื้นที่ แจ้งราคาตามคำขอ",
      '<div class="svg">' + "".join(card(c) for c in [
        dict(lv="ปีละ 1 ครั้ง", name="พื้นฐาน", br="บ้านขนาดเล็กในพื้นที่ฝุ่นน้อย", items=["ล้างแผงโซลาร์", "ตรวจสภาพแผง จุดยึดหลังคา และสายไฟด้วยสายตา", "ตรวจประวัติแจ้งเตือนและการตั้งค่าอินเวอร์เตอร์", "รายงานรูปถ่ายก่อนและหลัง"], btn="นัดแผนพื้นฐาน", href="/th/#consult"),
        dict(hl=True, lv="ปีละ 2 ครั้ง · แนะนำ", name="มาตรฐาน", br="บ้านและธุรกิจส่วนใหญ่ พื้นที่ฝุ่นมากหรือฟาร์ม", items=["ทุกอย่างในแผนพื้นฐาน", "วัดแรงดันและกระแสสตริง ก่อนและหลัง", "สแกนความร้อนแผงและตู้ไฟ", "ขันจุดต่อ DC/AC, MC4 และเบรกเกอร์", "ตรวจสายดินและอุปกรณ์ป้องกันฟ้าผ่า (SPD)", "รายงานผลการตรวจและคำแนะนำ"], btn="นัดแผนมาตรฐาน", href="/th/#consult"),
        dict(lv="ทุก 3 เดือน", name="พลัส", br="โรงงาน โรงแรม ฟาร์ม และระบบที่มีแบตเตอรี่", items=["ทุกอย่างในแผนมาตรฐาน", "ตรวจสุขภาพแบตเตอรี่: ระดับประจุ การสื่อสาร BMS ขั้วต่อ", "ตรวจข้อมูลระบบติดตามทุกเดือนและแจ้งเตือน", "ปรับการตั้งค่าให้เหมาะกับอัตราค่าไฟและโหลด", "เข้าแก้ไขเหตุขัดข้องเป็นลำดับแรก"], btn="นัดแผนพลัส", href="/th/#consult"),
      ]) + "</div>")
   + "\n" + section("ทุกครั้งที่เข้าดูแล", "รายการที่เราตรวจ", "",
      '<ul class="svinc">' + li(["ล้างแผงด้วยแปรงนุ่มและน้ำสะอาด ไม่ใช้สารเคมีรุนแรง", "รอยร้าว จุดร้อน (hot spot) เซลล์เปลี่ยนสี และกระจกแตก",
        "จุดยึดหลังคา ราง ตัวยึด และการกันน้ำ", "สายไฟ ท่อ เคเบิลแกลนด์ และขั้วต่อ MC4",
        "สวิตช์ตัดตอน DC ฟิวส์ เบรกเกอร์ และแรงขันขั้วต่อ", "อินเวอร์เตอร์: แจ้งเตือน การตั้งค่า เฟิร์มแวร์ การระบายอากาศ",
        "แบตเตอรี่ (ถ้ามี): ระดับประจุ การสื่อสาร BMS ขั้วต่อ", "ระบบสายดินและอุปกรณ์ป้องกันฟ้าผ่า (SPD)",
        "ระบบติดตามและดาต้าล็อกเกอร์ออนไลน์", "เปรียบเทียบการผลิตไฟกับค่าที่ระบบควรผลิตได้"]) + "</ul>"
      + f'<div class="svnote"><b>รายงานที่คุณได้รับ:</b> รูปก่อนและหลัง ค่าที่วัดได้ของแต่ละสตริง ผลการตรวจและคำแนะนำบนแบบฟอร์มรายงานของ Solar ESS <a href="{PM_FORM_TH}" download>แบบฟอร์มภาษาไทย ↓</a> · <a href="{PM_FORM_EN}" download>แบบฟอร์มภาษาอังกฤษ ↓</a></div>', paper=True)
   + "\n" + section("ทำไมต้องบำรุงรักษา", "ตรวจเล็กน้อย ประหยัดได้มาก", "",
      '<ol class="svsteps">' + li(["<b>ผลิตไฟได้มากขึ้น</b><br>แผงสกปรกทำให้ผลิตไฟลดลงได้พอสมควร โดยเฉพาะพื้นที่แห้งและฟาร์ม", "<b>ระบบปลอดภัยขึ้น</b><br>จุดต่อ DC หลวมและขั้ว MC4 ไหม้ เป็นสาเหตุที่พบบ่อยของไฟไหม้ในระบบโซลาร์",
        "<b>อายุการใช้งานยาวขึ้น</b><br>การตั้งค่าแบตเตอรี่และอินเวอร์เตอร์ที่ถูกต้องช่วยถนอมอุปกรณ์ราคาสูง", "<b>พร้อมเคลมประกัน</b><br>รายงานที่ระบุวันที่ช่วยเมื่อต้องเคลมประกัน"]) + "</ol>")
   + "\n" + cta("นัดบำรุงรักษาเชิงป้องกัน", "แจ้งขนาดระบบ พื้นที่ และแอปที่ใช้ติดตามระบบ แล้วเราจะวางแผนเข้าดูแล ทีมช่างของ Solar ESS ให้บริการทั่วประเทศไทย",
      PHONE.format(call="โทร") + '<a class="btn ghost" href="/th/#consult">นัดขอคำปรึกษา</a><a class="btn ghost" href="/th/care.html">Solar ESS Care</a>')),
}

OG = {"package": "home-aerial-share.jpg", "maintenance": "job-pv-samui-20a.jpg"}


def build(slug, lang, L):
    tpl = "th/quotation.html" if lang == "th" else "quotation.html"
    out = f"th/{slug}.html" if lang == "th" else f"{slug}.html"
    src = open(tpl, encoding="utf-8").read()
    head, rest = src.split("<!--/mnav-->", 1)
    foot = rest[rest.index("<footer"):]
    base = "https://solaress.org"
    url = f"{base}/th/{slug}" if lang == "th" else f"{base}/{slug}"
    head = re.sub(r"<title>.*?</title>", f"<title>{L['title']}</title>", head, flags=re.S)
    for k in ('<meta property="og:title" content="', '<meta name="twitter:title" content="'):
        head = re.sub(re.escape(k) + r'[^"]*', k + L["title"], head)
    for k in ('<meta property="og:description" content="', '<meta name="description" content="', '<meta name="twitter:description" content="'):
        head = re.sub(re.escape(k) + r'[^"]*', k + L["desc"], head)
    head = re.sub(r'(<meta property="og:url" content=")[^"]*', r"\g<1>" + url + ".html", head)
    for k in ('<meta property="og:image" content="', '<meta name="twitter:image" content="'):
        head = re.sub(re.escape(k) + r'[^"]*', k + base + "/images/" + OG[slug], head)
    head = head.replace(f'{base}/quotation"', f'{base}/{slug}"').replace(f'{base}/th/quotation"', f'{base}/th/{slug}"')
    head = re.sub(r'<link rel="alternate" hreflang="zh-Hans"[^>]*>\n?', "", head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', "", head, flags=re.S)
    head = head.replace("</head>", CSS + "</head>", 1)
    head = re.sub(r'<span class="langsw">.*?</span></nav>', lambda m: m.group(0).replace('/zh/quotation.html', f'/{slug}.html')
                  .replace('/th/quotation.html', f'/th/{slug}.html').replace('/quotation.html', f'/{slug}.html'), head, flags=re.S)
    open(out, "w", encoding="utf-8").write(head + "<!--/mnav-->\n" + L["body"]() + "\n" + foot)
    print("wrote", out)


if __name__ == "__main__":
    for lang in ("en", "th"):
        build("package", lang, PKG[lang])  # maintenance page retired 11 Nov 2026 (redirects to /system-check.html)
