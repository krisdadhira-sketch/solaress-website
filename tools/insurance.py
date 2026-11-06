# -*- coding: utf-8 -*-
"""All Risks insurance (Erection All Risks, EAR open cover, Dhipaya Insurance, 16 Oct 2026 - 16 Oct 2027).
1) Profile pages (EN/TH/ZH): section id="insurance" before the "03 — Fleet" section  (<!--ins--> markers).
2) Every page: blinking shield badge on the top "Solar ESS" menu link and an "All Risks Insured" item in its dropdown
   (<!--insm-->, <!--insdot--> markers, CSS <style id="ins-css">).
Policy certificate is furnished on request: never publish the policy PDF or the policy number.
Idempotent. Run from the repo root:  python3 tools/insurance.py   then  python3 tools/analytics_tag.py"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CSS = ('<style id="ins-css">@keyframes insblink{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.25;transform:scale(.8)}}'
       '.ins-dot{display:inline-flex;align-items:center;justify-content:center;width:16px;height:16px;margin-left:5px;vertical-align:-3px;animation:insblink 1.2s ease-in-out infinite}'
       '.ins-dot svg{width:16px;height:16px}.ddm a.ins-m{display:flex!important;align-items:center;gap:6px;color:#FDE68A!important;font-weight:700}'
       '.ddm a.ins-m .ins-dot{margin-left:0}'
       '@media (prefers-reduced-motion:reduce){.ins-dot{animation:none}}'
       '.ins-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:28px}@media(max-width:860px){.ins-grid{grid-template-columns:1fr}}'
       '.ins-card{border:1px solid var(--line);background:var(--white);padding:20px;display:flex;gap:14px}.ins-card h3{margin:0 0 6px;font-size:17px}.ins-card p{margin:0;font-size:14.5px;line-height:1.55;opacity:.88}'
       '.ins-ic{flex:none;width:44px;height:44px;border-radius:12px;background:var(--navy);display:flex;align-items:center;justify-content:center}'
       '.ins-hero{display:flex;gap:20px;align-items:center;flex-wrap:wrap}.ins-shield{flex:none;width:84px;height:84px;border-radius:20px;background:linear-gradient(135deg,#0A1230,#4F46E5);display:flex;align-items:center;justify-content:center;box-shadow:0 10px 30px rgba(79,70,229,.35)}'
       '.ins-why{margin-top:26px;background:var(--navy);color:#fff;padding:22px 24px;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}@media(max-width:860px){.ins-why{grid-template-columns:1fr}}'
       '.ins-why h3{margin:0 0 6px;font-size:18px;color:#C7D2FE}.ins-why p{margin:0;font-size:15px;line-height:1.55}'
       '.ins-note{margin-top:16px;font-size:13.5px;color:var(--mute)}</style>')

SHIELD = '<svg viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l8 3v6c0 5-3.4 9.3-8 11-4.6-1.7-8-6-8-11V5z"/><path d="M8.5 12l2.5 2.5 4.5-5"/></svg>'
ICONS = {
 "works": '<path d="M3 21h18"/><path d="M5 21V10l7-5 7 5v11"/><path d="M9 21v-6h6v6"/>',
 "tp": '<circle cx="9" cy="7" r="3"/><path d="M3 21v-1a6 6 0 0 1 12 0v1"/><path d="M16 11l2 2 4-4"/>',
 "prop": '<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M12 14v3"/>',
 "emp": '<path d="M12 2l8 3v6c0 5-3.4 9.3-8 11-4.6-1.7-8-6-8-11V5z"/><circle cx="12" cy="10" r="2.5"/><path d="M8 16a4 4 0 0 1 8 0"/>',
 "map": '<path d="M9 3L3 6v15l6-3 6 3 6-3V3l-6 3z"/><path d="M9 3v15M15 6v15"/>',
 "fire": '<path d="M12 22c4 0 7-3 7-7 0-3-2-5-3-7-1 2-2 3-4 3 0-3-1-6-3-9-1 4-4 7-4 11 0 5 3 9 7 9z"/>',
}
def ic(k):
    return f'<div class="ins-ic"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONS[k]}</svg></div>'

T = {
 "en": dict(
  menu="Contractor All Risk (CAR)", pre="",
  eyebrow="Insured · Contractor All Risk (CAR)", h2="Every installation insured: all risks, anywhere in Thailand.",
  lede="Solar ESS is insured under Contractor All Risk (CAR) insurance with Dhipaya Insurance Public Company Limited: an open cover for all our solar rooftop installation projects anywhere in Thailand, so domestic and international employers can hand over their site with confidence. The policy is issued in the erection form (Erection All Risks, EAR), the CAR cover used for installation work.",
  cards=[("works", "All risks on the works", "Accidental loss or damage to the installation and materials during construction, one week of testing and a 12-month maintenance period. Contract works up to 5 million baht per contract."),
         ("tp", "Third-party liability", "Injury to people or damage to property of others caused by the work: up to 1,000,000 baht per accident and per project, 2,000,000 baht in the policy year. No excess for injury or death."),
         ("prop", "Your existing building", "Damage to the employer's existing building or property caused by our work: up to 1,000,000 baht per accident and per project, 2,000,000 baht in the policy year."),
         ("emp", "Employers protected too", "The employer can be named as an insured together with Solar ESS, our subcontractors and consulting engineers, with cross liability, waiver of subrogation, and the employer's staff covered as third parties."),
         ("map", "Nationwide, renewed every year", "Any solar rooftop site in Thailand (airside and offshore areas excepted). Current policy period: 16 October 2026 to 16 October 2027."),
         ("fire", "Extra extensions", "Fire-fighting expenses, debris removal, 20% escalation of the insured value and automatic reinstatement of the sum insured.")],
  why=[("For international employers", "Factories, hotels, developers and overseas head offices often require contractor's all-risks insurance before work can start. Ours is already in place and can be endorsed for your project."),
       ("For homeowners and Thai businesses", "The same protection on every job: if an accident happens on site, the insurance is there for your building, your neighbours and our work.")],
  note="Policy certificate and project endorsement furnished upon request or upon signing of contract. Cover is subject to the policy terms, conditions and exclusions.",
  cta="Ask for the insurance certificate", consult="/#consult"),
 "th": dict(
  menu="ประกันภัย CAR ทุกความเสี่ยง", pre="/th",
  eyebrow="มีประกันภัย · Contractor All Risk (CAR)", h2="ทุกงานติดตั้งมีประกันภัยทุกความเสี่ยง ทั่วประเทศไทย",
  lede="โซลาร์ เอสส์ มีประกันภัยความเสี่ยงภัยทุกชนิดของผู้รับเหมา (Contractor All Risk: CAR) กับ บริษัท ทิพยประกันภัย จำกัด (มหาชน) แบบ Open Cover คุ้มครองงานติดตั้งโซลาร์บนหลังคาของเราทุกที่ในประเทศไทย ผู้ว่าจ้างทั้งในประเทศและต่างประเทศจึงมอบหน้างานให้เราได้อย่างมั่นใจ กรมธรรม์ออกในรูปแบบงานติดตั้ง (Erection All Risks: EAR) ซึ่งเป็นประกัน CAR สำหรับงานติดตั้ง",
  cards=[("works", "คุ้มครองทุกความเสี่ยงของงาน", "ความเสียหายหรือสูญหายจากอุบัติเหตุต่องานติดตั้งและวัสดุ ระหว่างก่อสร้าง ช่วงทดสอบ 1 สัปดาห์ และระยะบำรุงรักษา 12 เดือน มูลค่างานไม่เกิน 5 ล้านบาทต่อสัญญา"),
         ("tp", "ความรับผิดต่อบุคคลภายนอก", "การบาดเจ็บของบุคคลอื่นหรือความเสียหายต่อทรัพย์สินของผู้อื่นที่เกิดจากการทำงาน ไม่เกิน 1,000,000 บาทต่ออุบัติเหตุและต่อโครงการ และ 2,000,000 บาทตลอดปีกรมธรรม์ ไม่มีความเสียหายส่วนแรกกรณีบาดเจ็บหรือเสียชีวิต"),
         ("prop", "ทรัพย์สินเดิมของผู้ว่าจ้าง", "ความเสียหายต่ออาคารหรือทรัพย์สินเดิมของผู้ว่าจ้างที่เกิดจากการทำงานของเรา ไม่เกิน 1,000,000 บาทต่ออุบัติเหตุและต่อโครงการ และ 2,000,000 บาทตลอดปีกรมธรรม์"),
         ("emp", "คุ้มครองผู้ว่าจ้างด้วย", "ระบุผู้ว่าจ้างเป็นผู้เอาประกันภัยร่วมกับโซลาร์ เอสส์ ผู้รับเหมาช่วง และบริษัทวิศวกรที่ปรึกษาได้ พร้อมเงื่อนไขความรับผิดต่อกันระหว่างผู้เอาประกันภัย การสละสิทธิ์เรียกร้องค่าเสียหายซึ่งกันและกัน และคุ้มครองพนักงานของผู้ว่าจ้างเสมือนบุคคลภายนอก"),
         ("map", "ทั่วประเทศ ต่ออายุทุกปี", "ทุกหน้างานติดตั้งโซลาร์บนหลังคาในประเทศไทย (ยกเว้นพื้นที่ให้บริการทางอากาศยานและพื้นที่นอกชายฝั่ง) ระยะเวลากรมธรรม์ปัจจุบัน 16 ตุลาคม 2569 ถึง 16 ตุลาคม 2570"),
         ("fire", "ความคุ้มครองเพิ่มเติม", "ค่าใช้จ่ายในการดับเพลิง ค่าขนย้ายซากทรัพย์สิน การเพิ่มขึ้นของมูลค่าทรัพย์สิน 20% และการคงไว้ซึ่งจำนวนเงินเอาประกันภัย")],
  why=[("สำหรับผู้ว่าจ้างต่างประเทศ", "โรงงาน โรงแรม ผู้พัฒนาโครงการ และสำนักงานใหญ่ในต่างประเทศ มักกำหนดให้ผู้รับเหมาต้องมีประกันภัยทุกความเสี่ยงก่อนเริ่มงาน เรามีกรมธรรม์พร้อมแล้ว และออกเอกสารแนบท้ายสำหรับโครงการของท่านได้"),
       ("สำหรับบ้านและธุรกิจในประเทศ", "ทุกงานได้รับความคุ้มครองเหมือนกัน หากเกิดอุบัติเหตุที่หน้างาน ประกันภัยจะดูแลทั้งอาคารของท่าน เพื่อนบ้าน และงานของเรา")],
  note="แสดงหนังสือรับรองกรมธรรม์และเอกสารแนบท้ายโครงการตามคำขอ หรือเมื่อลงนามในสัญญา ความคุ้มครองเป็นไปตามเงื่อนไข ข้อกำหนด และข้อยกเว้นของกรมธรรม์",
  cta="ขอหนังสือรับรองประกันภัย", consult="/th/#consult"),
 "zh": dict(
  menu="承包商一切险 (CAR)", pre="/zh",
  eyebrow="已投保 · 承包商一切险 (CAR)", h2="每项安装均已投保一切险，覆盖泰国全境。",
  lede="Solar ESS 已向泰国 Dhipaya Insurance Public Company Limited（ทิพยประกันภัย）投保承包商一切险（Contractor All Risk，CAR）开放式保单，覆盖我们在泰国任何地点的屋顶光伏安装项目，让国内外业主可以放心交付现场。保单以安装工程一切险（EAR）形式签发，即适用于安装工程的 CAR 保障。",
  cards=[("works", "工程一切险", "施工期间、1 周调试期及 12 个月维护期内，安装工程及材料因意外造成的损失或损坏。每份合同工程价值最高 500 万泰铢。"),
         ("tp", "第三者责任", "施工造成他人人身伤害或财产损失：每次事故及每个项目最高 1,000,000 泰铢，保单年度累计 2,000,000 泰铢；人身伤亡无免赔额。"),
         ("prop", "业主现有建筑", "施工造成业主现有建筑或财产损坏：每次事故及每个项目最高 1,000,000 泰铢，保单年度累计 2,000,000 泰铢。"),
         ("emp", "同样保障业主", "业主可与 Solar ESS、分包商及咨询工程师共同列为被保险人，含交叉责任、放弃代位求偿，业主员工视为第三者。"),
         ("map", "全国覆盖，每年续保", "泰国境内任何屋顶光伏项目（机场空侧及离岸区域除外）。本期保单：2026 年 10 月 16 日至 2027 年 10 月 16 日。"),
         ("fire", "附加保障", "灭火费用、残骸清理、保险价值 20% 递增条款及保额自动恢复。")],
  why=[("国际业主", "工厂、酒店、开发商及海外总部通常要求承包商在开工前具备一切险。我们的保单已经生效，可为贵方项目出具批单。"),
       ("泰国本地住宅与企业", "每个项目享有同样保障：现场一旦发生意外，保险将覆盖您的建筑、邻居及我们的工程。")],
  note="保单证明及项目批单可应要求或在签订合同时提供。保障以保单条款、条件及除外责任为准。",
  cta="索取保险证明", consult="/zh/#consult"),
}


def section(L):
    cards = "".join(f'<div class="ins-card">{ic(k)}<div><h3>{h}</h3><p>{p}</p></div></div>' for k, h, p in L["cards"])
    why = "".join(f'<div><h3>{h}</h3><p>{p}</p></div>' for h, p in L["why"])
    return (f'<!--ins--><section class="band light" id="insurance" style="background:var(--paper)"><div class="wrap">'
            f'<div class="ins-hero"><div class="ins-shield">{SHIELD.format(c="#fff", w="1.8").replace("<svg ", "<svg width=\"48\" height=\"48\" ")}</div>'
            f'<div style="flex:1;min-width:260px"><p class="eyebrow">{L["eyebrow"]}</p><h2 style="font-size:clamp(28px,4vw,44px)">{L["h2"]}</h2></div></div>'
            f'<p class="lede" style="margin-top:16px;max-width:900px">{L["lede"]}</p><div class="ins-grid">{cards}</div><div class="ins-why">{why}</div>'
            f'<p class="ins-note">{L["note"]}</p><div style="margin-top:14px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn" href="{L["consult"]}">{L["cta"]}</a>'
            f'<a class="btn ghost" href="https://line.me/ti/p/~solaress1" target="_blank" rel="noopener">LINE: solaress1</a></div></div></section><!--/ins-->')


def lang_of(s):
    m = re.search(r'<html[^>]*\blang="([a-zA-Z-]+)"', s)
    l = (m.group(1) if m else "en")[:2].lower()
    return l if l in T else "en"


DOT = '<span class="ins-dot" aria-hidden="true">' + SHIELD.format(c="#FACC15", w="2.4") + '</span>'
n = 0
for f in sorted(ROOT.rglob("*.html")):
    s = f.read_text(encoding="utf-8"); new = s; lang = lang_of(s); L = T[lang]
    new = re.sub(r"<!--ins-->.*?<!--/ins-->\n?", "", new, flags=re.S)
    new = re.sub(r"<!--insm-->.*?<!--/insm-->", "", new, flags=re.S)
    new = re.sub(r"<!--insdot-->.*?<!--/insdot-->", "", new, flags=re.S)
    new = re.sub(r'<style id="ins-css">.*?</style>', "", new, flags=re.S)
    has_menu = '<span class="dd end">' in new
    if has_menu:
        i = new.index('<span class="dd end">')
        m = re.compile(r'(<a href="[^"]*#services">)([^<]*)(</a>)').match(new, i + len('<span class="dd end">'))
        if m:
            new = new[:m.end(2)] + "<!--insdot-->" + DOT + "<!--/insdot-->" + new[m.end(2):]
        j = new.index('<span class="ddm">', i) + len('<span class="ddm">')
        pm = re.compile(r'<a href="[^"]*profile\.html">[^<]*</a>').match(new, j)
        k = pm.end() if pm else j
        item = f'<!--insm--><a class="ins-m" href="{L["pre"]}/profile.html#insurance"><span class="ins-dot" aria-hidden="true">{SHIELD.format(c="#FACC15", w="2.4")}</span>{L["menu"]}</a><!--/insm-->'
        new = new[:k] + item + new[k:]
    if f.name == "profile.html" and f.parent.name in ("solaress-website", "th", "zh"):
        k = new.index('<section class="band light">', new.index('<section class="dark band">'))  # the "03 — Fleet" band, after "02 — What we offer"
        new = new[:k] + section(L) + "\n" + new[k:]
    if has_menu or "<!--ins-->" in new:
        new = new.replace("</head>", CSS + "</head>", 1)
    if new != s:
        f.write_text(new, encoding="utf-8"); n += 1
print("updated", n, "pages")
