# -*- coding: utf-8 -*-
"""Free Plant Design page (Nov 2026): /design.html and /th/design.html, built on the quotation page shell.
Shows real Solar ESS design drawings (equipment frame, ground mount on screw piles) with a short description each,
then sends visitors to the consultation form with "Free Plant Design" preselected (/?free=design#consult).
Photos: images/design-*_Rev01_20261111.jpg, watermarked "SOLAR ESS / www.solaress.org" by this script (from the
originals in tools/design_src/ if present). No customer names or exact locations.
Run from the repo root:  python3 tools/plant_design_page.py
then  python3 tools/projects_menu.py && python3 tools/nps_everywhere.py && python3 tools/analytics_tag.py
      && python3 tools/form_ink.py && python3 tools/accessibility.py && python3 tools/build_share.py && python3 tools/site_search.py"""
import os, re, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
os.chdir(ROOT)
from service_pages import CSS as SVC_CSS, hero, section  # noqa: E402

SRC = ROOT / "tools" / "design_src"
SUF = "_Rev01_20261111.jpg"
PHOTOS = ["design-equipment-frame-front", "design-equipment-frame-rear", "design-ground-mount-section",
          "design-ground-mount-array", "design-screw-piles-underside", "design-ground-mount-corner"]
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def watermark(src, dst):
    im = Image.open(src).convert("RGB")
    w, h = im.size
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    big = ImageFont.truetype(FONT, max(40, w // 11))
    small = ImageFont.truetype(FONT, max(18, w // 40))
    txt = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(txt)
    a, b = "SOLAR ESS", "www.solaress.org"
    bw = d.textbbox((0, 0), a, font=big); sw = d.textbbox((0, 0), b, font=small)
    cx, cy = w // 2, h // 2
    d.text((cx - (bw[2] - bw[0]) // 2, cy - (bw[3] - bw[1])), a, font=big, fill=(120, 120, 140, 70))
    d.text((cx - (sw[2] - sw[0]) // 2, cy + 12), b, font=small, fill=(91, 91, 214, 80))
    txt = txt.rotate(20, center=(cx, cy))
    layer.alpha_composite(txt)
    out = Image.alpha_composite(im.convert("RGBA"), layer).convert("RGB")
    if w > 1600:
        out = out.resize((1600, round(h * 1600 / w)), Image.LANCZOS)
    out.save(dst, "JPEG", quality=85, optimize=True, progressive=True)


CSS = """<style id="pd-css">
.pdgal{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,460px),1fr));gap:26px;margin-top:28px}
.pdgal figure{margin:0;background:var(--white);border:1.5px solid var(--line);display:flex;flex-direction:column}
.pdgal a{display:flex;align-items:center;justify-content:center;background:#fff;aspect-ratio:16/10;overflow:hidden}
.pdgal img{display:block;width:100%;height:100%;object-fit:contain}
.pdgal figcaption{padding:16px 18px 18px;line-height:1.5}
.pdgal figcaption b{display:block;font-size:18px;margin-bottom:4px}
.pdgal figcaption span{color:var(--mute);font-size:15px}
.pdgrp{margin-top:46px;font-size:24px}
.pdgrp:first-of-type{margin-top:20px}
</style>
"""

L = {
 "en": dict(
  title="Free Plant Design – solar system and structure drawings | Solar ESS",
  desc="Free solar plant design by Solar ESS: equipment frame layouts, ground-mount structures on screw piles, panel layout and dimensions, drawn for your site before you decide.",
  eyebrow="Services · Free Plant Design", h1="See your solar plant<br>before it is built.",
  lede="Send us your site details and electricity bill. Our engineers draw the plant for you: panel layout, mounting structure and the equipment wall for the inverter, batteries and switchboards, with real dimensions. Free and with no obligation. Below are designs we have drawn for real projects.",
  call="Call", go="Ask for my free design ↓",
  gh="Examples of our designs", gsub="3D models and sections from recent projects (customer details removed). Click a picture to open it full size.",
  g1="Equipment frame: inverter, batteries and switchboards", g2="Ground mount on screw piles",
  caps=[("Equipment frame, front view", "A 3.40 m × 2.20 m steel frame holds the main switchboard, the hybrid inverter and the DC box on top, with four batteries and the busbar breaker box on a raised plinth below. Everything is reachable from the front for service."),
        ("Equipment frame, rear view", "Three bays (1.05 m, 1.20 m, 1.05 m) and 0.33 m deep. Cross rails carry the cable runs and a 0.84 m cable tray separates the wall-mounted equipment from the batteries."),
        ("Ground-mount section", "Panels (2,382 × 1,134 mm, portrait) at 10°, clamped directly on 2\"×4\" purlins welded to the rafter. Columns sit on screw piles at 1,379 mm centres; front edge 0.60 m, back edge 1.01 m above ground."),
        ("Ground-mount array layout", "A 17.60 m × 16.60 m field with frames every 3.32 m and purlin rows 2.10 m apart. One row of four panels (7.16 m) is shown; column heights step from 0.50 m to 1.06 m to give the tilt."),
        ("Screw piles, no concrete", "Every column stands on a screw pile with a bolted base plate: fast to install, no concrete footings to cast, and adjustable to uneven ground."),
        ("Corner detail", "Panels clamped on the purlins, the purlins on the rafters and the columns bolted to the pile plates: the full load path from panel to ground.")],
  sh="How the free design works",
  steps=["Send your bill, roof or land photos and location (approximate is fine).",
         "We size the system to your use and draw the layout, structure and equipment wall.",
         "You get the drawings and a short explanation on LINE or by email.",
         "Use it to decide, or to compare quotations. No obligation."],
  ch="Get your free plant design", cp="Tell us about your site. We usually reply within 3 working days.",
  cbtn="Ask for my free design", cform="/?free=design#consult"),
 "th": dict(
  title="ออกแบบระบบฟรี – แบบระบบโซลาร์และโครงสร้าง | Solar ESS",
  desc="Solar ESS ออกแบบระบบโซลาร์ให้ฟรี: แบบโครงติดตั้งอุปกรณ์ โครงสร้างติดตั้งบนพื้นด้วยเสาเข็มเกลียว ผังแผงและขนาดจริง ก่อนตัดสินใจ",
  eyebrow="บริการ · ออกแบบระบบฟรี", h1="เห็นระบบโซลาร์ของคุณ<br>ก่อนเริ่มสร้าง",
  lede="ส่งข้อมูลหน้างานและบิลค่าไฟมาให้เรา วิศวกรของเราจะออกแบบระบบให้: ผังแผง โครงสร้างติดตั้ง และโครงติดตั้งอินเวอร์เตอร์ แบตเตอรี่ และตู้ไฟ พร้อมขนาดจริง ฟรีและไม่มีข้อผูกมัด ด้านล่างคือตัวอย่างแบบที่เราออกแบบให้โครงการจริง",
  call="โทร", go="ขอแบบระบบฟรี ↓",
  gh="ตัวอย่างงานออกแบบ", gsub="โมเดล 3 มิติและภาพตัดจากโครงการล่าสุด (ปิดข้อมูลลูกค้าแล้ว) คลิกที่ภาพเพื่อดูขนาดเต็ม",
  g1="โครงติดตั้งอุปกรณ์: อินเวอร์เตอร์ แบตเตอรี่ และตู้ไฟ", g2="โครงสร้างติดตั้งบนพื้นด้วยเสาเข็มเกลียว",
  caps=[("โครงติดตั้งอุปกรณ์ ด้านหน้า", "โครงเหล็กขนาด 3.40 × 2.20 ม. ติดตั้งตู้ไฟหลัก อินเวอร์เตอร์ไฮบริด และตู้ DC ด้านบน แบตเตอรี่ 4 ชุดและตู้บัสบาร์เบรกเกอร์วางบนฐานยกด้านล่าง เข้าถึงได้จากด้านหน้าทั้งหมดเพื่อการบำรุงรักษา"),
        ("โครงติดตั้งอุปกรณ์ ด้านหลัง", "แบ่ง 3 ช่อง (1.05, 1.20, 1.05 ม.) ลึก 0.33 ม. คานขวางใช้เดินสาย และรางสายไฟที่ระดับ 0.84 ม. แยกอุปกรณ์ติดผนังออกจากแบตเตอรี่"),
        ("ภาพตัดโครงสร้างติดตั้งบนพื้น", "แผง (2,382 × 1,134 มม. แนวตั้ง) เอียง 10° ยึดบนแป 2\"×4\" ที่เชื่อมกับจันทัน เสาตั้งบนเสาเข็มเกลียวระยะ 1,379 มม. ขอบหน้าสูง 0.60 ม. ขอบหลังสูง 1.01 ม. จากพื้น"),
        ("ผังแผงบนพื้นที่", "พื้นที่ 17.60 × 16.60 ม. โครงทุก 3.32 ม. แนวแปห่างกัน 2.10 ม. ภาพแสดงแผง 4 แผงหนึ่งแถว (7.16 ม.) ความสูงเสาไล่จาก 0.50 ถึง 1.06 ม. เพื่อให้ได้มุมเอียง"),
        ("เสาเข็มเกลียว ไม่ต้องเทคอนกรีต", "เสาทุกต้นตั้งบนเสาเข็มเกลียวพร้อมเพลทยึดน็อต ติดตั้งเร็ว ไม่ต้องหล่อฐานคอนกรีต และปรับระดับตามพื้นที่ไม่เรียบได้"),
        ("รายละเอียดมุมโครงสร้าง", "แผงยึดบนแป แปวางบนจันทัน และเสายึดน็อตกับเพลทเสาเข็ม: เส้นทางรับน้ำหนักครบตั้งแต่แผงลงถึงพื้น")],
  sh="ขั้นตอนการออกแบบฟรี",
  steps=["ส่งบิลค่าไฟ ภาพหลังคาหรือพื้นที่ และตำแหน่งโดยประมาณ",
         "เราคำนวณขนาดระบบตามการใช้ไฟ และออกแบบผังแผง โครงสร้าง และโครงติดตั้งอุปกรณ์",
         "คุณได้รับแบบพร้อมคำอธิบายสั้น ๆ ทาง LINE หรืออีเมล",
         "ใช้ประกอบการตัดสินใจหรือเทียบใบเสนอราคา ไม่มีข้อผูกมัด"],
  ch="ขอแบบระบบโซลาร์ฟรี", cp="บอกเราเกี่ยวกับหน้างานของคุณ ปกติเราตอบกลับภายใน 3 วันทำการ",
  cbtn="ขอแบบระบบฟรี", cform="/th/?free=design#consult"),
}


def gallery(t):
    def fig(i):
        a, b = t["caps"][i]
        src = f"/images/{PHOTOS[i]}{SUF}"
        return (f'<figure id="{PHOTOS[i]}"><a href="{src}" target="_blank" rel="noopener"><img src="{src}" alt="{a}" width="1559" height="920" loading="lazy" decoding="async"></a>'
                f'<figcaption><b>{a}</b><span>{b}</span></figcaption></figure>')
    return (f'<h3 class="pdgrp">{t["g1"]}</h3><div class="pdgal">{fig(0)}{fig(1)}</div>'
            f'<h3 class="pdgrp">{t["g2"]}</h3><div class="pdgal">{"".join(fig(i) for i in range(2, 6))}</div>')


def body(t):
    steps = "".join(f"<li>{s}</li>" for s in t["steps"])
    go = f'<a class="btn" href="{t["cform"]}" style="background:#16A34A;border-color:#16A34A">{t["cbtn"]}</a>'
    return (hero(t["eyebrow"], t["h1"], t["lede"], t["call"], f'<a class="btn" href="#examples" style="background:#16A34A;border-color:#16A34A">{t["go"]}</a>')
            + section(t["eyebrow"].split("·")[0].strip(), t["gh"], t["gsub"], gallery(t)).replace('<section class="band light"', '<section class="band light" id="examples"', 1)
            + section("1 → 4", t["sh"], "", f'<ol class="svsteps">{steps}</ol>', paper=True)
            + f'<section class="dark band" style="padding-block:56px"><div class="wrap"><h2 class="svh2">{t["ch"]}</h2>'
              f'<p class="lede" style="margin-top:10px">{t["cp"]}</p><div style="margin-top:22px;display:flex;gap:12px;flex-wrap:wrap">{go}</div></div></section>')


def build(lang):
    t = L[lang]
    tpl = "th/quotation.html" if lang == "th" else "quotation.html"
    out = ROOT / ("th/design.html" if lang == "th" else "design.html")
    src = (ROOT / tpl).read_text(encoding="utf-8")
    head, rest = src.split("<!--/mnav-->", 1)
    foot = rest[rest.index("<footer"):]
    base, slug = "https://solaress.org", "design"
    url = f"{base}/th/{slug}" if lang == "th" else f"{base}/{slug}"
    head = re.sub(r"<title>.*?</title>", f"<title>{t['title']}</title>", head, flags=re.S)
    for k in ('<meta property="og:title" content="', '<meta name="twitter:title" content="'):
        head = re.sub(re.escape(k) + r'[^"]*', k + t["title"], head)
    for k in ('<meta property="og:description" content="', '<meta name="description" content="', '<meta name="twitter:description" content="'):
        head = re.sub(re.escape(k) + r'[^"]*', k + t["desc"], head)
    head = re.sub(r'(<meta property="og:url" content=")[^"]*', r"\g<1>" + url + ".html", head)
    for k in ('<meta property="og:image" content="', '<meta name="twitter:image" content="'):
        head = re.sub(re.escape(k) + r'[^"]*', k + base + f"/images/{PHOTOS[3]}{SUF}", head)
    head = head.replace(f'{base}/quotation"', f'{base}/{slug}"').replace(f'{base}/th/quotation"', f'{base}/th/{slug}"')
    head = re.sub(r'<link rel="alternate" hreflang="zh-Hans"[^>]*>\n?', "", head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', "", head, flags=re.S)
    head = head.replace("</head>", SVC_CSS + CSS + "</head>", 1)
    head = re.sub(r'<span class="langsw">.*?</span></nav>', lambda m: m.group(0).replace('/zh/quotation.html', f'/{slug}.html')
                  .replace('/th/quotation.html', f'/th/{slug}.html').replace('/quotation.html', f'/{slug}.html'), head, flags=re.S)
    out.write_text(head + "<!--/mnav-->\n" + body(t) + "\n" + foot, encoding="utf-8")
    print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    if SRC.exists():
        for i, name in enumerate(PHOTOS):
            s = SRC / f"{i + 1}.jpg"
            if s.exists():
                watermark(s, ROOT / "images" / f"{name}{SUF}")
    build("en"); build("th")
