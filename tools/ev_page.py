# -*- coding: utf-8 -*-
"""Build the EV Charger page (ev.html, th/ev.html) from the quotation page shell.

Run from the repo root:  python3 tools/ev_page.py
"""
import re

CSS = """<style>
.evg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;margin-top:28px}
.evc{position:relative;background:var(--white);border:1.5px solid var(--line);padding:26px 24px 24px;display:flex;flex-direction:column;gap:6px}
.evc.hl{background:var(--navy);border-color:var(--navy);color:var(--white)}
.evc .lv{font-family:var(--mono);font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--mute)}
.evc.hl .lv,.evc.hl .br{color:var(--sky)}
.evc h3{font-size:clamp(24px,2.6vw,32px);margin:0}
.evc .br{color:var(--mute);font-size:15px}
.evc .pr{font-size:clamp(38px,4.4vw,50px);font-weight:800;line-height:1.1;margin:10px 0 4px}
.evc .pr small{font-size:18px;font-weight:600;margin-left:6px}
.evc .bdg{position:absolute;top:-14px;right:16px;background:#C8102E;color:#fff;font-size:13px;font-weight:700;padding:4px 12px;border-radius:999px}
.evc .plus{font-weight:700;font-size:15px;color:var(--mute);margin-top:6px}
.evc.hl .plus{color:var(--sky)}
.evc ul,.evinc{list-style:none;margin:6px 0 0;padding:0;display:grid;gap:8px}
.evc li,.evinc li{position:relative;padding-left:28px;line-height:1.45}
.evc li::before,.evinc li::before{content:"";position:absolute;left:0;top:3px;width:18px;height:18px;border-radius:50%;background:var(--navy) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 18 18'%3E%3Cpath d='M5.2 9.2l2.5 2.4 5-5.2' stroke='%23fff' stroke-width='2' fill='none' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center/18px no-repeat}
.evc.hl li::before{background-color:#fff;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 18 18'%3E%3Cpath d='M5.2 9.2l2.5 2.4 5-5.2' stroke='%230A1230' stroke-width='2' fill='none' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E")}
.evinc{grid-template-columns:repeat(2,minmax(0,1fr));column-gap:32px;margin-top:16px}
.evfree{margin-top:28px;background:#C8102E;color:#fff;padding:20px 24px;display:grid;grid-template-columns:auto minmax(0,1fr);gap:20px;align-items:center}
.evfree b.t{font-size:26px;font-weight:800;line-height:1.15}
.evfree ul{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px 24px}
.evsolar{margin-top:20px;background:var(--sky);padding:20px 24px}
.evsolar h3{font-size:22px;margin:0 0 4px}
.evterms{margin-top:18px;color:var(--mute);font-size:14px}
.evh2{font-size:clamp(28px,3.4vw,40px);margin:0}
.evsub{color:var(--mute);margin-top:8px}
@media(max-width:820px){.evg{grid-template-columns:minmax(0,1fr);gap:26px}.evinc,.evfree ul{grid-template-columns:minmax(0,1fr)}.evfree{grid-template-columns:minmax(0,1fr)}}
</style>
"""

def li(items):
    return "".join(f"<li>{i}</li>" for i in items)

def card(c):
    hl = " hl" if c.get("hl") else ""
    bdg = f'<span class="bdg">{c["badge"]}</span>' if c.get("badge") else ""
    plus = f'<p class="plus">{c["plus"]}</p>' if c.get("plus") else ""
    items = f'<ul>{li(c["items"])}</ul>' if c.get("items") else ""
    return (f'<article class="evc{hl}">{bdg}<span class="lv">{c["lv"]}</span><h3>{c["name"]}</h3>'
            f'<span class="br">{c["brand"]}</span><div class="pr">{c["price"]}<small>{c["baht"]}</small></div>{plus}{items}</article>')

