"""Marketing landing pages (Nov 2026 marketing plan).

Builds, from the header/footer of th/solar-subsidy-50000.html (TH) and
solar-subsidy-50000.html (EN):
  /tax-deduction, /th/tax-deduction           200,000-baht solar tax deduction offer
  /th/solar-<province>                        Thai province landing pages
  /review                                     Google review page + QR for handover
Run:  python3 tools/marketing_pages.py && python3 tools/analytics_tag.py && python3 tools/form_ink.py
"""
import json, re, pathlib, collections, datetime, base64, io

ROOT = pathlib.Path(__file__).resolve().parent.parent
TODAY = "2026-11-16"
LINE = "https://line.me/R/ti/p/@441hmruu"
REVIEW = "https://search.google.com/local/writereview?placeid=ChIJ4bqvH18B1zARaxxYfvXqdBw"
SITE = "https://solaress.org"


def template(path):
    html = (ROOT / path).read_text(encoding="utf-8")
    head_end = html.index("</head>")
    main_s = html.index('<main id="main" tabindex="-1">')
    main_e = html.index("</main>") + len("</main>")
    return html, head_end, main_s, main_e


def strip_head(head):
    pats = [r"<title>.*?</title>", r'<meta property="og:[^"]+" content="[^"]*">', r'<meta name="twitter:card"[^>]*>',
            r'<meta name="description"[^>]*>', r'<link rel="canonical"[^>]*>', r'<link rel="alternate" hreflang[^>]*>',
            r'<script type="application/ld\+json">.*?</script>']
    for p in pats:
        head = re.sub(p, "", head, flags=re.S)
    return head


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def page(src, out, lang, title, desc, url, alts, main, ld, image="/images/news-combiner-mdb-front.jpg"):
    html, head_end, ms, me = template(src)
    head = strip_head(html[:head_end])
    meta = (f'<title>{esc(title)}</title>\n<meta name="description" content="{esc(desc)}">\n'
            f'<meta property="og:type" content="article"><meta property="og:site_name" content="Solar ESS">'
            f'<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">'
            f'<meta property="og:url" content="{SITE}{url}"><meta property="og:image" content="{SITE}{image}">'
            f'<meta property="og:locale" content="{"th_TH" if lang == "th" else "en_US"}"><meta name="twitter:card" content="summary_large_image">\n'
            f'<link rel="canonical" href="{SITE}{url}">\n')
    for hl, u in alts:
        meta += f'<link rel="alternate" hreflang="{hl}" href="{SITE}{u}">\n'
    for obj in ld:
        meta += '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>\n"
    body = html[head_end:ms] + '<main id="main" tabindex="-1"><!--main-->' + main + "<!--/main--></main>" + html[me:]
    (ROOT / out).parent.mkdir(parents=True, exist_ok=True)
    (ROOT / out).write_text(head + meta + body, encoding="utf-8")
    print("wrote", out)


def hero(crumbs, eyebrow, h1, lede):
    c = " › ".join(f'<a href="{u}">{t}</a>' for t, u in crumbs)
    return (f'<section class="dark band" style="padding-block:64px"><div class="wrap sp"><p class="crumb">{c}</p>'
            f'<p class="eyebrow">{eyebrow}</p><h1 style="font-size:clamp(34px,5.6vw,60px)">{h1}</h1>'
            f'<p class="lede" style="margin-top:18px">{lede}</p></div></section>')


def body(inner):
    return f'<section class="band light" style="padding-block:56px"><div class="wrap sp"><article style="max-width:760px">{inner}</article></div></section>'


def cta(lang):
    if lang == "th":
        return (f'<div style="margin-top:28px;display:flex;gap:12px;flex-wrap:wrap">'
                f'<a class="btn" href="{LINE}" target="_blank" rel="noopener" style="background:#06C755;color:#fff">แชท LINE @441hmruu ประเมินฟรี</a>'
                f'<a class="btn" href="/th/?free=consultation#consult">ขอใบเสนอราคาฟรี</a>'
                f'<a class="btn" href="tel:0631516694">โทร 063 151 6694</a></div>')
    return (f'<div style="margin-top:28px;display:flex;gap:12px;flex-wrap:wrap">'
            f'<a class="btn" href="{LINE}" target="_blank" rel="noopener" style="background:#06C755;color:#fff">Chat on LINE @441hmruu</a>'
            f'<a class="btn" href="/?free=consultation#consult">Free quotation</a>'
            f'<a class="btn" href="tel:0631516694">Call 063 151 6694</a></div>')


