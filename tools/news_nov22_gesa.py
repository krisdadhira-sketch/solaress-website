# -*- coding: utf-8 -*-
"""News article (22 Nov 2026): Global Energy Storage Alliance (GESA) launched at COP31.
Inserted as the newest article on /news.html and /th/news.html (id gesa-storage-alliance-cop31). Idempotent.
Run: python3 tools/news_nov22_gesa.py, then tools/news_topics.py, tools/build_share.py, tools/site_search.py, tools/news_menu.py"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ID = "gesa-storage-alliance-cop31"
SEP = 'style="max-width:760px;margin-top:64px;padding-top:48px;border-top:1.5px solid var(--navy)"'
SRCS = [("pv magazine", "https://www.pv-magazine.com/2026/11/21/catl-byd-acwa-among-co-initiators-of-storage-alliance-unveiled-at-cop31/"),
        ("Energy-Storage.news", "https://www.energy-storage.news/global-energy-storage-alliance-launches-at-cop31-aims-to-address-persistent-energy-transition-challenges/"),
        ("Power Technology", "https://www.power-technology.com/?p=416491")]
T = {
 "en": dict(eyebrow="22 November 2026 · Global Adoption",
  h2="CATL, BYD and ACWA Power among founders of a new Global Energy Storage Alliance at COP31",
  lede="The Global Energy Storage Alliance (GESA), a new platform for international cooperation on energy storage, was launched on 13 November 2026 at the China Pavilion, COP31, in Antalya, Türkiye.",
  pts=[("Founders", "China Energy Storage Alliance (CNESA), China Renewable Energy Engineering Institute (CREEI) and China Southern Power Grid Energy Storage."),
       ("Members", "CATL, BYD Energy Storage, Sungrow, Trina Storage, EVE Energy, Hithium and Envision, plus Saudi power producer ACWA Power."),
       ("At the launch", "UN, IRENA and Chinese government officials."),
       ("Goal", "Make energy storage central to grid flexibility and to bringing more renewable energy onto the grid."),
       ("Open to join", "Industry associations, research institutes and companies worldwide are invited."),
       ("Status", "Still at an early stage: no governance, funding, capacity target or binding commitment yet."),
       ("Market", "The world's six largest battery cell makers are all Chinese, and battery storage prices keep falling."),
       ("What it means in Thailand", "Cheaper, better batteries make adding storage to an existing solar system easier and more worthwhile. If you are installing solar now, choose a hybrid inverter so a battery can be added later.")],
  cta=("/#consult", "Talk to us about adding a battery"), src="Sources:", tail="Summary by Solar ESS Working Group."),
 "th": dict(eyebrow="22 พฤศจิกายน 2569 · การติดตั้งโซลาร์ทั่วโลก",
  h2="CATL, BYD และ ACWA Power ร่วมก่อตั้งพันธมิตรกักเก็บพลังงานโลก (GESA) ที่ COP31",
  lede="พันธมิตรกักเก็บพลังงานโลก (GESA) แพลตฟอร์มความร่วมมือระหว่างประเทศด้านการกักเก็บพลังงาน เปิดตัวเมื่อ 13 พ.ย. 2569 ที่ China Pavilion งาน COP31 เมืองอันตัลยา ประเทศตุรกี",
  pts=[("ผู้ก่อตั้ง", "China Energy Storage Alliance (CNESA), China Renewable Energy Engineering Institute (CREEI) และ China Southern Power Grid Energy Storage"),
       ("สมาชิก", "CATL, BYD Energy Storage, Sungrow, Trina Storage, EVE Energy, Hithium, Envision และ ACWA Power ผู้ผลิตไฟฟ้าจากซาอุดีอาระเบีย"),
       ("ผู้ร่วมงานเปิดตัว", "เจ้าหน้าที่จาก UN, IRENA และรัฐบาลจีน"),
       ("เป้าหมาย", "ให้ระบบกักเก็บพลังงานเป็นหัวใจของความยืดหยุ่นของระบบไฟฟ้า และช่วยให้นำพลังงานหมุนเวียนเข้าสู่ระบบได้มากขึ้น"),
       ("เปิดรับสมาชิก", "สมาคม สถาบันวิจัย และบริษัททั่วโลก"),
       ("สถานะ", "ยังอยู่ในช่วงเริ่มต้น ยังไม่มีโครงสร้างการบริหาร งบประมาณ เป้าหมายกำลังการผลิต หรือข้อผูกพันใด ๆ"),
       ("ภาพรวมตลาด", "ผู้ผลิตเซลล์แบตเตอรี่ 6 อันดับแรกของโลกเป็นบริษัทจีนทั้งหมด และราคาระบบกักเก็บพลังงานยังลดลงต่อเนื่อง"),
       ("ความหมายต่อเจ้าของบ้านในไทย", "แบตเตอรี่ที่ถูกลงและดีขึ้น ทำให้การเพิ่มแบตเตอรี่ในระบบโซลาร์ที่มีอยู่แล้วคุ้มค่าและง่ายขึ้น หากกำลังจะติดโซลาร์ ควรเลือกอินเวอร์เตอร์ไฮบริดที่เพิ่มแบตเตอรี่ภายหลังได้")],
  cta=("/th/#consult", "ปรึกษาเรื่องแบตเตอรี่"), src="ที่มา:", tail="สรุปโดย โซลาร์ เอสส์"),
}


def article(t):
    lis = "".join(f'<li style="margin-bottom:10px"><b>{a}:</b> {b}</li>' for a, b in t["pts"])
    srcs = " · ".join(f'{n} <a href="{u}" rel="noopener">↗</a>' for n, u in SRCS)
    return (f'<article id="{ID}" data-topics="adoption" style="max-width:760px">\n'
            f'<p class="eyebrow">{t["eyebrow"]}</p><h2 style="font-size:clamp(26px,3.6vw,40px)">{t["h2"]}</h2>\n'
            f'<p class="lede" style="margin-top:16px;opacity:1">{t["lede"]}</p>\n'
            f'<ul style="margin-top:22px;padding-left:20px">{lis}</ul>\n'
            f'<p style="margin-top:22px;display:flex;gap:10px;flex-wrap:wrap"><a class="btn" href="{t["cta"][0]}">{t["cta"][1]}</a></p>\n'
            f'<p style="margin-top:28px;font-size:14px;color:var(--mute)">{t["src"]} {srcs}. {t["tail"]}</p>\n</article>\n')


for lang, path in (("en", "news.html"), ("th", "th/news.html")):
    p = ROOT / path
    s = p.read_text(encoding="utf-8")
    s = re.sub(rf'<article id="{ID}".*?</article>\n?', "", s, flags=re.S)
    m = re.search(r'<article id="([^"]+)"( data-topics="[^"]*")? style="[^"]*">', s)
    first = re.sub(r'style="[^"]*"', SEP, m.group(0))
    s = s[:m.start()] + article(T[lang]) + first + s[m.end():]
    p.write_text(s, encoding="utf-8")
    print("article on", path, "before", m.group(1))
