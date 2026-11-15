# -*- coding: utf-8 -*-
"""News article (16 Nov 2026): Netze BW (Germany) approves home-solar grid connections in about 5 minutes.
Inserted as the newest article on /news.html and /th/news.html (id netze-bw-5-minute-grid-approval). Idempotent.
Run: python3 tools/news_nov16_netze.py, then tools/news_topics.py, tools/build_share.py, tools/site_search.py, tools/news_menu.py"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ID, SLUG, IMG = "netze-bw-5-minute-grid-approval", "netze-bw-5-minute-grid-approval", "news-netze-bw-5-minute-grid-approval-20261116.jpg"
EN_PDF = f"/downloads/Solar-ESS-News-{SLUG}_Rev01_WM_20261116.pdf"; TH_PDF = f"/downloads/Solar-ESS-News-{SLUG}-TH_Rev01_WM_20261116.pdf"
SRC = "https://now.solar/2026/10/20/german-dso-cuts-residential-solar-grid-connection-approval-time-to-5-minutes-pv-magazine-global/"
SEP = 'style="max-width:760px;margin-top:64px;padding-top:48px;border-top:1.5px solid var(--navy)"'
T = {
 "en": dict(eyebrow="16 November 2026 · Global Adoption", h2="Germany's Netze BW approves home solar grid connections in 5 minutes",
  lede="A German grid operator now checks rooftop PV applications up to 15 kW automatically: where the local grid has room, the applicant gets a binding answer in about five minutes instead of about 12 days.",
  pts=[("How it works", "A digital model of the low-voltage grid checks cables, transformers and existing systems, then returns the connection point. One request sent at 1:03 am was answered at 1:08 am."),
       ("Results", "Since launch in late July 2026, more than 16,000 small-PV requests; more than 5,000 applicants got binding automated answers within five minutes."),
       ("Why", "About 60,000 PV applications a year, swinging from about 2,000 to 7,000 a month; about 99% arrive through the online portal."),
       ("In Thailand", "Grid approval with PEA/MEA can take longer than the installation itself. Solar ESS prepares complete application files, and a hybrid system with zero-export lets owners start saving while they wait.")],
  dl="Download the summary (PDF) ↓", other=("ภาษาไทย (PDF)", TH_PDF, "th"), src="Source: pv magazine Global, 20 Oct 2026", tail="Summary by Solar ESS.", alt="First page of the Solar ESS summary", pdf=EN_PDF),
 "th": dict(eyebrow="16 พฤศจิกายน 2569 · การติดตั้งโซลาร์ทั่วโลก", h2="เยอรมนี: Netze BW อนุมัติการเชื่อมต่อโซลาร์บ้านภายใน 5 นาที",
  lede="ผู้ดูแลระบบจำหน่ายไฟฟ้าในเยอรมนีตรวจคำขอโซลาร์บนหลังคาไม่เกิน 15 kW โดยอัตโนมัติ หากกริดในพื้นที่ยังรับได้ ผู้ยื่นจะได้คำตอบที่มีผลผูกพันภายในราว 5 นาที แทนที่จะรอเฉลี่ยราว 12 วัน",
  pts=[("ทำงานอย่างไร", "แบบจำลองดิจิทัลของระบบแรงต่ำตรวจสายไฟ หม้อแปลง และระบบที่มีอยู่ แล้วแจ้งจุดเชื่อมต่อ คำขอหนึ่งยื่นตอนตี 1:03 และได้คำตอบตอนตี 1:08"),
       ("ผลลัพธ์", "ตั้งแต่เปิดใช้ปลาย ก.ค. 2569 มีคำขอโซลาร์ขนาดเล็กกว่า 16,000 รายการ ผู้ยื่นกว่า 5,000 รายได้คำตอบอัตโนมัติที่ผูกพันภายใน 5 นาที"),
       ("ทำไม", "มีคำขอราว 60,000 รายการต่อปี ผันผวนตั้งแต่ราว 2,000 ถึง 7,000 รายการต่อเดือน ราว 99% ยื่นผ่านพอร์ทัลออนไลน์"),
       ("ในประเทศไทย", "การขออนุญาตกับ กฟภ./กฟน. อาจใช้เวลานานกว่างานติดตั้ง โซลาร์ เอสส์ เตรียมเอกสารให้ครบ และระบบไฮบริดแบบ zero-export ช่วยให้เริ่มประหยัดได้ระหว่างรอ")],
  dl="ดาวน์โหลดสรุป (PDF ภาษาไทย) ↓", other=("English (PDF)", EN_PDF, "en"), src="ที่มา: pv magazine Global, 20 ต.ค. 2569", tail="สรุปโดย โซลาร์ เอสส์", alt="หน้าแรกของสรุปโดย Solar ESS", pdf=TH_PDF),
}


def article(t):
    lis = "".join(f'<li style="margin-bottom:10px"><b>{a}:</b> {b}</li>' for a, b in t["pts"])
    o = t["other"]; ostyle = ' style="font-family:var(--thai)"' if o[2] == "th" else ""
    return (f'<article id="{ID}" data-topics="adoption" style="max-width:760px">\n'
            f'<p class="eyebrow">{t["eyebrow"]}</p><h2 style="font-size:clamp(26px,3.6vw,40px)">{t["h2"]}</h2>\n'
            f'<p class="lede" style="margin-top:16px;opacity:1">{t["lede"]}</p>\n'
            f'<ul style="margin-top:22px;padding-left:20px">{lis}</ul>\n'
            f'<p style="margin-top:22px"><a href="{t["pdf"]}"><img src="/images/{IMG}" alt="{t["alt"]}" width="579" height="819" loading="lazy" style="width:100%;max-width:360px;height:auto;border:1.5px solid var(--line)"></a></p>\n'
            f'<p style="margin-top:18px;display:flex;gap:10px;flex-wrap:wrap"><a class="btn" href="{t["pdf"]}" download>{t["dl"]}</a>'
            f'<a class="btn ghost" href="{o[1]}" lang="{o[2]}"{ostyle}>{o[0]}</a></p>\n'
            f'<p style="margin-top:28px;font-size:14px;color:var(--mute)">{t["src"]} <a href="{SRC}" rel="noopener">↗</a>. {t["tail"]}</p>\n</article>\n')


for lang, path in (("en", "news.html"), ("th", "th/news.html")):
    p = ROOT / path
    s = p.read_text(encoding="utf-8")
    s = re.sub(rf'<article id="{ID}".*?</article>\n?', "", s, flags=re.S)
    m = re.search(r'<article id="([^"]+)"( data-topics="[^"]*")? style="[^"]*">', s)
    first = re.sub(r'style="[^"]*"', SEP, m.group(0))
    s = s[:m.start()] + article(T[lang]) + first + s[m.end():]
    p.write_text(s, encoding="utf-8")
    print("article on", path, "before", m.group(1))