EN = dict(
    lang="en", tpl="quotation.html", out="ev.html",
    title="EV Charger Circuit Packages: Home EV Charging Installation | Solar ESS",
    desc="Dedicated EV charger circuit packages by Solar ESS: CHINT, ABB or Schneider, shock-protection RCBO, earthing, testing and free gifts. Call for a free inspection.",
    hero=('<section class="dark band" style="padding-block:64px"><div class="wrap"><p class="eyebrow">Projects · EV Charger</p>'
          '<h1 style="font-size:clamp(36px,6vw,64px)">EV home charging,<br>wired safely.</h1>'
          '<p class="lede" style="margin-top:18px">A dedicated second circuit for your EV charger: a separate run from your board, a shock-protection breaker, proper earthing, and every connection tested. Two promotions: pick a brand, or pick a protection level.</p>'
          '<div class="cta" style="margin-top:26px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn" href="tel:+66631516694">Call for a free inspection · 063 151 6694</a><a class="btn ghost" href="https://line.me/ti/p/~solaress1" target="_blank" rel="noopener">LINE: solaress1</a></div></div></section>'),
    p1=("Promotion 1", "Pick your brand", "The same professional installation in every package."),
    p1cards=[dict(lv="Value", name="CHINT", brand="CHINT board and breakers", price="8,900", baht="baht"),
             dict(lv="European standard", name="ABB", brand="ABB board and breakers", price="9,900", baht="baht", hl=1, badge="Most popular"),
             dict(lv="Premium", name="Schneider", brand="Schneider board and breakers", price="10,900", baht="baht")],
    inc_h="Every package includes",
    inc=["4-way consumer unit in the brand you choose", "2P 50A 10kA main breaker", "40A 30mA RCBO (shock protection)",
         "IEC01 / THW 16 mm² copper cable", '5/8" × 2.4 m earth rod + 10 mm² THW earth cable, 3 m', '3/4" U-PVC conduit with all fittings',
         "Insulation and earth-resistance test", "Test report with site photos"],
    free_t="Free<br>gifts",
    free1=["<b>Automatic over/under-voltage protector</b> in the consumer unit (worth 790 baht)", "<b>15 m THW cable</b>, 100% copper, TIS-certified, every package"],
    p2=("Promotion 2", "Pick your protection level", "Three levels at the same prices. Each level adds more protection."),
    p2cards=[dict(lv="Level 1", name="Start Charging", brand="CHINT equipment", price="8,900", baht="baht",
                  items=["4-way consumer unit", "2P 50A 10kA main breaker", "40A 30mA RCBO (shock protection)", "IEC01 / THW 16 mm² cable", '5/8" 2.4 m earth rod + 10 mm² earth cable', "U-PVC conduit with all fittings"]),
             dict(lv="Level 2", name="Full-System Safety", brand="ABB equipment", price="9,900", baht="baht", hl=1, badge="Best value", plus="Everything in Level 1, plus",
                  items=["Surge and lightning protector (SPD)", "EMT steel conduit for outdoor runs", "Insulation and earth-resistance test", "Test report with photos"]),
             dict(lv="Level 3", name="Solar-Ready", brand="Schneider equipment", price="10,900", baht="baht", plus="Everything in Level 2, plus",
                  items=["Spare ways in the board for future solar and battery", "Free estimate: how much of your charging solar can cover each month", "One free system check in the first year"])],
    free2_t="Free in<br>every level",
    free2=["<b>Over/under-voltage protector</b> (worth 790 baht)", "<b>15 m THW cable</b>, copper, TIS-certified", "<b>Free site inspection</b>, just call", "<b>1-year installation warranty</b>"],
    solar_h="Want to charge from the sun? We are a solar team first.",
    solar_p="Ask about our EV + solar bundle discount when you install solar with Solar ESS within 12 months of your EV circuit.",
    terms="Cable run up to 15 m · extra 300 baht per metre · prices exclude the charger and the 35 mm² meter supply cable (if it needs replacing) · e-Tax Invoice available.",
    cta=('<section class="dark band" style="padding-block:56px"><div class="wrap"><h2 class="evh2">Call for a free inspection</h2>'
         '<p class="lede" style="margin-top:10px">Call us to book a free site inspection and quotation, or send photos of your electricity meter and main board on LINE.</p>'
         '<div style="margin-top:22px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn" href="tel:+66631516694">Call 063 151 6694</a><a class="btn ghost" href="tel:+66896325829">089 632 5829</a><a class="btn ghost" href="https://line.me/ti/p/~solaress1" target="_blank" rel="noopener">LINE ID: solaress1</a><a class="btn ghost" href="/#consult">Book a consultation</a></div></div></section>'),
)

