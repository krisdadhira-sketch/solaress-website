# -*- coding: utf-8 -*-
"""Jobs page apply form (EN /job.html, TH /th/job.html): job picker and job proposal box. Idempotent.
- Job picker: a filter box + the "Position or project job" list (built live from the open job posts by
  /js/job-apply.js; the static <option>s stay as a fallback and for tools/feedback_page.py) + a box showing the
  chosen job's location with a link back to the post. Hidden field job-id carries the post id.
- Job proposal box (project jobs only): Price 1 labour only, Price 2 labour + materials, the proposal itself,
  earliest start date and days on site. Hidden quoted-price keeps the old single field filled for the inbox.
Run:  python3 tools/job_apply_box.py   (then tools/form_ink.py and tools/accessibility.py)"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
T = {
    "en": dict(
        find="Type to filter: province, district or type of work (e.g. Chiang Rai, cleaning, battery)",
        count="open jobs",
        legend="Your job proposal",
        intro="Read the job details carefully and quote for exactly that scope. Give both prices; we compare proposals, not only prices.",
        p1="Price 1: labour only (THB)", p2="Price 2: labour and materials (THB)",
        prop="Your proposal: how you will do the job: scope, method, materials (brand and size), team size",
        prop_ph="e.g. 2 technicians + 1 helper. Mount 24 panels on the existing rails, DC cable 6 mm² in conduit, Solis 16 kW inverter on the battery wall, AC breaker 63 A, test and commission with the owner…",
        start="Earliest start date", days="Days needed on site"),
    "th": dict(
        find="พิมพ์เพื่อค้นหา: จังหวัด อำเภอ หรือประเภทงาน (เช่น เชียงราย ล้างแผง แบตเตอรี่)",
        count="งานที่เปิดรับ",
        legend="ข้อเสนองานของคุณ",
        intro="อ่านรายละเอียดงานให้ครบ และเสนอราคาตามขอบเขตงานนั้น ให้ราคาทั้ง 2 แบบ เราพิจารณาข้อเสนอโดยรวม ไม่ใช่เฉพาะราคา",
        p1="ราคาที่ 1: ค่าแรงอย่างเดียว (บาท)", p2="ราคาที่ 2: ค่าแรงและวัสดุ (บาท)",
        prop="ข้อเสนอของคุณ: วิธีทำงาน ขอบเขตงาน วัสดุ (ยี่ห้อและขนาด) จำนวนทีมงาน",
        prop_ph="เช่น ช่าง 2 คน + ผู้ช่วย 1 คน ติดตั้งแผง 24 แผงบนรางเดิม สาย DC 6 ตร.มม. ร้อยท่อ ติดตั้งอินเวอร์เตอร์บนผนังแบตเตอรี่ เบรกเกอร์ AC 63 A ทดสอบและส่งมอบระบบกับเจ้าของ…",
        start="วันที่เริ่มงานได้เร็วที่สุด", days="จำนวนวันที่ใช้ทำงานหน้างาน"),
}

CSS = """<style id="japply-css">
.jpick{display:grid;gap:8px;padding:14px;border:1.5px solid rgba(165,180,252,.55);border-radius:12px;background:rgba(91,91,214,.12)}
.jpick>label{margin:0}
.jpick .jcount{font-family:var(--mono);font-size:11.5px;letter-spacing:.08em;color:#C7D2FE}
.jpick select{appearance:none;-webkit-appearance:none;background:#fff url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='9' viewBox='0 0 14 9'%3E%3Cpath d='M1 1l6 6 6-6' fill='none' stroke='%230A1230' stroke-width='2'/%3E%3C/svg%3E") no-repeat right 14px center!important;padding-right:40px!important;cursor:pointer;font-size:15px}
.jpick select optgroup{font-weight:700;color:#4338CA}
.jpick select option{color:#0A0E2E;font-weight:400}
.jinfo{display:grid;gap:3px;background:#fff;color:#0A1230;border-radius:10px;padding:10px 14px;font-size:14.5px;line-height:1.45}
.jinfo span{color:#3E548E}.jinfo a{color:#4338CA;font-weight:600;font-size:13.5px}
.jprop{border:1.5px solid rgba(165,180,252,.55);border-radius:12px;padding:14px 14px 6px;margin:6px 0 4px;display:grid;gap:10px;background:rgba(91,91,214,.10)}
.jprop legend{padding:0 8px;font-weight:700;color:#C7D2FE!important;font-size:16px}
.jprop .fine{margin:0}
.jp2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
@media(max-width:560px){.jp2{grid-template-columns:1fr}}
.apply>form,.jpick,.jprop,.jp2>label,.jpick>*{min-width:0;max-width:100%}
.jpick select,.jpick input,.jprop input,.jprop textarea{width:100%;min-width:0;box-sizing:border-box;text-overflow:ellipsis}
.jinfo b,.jinfo span{overflow-wrap:anywhere}
</style>"""


def pick_html(t, label, select):
    return (f'<!--jpick--><div class="jpick"><label for="j-role">{label}</label>'
            f'<span class="jcount"><span id="j-count"></span></span>'
            f'<input id="j-find" type="search" autocomplete="off" placeholder="{t["find"]}" aria-label="{t["find"]}" aria-controls="j-role">'
            f'{select}<div id="j-info" class="jinfo" aria-live="polite" hidden></div>'
            f'<input type="hidden" name="job-id" id="j-id"></div><!--/jpick-->')


def prop_html(t):
    return (f'<!--jprop--><fieldset class="jprop" id="j-prop"><legend>{t["legend"]}</legend><p class="fine">{t["intro"]}</p>'
            f'<div class="jp2"><label for="j-p1">{t["p1"]}<input id="j-p1" name="price-labour-only" inputmode="numeric" required data-req></label>'
            f'<label for="j-p2">{t["p2"]}<input id="j-p2" name="price-labour-materials" inputmode="numeric" required data-req></label></div>'
            f'<label for="j-proposal">{t["prop"]}<textarea id="j-proposal" name="proposal" rows="5" required data-req placeholder="{t["prop_ph"]}"></textarea></label>'
            f'<div class="jp2"><label for="j-start">{t["start"]}<input id="j-start" name="start-date" type="date"></label>'
            f'<label for="j-days">{t["days"]}<input id="j-days" name="days-needed" inputmode="numeric"></label></div>'
            f'<input type="hidden" name="quoted-price" id="j-price"><input type="hidden" name="price-includes-materials" value="Both options quoted">'
            f'</fieldset><!--/jprop-->')


for lg, path in (("en", "job.html"), ("th", "th/job.html")):
    p = ROOT / path
    s = p.read_text(encoding="utf-8")
    t = T[lg]
    # job picker
    if "<!--jpick-->" in s:
        m = re.search(r"<!--jpick-->.*?<!--/jpick-->", s, re.S)
        sel = re.search(r'<select id="j-role".*?</select>', m.group(0), re.S).group(0)
        lab = re.search(r'<label for="j-role">(.*?)</label>', m.group(0), re.S).group(1)
        s = s[: m.start()] + pick_html(t, lab, sel) + s[m.end():]
    else:
        m = re.search(r'<label for="j-role">(.*?)(<select id="j-role".*?</select>)</label>', s, re.S)
        s = s[: m.start()] + pick_html(t, m.group(1), m.group(2)) + s[m.end():]
    # proposal box (replaces the single price + "includes materials" fields)
    if "<!--jprop-->" in s:
        s = re.sub(r"<!--jprop-->.*?<!--/jprop-->", lambda _: prop_html(t), s, flags=re.S)
    else:
        m1 = re.search(r'<label for="j-price">.*?</label>\s*<label for="j-mat">.*?</select></label>', s, re.S)
        s = s[: m1.start()] + prop_html(t) + s[m1.end():]
    s = re.sub(r'<style id="japply-css">.*?</style>', "", s, flags=re.S)
    s = s.replace("</head>", CSS + "</head>", 1)
    s = re.sub(r'<script src="/js/job-apply\.js[^"]*" defer></script>', "", s)
    s = s.replace("</body>", '<script src="/js/job-apply.js?v=1" defer></script></body>', 1)
    p.write_text(s, encoding="utf-8")
    print("updated", path)