SRC_TH = '<p style="font-size:13px;margin-top:28px">ที่มา: <a href="https://www.nationthailand.com/news/policy/40063299">Nation Thailand (4 มี.ค. 2569)</a> · <a href="https://www.finnomena.com/?p=277083">Finnomena</a> · <a href="https://www.forvismazars.com/th/en/insights/doing-business-in-thailand/tax/new-energy-tax-measures-for-greener-homes">Forvis Mazars</a>. ข้อมูลทั่วไป ไม่ใช่คำแนะนำด้านภาษี กรุณาตรวจสอบกับกรมสรรพากรหรือที่ปรึกษาภาษีของท่าน</p>'
SRC_EN = '<p style="font-size:13px;margin-top:28px">Sources: <a href="https://www.nationthailand.com/news/policy/40063299">Nation Thailand (4 Mar 2026)</a> · <a href="https://www.finnomena.com/?p=277083">Finnomena</a> · <a href="https://www.forvismazars.com/th/en/insights/doing-business-in-thailand/tax/new-energy-tax-measures-for-greener-homes">Forvis Mazars</a>. General information, not tax advice; please check with the Revenue Department or your tax adviser.</p>'

RATES = [(5, "150,001–300,000"), (10, "300,001–500,000"), (15, "500,001–750,000"), (20, "750,001–1,000,000"),
         (25, "1,000,001–2,000,000"), (30, "2,000,001–5,000,000"), (35, "5,000,001+")]


