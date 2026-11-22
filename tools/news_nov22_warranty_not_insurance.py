# -*- coding: utf-8 -*-
"""News article (22 Nov 2026): installation warranty is not insurance – coverage guide Rev06 (Thai PDF).
Inserted as the newest article on /news.html and /th/news.html (id warranty-not-insurance-coverage-rev06). Idempotent.
Run: python3 tools/news_nov22_warranty_not_insurance.py, then tools/news_topics.py, tools/site_search.py, tools/news_menu.py"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ID = "warranty-not-insurance-coverage-rev06"
PDF = "/downloads/Solar-ESS_Installation-Coverage-Nationwide_TH_Rev06_WM_20261122.pdf"
IMG = "/images/doc-installation-coverage-nationwide-th-rev06.jpg"
SEP = 'style="max-width:760px;margin-top:64px;padding-top:48px;border-top:1.5px solid var(--navy)"'
T = {
 "en": dict(eyebrow="22 November 2026 · Customer guide",
  h2="An installation warranty is not insurance: what it covers, and how to plan for the unexpected",
  lede="Our updated coverage guide (Thai, Rev06) explains what the Solar ESS installation warranty is for, why it is not an insurance policy, and what resorts, hotels and homes should have in place.",
  pts=[("Purpose", "The installation warranty helps fix faulty or damaged equipment, finds the cause and prevents installation-related problems from coming back. It does not pay for losses like an insurance policy, and it is not an emergency call-out service."),
       ("2 or 5 years", "Our workmanship warranty is 2 years or 5 years, as stated in each proposal or contract. We find what the problem is and what caused it, and support the claim with the manufacturer based on the facts found."),
       ("Solar is a cost saver", "We know electricity is critical to every business, but a solar system is first a way to cut the power bill. Electrical appliances and systems can fail without warning."),
       ("Plan for acts of God", "To ride through events such as a PEA power cut, add batteries, a backup circuit or a generator, or other backup systems. No single system has been shown to protect against every act of God."),
       ("Have a person in charge", "Resorts and hotels must have an in-house technician or staff member who looks after internal electrical issues, checks first, sends photos and coordinates with us and other contractors."),
       ("Insure the building", "Damage from storms, lightning or floods is claimed from the building's property insurance; Solar ESS supplies system data to the insurer.")],
  dl="Open the PDF ↓ · Thai", tail="Solar ESS Working Group.", alt="First page of the Solar ESS coverage guide"),
 "th": dict(eyebrow="22 พฤศจิกายน 2569 · คู่มือลูกค้า",
  h2="การรับประกันการติดตั้ง มิใช่การประกันภัย: ครอบคลุมอะไร และควรเตรียมรับเหตุไม่คาดคิดอย่างไร",
  lede="คู่มือการรับประกันฉบับปรับปรุง (Rev06) อธิบายว่าการรับประกันการติดตั้งของ Solar ESS มีไว้เพื่ออะไร ทำไมจึงไม่ใช่ประกันภัย และรีสอร์ท โรงแรม และบ้าน ควรเตรียมอะไรไว้",
  pts=[("เป้าหมาย", "การรับประกันการติดตั้งมีไว้เพื่อช่วยแก้ไขอุปกรณ์ชำรุดหรือเสียหาย วิเคราะห์หาสาเหตุ และป้องกันไม่ให้ปัญหาที่เกี่ยวกับงานติดตั้งเกิดซ้ำ ไม่ใช่การชดใช้ความเสียหายแบบประกันภัย และไม่ใช่บริการฉุกเฉิน"),
       ("2 ปี หรือ 5 ปี", "การรับประกันงานติดตั้งของเรามี 2 ปี หรือ 5 ปี ตามข้อเสนอหรือสัญญา เราตรวจหาว่าปัญหาคืออะไร เกิดจากอะไร และช่วยเคลมกับผู้ผลิตตามข้อเท็จจริงที่ตรวจพบ"),
       ("โซลาร์คือระบบช่วยลดค่าไฟ", "ผู้ติดตั้งเข้าใจดีว่าระบบไฟฟ้าสำคัญต่อธุรกิจอย่างที่สุด แต่ระบบโซลาร์เซลล์เป็นเพียงระบบผลิตไฟเพื่อช่วยลดค่าใช้จ่ายในเบื้องต้น เครื่องใช้ไฟฟ้าและระบบไฟฟ้าอาจขัดข้องได้โดยไม่คาดคิด"),
       ("เตรียมรับเหตุสุดวิสัย", "หากต้องการรับมือเหตุสุดวิสัย เช่น ไฟดับจากการไฟฟ้า สามารถเพิ่มแบตเตอรี่ วงจรสำรองไฟ เครื่องปั่นไฟ หรือระบบสำรองไฟอื่น ๆ ได้ แต่ไม่มีระบบใดระบบเดียวที่ป้องกันเหตุสุดวิสัยได้ทั้งหมด"),
       ("มีผู้รับผิดชอบโดยตรง", "รีสอร์ทและโรงแรมต้องมีช่างหรือผู้ดูแลประจำ ดูแลปัญหาไฟฟ้าภายใน ตรวจเบื้องต้น ส่งรูปและข้อมูล และประสานงานกับเราและผู้รับเหมาที่เกี่ยวข้อง"),
       ("ทำประกันทรัพย์สิน", "ความเสียหายจากพายุ ฟ้าผ่า หรือน้ำท่วม เคลมจากประกันทรัพย์สินของอาคาร Solar ESS ช่วยให้ข้อมูลระบบแก่บริษัทประกันได้")],
  dl="เปิด PDF ↓ · ภาษาไทย", tail="Solar ESS Working Group", alt="หน้าแรกของคู่มือการรับประกันของ Solar ESS"),
}


def article(t):
    lis = "".join(f'<li style="margin-bottom:10px"><b>{a}:</b> {b}</li>' for a, b in t["pts"])
    return (f'<article id="{ID}" style="max-width:760px">\n'
            f'<p class="eyebrow">{t["eyebrow"]}</p><h2 style="font-size:clamp(26px,3.6vw,40px)">{t["h2"]}</h2>\n'
            f'<p class="lede" style="margin-top:16px;opacity:1">{t["lede"]}</p>\n'
            f'<ul style="margin-top:22px;padding-left:20px">{lis}</ul>\n'
            f'<p style="margin-top:22px"><a href="{PDF}"><img src="{IMG}" alt="{t["alt"]}" width="579" height="819" loading="lazy" style="width:100%;max-width:360px;height:auto;border:1.5px solid var(--line)"></a></p>\n'
            f'<p style="margin-top:18px;display:flex;gap:10px;flex-wrap:wrap"><a class="btn" href="{PDF}" download>{t["dl"]}</a></p>\n'
            f'<p style="margin-top:20px;font-size:14px;color:var(--mute)">{t["tail"]}</p>\n</article>\n')


for lang, path in (("en", "news.html"), ("th", "th/news.html")):
    p = ROOT / path
    s = p.read_text(encoding="utf-8")
    s = re.sub(rf'<article id="{ID}".*?</article>\n?', "", s, flags=re.S)
    m = re.search(r'<article id="([^"]+)"( data-topics="[^"]*")? style="[^"]*">', s)
    first = re.sub(r'style="[^"]*"', SEP, m.group(0))
    s = s[:m.start()] + article(T[lang]) + first + s[m.end():]
    p.write_text(s, encoding="utf-8")
    print("article on", path, "before", m.group(1))
