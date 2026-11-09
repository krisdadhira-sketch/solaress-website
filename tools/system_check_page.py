# -*- coding: utf-8 -*-
"""Free System Check (Nov 2026): /system-check.html and /th/system-check.html, built on the quotation page shell.
Owners of any solar system (any brand, any installer) send monitoring screenshots; Solar ESS replies with findings.
Netlify form "system-check" (copied to the admin inbox by submission-created.mjs).
Also adds a promo band under the hero of the home pages (between <!--syscheck--> markers).
Run from the repo root:  python3 tools/system_check_page.py
then  python3 tools/projects_menu.py && python3 tools/nps_everywhere.py && python3 tools/analytics_tag.py
      && python3 tools/form_ink.py && python3 tools/accessibility.py && python3 tools/build_share.py && python3 tools/site_search.py"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import os
os.chdir(ROOT)
from service_pages import CSS as SVC_CSS, hero, section, li  # noqa: E402

FORM_CSS = """<style id="sc-css">
.scgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;margin-top:26px}
.scgrid div{border:1.5px solid var(--line);background:var(--white);padding:20px}
.scgrid b{display:block;font-size:18px;margin-bottom:6px}
.scgrid span{color:var(--mute);font-size:15px;line-height:1.5}
.scbadge{display:inline-block;background:#16A34A;color:#fff;font-weight:800;letter-spacing:.06em;padding:6px 14px;border-radius:999px;font-size:14px;margin-bottom:14px}
#check form{display:grid;gap:14px;max-width:820px;margin-top:22px}
#check form label{display:grid;gap:6px;font-weight:600;font-size:15px}
#check form input:not([type=checkbox]):not([type=radio]),#check form select,#check form textarea{font:inherit;font-size:16px;padding:12px 14px;border:1.5px solid var(--line);border-radius:8px;background:#fff;color:#0A0E2E}
#check form .row2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
#check form .chk{display:flex;gap:10px;align-items:flex-start;font-weight:400}
#check form .chk input{margin-top:4px;width:18px;height:18px}
#check .hint{font-weight:400;color:var(--mute);font-size:13.5px}
#check .files{display:grid;gap:8px;border:1.5px dashed var(--line);padding:14px;border-radius:8px}
#check button[type=submit]{justify-self:start}
@media(max-width:700px){#check form .row2{grid-template-columns:1fr}}
.scpromo{background:linear-gradient(90deg,#0B7A3E,#15803D);color:#fff}
.scpromo .wrap{display:flex;gap:18px;align-items:center;justify-content:space-between;flex-wrap:wrap;padding-block:22px}
.scpromo b{font-size:clamp(20px,2.4vw,26px);display:block}
.scpromo span{color:#DCFCE7}
.scpromo a{background:#fff;color:#0B7A3E;font-weight:800;padding:13px 22px;border-radius:999px;text-decoration:none;white-space:nowrap}
.scpromo .free{display:inline-block;background:#FACC15;color:#1E1B4B;font-weight:800;border-radius:6px;padding:2px 8px;margin-right:8px;animation:scblink 1.2s steps(2) infinite}
@keyframes scblink{50%{opacity:.35}}
</style>
"""

BRANDS = ["Solis", "Deye", "Huawei", "GoodWe", "Growatt", "SolarEdge", "Enphase", "Sungrow", "SAJ", "AlphaESS"]
PLAT = ["SolisCloud", "DeyeCloud", "Huawei FusionSolar", "SEMS (GoodWe)", "ShinePhone (Growatt)", "SolarEdge", "Enphase Enlighten", "Solarman"]

L = {
 "en": dict(
  title="Free Solar System Check – send your monitoring screenshots | Solar ESS",
  desc="Free remote check of your solar system, any brand and any installer: production, CT and meter, battery settings and zero export. Send your monitoring screenshots and Solar ESS replies with findings.",
  eyebrow="Services · Free System Check", h1="Is your solar system<br>really working? Free check.",
  lede="Send us a few screenshots from your monitoring app. Our engineers check production, the CT and meter, battery settings and zero export, and reply on LINE or by phone with what we find, usually within 3 working days. Any brand, any installer, no obligation.",
  call="Call", go="Start my free check ↓",
  wh="What we check", wsub="The six problems we find most often when we review systems on SolisCloud, DeyeCloud, FusionSolar and other platforms.",
  checks=[("Production", "kWh per kWp per day against what your roof should give: dirt, shading or a failed string show up here."),
          ("CT and meter", "Does solar + grid − export + battery match your load? A wrong CT makes the app, the battery and zero export all wrong."),
          ("Battery settings", "Battery held full and never used, reserve set too high or too low, time-of-use slots that buy from the grid."),
          ("Zero export and phases", "Solar curtailed when it could be used, or one phase buying from the grid while another exports."),
          ("Alarms and offline loggers", "Monitoring gaps, a datalogger offline for weeks, or repeating fault codes."),
          ("Sizing for your bill", "Whether more panels or a battery would actually lower your bill, based on your real daily curves.")],
  sh="How it works",
  steps=["Fill in the form below and attach 2–3 screenshots (the daily energy page, the 1-day power curve, and the battery page if you have one).",
         "Our engineers compare your data with the energy balance and what your roof should produce.",
         "We reply on LINE or by phone with our findings and the settings we suggest, usually within 3 working days.",
         "If something needs a site visit (cleaning, a CT fix, a repair), we send a quote first. You decide; there is no obligation."],
  fh="Request your free check", fsub="One free check per system. Your details are used only for this check.",
  f=dict(name="Your name", phone="Phone", line="LINE ID (optional)", prov="Province", dist="District (optional)",
         kwp="System size (kWp, if you know)", brand="Inverter brand", plat="Monitoring app", bat="Battery?", bat_o=["Yes", "No", "Not sure"],
         inst="Who installed it?", inst_o=["Solar ESS", "Another installer", "Not sure"], other="Other / not sure", choose="Choose one",
         concern="What worries you, or what should we look at?",
         files="Screenshots (optional but they help a lot)", file_hint="Daily energy page · 1-day power curve · battery page. JPG, PNG or PDF.",
         access="Or give us read-only access: add solaress as a visitor/installer on your monitoring app and tell us here (optional)",
         consent="I agree that Solar ESS may use my data and screenshots only to check my system and contact me about it.",
         send="Send for my free check", lang="EN"),
  fine="Free remote check of the data you send. Site visits, cleaning and repairs are quoted separately and only done if you agree.",
  promo_b="Free solar system check", promo_s="Send your monitoring screenshots: we tell you what is wrong and how to fix it. Any brand.", promo_go="Check my system →",
  thanks="/thanks.html"),
 "th": dict(
  title="ตรวจระบบโซลาร์ฟรี – ส่งภาพหน้าจอแอปมอนิเตอร์ของคุณ | Solar ESS",
  desc="ตรวจระบบโซลาร์เซลล์ฟรีแบบออนไลน์ ทุกยี่ห้อ ทุกผู้ติดตั้ง: การผลิตไฟ CT และมิเตอร์ ค่าตั้งแบตเตอรี่ และระบบไม่ขายไฟคืน ส่งภาพหน้าจอแอปมอนิเตอร์ แล้ววิศวกรของโซลาร์ เอสส์ ตอบกลับพร้อมข้อค้นพบ",
  eyebrow="บริการ · ตรวจระบบฟรี", h1="ระบบโซลาร์ของคุณ<br>ทำงานเต็มที่จริงไหม? ตรวจฟรี",
  lede="ส่งภาพหน้าจอจากแอปมอนิเตอร์ของคุณมาไม่กี่ภาพ วิศวกรของเราจะตรวจการผลิตไฟ CT และมิเตอร์ ค่าตั้งแบตเตอรี่ และระบบไม่ขายไฟคืน แล้วตอบกลับทาง LINE หรือโทรศัพท์ โดยปกติภายใน 3 วันทำการ ทุกยี่ห้อ ทุกผู้ติดตั้ง ไม่มีข้อผูกมัด",
  call="โทร", go="เริ่มตรวจระบบฟรี ↓",
  wh="เราตรวจอะไรบ้าง", wsub="6 ปัญหาที่เราพบบ่อยที่สุดเมื่อทบทวนระบบบน SolisCloud, DeyeCloud, FusionSolar และแพลตฟอร์มอื่น ๆ",
  checks=[("การผลิตไฟ", "หน่วยต่อ kWp ต่อวัน เทียบกับที่หลังคาของคุณควรผลิตได้ ฝุ่น เงาบัง หรือสตริงเสีย จะเห็นจากตรงนี้"),
          ("CT และมิเตอร์", "โซลาร์ + ไฟซื้อ − ไฟขาย + แบตเตอรี่ ตรงกับโหลดไหม CT ผิดทำให้แอป แบตเตอรี่ และการไม่ขายไฟคืนผิดทั้งหมด"),
          ("ค่าตั้งแบตเตอรี่", "แบตถูกค้างไว้เต็มไม่ได้ใช้ ตั้งสำรองสูงหรือต่ำเกินไป หรือช่วงเวลา TOU ที่ดึงไฟจากกริด"),
          ("ไม่ขายไฟคืนและสมดุลเฟส", "โซลาร์ถูกตัดทั้งที่ยังใช้ได้ หรือเฟสหนึ่งซื้อไฟขณะที่อีกเฟสขายไฟ"),
          ("แจ้งเตือนและดาต้าล็อกเกอร์ออฟไลน์", "ข้อมูลขาดหาย ดาต้าล็อกเกอร์ออฟไลน์นานหลายสัปดาห์ หรือรหัสผิดพลาดซ้ำ ๆ"),
          ("ขนาดระบบกับค่าไฟ", "เพิ่มแผงหรือแบตเตอรี่แล้วค่าไฟลดลงจริงไหม ดูจากกราฟการใช้ไฟจริงของคุณ")],
  sh="ขั้นตอน",
  steps=["กรอกแบบฟอร์มด้านล่าง และแนบภาพหน้าจอ 2–3 ภาพ (หน้าพลังงานรายวัน กราฟกำลังไฟ 1 วัน และหน้าแบตเตอรี่ถ้ามี)",
         "วิศวกรของเราเทียบข้อมูลของคุณกับสมดุลพลังงาน และค่าที่หลังคาของคุณควรผลิตได้",
         "เราตอบกลับทาง LINE หรือโทรศัพท์ พร้อมข้อค้นพบและค่าตั้งที่แนะนำ โดยปกติภายใน 3 วันทำการ",
         "หากต้องเข้าหน้างาน (ล้างแผง แก้ CT ซ่อม) เราเสนอราคาให้ก่อนเสมอ คุณตัดสินใจเอง ไม่มีข้อผูกมัด"],
  fh="ขอรับการตรวจระบบฟรี", fsub="ตรวจฟรี 1 ครั้งต่อ 1 ระบบ ข้อมูลของคุณใช้เพื่อการตรวจนี้เท่านั้น",
  f=dict(name="ชื่อของคุณ", phone="เบอร์โทร", line="LINE ID (ไม่บังคับ)", prov="จังหวัด", dist="อำเภอ (ไม่บังคับ)",
         kwp="ขนาดระบบ (kWp ถ้าทราบ)", brand="ยี่ห้ออินเวอร์เตอร์", plat="แอปมอนิเตอร์", bat="มีแบตเตอรี่ไหม?", bat_o=["มี", "ไม่มี", "ไม่แน่ใจ"],
         inst="ใครเป็นผู้ติดตั้ง?", inst_o=["โซลาร์ เอสส์", "ผู้ติดตั้งรายอื่น", "ไม่แน่ใจ"], other="อื่น ๆ / ไม่ทราบ", choose="เลือก",
         concern="กังวลเรื่องอะไร หรืออยากให้เราดูเรื่องไหน?",
         files="ภาพหน้าจอ (ไม่บังคับ แต่ช่วยได้มาก)", file_hint="หน้าพลังงานรายวัน · กราฟกำลังไฟ 1 วัน · หน้าแบตเตอรี่ ไฟล์ JPG, PNG หรือ PDF",
         access="หรือให้สิทธิ์ดูข้อมูลแบบอ่านอย่างเดียว: เพิ่ม solaress เป็นผู้เยี่ยมชม/ผู้ติดตั้งในแอปมอนิเตอร์ แล้วแจ้งที่นี่ (ไม่บังคับ)",
         consent="ข้าพเจ้ายินยอมให้โซลาร์ เอสส์ ใช้ข้อมูลและภาพหน้าจอเพื่อตรวจระบบของข้าพเจ้า และติดต่อกลับเรื่องนี้เท่านั้น",
         send="ส่งขอตรวจระบบฟรี", lang="TH"),
  fine="ตรวจฟรีจากข้อมูลที่คุณส่งมา การเข้าหน้างาน ล้างแผง และงานซ่อม เสนอราคาแยก และทำเมื่อคุณตกลงเท่านั้น",
  promo_b="ตรวจระบบโซลาร์ฟรี", promo_s="ส่งภาพหน้าจอแอปมอนิเตอร์ เราบอกว่าผิดตรงไหนและแก้อย่างไร ทุกยี่ห้อ", promo_go="ตรวจระบบของฉัน →",
  thanks="/th/thanks.html"),
}


def form(t):
    f = t["f"]
    opts = lambda xs: "".join(f"<option>{x}</option>" for x in xs)
    up = "".join(f'<input name="screenshot-{i}" type="file" accept="image/*,.pdf">' for i in (1, 2, 3))
    return (f'<form name="system-check" method="POST" data-netlify="true" netlify-honeypot="bot-field" enctype="multipart/form-data" action="{t["thanks"]}">'
            f'<input type="hidden" name="form-name" value="system-check"><input type="hidden" name="page-language" value="{f["lang"]}">'
            f'<p hidden><label>Leave empty <input name="bot-field"></label></p>'
            f'<div class="row2"><label>{f["name"]}<input name="name" required autocomplete="name"></label><label>{f["phone"]}<input name="phone" type="tel" required autocomplete="tel"></label></div>'
            f'<div class="row2"><label>{f["line"]}<input name="line-id"></label><label>{f["kwp"]}<input name="kwp" inputmode="decimal"></label></div>'
            f'<div class="row2"><label>{f["prov"]}<input name="province" required></label><label>{f["dist"]}<input name="district"></label></div>'
            f'<div class="row2"><label>{f["brand"]}<select name="inverter-brand"><option value="">{f["choose"]}</option>{opts(BRANDS + [f["other"]])}</select></label>'
            f'<label>{f["plat"]}<select name="monitoring-app"><option value="">{f["choose"]}</option>{opts(PLAT + [f["other"]])}</select></label></div>'
            f'<div class="row2"><label>{f["bat"]}<select name="battery"><option value="">{f["choose"]}</option>{opts(f["bat_o"])}</select></label>'
            f'<label>{f["inst"]}<select name="installed-by"><option value="">{f["choose"]}</option>{opts(f["inst_o"])}</select></label></div>'
            f'<label>{f["concern"]}<textarea name="concern" rows="4" required></textarea></label>'
            f'<div class="files"><b>{f["files"]}</b><span class="hint">{f["file_hint"]}</span>{up}</div>'
            f'<label>{f["access"]}<input name="monitoring-access"></label>'
            f'<label class="chk"><input type="checkbox" name="consent" value="yes" required><span>{f["consent"]}</span></label>'
            f'<button class="btn" type="submit">{f["send"]}</button></form>')


def body(t):
    checks = "".join(f"<div><b>{a}</b><span>{b}</span></div>" for a, b in t["checks"])
    steps = "".join(f"<li>{s}</li>" for s in t["steps"])
    return (hero(t["eyebrow"], t["h1"], t["lede"], t["call"], f'<a class="btn" href="#check" style="background:#16A34A;border-color:#16A34A">{t["go"]}</a>')
            + section(t["eyebrow"].split("·")[0].strip(), t["wh"], t["wsub"], f'<div class="scgrid">{checks}</div>')
            + section("1 → 4", t["sh"], "", f'<ol class="svsteps">{steps}</ol>', paper=True)
            + f'<section class="band light" id="check" style="padding-block:64px"><div class="wrap"><span class="scbadge">FREE · ฟรี</span>'
              f'<h2 class="svh2">{t["fh"]}</h2><p class="svsub">{t["fsub"]}</p>{form(t)}<p class="svnote">{t["fine"]}</p></div></section>')


def build(lang):
    t = L[lang]
    tpl = "th/quotation.html" if lang == "th" else "quotation.html"
    out = ROOT / ("th/system-check.html" if lang == "th" else "system-check.html")
    src = (ROOT / tpl).read_text(encoding="utf-8")
    head, rest = src.split("<!--/mnav-->", 1)
    foot = rest[rest.index("<footer"):]
    base, slug = "https://solaress.org", "system-check"
    url = f"{base}/th/{slug}" if lang == "th" else f"{base}/{slug}"
    head = re.sub(r"<title>.*?</title>", f"<title>{t['title']}</title>", head, flags=re.S)
    for k in ('<meta property="og:title" content="', '<meta name="twitter:title" content="'):
        head = re.sub(re.escape(k) + r'[^"]*', k + t["title"], head)
    for k in ('<meta property="og:description" content="', '<meta name="description" content="', '<meta name="twitter:description" content="'):
        head = re.sub(re.escape(k) + r'[^"]*', k + t["desc"], head)
    head = re.sub(r'(<meta property="og:url" content=")[^"]*', r"\g<1>" + url + ".html", head)
    for k in ('<meta property="og:image" content="', '<meta name="twitter:image" content="'):
        head = re.sub(re.escape(k) + r'[^"]*', k + base + "/images/job-pv-samui-20a.jpg", head)
    head = head.replace(f'{base}/quotation"', f'{base}/{slug}"').replace(f'{base}/th/quotation"', f'{base}/th/{slug}"')
    head = re.sub(r'<link rel="alternate" hreflang="zh-Hans"[^>]*>\n?', "", head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', "", head, flags=re.S)
    head = head.replace("</head>", SVC_CSS + FORM_CSS + "</head>", 1)
    head = re.sub(r'<span class="langsw">.*?</span></nav>', lambda m: m.group(0).replace('/zh/quotation.html', f'/{slug}.html')
                  .replace('/th/quotation.html', f'/th/{slug}.html').replace('/quotation.html', f'/{slug}.html'), head, flags=re.S)
    # drop blocks the quotation shell carries before </head> that belong to other tools (re-added by their own scripts)
    out.write_text(head + "<!--/mnav-->\n" + body(t) + "\n" + foot, encoding="utf-8")
    print("wrote", out.relative_to(ROOT))


def promo(lang, path):
    t = L[lang]
    p = ROOT / path
    s = p.read_text(encoding="utf-8")
    s = re.sub(r"<!--syscheck-->.*?<!--/syscheck-->\n?", "", s, flags=re.S)
    s = re.sub(r'<style id="sc-css">.*?</style>\n?', "", s, flags=re.S)
    s = s.replace("</head>", FORM_CSS + "</head>", 1)
    href = "/th/system-check.html" if lang == "th" else "/system-check.html"
    band = (f'<!--syscheck--><section class="scpromo"><div class="wrap"><div><b><span class="free">FREE</span>{t["promo_b"]}</b>'
            f'<span>{t["promo_s"]}</span></div><a href="{href}">{t["promo_go"]}</a></div></section><!--/syscheck-->\n')
    m = re.search(r'<main id="main"[^>]*>(?:<!--main-->)?', s)
    i = s.index("</section>", m.end()) + len("</section>")  # right after the hero
    s = s[:i] + "\n" + band + s[i:]
    p.write_text(s, encoding="utf-8")
    print("promo on", path)


if __name__ == "__main__":
    build("en"); build("th")
    promo("en", "index.html"); promo("th", "th/index.html")