def tax_pages():
    rows_th = "".join(f"<tr><td>{b}</td><td>{r}%</td><td><b>{r * 2000:,}</b></td></tr>" for r, b in RATES)
    th = (hero([("หน้าแรก", "/th/"), ("ลดหย่อนภาษีโซลาร์", "/th/tax-deduction")], "อัปเดต 16 พฤศจิกายน 2569",
               "ติดโซลาร์บ้าน<br>ลดหย่อนภาษีได้สูงสุด 200,000 บาท",
               "ใช้สิทธิได้ถึง 31 ธันวาคม 2571 สำหรับระบบออนกริดบนหลังคาบ้านไม่เกิน 10 kWp โซลาร์ เอสส์ ออกใบกำกับภาษีอิเล็กทรอนิกส์ (e-Tax Invoice) เต็มรูปแบบ และดำเนินการขออนุญาตเชื่อมต่อกับ กฟภ./กฟน. ให้ครบ")
          + body(
        '<div class="kf"><div><b>200,000 บาท</b><span>ลดหย่อนสูงสุด</span></div><div><b>10 kWp</b><span>ขนาดระบบสูงสุดต่อหลัง</span></div><div><b>31 ธ.ค. 2571</b><span>วันสุดท้ายของมาตรการ</span></div></div>'
        "<h2>เงื่อนไขหลัก</h2><ul>"
        "<li>บุคคลธรรมดา 1 คน ใช้สิทธิได้ 1 ครั้ง 1 ระบบ ในปีภาษีที่เชื่อมต่อกับระบบไฟฟ้าสำเร็จ</li>"
        "<li>ติดตั้งบนหลังคา ดาดฟ้า หรือตัวอาคารที่อยู่อาศัย ติดแบตเตอรี่ได้</li>"
        "<li>เป็นระบบออนกริด เชื่อมต่อกับ กฟภ. หรือ กฟน. ขนาดไม่เกิน 10 kWp ต่อหลัง</li>"
        "<li>ใช้ใบกำกับภาษีอิเล็กทรอนิกส์ (e-Tax Invoice) เต็มรูปแบบ</li>"
        "<li>ชื่อผู้ซื้อในใบกำกับภาษี ชื่อเจ้าของมิเตอร์ ชื่อผู้ยื่นขอเชื่อมต่อ และผู้ใช้สิทธิ ต้องเป็นคนเดียวกัน</li>"
        "<li>ระบบที่ติดตั้งก่อนมาตรการมีผล (3 มี.ค. 2569) ใช้สิทธิย้อนหลังไม่ได้</li></ul>"
        "<h2>ประหยัดภาษีได้เท่าไร</h2><p>ภาษีที่ประหยัดได้ = ค่าติดตั้งที่ใช้ลดหย่อน (ไม่เกิน 200,000 บาท) × อัตราภาษีขั้นสูงสุดของท่าน ตัวอย่างเมื่อใช้สิทธิเต็ม 200,000 บาท:</p>"
        f'<table><thead><tr><th>เงินได้สุทธิ (บาท/ปี)</th><th>อัตราภาษี</th><th>ภาษีที่ประหยัดได้ (บาท)</th></tr></thead><tbody>{rows_th}</tbody></table>'
        '<p style="font-size:13px">ตัวเลขประมาณการ ถ้าเงินได้สุทธิอยู่ใกล้ขอบขั้นภาษี ส่วนที่ประหยัดจะน้อยกว่านี้</p>'
        "<h2>โซลาร์ เอสส์ ทำอะไรให้</h2><ol>"
        "<li>ตรวจหน้างาน ดูบิลค่าไฟ และออกแบบขนาดระบบให้คุ้มที่สุดภายใน 10 kWp ฟรี</li>"
        "<li>ทำเอกสารขออนุญาตเชื่อมต่อกับ กฟภ./กฟน. ในชื่อเจ้าของมิเตอร์</li>"
        "<li>ออก e-Tax Invoice เต็มรูปแบบในชื่อเดียวกัน พร้อมใช้ยื่นภาษี</li>"
        "<li>ติดตั้ง ทดสอบ และส่งรายงานผลผลิตรายเดือนผ่านแอป</li></ol>"
        '<p>ดูราคาต่อ kWp และตัวอย่างบิลค่าไฟจริงก่อน-หลังติดตั้งได้ที่ <a href="/th/package">แพ็กเกจโซลาร์</a> สนใจโครงการ 50,000 บาท อ่าน <a href="/th/solar-subsidy-50000">สรุปโครงการโซลาร์ 50,000 บาท</a></p>'
        + cta("th") + SRC_TH))
    rows_en = "".join(f"<tr><td>{b}</td><td>{r}%</td><td><b>{r * 2000:,}</b></td></tr>" for r, b in RATES)
    en = (hero([("Home", "/"), ("Solar tax deduction", "/tax-deduction")], "Updated 16 November 2026",
               "Home solar in Thailand:<br>deduct up to 200,000 baht from income tax",
               "Open until 31 December 2028 for on-grid rooftop systems up to 10 kWp on your home. Solar ESS issues a full e-Tax Invoice and handles the PEA/MEA grid connection.")
          + body(
        '<div class="kf"><div><b>THB 200,000</b><span>maximum deduction</span></div><div><b>10 kWp</b><span>maximum system size per home</span></div><div><b>31 Dec 2028</b><span>last day of the measure</span></div></div>'
        "<h2>Main conditions</h2><ul>"
        "<li>One person, one claim, one system, in the tax year the grid connection is completed</li>"
        "<li>On the roof, rooftop or structure of a home; batteries are allowed</li>"
        "<li>On-grid, connected to PEA or MEA, up to 10 kWp per home</li>"
        "<li>Full electronic tax invoice (e-Tax Invoice)</li>"
        "<li>The buyer on the invoice, the meter owner, the grid applicant and the claimant must be the same person</li>"
        "<li>Systems installed before the measure took effect (3 Mar 2026) cannot claim</li></ul>"
        "<h2>How much tax you save</h2><p>Tax saved = deductible cost (up to THB 200,000) × your top tax rate. Using the full THB 200,000:</p>"
        f'<table><thead><tr><th>Net taxable income (THB/yr)</th><th>Tax rate</th><th>Tax saved (THB)</th></tr></thead><tbody>{rows_en}</tbody></table>'
        '<p style="font-size:13px">Estimates; near the edge of a bracket the saving is lower.</p>'
        "<h2>What Solar ESS does for you</h2><ol>"
        "<li>Free site check, bill review and a design sized for the best payback within 10 kWp</li>"
        "<li>PEA/MEA grid-connection paperwork in the meter owner's name</li>"
        "<li>A full e-Tax Invoice in the same name, ready for your tax return</li>"
        "<li>Installation, testing and monthly production reports in the app</li></ol>"
        '<p>See prices per kWp and real bills before and after on <a href="/package">Solar Package</a>.</p>'
        + cta("en") + SRC_EN))
    alts = [("th", "/th/tax-deduction"), ("en", "/tax-deduction"), ("x-default", "/tax-deduction")]
    faq_th = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": "ติดโซลาร์ลดหย่อนภาษีได้เท่าไร", "acceptedAnswer": {"@type": "Answer", "text": "ลดหย่อนตามค่าใช้จ่ายจริงสูงสุด 200,000 บาท สำหรับระบบออนกริดบนบ้านไม่เกิน 10 kWp ใช้สิทธิได้ 1 ครั้ง ระหว่าง 3 มี.ค. 2569 ถึง 31 ธ.ค. 2571"}},
        {"@type": "Question", "name": "ต้องใช้เอกสารอะไร", "acceptedAnswer": {"@type": "Answer", "text": "ใบกำกับภาษีอิเล็กทรอนิกส์ (e-Tax Invoice) เต็มรูปแบบ และชื่อผู้ซื้อ เจ้าของมิเตอร์ ผู้ขอเชื่อมต่อ และผู้ใช้สิทธิต้องเป็นคนเดียวกัน"}},
        {"@type": "Question", "name": "ติดแบตเตอรี่แล้วใช้สิทธิได้ไหม", "acceptedAnswer": {"@type": "Answer", "text": "ได้ ถ้าระบบยังเชื่อมต่อกับ กฟภ. หรือ กฟน. แบบออนกริด"}}]}
    page("th/solar-subsidy-50000.html", "th/tax-deduction.html", "th",
         "ติดโซลาร์ลดหย่อนภาษี 200,000 บาท เงื่อนไขและเอกสาร | Solar ESS",
         "ติดโซลาร์เซลล์บ้านออนกริดไม่เกิน 10 kWp ลดหย่อนภาษีได้สูงสุด 200,000 บาท ถึง 31 ธ.ค. 2571 เงื่อนไข ตัวอย่างภาษีที่ประหยัด และ e-Tax Invoice จากโซลาร์ เอสส์",
         "/th/tax-deduction", alts, th, [faq_th])
    page("solar-subsidy-50000.html", "tax-deduction.html", "en",
         "Thailand Solar Tax Deduction: up to 200,000 Baht | Solar ESS",
         "Deduct up to THB 200,000 for an on-grid home solar system up to 10 kWp in Thailand, until 31 Dec 2028. Conditions, tax saved by bracket, and how Solar ESS handles the paperwork.",
         "/tax-deduction", alts, en, [])


