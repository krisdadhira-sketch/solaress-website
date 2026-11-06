# -*- coding: utf-8 -*-
"""Add "Solar Test" (Level 1–5 installer test) to the end of the Solar ESS dropdown
(<span class="dd end">) on every page, replacing the old standalone vocabulary link.
Idempotent (markers <!--tmenu-->...<!--/tmenu-->). Run from the repo root:  python3 tools/test_menu.py"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LV = [("Solar Enterer", "ผู้เริ่มต้นเข้าสู่โซลาร์"), ("Solar Enthusiast", "ผู้สนใจโซลาร์"), ("Solar in Practice", "ผู้ปฏิบัติงานโซลาร์"),
      ("Solar Professional", "มืออาชีพด้านโซลาร์"), ("Solar Expert", "ผู้เชี่ยวชาญด้านโซลาร์")]
L = {"en": dict(top="Solar Test", lv="Level", mine="My levels & certificates", voc="Vocabulary test", page="/installer-test.html"),
     "th": dict(top="แบบทดสอบโซลาร์", lv="ระดับ", mine="ระดับและใบประกาศของฉัน", voc="แบบทดสอบคำศัพท์", page="/th/installer-test.html"),
     "zh": dict(top="太阳能测试", lv="等级", mine="我的等级与证书", voc="词汇测试", page="/installer-test.html")}
VOC = re.compile(r'<a href="/vocabulary\.html">(?:Solar ESS Test|แบบทดสอบ Solar ESS|Solar ESS 测试)</a>')


def menu(lang):
    """Items appended to the Solar ESS dropdown: Solar Test and its 5 levels (indented). The vocabulary test is not in the menu (Nov 2026); share www.solaress.org/vocabulary.html directly."""
    t = L[lang]
    items = "".join(f'<a href="{t["page"]}?level={i}" style="padding-left:30px;font-size:.92em">{t["lv"]} {i} · {(th if lang == "th" else en)}</a>' for i, (en, th) in enumerate(LV, 1))
    return (f'<!--tmenu--><a href="{t["page"]}" style="border-top:1px solid rgba(255,255,255,.15)">{t["top"]} ▸</a>{items}'
            f'<!--/tmenu-->')


n = 0
for f in sorted(ROOT.rglob("*.html")):
    s = f.read_text(encoding="utf-8")
    if '<span class="dd end">' not in s:
        continue
    m = re.search(r'<html[^>]*\blang="([a-zA-Z-]+)"', s)
    lang = (m.group(1) if m else "en").lower()[:2]
    lang = lang if lang in L else "en"
    new = re.sub(r"<!--tmenu-->.*?<!--/tmenu-->", "", s, flags=re.S)
    new = VOC.sub("", new)
    i = new.index('<span class="dd end">')
    j = new.index("</span></span>", i)          # end of the Solar ESS dropdown list
    new = new[:j] + menu(lang) + new[j:]
    if new != s:
        f.write_text(new, encoding="utf-8"); n += 1
print("updated", n, "pages")
