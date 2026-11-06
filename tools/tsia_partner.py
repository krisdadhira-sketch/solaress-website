# -*- coding: utf-8 -*-
"""TSIA and Installer Partner as one category: every Installer Partner is a TSIA member.
- Team pages (EN/TH/ZH), Join TSIA section: a "Two ways to join TSIA" box (Installer Partner -> /partners.html#register,
  company member -> the form below) and the Solar Test button text (<!--itl-->).
- Job pages: Solar Test button text in the hero (<!--itl-->).
- Solar ESS dropdown on every page: TSIA first, then "Installer Partners (TSIA)" indented under it.
Idempotent (markers <!--tsjoin-->, <!--itl-->). Run from the repo root after tools/job_links.py:  python3 tools/tsia_partner.py"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

JOIN = {
 "en": ("Two ways to join TSIA",
        [("Installer Partner", "Individual installers, installation teams and installation companies that take installation work. Register your team; you become a TSIA member and are listed in your region.", "/partners.html#register", "Register as TSIA Installer Partner"),
         ("Company member", "Solar companies, EPCs, electrical contractors and engineering firms. Use the application form on this page.", "#tsia-form", "Apply as company member")]),
 "th": ("สมัคร TSIA ได้ 2 แบบ",
        [("ช่างพันธมิตร (Installer Partner)", "ช่างติดตั้งรายบุคคล ทีมช่าง และบริษัทติดตั้งที่รับงานติดตั้ง ลงทะเบียนทีมของคุณ แล้วจะเป็นสมาชิก TSIA และแสดงในรายชื่อตามภูมิภาค", "/th/partners.html#register", "สมัครเป็นช่างพันธมิตร TSIA"),
         ("สมาชิกประเภทบริษัท", "บริษัทโซลาร์ EPC ผู้รับเหมาไฟฟ้า และบริษัทวิศวกรรม ใช้แบบฟอร์มสมัครในหน้านี้", "#tsia-form", "สมัครสมาชิกประเภทบริษัท")]),
 "zh": ("加入 TSIA 的两种方式",
        [("安装合作伙伴 (Installer Partner)", "承接安装工作的个人安装师傅、安装团队和安装公司。登记团队后即成为 TSIA 会员，并在所在地区列出。", "/partners.html#register", "登记为 TSIA 安装合作伙伴"),
         ("企业会员", "太阳能公司、EPC、电气承包商和工程公司，请使用本页申请表。", "#tsia-form", "申请企业会员")]),
}
TEST = {"en": "Take the Solar Test (5 levels; Level 3+ accepted for installation work)",
        "th": "ทำแบบทดสอบโซลาร์ (5 ระดับ ผ่านระดับ 3 ขึ้นไปรับงานติดตั้งได้)",
        "zh": "参加太阳能测试（5 个等级，3 级及以上可承接安装工作）"}
PARTNER_LINK = {"en": "Installer Partners (TSIA)", "th": "ทีมช่างพันธมิตร (TSIA)", "zh": "安装合作伙伴（TSIA）"}


def box(lang):
    h, items = JOIN[lang]
    cards = "".join(f'<div style="flex:1 1 220px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.18);border-radius:12px;padding:12px 14px">'
                    f'<b>{n}</b><p style="margin:6px 0 10px;font-size:14px">{d}</p><a class="btn" href="{u}">{b}</a></div>' for n, d, u, b in items)
    return f'<!--tsjoin--><div class="mediate" style="border-color:#A5B4FC"><h3>{h}</h3><div style="display:flex;flex-wrap:wrap;gap:10px">{cards}</div></div><!--/tsjoin-->'


def lang_of(s):
    m = re.search(r'<html[^>]*\blang="([a-zA-Z-]+)"', s)
    l = (m.group(1) if m else "en")[:2].lower()
    return l if l in JOIN else "en"


n = 0
for f in sorted(ROOT.rglob("*.html")):
    s = f.read_text(encoding="utf-8"); new = s; lang = lang_of(s); pre = "/th" if lang == "th" else ""
    # team pages: join box + form anchor + test button
    if 'id="join-tsia"' in new:
        new = re.sub(r"<!--tsjoin-->.*?<!--/tsjoin-->", "", new, flags=re.S)
        i = new.index('id="join-tsia"'); j = new.index('<div class="mediate">', i)
        new = new[:j] + box(lang) + new[j:]
        new = new.replace('<form name="tsia-membership" method="POST"', '<form id="tsia-form" name="tsia-membership" method="POST"', 1) if 'id="tsia-form"' not in new else new
    new = re.sub(r'(<!--itl-->.*?<a class="btn ghost" href="[^"]*installer-test\.html"[^>]*>)[^<]*(</a>)',
                 lambda m: m.group(1) + TEST[lang] + m.group(2), new, flags=re.S)
    # nav: TSIA first, partners indented under it
    if '<span class="dd end">' in new:
        i = new.index('<span class="dd end">'); j = new.index("</span></span>", i); dd = new[i:j]
        pl = re.search(r'<a href="(/(?:th/)?partners\.html)"[^>]*>[^<]*</a>', dd)
        tl = re.search(r'<a href="[^"]*team\.html#network"[^>]*>[^<]*</a>', dd)
        if pl and tl:
            part = f'<a href="{pl.group(1)}" style="padding-left:30px;font-size:.92em">{PARTNER_LINK[lang]}</a>'
            dd2 = dd.replace(pl.group(0), "", 1)
            tl2 = re.search(r'<a href="[^"]*team\.html#network"[^>]*>[^<]*</a>', dd2)
            dd2 = dd2[:tl2.end()] + part + dd2[tl2.end():]
            new = new[:i] + dd2 + new[j:]
    if new != s:
        f.write_text(new, encoding="utf-8"); n += 1
print("updated", n, "pages")