PROV = {  # province: (slug, Thai name, area text, office)
    "Chiang Rai": ("chiang-rai", "เชียงราย", "เมืองเชียงราย แม่สาย แม่จัน เชียงของ เวียงชัย ศรีค้ำ และทุกอำเภอ", "hq"),
    "Songkhla": ("songkhla", "สงขลา", "หาดใหญ่ คลองแห เมืองสงขลา สะเดา และทุกอำเภอ", "south"),
    "Chiang Mai": ("chiang-mai", "เชียงใหม่", "เมืองเชียงใหม่ หางดง สันกำแพง เชียงดาว แม่ริม และทุกอำเภอ", "hq"),
    "Lampang": ("lampang", "ลำปาง", "เมืองลำปาง นิคมพัฒนา และทุกอำเภอ", "hq"),
    "Lamphun": ("lamphun", "ลำพูน", "เมืองลำพูน และทุกอำเภอ", "hq"),
    "Surat Thani": ("surat-thani", "สุราษฎร์ธานี", "เกาะสมุย เมืองสุราษฎร์ธานี และทุกอำเภอ", "south"),
    "Trang": ("trang", "ตรัง", "เมืองตรัง ปะเหลียน และทุกอำเภอ", "south"),
    "Krabi": ("krabi", "กระบี่", "เมืองกระบี่ อ่าวนาง คลองท่อม และทุกอำเภอ", "krabi"),
    "Pathum Thani": ("pathum-thani", "ปทุมธานี", "คลองหลวง ธัญบุรี ลำลูกกา และทุกอำเภอ", "central"),
    "Bangkok": ("bangkok", "กรุงเทพมหานคร", "ทุกเขตในกรุงเทพฯ และปริมณฑล", "central"),
}
OFFICE = {
    "hq": "สำนักงานใหญ่: 53 หมู่ 2 ต.นางแล อ.เมืองเชียงราย จ.เชียงราย 57100 โทร 063 151 6694",
    "krabi": "สาขากระบี่: 140/2 หมู่ 4 ต.ไสไทย อ.เมืองกระบี่ จ.กระบี่ 81000 โทร 094-269-5291",
    "south": "ทีมภาคใต้ดูแลงานติดตั้งและบริการหลังการขาย สาขากระบี่โทร 094-269-5291 สำนักงานใหญ่โทร 063 151 6694",
    "central": "ทีมช่างเครือข่ายดูแลงานในพื้นที่ สำนักงานใหญ่โทร 063 151 6694",
}


