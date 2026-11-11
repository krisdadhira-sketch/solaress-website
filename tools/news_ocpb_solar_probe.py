# -*- coding: utf-8 -*-
"""News article (11 Nov 2026): Thailand's OCPB crackdown on unsafe rooftop solar (May 2026) + how to check your installer.
Inserted as the newest article on /news.html and /th/news.html (id ocpb-solar-probe-what-to-check). Idempotent.
Run: python3 tools/news_ocpb_solar_probe.py, then tools/build_share.py, tools/site_search.py, tools/analytics_tag.py"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ID = "ocpb-solar-probe-what-to-check"
SRC = ('<p style="margin-top:28px;font-size:14px;color:var(--mute)">{lbl} pv magazine, 19 May 2026 '
       '<a href="https://www.pv-magazine.com/2026/05/19/thailand-opens-investigation-into-faulty-solar-installations/" rel="noopener">↗</a> · '
       'Thai PBS World, 16 May 2026 <a href="https://www.thaipbsworld.com/news/solar-panel-probe-(drafted)" rel="noopener">↗</a> · '
       'Pattaya Mail / NNT, 20 May 2026 <a href="https://www.pattayamail.com/thailandnews/thailand-tightens-solar-safety-checks-amid-surge-in-faulty-rooftop-system-complaints-550101" rel="noopener">↗</a> · '
       'pv magazine, 5 Aug 2026 <a href="https://www.pv-magazine.com/2026/08/05/thailand-registers-solar-installers-equipment-ahead-of-rooftop-pv-expansion/" rel="noopener">↗</a>. {tail}</p>')
BOX = ('<div style="margin-top:26px;border:1.5px solid var(--navy);padding:20px 22px;background:var(--paper)"><p style="font-weight:700;font-size:18px;margin:0 0 10px">{h}</p>'
       '<ol style="margin:0;padding-left:20px">{items}</ol></div>')

T = {
 "en": dict(
  eyebrow="11 November 2026 · Thailand", h2="Unsafe rooftop solar in Thailand: what went wrong, and how to check your installer",
  lede="In May the government ordered an urgent investigation after a home solar system melted and smelled of burning. Six months on, the lessons apply to every homeowner who is about to buy solar.",
  pts=[("What happened", "On 15 May 2026 PM's Office Minister Supamas Isarabhakdi ordered the Office of the Consumer Protection Board (OCPB) to investigate substandard rooftop solar. In the case that started it, parts melted and smelled of burning, the power dropped often, the electricity bill did not fall as promised, and losses passed 500,000 baht."),
       ("What was found", "Non-standard equipment; the contractor allegedly changed the home's supply from three-phase to single-phase; and aluminium wiring was used instead of the required copper."),
       ("How big the problem is", "By 20 May the OCPB had received 156 solar complaints since 2024. 84 were resolved, with damages of more than 40 million baht; the rest were still under review."),
       ("The crackdown", "Nationwide checks of the labels on panels, inverters and batteries. Products without Thai labels, importer details or safety information are seized and tested. Retailers face up to 6 months in prison and/or a 100,000-baht fine; manufacturers and importers up to 1 year and/or 200,000 baht. Installation services are to be put under contract control, so contracts must state equipment standards."),
       ("Since then", "The MEA and PEA registered installers and equipment until 30 September ahead of the 500,000-household rooftop programme, and crystalline silicon panels now have to meet a national safety standard.")],
  box_h="Before you sign: 6 checks",
  box=["Every panel, inverter and battery has a Thai label, the manufacturer or importer's name and the TISI mark.",
       "Copper cables only, sized to match the breakers. Never aluminium in the solar circuits.",
       "Nobody changes your supply (for example from three-phase to single-phase) without PEA/MEA approval and a signed single-line diagram.",
       "The contract names the brands, models and quantities, the warranty, and who signs the work off.",
       "An unusually low price is a warning sign, not a bargain.",
       "Keep the contract, invoices and photos. To complain, call the OCPB hotline 1166."],
  mean="<b>What it means for you:</b> solar is safe when the materials and the work are right. At Solar ESS every job uses copper cables with well-matched breakers, certified protection devices and a signed single-line diagram, and our work is covered by Contractor All Risk (CAR) insurance. Qualifications and certificates are furnished upon request. Already have a system and not sure about it? Send us a few screenshots and we will check it for free.",
  b1="Free System Check", b1h="/system-check.html", b2="Book a consultation", b2h="/#consult",
  lbl="Sources:", tail="Summary by Solar ESS."),
 "th": dict(
  eyebrow="11 พฤศจิกายน 2569 · ประเทศไทย", h2="โซลาร์รูฟท็อปไม่ได้มาตรฐานในไทย: เกิดอะไรขึ้น และตรวจผู้ติดตั้งอย่างไร",
  lede="เมื่อเดือนพฤษภาคม รัฐบาลสั่งตรวจสอบเร่งด่วนหลังระบบโซลาร์ของบ้านหลังหนึ่งละลายและมีกลิ่นไหม้ ผ่านมาหกเดือน บทเรียนนี้ยังใช้ได้กับทุกบ้านที่กำลังจะติดโซลาร์",
  pts=[("เกิดอะไรขึ้น", "วันที่ 15 พฤษภาคม 2569 รัฐมนตรีประจำสำนักนายกรัฐมนตรี ศุภมาส อิศรภักดี สั่งให้สำนักงานคณะกรรมการคุ้มครองผู้บริโภค (สคบ.) ตรวจสอบการติดตั้งโซลาร์รูฟท็อปที่ไม่ได้มาตรฐาน กรณีที่เป็นต้นเรื่อง อุปกรณ์ละลายและมีกลิ่นไหม้ ไฟตกและไฟดับบ่อย ค่าไฟไม่ลดตามที่โฆษณา และความเสียหายเกิน 500,000 บาท"),
       ("สิ่งที่ตรวจพบ", "ใช้อุปกรณ์ไม่ได้มาตรฐาน ผู้รับเหมาถูกกล่าวหาว่าเปลี่ยนระบบไฟของบ้านจาก 3 เฟสเป็น 1 เฟส และใช้สายอะลูมิเนียมแทนสายทองแดงตามที่กำหนด"),
       ("ปัญหาใหญ่แค่ไหน", "ถึงวันที่ 20 พฤษภาคม สคบ. ได้รับเรื่องร้องเรียนเกี่ยวกับโซลาร์ 156 เรื่องตั้งแต่ปี 2567 แก้ไขแล้ว 84 เรื่อง ความเสียหายรวมกว่า 40 ล้านบาท ที่เหลืออยู่ระหว่างดำเนินการ"),
       ("มาตรการ", "ตรวจฉลากแผง อินเวอร์เตอร์ และแบตเตอรี่ทั่วประเทศ สินค้าที่ไม่มีฉลากภาษาไทย ข้อมูลผู้นำเข้า หรือข้อมูลความปลอดภัย จะถูกยึดและส่งตรวจ ผู้ขายมีโทษจำคุกไม่เกิน 6 เดือนและ/หรือปรับไม่เกิน 100,000 บาท ผู้ผลิตและผู้นำเข้าจำคุกไม่เกิน 1 ปีและ/หรือปรับไม่เกิน 200,000 บาท และจะกำหนดให้ธุรกิจติดตั้งโซลาร์เป็นธุรกิจควบคุมสัญญา สัญญาต้องระบุมาตรฐานอุปกรณ์"),
       ("หลังจากนั้น", "การไฟฟ้านครหลวงและการไฟฟ้าส่วนภูมิภาคเปิดขึ้นทะเบียนผู้ติดตั้งและอุปกรณ์ถึง 30 กันยายน ก่อนโครงการโซลาร์รูฟท็อป 500,000 ครัวเรือน และแผงซิลิคอนผลึกต้องผ่านมาตรฐานความปลอดภัยของประเทศ")],
  box_h="ก่อนเซ็นสัญญา: 6 ข้อที่ต้องตรวจ",
  box=["แผง อินเวอร์เตอร์ และแบตเตอรี่ทุกชิ้นมีฉลากภาษาไทย ชื่อผู้ผลิตหรือผู้นำเข้า และเครื่องหมาย มอก.",
       "ใช้สายทองแดงเท่านั้น ขนาดเหมาะกับเบรกเกอร์ ห้ามใช้สายอะลูมิเนียมในวงจรโซลาร์",
       "ห้ามใครเปลี่ยนระบบไฟของบ้าน (เช่น จาก 3 เฟสเป็น 1 เฟส) โดยไม่ได้รับอนุมัติจากการไฟฟ้าและไม่มีแบบไฟฟ้า (Single-line diagram) ที่ลงนามแล้ว",
       "สัญญาระบุยี่ห้อ รุ่น จำนวน การรับประกัน และผู้ตรวจรับงาน",
       "ราคาถูกผิดปกติคือสัญญาณเตือน ไม่ใช่ของดี",
       "เก็บสัญญา ใบเสร็จ และรูปถ่ายไว้ หากต้องการร้องเรียน โทรสายด่วน สคบ. 1166"],
  mean="<b>สำหรับคุณ:</b> โซลาร์ปลอดภัยเมื่อวัสดุและงานติดตั้งถูกต้อง โซลาร์ เอสส์ ใช้สายทองแดง เบรกเกอร์ที่ขนาดเหมาะสม อุปกรณ์ป้องกันที่ได้มาตรฐาน และแบบไฟฟ้าที่ลงนามทุกงาน งานของเรามีประกันภัยความเสี่ยงภัยทุกชนิดของผู้รับเหมา (CAR) คุณวุฒิและใบรับรองแสดงได้เมื่อมีการร้องขอ มีระบบอยู่แล้วแต่ไม่แน่ใจ? ส่งภาพหน้าจอมาให้เรา เราตรวจให้ฟรี",
  b1="ตรวจระบบฟรี", b1h="/th/system-check.html", b2="นัดปรึกษา", b2h="/th/#consult",
  lbl="แหล่งข่าว:", tail="สรุปโดย โซลาร์ เอสส์"),
}


def article(t):
    lis = "".join(f'<li style="margin-bottom:10px"><b>{a}:</b> {b}</li>' for a, b in t["pts"])
    box = BOX.format(h=t["box_h"], items="".join(f'<li style="margin-bottom:6px">{x}</li>' for x in t["box"]))
    return (f'<article id="{ID}" data-topics="adoption" style="max-width:760px">\n'
            f'<p class="eyebrow">{t["eyebrow"]}</p><h2 style="font-size:clamp(26px,3.6vw,40px)">{t["h2"]}</h2>\n'
            f'<p class="lede" style="margin-top:16px;opacity:1">{t["lede"]}</p>\n'
            f'<ul style="margin-top:22px;padding-left:20px">{lis}</ul>\n{box}\n'
            f'<p style="margin-top:22px">{t["mean"]}</p>\n'
            f'<p style="margin-top:22px;display:flex;gap:10px;flex-wrap:wrap"><a class="btn" href="{t["b1h"]}">{t["b1"]}</a><a class="btn ghost" href="{t["b2h"]}">{t["b2"]}</a></p>\n'
            + SRC.format(lbl=t["lbl"], tail=t["tail"]) + '\n</article>\n')


SEP = 'style="max-width:760px;margin-top:64px;padding-top:48px;border-top:1.5px solid var(--navy)"'
for lang, path in (("en", "news.html"), ("th", "th/news.html")):
    p = ROOT / path
    s = p.read_text(encoding="utf-8")
    s = re.sub(rf'<article id="{ID}".*?</article>\n?', "", s, flags=re.S)
    m = re.search(r'<article id="([^"]+)" data-topics="[^"]*" style="max-width:760px">', s)
    first = m.group(0)
    s = s[:m.start()] + article(T[lang]) + first.replace('style="max-width:760px"', SEP) + s[m.end():]
    p.write_text(s, encoding="utf-8")
    print("article on", path, "before", m.group(1))
