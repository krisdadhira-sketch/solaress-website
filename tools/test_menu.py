# -*- coding: utf-8 -*-
"""Test links in the Solar ESS dropdown (the last top menu, "dd end") on every page (Nov 2026: test groups, flat items):
Homeowner test, Installer Levels 1–5, Troubleshooting, Inverters, Panels & battery, Breakers, Cables.
Each opens the test page focused on that test (?test=key or ?level=1).
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


GROUPS = [  # (link query, EN, TH, ZH)
    ("?test=home-electrician", "Self-Appointed Electrician (homeowners)", "ช่างไฟประจำบ้าน (เจ้าของบ้าน)", "家庭电工（房主）"),
    ("?level=1", "Installer Levels 1–5", "ช่างติดตั้ง ระดับ 1–5", "安装工 1–5 级"),
    ("?test=solar-issues", "Solar issues & troubleshooting", "ปัญหาระบบโซลาร์และการแก้ไข", "光伏故障排查"),
    ("?test=inverter", "Inverters", "อินเวอร์เตอร์", "逆变器"),
    ("?test=pv", "Solar panels & battery", "แผงโซลาร์และแบตเตอรี่", "光伏组件与电池"),
    ("?test=breaker", "Breakers & protection", "เบรกเกอร์และอุปกรณ์ป้องกัน", "断路器与保护"),
    ("?test=cable", "Cables", "สายไฟ", "电缆"),
]


def menu(lang):
    t = L[lang]
    col = {"en": 1, "th": 2, "zh": 3}[lang]
    items = "".join(f'<a href="{t["page"]}{g[0]}">{t["top"]} · {g[col]}</a>' for g in GROUPS)
    return f'<!--tmenu-->{items}<!--/tmenu-->'


SOLAR_ESS = re.compile(r'<span class="dd end"><a href="[^"]*#services">')
n = 0
for f in sorted(ROOT.rglob("*.html")):
    if f.relative_to(ROOT).parts[0] in ("tools", "netlify", "node_modules", ".git"):
        continue
    s = f.read_text(encoding="utf-8")
    m0 = SOLAR_ESS.search(s)
    if not m0:
        continue
    m = re.search(r'<html[^>]*\blang="([a-zA-Z-]+)"', s)
    lang = (m.group(1) if m else "en").lower()[:2]
    lang = lang if lang in L else "en"
    new = re.sub(r"<!--tmenu-->.*?<!--/tmenu-->", "", s, flags=re.S)
    new = VOC.sub("", new)
    i = new.index('<span class="ddm">', SOLAR_ESS.search(new).end()) + len('<span class="ddm">')
    j = new.index("</span></span>", i)          # end of the Solar ESS dropdown list
    new = new[:j] + menu(lang) + new[j:]
    if new != s:
        f.write_text(new, encoding="utf-8"); n += 1
print("updated", n, "pages")
