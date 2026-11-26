# -*- coding: utf-8 -*-
"""News article (27 Nov 2026): Indonesia's Cirata floating solar farm (Daily Sabah/AFP, Nov 2023) with a 2026 update
(still the region's largest operating FPV; expansion to 500 MW agreed Apr 2025; Malaysia's 200 MW Chereh FPV under
construction since Oct 2026). Newest article on /news.html and /th/news.html (id cirata-floating-solar-indonesia).
Idempotent. Run after tools/news_nov27_gaotu_ev.py, then tools/news_topics.py, tools/build_share.py, tools/site_search.py, tools/news_menu.py"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ID = "cirata-floating-solar-indonesia"
SEP = 'style="max-width:760px;margin-top:64px;padding-top:48px;border-top:1.5px solid var(--navy)"'
SRCS = [("Daily Sabah / AFP", "https://www.dailysabah.com/life/indonesia-unveils-largest-floating-solar-farm-in-southeast-asia/news"),
        ("PV Tech", "https://www.pv-tech.org/masdar-and-pln-inaugurate-192mwp-largest-floating-pv-site-in-southeast-asia"),
        ("ANTARA", "https://en.antaranews.com/news/399929/homepage-v2.html"),
        ("The Star", "https://www.thestar.com.my/business/business-news/2026/10/29/masdar-citaglobal-and-tiza-global-kick-off-construction-of-200mw-floating-solar-project-in-pahang")]
T = {
 "en": dict(eyebrow="27 November 2026 · Global Adoption · story from November 2023, updated",
  h2="Indonesia's Cirata: Southeast Asia's largest floating solar farm, and what has happened since",
  lede="In November 2023 Indonesia opened the Cirata floating solar farm on a reservoir in West Java, about 130 km from Jakarta. Three years on, it is still the region's largest operating floating solar plant, and bigger projects are on the way.",
  pts=[("The plant", "145 MWac (192 MWp) with about 340,000 panels covering 200 hectares of the Cirata Reservoir; built in three years for about US$100 million."),
       ("Who built it", "Indonesia's state utility PLN and Masdar of Abu Dhabi, financed by Sumitomo Mitsui Banking Corporation, Société Générale and Standard Chartered."),
       ("Output", "Enough electricity for about 50,000 households."),
       ("At the opening", "President Joko Widodo called it the largest floating solar farm in Southeast Asia and the third largest in the world."),
       ("Indonesia's challenge", "Solar and wind were each under 1% of the power mix in 2023; the country targets net zero by 2060 but still builds already-planned coal plants."),
       ("2026 update", "Masdar says the plant performs as expected. In April 2025 Masdar and PLN agreed to expand Cirata to a total of 500 MW, helped by a rule allowing up to 20% of a reservoir's surface for renewables."),
       ("Next in the region", "Masdar started building a 200 MW floating solar plant at Chereh, Pahang (Malaysia) in October 2026, set to be the largest standalone floating solar installation in Southeast Asia."),
       ("What it means in Thailand", "Floating solar saves land and the water keeps panels cooler. Thailand already has large floating hybrids on dam reservoirs, and the same idea works on a small scale on farm ponds and factory retention ponds. Ask us if you have a pond or reservoir.")],
  cta=("/#consult", "Ask about solar for your site"), src="Sources:", tail="Summary by Solar ESS Working Group."),
 "th": dict(eyebrow="27 พฤศจิกายน 2569 · การติดตั้งโซลาร์ทั่วโลก · ข่าวจากพฤศจิกายน 2566 พร้อมข้อมูลล่าสุด",
  h2="Cirata ของอินโดนีเซีย: โซลาร์ลอยน้ำใหญ่ที่สุดในเอเชียตะวันออกเฉียงใต้ และความคืบหน้าล่าสุด",
  lede="เดือนพฤศจิกายน 2566 อินโดนีเซียเปิดโซลาร์ฟาร์มลอยน้ำ Cirata บนอ่างเก็บน้ำในชวาตะวันตก ห่างจากจาการ์ตาประมาณ 130 กม. สามปีผ่านไป ยังคงเป็นโรงไฟฟ้าโซลาร์ลอยน้ำที่เดินเครื่องอยู่ใหญ่ที่สุดในภูมิภาค และมีโครงการที่ใหญ่กว่ากำลังตามมา",
  pts=[("โรงไฟฟ้า", "145 MWac (192 MWp) แผงประมาณ 340,000 แผ่น บนพื้นที่ 200 เฮกตาร์ของอ่างเก็บน้ำ Cirata ใช้เวลาก่อสร้าง 3 ปี ลงทุนประมาณ 100 ล้านดอลลาร์สหรัฐ"),
       ("ผู้พัฒนา", "PLN การไฟฟ้าของรัฐอินโดนีเซีย และ Masdar จากอาบูดาบี โดยมี Sumitomo Mitsui Banking Corporation, Société Générale และ Standard Chartered ให้เงินกู้"),
       ("ผลิตไฟ", "เพียงพอสำหรับประมาณ 50,000 ครัวเรือน"),
       ("วันเปิด", "ประธานาธิบดีโจโก วิโดโด กล่าวว่าเป็นโซลาร์ลอยน้ำที่ใหญ่ที่สุดในเอเชียตะวันออกเฉียงใต้ และใหญ่เป็นอันดับ 3 ของโลก"),
       ("ความท้าทายของอินโดนีเซีย", "ปี 2566 พลังงานแสงอาทิตย์และลมมีสัดส่วนอย่างละไม่ถึง 1% ของการผลิตไฟฟ้า ตั้งเป้าปล่อยคาร์บอนสุทธิเป็นศูนย์ในปี 2603 แต่ยังสร้างโรงไฟฟ้าถ่านหินที่วางแผนไว้แล้ว"),
       ("ความคืบหน้าปี 2569", "Masdar ระบุว่าโรงไฟฟ้าทำงานได้ตามที่คาด เมษายน 2568 Masdar และ PLN ตกลงขยาย Cirata เป็นรวม 500 MW โดยได้แรงหนุนจากกฎที่อนุญาตให้ใช้พื้นผิวอ่างเก็บน้ำได้ถึง 20% สำหรับพลังงานหมุนเวียน"),
       ("โครงการถัดไปในภูมิภาค", "Masdar เริ่มก่อสร้างโซลาร์ลอยน้ำ 200 MW ที่ Chereh รัฐปะหัง (มาเลเซีย) ในเดือนตุลาคม 2569 ซึ่งจะเป็นโซลาร์ลอยน้ำแบบแยกเดี่ยวที่ใหญ่ที่สุดในเอเชียตะวันออกเฉียงใต้"),
       ("ความหมายต่อประเทศไทย", "โซลาร์ลอยน้ำช่วยประหยัดพื้นที่ และน้ำช่วยให้แผงเย็นลง ประเทศไทยมีโซลาร์ลอยน้ำแบบไฮบริดขนาดใหญ่บนเขื่อนแล้ว และแนวคิดเดียวกันใช้ได้ในขนาดเล็กบนบ่อน้ำในฟาร์มหรือบ่อพักน้ำของโรงงาน หากมีบ่อหรืออ่างเก็บน้ำ ปรึกษาเราได้")],
  cta=("/th/#consult", "ปรึกษาโซลาร์สำหรับพื้นที่ของคุณ"), src="ที่มา:", tail="สรุปโดย โซลาร์ เอสส์"),
}


def article(t):
    lis = "".join(f'<li style="margin-bottom:10px"><b>{a}:</b> {b}</li>' for a, b in t["pts"])
    srcs = " · ".join(f'{n} <a href="{u}" rel="noopener">↗</a>' for n, u in SRCS)
    return (f'<article id="{ID}" data-topics="adoption innovation" style="max-width:760px">\n'
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