TH = dict(
    lang="th", tpl="th/quotation.html", out="th/ev.html",
    title="แพ็กเกจติดตั้งวงจรชาร์จรถ EV ที่บ้าน | Solar ESS",
    desc="แพ็กเกจวงจรที่ 2 สำหรับเครื่องชาร์จรถ EV โดยโซลาร์ เอสส์ เลือก CHINT ABB หรือ Schneider มีเบรกเกอร์กันไฟดูด หลักดิน ทดสอบ และของแถม โทรนัดตรวจหน้างานฟรี",
    hero=('<section class="dark band" style="padding-block:64px"><div class="wrap"><p class="eyebrow">ผลงาน · ที่ชาร์จรถ EV</p>'
          '<h1 style="font-size:clamp(34px,5.6vw,60px)">ติดตั้งวงจรชาร์จรถ EV<br>ถูกต้อง ปลอดภัย</h1>'
          '<p class="lede" style="margin-top:18px">วงจรที่ 2 สำหรับเครื่องชาร์จ EV โดยเฉพาะ เดินสายแยกจากไฟบ้าน มีเบรกเกอร์กันไฟดูด ต่อหลักดินถูกต้อง และทดสอบทุกจุด มี 2 โปรโมชันให้เลือก: เลือกตามแบรนด์ หรือเลือกตามระดับการป้องกัน</p>'
          '<div class="cta" style="margin-top:26px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn" href="tel:+66631516694">โทรนัดตรวจหน้างานฟรี · 063 151 6694</a><a class="btn ghost" href="https://line.me/ti/p/~solaress1" target="_blank" rel="noopener">ไลน์: solaress1</a></div></div></section>'),
    p1=("โปรโมชัน 1", "เลือกแบรนด์อุปกรณ์ที่ต้องการ", "ทุกแพ็กเกจได้งานติดตั้งมาตรฐานเดียวกัน"),
    p1cards=[dict(lv="คุ้มค่า", name="CHINT", brand="ตู้ + เบรกเกอร์ CHINT", price="8,900", baht="บาท"),
             dict(lv="มาตรฐานยุโรป", name="ABB", brand="ตู้ + เบรกเกอร์ ABB", price="9,900", baht="บาท", hl=1, badge="ยอดนิยม"),
             dict(lv="พรีเมียม", name="Schneider", brand="ตู้ + เบรกเกอร์ Schneider", price="10,900", baht="บาท")],
    inc_h="ทุกแพ็กเกจรวม",
    inc=["ตู้คอนซูมเมอร์ยูนิต 4 ช่อง ตามแบรนด์ที่เลือก", "เมนเบรกเกอร์ 2P 50A 10kA", "เบรกเกอร์กันไฟดูด (RCBO) 40A 30mA",
         "สายไฟทองแดง IEC01 / THW 16 ตร.มม.", 'หลักดิน 5/8" ยาว 2.4 ม. + สายดิน THW 10 ตร.มม. 3 ม.', 'ท่อ U-PVC 3/4" พร้อมอุปกรณ์ยึดครบชุด',
         "ทดสอบฉนวนสายและค่าความต้านทานดิน", "รายงานผลการทดสอบพร้อมรูปถ่ายหน้างาน"],
    free_t="แถมฟรี!",
    free1=["<b>อุปกรณ์ป้องกันไฟตก-ไฟเกินอัตโนมัติ</b> ในตู้คอนซูมเมอร์ (มูลค่า 790 บาท)", "<b>สายไฟ THW 15 เมตร</b> ทองแดงแท้ 100% มาตรฐาน มอก. ทุกแพ็กเกจ"],
    p2=("โปรโมชัน 2", "เลือกตามระดับการป้องกัน", "3 ระดับ ราคาเดียวกัน ยิ่งระดับสูงยิ่งป้องกันครบ"),
    p2cards=[dict(lv="ระดับ 1", name="เริ่มต้นชาร์จ", brand="อุปกรณ์ CHINT", price="8,900", baht="บาท",
                  items=["ตู้คอนซูมเมอร์ 4 ช่อง", "เมนเบรกเกอร์ 2P 50A 10kA", "เบรกเกอร์กันไฟดูด RCBO 40A 30mA", "สายไฟ IEC01 / THW 16 ตร.มม.", 'หลักดิน 5/8" 2.4 ม. + สายดิน 10 ตร.มม.', "ท่อ U-PVC พร้อมอุปกรณ์ครบชุด"]),
             dict(lv="ระดับ 2", name="ปลอดภัยเต็มระบบ", brand="อุปกรณ์ ABB", price="9,900", baht="บาท", hl=1, badge="คุ้มที่สุด", plus="ทุกอย่างในระดับ 1 และเพิ่ม",
                  items=["อุปกรณ์กันฟ้าผ่า / ไฟกระชาก (SPD)", "ท่อโลหะ EMT สำหรับช่วงนอกอาคาร", "ทดสอบฉนวนสายและค่าความต้านทานดิน", "รายงานผลการทดสอบพร้อมรูปถ่าย"]),
             dict(lv="ระดับ 3", name="พร้อมโซลาร์", brand="อุปกรณ์ Schneider", price="10,900", baht="บาท", plus="ทุกอย่างในระดับ 2 และเพิ่ม",
                  items=["ช่องสำรองในตู้ สำหรับโซลาร์และแบตเตอรี่ในอนาคต", "ประเมินฟรี: โซลาร์ชาร์จรถให้ได้กี่ % ต่อเดือน", "ตรวจเช็กระบบไฟฟรี 1 ครั้งในปีแรก"])],
    free2_t="แถมฟรี<br>ทุกระดับ",
    free2=["<b>อุปกรณ์ป้องกันไฟตก-ไฟเกิน</b> (มูลค่า 790 บาท)", "<b>สายไฟ THW 15 เมตร</b> ทองแดงแท้ มอก.", "<b>ตรวจหน้างานฟรี</b> โทรนัดได้เลย", "<b>รับประกันงานติดตั้ง 1 ปี</b>"],
    solar_h="อยากชาร์จรถด้วยแดด? เราคือทีมโซลาร์โดยตรง",
    solar_p="สอบถามส่วนลดแพ็กเกจ EV + โซลาร์ เมื่อติดตั้งโซลาร์กับ Solar ESS ภายใน 12 เดือนหลังติดตั้งวงจร EV",
    terms="ระยะเดินสายไม่เกิน 15 ม. · ส่วนเกิน 300 บาท/ม. · ราคาไม่รวมเครื่องชาร์จ และสายเมนเข้ามิเตอร์ 35 ตร.มม. (ถ้าต้องเปลี่ยน) · ออกใบกำกับภาษีอิเล็กทรอนิกส์ (e-Tax Invoice) ได้",
    cta=('<section class="dark band" style="padding-block:56px"><div class="wrap"><h2 class="evh2">โทรนัดตรวจหน้างานฟรี</h2>'
         '<p class="lede" style="margin-top:10px">โทรนัดตรวจหน้างานและรับใบเสนอราคาฟรี หรือส่งรูปมิเตอร์และตู้ไฟมาทางไลน์</p>'
         '<div style="margin-top:22px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn" href="tel:+66631516694">โทร 063 151 6694</a><a class="btn ghost" href="tel:+66896325829">089 632 5829</a><a class="btn ghost" href="https://line.me/ti/p/~solaress1" target="_blank" rel="noopener">LINE ID: solaress1</a><a class="btn ghost" href="/th/#consult">นัดขอคำปรึกษา</a></div></div></section>'),
)

