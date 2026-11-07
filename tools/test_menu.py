# -*- coding: utf-8 -*-
"""Add "Solar Test" (Level 1–5 installer test) to the end of the Services dropdown
(the dropdown whose top link ends in "#projects") on every page, replacing the old standalone vocabulary link.
Moved from the Solar ESS dropdown to Services in Nov 2026.
Idempotent (markers <!--tmenu-->...<!--/tmenu-->). Run from the repo root:  python3 tools/test_menu.py"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LV = [("Solar Enterer", "ผู้เริ่มต้นเข้าสู่โซลาร์"), ("Solar Enthusiast", "ผู้สนใจโซลาร์"), ("Solar in Practice", "ผู้ปฏิบัติงานโซลาร์"),
      ("Solar Professional", "มืออาชีพด้านโซลาร์"), ("Solar Expert", "ผู้เชี่ยวชาญด้านโซลาร์")]
PR = [("inverter", "Inverters", "อินเวอร์เตอร์", "逆变器"), ("inverter-solis", "Inverters · Solis", "อินเวอร์เตอร์ · Solis", "逆变器 · Solis"),
      ("inverter-deye", "Inverters · Deye", "อินเวอร์เตอร์ · Deye", "逆变器 · Deye"), ("inverter-goodwe", "Inverters · GoodWe", "อินเวอร์เตอร์ · GoodWe", "逆变器 · GoodWe"),
      ("pv", "PV Modules", "แผงโซลาร์เซลล์", "光伏组件"), ("battery", "Battery", "แบตเตอรี่", "电池"),
      ("breaker", "Breakers & Protection", "เบรกเกอร์และอุปกรณ์ป้องกัน", "断路器与保护"), ("cable", "Cables & Wiring", "สายไฟและการเดินสาย", "电缆与布线")]
PH = {"en": "Brand & Product Test", "th": "แบบทดสอบแบรนด์และผลิตภัณฑ์", "zh": "品牌与产品测试"}
L = {"en": dict(top="Test", lv="Level", mine="My levels & certificates", voc="Vocabulary test", page="/installer-test.html"),
     "th": dict(top="แบบทดสอบ", lv="ระดับ", mine="ระดับและใบประกาศของฉัน", voc="แบบทดสอบคำศัพท์", page="/th/installer-test.html"),
     "zh": dict(top="测试", lv="等级", mine="我的等级与证书", voc="词汇测试", page="/installer-test.html")}
VOC = re.compile(r'<a href="/vocabulary\.html">(?:Solar ESS Test|แบบทดสอบ Solar ESS|Solar ESS 测试)</a>')


def menu(lang):
    """Items appended to the Solar ESS dropdown: Solar Test and its 5 levels (indented). The vocabulary test is not in the menu (Nov 2026); share www.solaress.org/vocabulary.html directly."""
    t = L[lang]
    items = "".join(f'<a href="{t["page"]}?level={i}">{t["lv"]} {i} · {(th if lang == "th" else en)}</a>' for i, (en, th) in enumerate(LV, 1))
    col = {"en": 1, "th": 2, "zh": 3}[lang]
    prod = "".join(f'<a href="{t["page"]}?test={p[0]}">{p[col]}</a>' for p in PR)
    # Nov 2026: one "Test" item only; levels and brand/product tests are picked on the test page itself.
    return f'<!--tmenu--><a href="{t["page"]}">{t["top"]}</a><!--/tmenu-->'


n = 0
for f in sorted(ROOT.rglob("*.html")):
    s = f.read_text(encoding="utf-8")
    svc = re.search(r'<span class="dd"><a href="[^"]*#projects">[^<]*</a><span class="ddm">', s)
    if not svc:
        continue
    m = re.search(r'<html[^>]*\blang="([a-zA-Z-]+)"', s)
    lang = (m.group(1) if m else "en").lower()[:2]
    lang = lang if lang in L else "en"
    new = re.sub(r"<!--tmenu-->.*?<!--/tmenu-->", "", s, flags=re.S)
    new = VOC.sub("", new)
    i = re.search(r'<span class="dd"><a href="[^"]*#projects">[^<]*</a><span class="ddm">', new).end()
    j = new.index("</span></span>", i)          # end of the Services dropdown list
    new = new[:j] + menu(lang) + new[j:]
    if new != s:
        f.write_text(new, encoding="utf-8"); n += 1
print("updated", n, "pages")