def province_pages():
    d = json.load(open(ROOT / "data/plant-index.json", encoding="utf-8"))["plants"]
    cnt = collections.Counter(v["province"] for v in d.values())
    links = []
    for prov, (slug, th, area, off) in PROV.items():
        n = cnt.get(prov, 0)
        url = f"/th/solar-{slug}"
        links.append((th, url))
        main = (hero([("หน้าแรก", "/th/"), (th, url)], f"โซลาร์ เอสส์ · {th}",
                     f"ติดตั้งโซลาร์เซลล์{th}<br>บ้าน รีสอร์ท และธุรกิจ",
                     f"ออกแบบ ติดตั้ง และดูแลระบบออนกริด ไฮบริด และออฟกริดใน{th} ({area}) พร้อมงานขออนุญาต กฟภ. และใบกำกับภาษีอิเล็กทรอนิกส์เต็มรูปแบบ")
                + body(
            f'<div class="kf"><div><b>200+</b><span>ระบบโซลาร์ที่ติดตั้งแล้ว เฉลี่ย 10 kW (รวมราว 2 MWp)</span></div><div><b>{n}</b><span>ระบบใน{th}ที่ติดตามผลออนไลน์ทุกเดือน</span></div><div><b>200,000 บาท</b><span>ลดหย่อนภาษีสูงสุด</span></div></div>'
            f"<h2>ทำไมคนใน{th}เลือกโซลาร์ เอสส์</h2><ul>"
            f'<li>ติดตั้งระบบโซลาร์แล้วกว่า 200 แห่ง เฉลี่ยแห่งละ 10 kW และติดตามผลผลิตออนไลน์ใน{th}อยู่ {n} ระบบ</li>'
            "<li>รายงานผลผลิตรายเดือนและตรวจระบบผ่านแอปหลังติดตั้ง</li>"
            "<li>บิลค่าไฟจริงก่อน-หลังติดตั้ง ค่ามัธยฐานประหยัด 62% (9 ไซต์)</li>"
            "<li>ประกันภัยงานก่อสร้าง Contractor All Risk (CAR) ระหว่างติดตั้ง</li></ul>"
            "<h2>ราคาโดยประมาณ</h2><p>ระบบออนกริดไม่มีแบตเตอรี่ เริ่มประมาณ 26,000 บาท/kWp สำหรับระบบไม่เกิน 5 kWp และลดลงเหลือประมาณ 12,000 บาท/kWp สำหรับระบบ 100 kWp ขึ้นไป ราคาจริงขึ้นกับหลังคา ระยะสาย และอุปกรณ์ ดู <a href=\"/th/package\">แพ็กเกจโซลาร์</a></p>"
            "<h2>ลดหย่อนภาษีได้สูงสุด 200,000 บาท</h2><p>บ้านพักอาศัยที่ติดระบบออนกริดไม่เกิน 10 kWp ใช้สิทธิได้ถึง 31 ธ.ค. 2571 เราออก e-Tax Invoice และทำเรื่องเชื่อมต่อให้ในชื่อเดียวกัน อ่าน <a href=\"/th/tax-deduction\">เงื่อนไขลดหย่อนภาษีโซลาร์</a></p>"
            "<h2>ขั้นตอน</h2><ol><li>ส่งรูปบิลค่าไฟและหลังคาทาง LINE</li><li>ประเมินขนาดระบบและความคุ้มค่าฟรี</li><li>สำรวจหน้างานและเสนอราคา</li><li>ขออนุญาต ติดตั้ง ทดสอบ และส่งมอบ</li><li>ติดตามผลผลิตรายเดือน</li></ol>"
            f"<p>{OFFICE[off]}</p>" + cta("th")))
        ld = [{"@context": "https://schema.org", "@type": "Service", "serviceType": "ติดตั้งโซลาร์เซลล์",
               "provider": {"@type": "LocalBusiness", "name": "Solar ESS (บริษัท โซลาร์ เอสส์ จำกัด)", "url": SITE + "/th/", "telephone": "+66631516694"},
               "areaServed": {"@type": "AdministrativeArea", "name": th}, "url": SITE + url},
              {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "หน้าแรก", "item": SITE + "/th/"},
                  {"@type": "ListItem", "position": 2, "name": th, "item": SITE + url}]}]
        page("th/solar-subsidy-50000.html", f"th/solar-{slug}.html", "th",
             f"ติดตั้งโซลาร์เซลล์{th} ราคา ลดหย่อนภาษี 200,000 | Solar ESS",
             f"รับติดตั้งโซลาร์เซลล์{th} ({area}) บ้าน รีสอร์ท ธุรกิจ ออนกริด ไฮบริด ออฟกริด ติดตั้งระบบโซลาร์แล้วกว่า 200 แห่ง ประเมินฟรีทาง LINE ลดหย่อนภาษีได้สูงสุด 200,000 บาท",
             url, [("th", url)], main, ld)
    return links