def body(L):
    e1, h1, s1 = L["p1"]; e2, h2, s2 = L["p2"]
    sec1 = (f'<section class="band light" id="by-brand" style="padding-block:64px"><div class="wrap"><p class="eyebrow">{e1}</p><h2 class="evh2">{h1}</h2><p class="evsub">{s1}</p>'
            f'<div class="evg">{"".join(card(c) for c in L["p1cards"])}</div>'
            f'<h3 style="margin:36px 0 0;font-size:24px">{L["inc_h"]}</h3><ul class="evinc">{li(L["inc"])}</ul>'
            f'<div class="evfree"><b class="t">{L["free_t"]}</b><ul>{li(L["free1"])}</ul></div>'
            f'<p class="evterms">{L["terms"]}</p></div></section>')
    sec2 = (f'<section class="band" id="by-level" style="padding-block:64px;background:var(--paper)"><div class="wrap"><p class="eyebrow">{e2}</p><h2 class="evh2">{h2}</h2><p class="evsub">{s2}</p>'
            f'<div class="evg">{"".join(card(c) for c in L["p2cards"])}</div>'
            f'<div class="evfree"><b class="t">{L["free2_t"]}</b><ul>{li(L["free2"])}</ul></div>'
            f'<div class="evsolar"><h3>{L["solar_h"]}</h3><p style="margin:0">{L["solar_p"]}</p></div>'
            f'<p class="evterms">{L["terms"]}</p></div></section>')
    return L["hero"] + "\n" + sec1 + "\n" + sec2 + "\n" + L["cta"] + "\n"

