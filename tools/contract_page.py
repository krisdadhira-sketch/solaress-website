# -*- coding: utf-8 -*-
"""Installer hiring contract pages (/contract.html EN, /th/contract.html TH), Nov 2026.
Read-only: candidates can read the contract here; there is NO download. Solar ESS sends the PDF only after the
price is agreed (the master copy is the Claude Docs "Installer Hiring Contract – Solar ESS"). Text: tools/contract/en.md, th.md.
Page shell is taken from statement.html / th/statement.html. Run:  python3 tools/contract_page.py
then python3 tools/analytics_tag.py, tools/form_ink.py, tools/accessibility.py"""
import re
from pathlib import Path
import markdown

ROOT = Path(__file__).resolve().parents[1]
T = {
    "en": dict(src=ROOT / "statement.html", out=ROOT / "contract.html", md=ROOT / "tools/contract/en.md", other="/th/contract.html", olang="th",
               title="Installer Hiring Contract – Solar ESS Co. Ltd.",
               desc="Read the Solar ESS installer hiring contract: parties, job scope, responsibilities, payment, breach and warranty terms.",
               eyebrow="Solar ESS · Job Platform", h1="Installer Hiring Contract",
               lede="The contract every qualified installer signs with Solar ESS. Read it before you apply.",
               lock=("<b>Read only.</b> This contract cannot be downloaded here. When your application is selected and the price is agreed, "
                     "Solar ESS fills in your details and the job, and sends you the contract to sign."),
               back='<a class="btn" href="/job.html#apply">Back to the jobs and apply</a>'),
    "th": dict(src=ROOT / "th/statement.html", out=ROOT / "th/contract.html", md=ROOT / "tools/contract/th.md", other="/contract.html", olang="en",
               title="สัญญาจ้างช่างติดตั้ง – บริษัท โซลาร์ เอสส์ จำกัด",
               desc="อ่านสัญญาจ้างช่างติดตั้งของ Solar ESS: คู่สัญญา ขอบเขตงาน ความรับผิดชอบ การชำระเงิน การผิดสัญญา และการรับประกันผลงาน",
               eyebrow="Solar ESS · แพลตฟอร์มงาน", h1="สัญญาจ้างช่างติดตั้ง",
               lede="สัญญาที่ช่างที่ผ่านการคัดเลือกทุกคนลงนามกับ Solar ESS กรุณาอ่านก่อนสมัครงาน",
               lock=("<b>อ่านได้อย่างเดียว</b> ไม่สามารถดาวน์โหลดสัญญาจากหน้านี้ได้ เมื่อใบสมัครของคุณได้รับการคัดเลือกและตกลงราคากันเรียบร้อยแล้ว "
                     "Solar ESS จะกรอกข้อมูลของคุณและรายละเอียดงาน แล้วส่งสัญญาให้คุณลงนาม"),
               back='<a class="btn" href="/th/job.html#apply">กลับไปหน้างานและสมัคร</a>'),
}
CSS = ("<style id=\"contract-css\">.ct article{max-width:860px}.ct table{width:100%;border-collapse:collapse;margin:12px 0 18px;font-size:15px}"
       ".ct th,.ct td{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}.ct th{background:rgba(91,91,214,.08)}"
       ".ct h2{font-size:22px;margin-top:30px}.ct ol,.ct ul{padding-left:22px;line-height:1.6}.ct li{margin:4px 0}"
       ".ct .lock{border:1.5px solid #5B5BD6;border-radius:12px;padding:14px 16px;background:rgba(91,91,214,.07);margin:0 0 22px}"
       "@media print{.ct{display:none}}</style>")

for lang, t in T.items():
    s = t["src"].read_text(encoding="utf-8")
    head, rest = s.split("</head>", 1)
    head = re.sub(r"<title>[^<]*</title>", f"<title>{t['title']}</title>", head)
    head = re.sub(r'(<meta (?:name="description"|property="og:description"|name="twitter:description") content=")[^"]*"', lambda m: m.group(1) + t["desc"] + '"', head)
    head = re.sub(r'(<meta (?:property="og:title"|name="twitter:title") content=")[^"]*"', lambda m: m.group(1) + t["title"] + '"', head)
    head = head.replace("/statement", "/contract")
    if 'id="contract-css"' not in head:
        head += CSS
    body = markdown.markdown(t["md"].read_text(encoding="utf-8"), extensions=["tables"])
    main = (f'<main id="main" tabindex="-1"><!--main--><section class="dark band" style="padding-block:64px"><div class="wrap">'
            f'<p class="eyebrow">{t["eyebrow"]}</p><h1 style="font-size:clamp(36px,6vw,60px)">{t["h1"]}</h1>'
            f'<p class="lede" style="margin-top:18px">{t["lede"]}</p></div></section>'
            f'<section class="band light ct"><div class="wrap"><article><p class="lock">{t["lock"]}</p>{body}'
            f'<p style="margin-top:28px">{t["back"]}</p></article></div></section>\n<!--/main--></main>')
    rest = re.sub(r'<main id="main".*?</main>', lambda m: main, rest, count=1, flags=re.S)
    rest = re.sub(r'href="[^"]*"( lang="' + t["olang"] + '")', lambda m: f'href="{t["other"]}"' + m.group(1), rest, count=1)
    t["out"].write_text(head + "</head>" + rest, encoding="utf-8")
    print("wrote", t["out"].relative_to(ROOT))