def review_page():
    import qrcode
    img = qrcode.make(REVIEW, box_size=8, border=2)
    out = ROOT / "images/google-review-qr.png"
    img.save(out)
    main = (hero([("Home", "/"), ("Review", "/review")], "Thank you · ขอบคุณครับ",
                 "How did we do?<br>รีวิว Solar ESS บน Google",
                 "Your review helps other homeowners and businesses choose a trustworthy installer. It takes one minute. · รีวิวของท่านช่วยให้คนอื่นเลือกช่างที่ไว้ใจได้ ใช้เวลาเพียง 1 นาที")
            + body(f'<p style="text-align:center"><a class="btn" href="{REVIEW}" target="_blank" rel="noopener" style="font-size:20px">Write a Google review · เขียนรีวิว</a></p>'
                   '<p style="text-align:center"><img src="/images/google-review-qr.png" alt="QR code to write a Google review for Solar ESS" width="260" height="260" style="max-width:260px"></p>'
                   '<p style="text-align:center">Scan with your phone camera · สแกนด้วยกล้องมือถือ</p>'
                   "<p>Helpful things to mention: your district, system size, how the team worked on site, and your electricity bill before and after. · สิ่งที่ช่วยคนอ่าน: อำเภอ ขนาดระบบ การทำงานของทีมช่าง และค่าไฟก่อน-หลังติดตั้ง</p>"))
    page("solar-subsidy-50000.html", "review.html", "en", "Review Solar ESS on Google · รีวิว Solar ESS",
         "Leave a Google review for Solar ESS solar installation. รีวิว Solar ESS บน Google ใช้เวลา 1 นาที",
         "/review", [("en", "/review")], main, [])


def sitemap(prov_links):
    sm = ROOT / "sitemap.xml"
    s = sm.read_text(encoding="utf-8")
    urls = ["/tax-deduction", "/th/tax-deduction"] + [u for _, u in prov_links]
    add = ""
    for u in urls:
        if f"<loc>{SITE}{u}</loc>" in s:
            continue
        add += f"  <url>\n    <loc>{SITE}{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n  </url>\n"
    if add:
        s = s.replace("</urlset>", add + "</urlset>")
        sm.write_text(s, encoding="utf-8")
    print("sitemap +", add.count("<url>"))


def plants_links(prov_links):
    """Add a 'province pages' link row near the top of /th/plants."""
    p = ROOT / "th/plants.html"
    s = p.read_text(encoding="utf-8")
    s = re.sub(r"<!--provpages-->.*?<!--/provpages-->", "", s, flags=re.S)
    row = ('<!--provpages--><section class="band light" style="padding-block:24px"><div class="wrap sp"><p><b>ติดตั้งโซลาร์เซลล์รายจังหวัด:</b> '
           + " · ".join(f'<a href="{u}">{t}</a>' for t, u in prov_links)
           + ' · <a href="/th/tax-deduction">ลดหย่อนภาษี 200,000 บาท</a></p></div></section><!--/provpages-->')
    m = re.search(r'<main id="main"[^>]*>(<!--main-->)?', s)
    s = s[:m.end()] + row + s[m.end():]
    p.write_text(s, encoding="utf-8")
    print("plants links")


if __name__ == "__main__":
    tax_pages()
    links = province_pages()
    review_page()
    sitemap(links)
    plants_links(links)
