# -*- coding: utf-8 -*-
"""Preventive Maintenance pages (EN/TH): "On site" photo band (cleaning + torque check), inserted after "What we check",
between <!--mphotos--> markers. Photos images/maint-*_Rev01_20261111.jpg, watermarked from tools/maint_src/1..3.jpg if present
(watermark() from tools/plant_design_page.py). Idempotent. Run: python3 tools/maintenance_photos.py"""
import re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from plant_design_page import watermark, CSS  # noqa: E402

SRC = ROOT / "tools" / "maint_src"
NAMES = ["maint-pv-cleaning-brush", "maint-torque-end-clamp", "maint-torque-mid-clamp"]
SUF = "_Rev01_20261111.jpg"
T = {
 "en": dict(eyebrow="On site", h2="Cleaning and checking, in practice",
   sub="From a recent preventive maintenance visit on a tiled home roof (Nov 2026). Click a picture to open it full size.",
   caps=[("Panel cleaning", "A soft rotating brush on an extension pole and a water rinse lift dust and bird droppings without scratching the glass. The technician works in a high-visibility vest and stays on the roof tiles, never on the panels."),
         ("Torque check on the end clamps", "After cleaning, every end clamp is re-tightened with a torque wrench to the mounting maker's value, so panels stay fixed in strong wind. The earth wire bonded to the rail is checked at the same time."),
         ("Torque check on the mid clamps", "Mid clamps between panels are checked the same way: not too loose to hold the panel, not so tight that they bend the frame or crack the glass.")]),
 "th": dict(eyebrow="หน้างานจริง", h2="ล้างแผงและตรวจเช็ก ทำอย่างไร",
   sub="จากการบำรุงรักษาเชิงป้องกันบนหลังคากระเบื้องบ้านพักอาศัย (พ.ย. 2569) คลิกที่ภาพเพื่อดูขนาดเต็ม",
   caps=[("ล้างแผงโซลาร์", "ใช้แปรงหมุนขนนุ่มต่อด้ามยาวและน้ำล้าง ขจัดฝุ่นและมูลนกโดยไม่ทำให้กระจกเป็นรอย ช่างสวมเสื้อสะท้อนแสงและยืนบนกระเบื้อง ไม่เหยียบแผง"),
         ("ตรวจแรงขันแคลมป์ปลาย (End clamp)", "หลังล้างแผง ขันแคลมป์ปลายทุกตัวด้วยประแจทอร์กตามค่าของผู้ผลิตระบบยึด เพื่อให้แผงยึดแน่นเมื่อมีลมแรง พร้อมตรวจสายดินที่ต่อกับราง"),
         ("ตรวจแรงขันแคลมป์กลาง (Mid clamp)", "แคลมป์กลางระหว่างแผงตรวจด้วยวิธีเดียวกัน ไม่หลวมจนยึดแผงไม่อยู่ และไม่แน่นจนกรอบแผงงอหรือกระจกร้าว")]),
}


def band(t):
    figs = "".join(f'<figure id="{n}"><a href="/images/{n}{SUF}" target="_blank" rel="noopener"><img src="/images/{n}{SUF}" alt="{a}" width="960" height="1280" loading="lazy" decoding="async"></a>'
                   f'<figcaption><b>{a}</b><span>{b}</span></figcaption></figure>' for n, (a, b) in zip(NAMES, t["caps"]))
    return (f'<!--mphotos--><section class="band light" id="on-site" style="padding-block:64px"><div class="wrap"><p class="eyebrow">{t["eyebrow"]}</p>'
            f'<h2 class="svh2">{t["h2"]}</h2><p class="svsub">{t["sub"]}</p><div class="pdgal mp">{figs}</div></div></section><!--/mphotos-->\n')


MCSS = '<style id="mp-css">.pdgal.mp{grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr))}.pdgal.mp a{aspect-ratio:3/4}.pdgal.mp img{object-fit:cover}</style>\n'

if __name__ == "__main__":
    if SRC.exists():
        for i, n in enumerate(NAMES):
            if (SRC / f"{i + 1}.jpg").exists():
                watermark(SRC / f"{i + 1}.jpg", ROOT / "images" / f"{n}{SUF}")
    for lang, path in (("en", "maintenance.html"), ("th", "th/maintenance.html")):
        p = ROOT / path
        s = p.read_text(encoding="utf-8")
        s = re.sub(r"<!--mphotos-->.*?<!--/mphotos-->\n?", "", s, flags=re.S)
        s = re.sub(r'<style id="pd-css">.*?</style>\n?|<style id="mp-css">.*?</style>\n?', "", s, flags=re.S)
        s = s.replace("</head>", CSS + MCSS + "</head>", 1)
        i = s.index('<section class="band" style="padding-block:64px;background:var(--paper)">')
        j = s.index("</section>", i) + len("</section>")
        s = s[:j] + "\n" + band(T[lang]) + s[j:]
        p.write_text(s, encoding="utf-8")
        print("photos on", path)
