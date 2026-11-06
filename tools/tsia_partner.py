# -*- coding: utf-8 -*-
"""TSIA and Installer Partner as one category: every Installer Partner is a TSIA member.
- Team pages (EN/TH/ZH), Join TSIA section: a "Two ways to join TSIA" box (Installer Partner -> /partners.html#register,
  company member -> the form below) and the Solar Test button text (<!--itl-->).
- Job pages: Solar Test button text in the hero (<!--itl-->).
- Solar ESS dropdown on every page: one item "TSIA & Partners" (team.html#network); no separate partners link (Nov 2026).
- Team pages: "Who is TSIA, and who can be a partner?" block (domestic and global partners, <!--tswho-->) and a partner-type select on the membership form (<!--tsptype-->).
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
MENU = {"en": "TSIA &amp; Partners", "th": "TSIA และพันธมิตร", "zh": "TSIA 与合作伙伴"}

WHO = {
 "en": dict(h="Who is TSIA, and who can be a partner?",
   tsia=("Who is TSIA", "TSIA is the Thailand Solar Installer Alliance: an independent network of solar installers, electricians, engineers and clean-energy companies working across Thailand. Members share technical know-how, pass work to each other by recommendation and support each other with standards, training and legal help. Solar ESS coordinates the alliance."),
   dom=("Domestic partners · Thailand", "Anyone who installs or supports solar in Thailand.",
        ["Installer Partners: individual installers, installation teams and installation companies who take work in their region",
         "Company members: solar companies, EPCs, electrical contractors and engineering firms",
         "Every domestic partner is a TSIA member and can be listed by region"],
        [("/partners.html#register", "Register as Installer Partner"), ("#tsia-form", "Apply as company member")]),
   glo=("Global partners · outside Thailand", "Solar businesses abroad that share TSIA's standards.",
        ["Installers, EPCs and engineering firms in other countries",
         "Work together on projects abroad and in Thailand, referrals and know-how exchange",
         "Training, technical standards and quality-material sourcing"],
        [("#tsia-form", "Apply as global partner")]),
   note="Global partners: choose \u201cGlobal partner\u201d in the form and write your country where it asks for the province."),
 "th": dict(h="TSIA คือใคร และใครเป็นพันธมิตรได้บ้าง",
   tsia=("TSIA คือใคร", "TSIA คือเครือข่ายผู้ติดตั้งโซลาร์เซลล์ประเทศไทย (Thailand Solar Installer Alliance) เครือข่ายอิสระของช่างติดตั้งโซลาร์ ช่างไฟฟ้า วิศวกร และบริษัทพลังงานสะอาดทั่วประเทศ สมาชิกแบ่งปันความรู้ทางเทคนิค ส่งต่องานกันด้วยการแนะนำ และช่วยเหลือกันด้านมาตรฐาน การฝึกอบรม และกฎหมาย โดยมีโซลาร์ เอสส์ เป็นผู้ประสานงานเครือข่าย"),
   dom=("พันธมิตรในประเทศ · ประเทศไทย", "ผู้ที่ติดตั้งหรือสนับสนุนงานโซลาร์ในประเทศไทย",
        ["ช่างพันธมิตร (Installer Partner): ช่างรายบุคคล ทีมช่าง และบริษัทติดตั้งที่รับงานในพื้นที่ของตน",
         "สมาชิกประเภทบริษัท: บริษัทโซลาร์ EPC ผู้รับเหมาไฟฟ้า และบริษัทวิศวกรรม",
         "พันธมิตรในประเทศทุกรายเป็นสมาชิก TSIA และแสดงรายชื่อตามภูมิภาคได้"],
        [("/th/partners.html#register", "สมัครเป็นช่างพันธมิตร"), ("#tsia-form", "สมัครสมาชิกประเภทบริษัท")]),
   glo=("พันธมิตรต่างประเทศ · นอกประเทศไทย", "ธุรกิจโซลาร์ในต่างประเทศที่ยึดมาตรฐานเดียวกับ TSIA",
        ["ช่างติดตั้ง EPC และบริษัทวิศวกรรมในประเทศอื่น",
         "ร่วมทำโครงการทั้งในต่างประเทศและในไทย ส่งต่องาน และแลกเปลี่ยนความรู้",
         "การฝึกอบรม มาตรฐานทางเทคนิค และการจัดหาวัสดุคุณภาพ"],
        [("#tsia-form", "สมัครเป็นพันธมิตรต่างประเทศ")]),
   note="พันธมิตรต่างประเทศ: เลือก \u201cพันธมิตรต่างประเทศ\u201d ในแบบฟอร์ม และกรอกชื่อประเทศในช่องจังหวัด"),
 "zh": dict(h="TSIA 是谁？谁可以成为合作伙伴？",
   tsia=("TSIA 是谁", "TSIA 即泰国太阳能安装商联盟（Thailand Solar Installer Alliance），是由泰国各地的太阳能安装师傅、电工、工程师和清洁能源企业组成的独立网络。会员分享技术经验，通过推荐互相转介工作，并在标准、培训和法律方面互相支持。Solar ESS 负责联盟的协调工作。"),
   dom=("国内合作伙伴 · 泰国", "在泰国从事或支持太阳能安装的个人和企业。",
        ["安装合作伙伴：在本地区承接工作的个人安装师傅、安装团队和安装公司",
         "企业会员：太阳能公司、EPC、电气承包商和工程公司",
         "所有国内合作伙伴均为 TSIA 会员，可按地区列出"],
        [("/partners.html#register", "登记为安装合作伙伴"), ("#tsia-form", "申请企业会员")]),
   glo=("全球合作伙伴 · 泰国以外", "认同 TSIA 标准的海外太阳能企业。",
        ["其他国家的安装商、EPC 和工程公司",
         "在海外和泰国合作项目、转介工作、交流经验",
         "培训、技术标准和优质材料采购"],
        [("#tsia-form", "申请成为全球合作伙伴")]),
   note="全球合作伙伴：请在表格中选择“全球合作伙伴”，并在“府”一栏填写您的国家。"),
}
PTYPE = {
 "en": '<!--tsptype--><label for="t-ptype">Partner type<select id="t-ptype" name="partner-type"><option>Domestic partner (Thailand)</option><option>Global partner (outside Thailand)</option></select></label>\n<!--/tsptype-->',
 "th": '<!--tsptype--><label for="t-ptype">ประเภทพันธมิตร<select id="t-ptype" name="partner-type"><option value="Domestic partner (Thailand)">พันธมิตรในประเทศ (ประเทศไทย)</option><option value="Global partner (outside Thailand)">พันธมิตรต่างประเทศ (นอกประเทศไทย)</option></select></label>\n<!--/tsptype-->',
 "zh": '<!--tsptype--><label for="t-ptype">合作伙伴类型<select id="t-ptype" name="partner-type"><option value="Domestic partner (Thailand)">国内合作伙伴（泰国）</option><option value="Global partner (outside Thailand)">全球合作伙伴（泰国以外）</option></select></label>\n<!--/tsptype-->',
}


def who(lang, pre):
    w = WHO[lang]
    def card(t, accent):
        name, sub, items, links = t
        lis = "".join(f"<li>{x}</li>" for x in items)
        btns = "".join(f'<a class="btn" href="{u}" style="margin:4px 8px 0 0">{b}</a>' for u, b in links)
        return (f'<div style="flex:1 1 280px;background:var(--white);border:1px solid var(--line);border-top:4px solid {accent};border-radius:14px;padding:18px 20px">'
                f'<b style="font-size:19px">{name}</b><p style="margin:6px 0 8px;color:var(--mute)">{sub}</p><ul style="margin:0 0 12px;padding-left:20px;line-height:1.55">{lis}</ul>{btns}</div>')
    t, d = w["tsia"]
    return (f'<!--tswho--><div class="tsec" id="tsia-partners"><h3>{w["h"]}</h3>'
            f'<div style="background:var(--white);border:1px solid var(--line);border-radius:14px;padding:18px 20px;margin-bottom:14px"><b style="font-size:19px">{t}</b><p style="margin:6px 0 0;line-height:1.6">{d}</p></div>'
            f'<div style="display:flex;flex-wrap:wrap;gap:14px">{card(w["dom"], "#3B4BDB")}{card(w["glo"], "#7C3AED")}</div>'
            f'<p style="margin-top:10px;font-size:14px;color:var(--mute)">{w["note"]}</p></div><!--/tswho-->')


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
    # nav (Nov 2026): one item "TSIA & Partners" -> team.html#network; the separate partners link is removed
    if '<span class="dd end">' in new:
        i = new.index('<span class="dd end">'); j = new.index("</span></span>", i); dd = new[i:j]
        dd2 = re.sub(r'<a href="/(?:th/)?partners\.html"[^>]*>[^<]*</a>', "", dd)
        dd2 = re.sub(r'(<a href="[^"]*team\.html#network")[^>]*>[^<]*</a>', lambda m: m.group(1) + ">" + MENU[lang] + "</a>", dd2, count=1)
        new = new[:i] + dd2 + new[j:]
    # team pages: "Who is TSIA / who can be a partner" block before the Apply button of the TSIA section
    if 'id="network"' in new:
        new = re.sub(r"<!--tswho-->.*?<!--/tswho-->", "", new, flags=re.S)
        i = new.index('id="network"'); k = new.index('<div style="margin-top:22px"><a class="btn" href="#join-tsia">', i)
        new = new[:k] + who(lang, pre) + new[k:]
    # membership form: partner type (domestic / global)
    if 'name="tsia-membership"' in new:
        new = re.sub(r"<!--tsptype-->.*?<!--/tsptype-->", "", new, flags=re.S)
        i = new.index('name="tsia-membership"'); k = new.index('<label for="t-org">', i)
        new = new[:k] + PTYPE[lang] + new[k:]
    if new != s:
        f.write_text(new, encoding="utf-8"); n += 1
print("updated", n, "pages")