def build(L):
    src = open(L["tpl"], encoding="utf-8").read()
    head, rest = src.split("<!--/mnav-->", 1)
    foot = rest[rest.index("<footer"):]
    slug = "ev"
    base = "https://solaress.org"
    url = f"{base}/th/{slug}" if L["lang"] == "th" else f"{base}/{slug}"
    old = "quotation"
    head = re.sub(r"<title>.*?</title>", f"<title>{L['title']}</title>", head, flags=re.S)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', r"\g<1>" + L["title"], head)
    head = re.sub(r'(<meta name="twitter:title" content=")[^"]*', r"\g<1>" + L["title"], head)
    for k in ('<meta property="og:description" content="', '<meta name="description" content="', '<meta name="twitter:description" content="'):
        head = re.sub(re.escape(k) + r'[^"]*', k + L["desc"], head)
    head = re.sub(r'(<meta property="og:url" content=")[^"]*', r"\g<1>" + url + ".html", head)
    head = re.sub(r'(<meta property="og:image" content=")[^"]*', r"\g<1>" + base + "/images/ev-packages-og.jpg", head)
    head = re.sub(r'(<meta name="twitter:image" content=")[^"]*', r"\g<1>" + base + "/images/ev-packages-og.jpg", head)
    head = head.replace(f"{base}/{old}\"", f"{base}/{slug}\"").replace(f"{base}/th/{old}\"", f"{base}/th/{slug}\"").replace(f"{base}/zh/{old}\"", f"{base}/{slug}\"")
    head = head.replace('<link rel="alternate" hreflang="zh-Hans" href="https://solaress.org/ev">\n', "")
    head = head.replace("</head>", CSS + "</head>")
    head = re.sub(r'<span class="langsw">.*?</span></nav>', lambda m: m.group(0).replace('/zh/quotation.html', '/ev.html').replace('/th/quotation.html', '/th/ev.html').replace('/quotation.html', '/ev.html'), head, flags=re.S)
    open(L["out"], "w", encoding="utf-8").write(head + "<!--/mnav-->\n" + body(L) + "\n" + foot)
    print("wrote", L["out"])

if __name__ == "__main__":
    build(EN); build(TH)
