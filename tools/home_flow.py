# -*- coding: utf-8 -*-
"""Marketing order for the home pages (EN/TH/ZH):
hero -> savings calculator -> RESULTS (real bills + reviews + call to action) -> services -> projects -> about -> FAQ -> consultation.
Moves the #bills and #voices blocks out of #projects into a new #results section. Idempotent."""
import re
T = {
 "index.html": dict(eb="Results", h2="Real bills.<br>Real owners.", cta="Book a consultation", call="Call 063 151 6694",
     lede="Before you take our word for it, see what solar did to nine real PEA bills and what owners say about working with us.",
     stat='<div><a href="#voices" style="text-decoration:none"><b>4.7★</b><span>Google rating · 15 reviews</span></a></div>'),
 "th/index.html": dict(eb="ผลลัพธ์จริง", h2="บิลจริง<br>ลูกค้าจริง", cta="ขอคำปรึกษา", call="โทร 063 151 6694",
     lede="ดูบิลค่าไฟจริงจาก 9 สถานที่ก่อนและหลังติดโซลาร์ และเสียงจากเจ้าของระบบที่ทำงานกับเรา",
     stat='<div><a href="#voices" style="text-decoration:none"><b>4.7★</b><span>คะแนน Google · 15 รีวิว</span></a></div>'),
 "zh/index.html": dict(eb="真实成果", h2="真实电费单，<br>真实业主。", cta="预约咨询", call="致电 063 151 6694",
     lede="看看九份真实的 PEA 电费单在安装光伏前后的变化，以及业主对我们的评价。",
     stat='<div><a href="#voices" style="text-decoration:none"><b>4.7★</b><span>Google 评分 · 15 条评价</span></a></div>'),
}
for f, t in T.items():
    h = open(f, encoding="utf-8").read()
    if 'id="results"' in h:
        print("skip", f); continue
    # 1. hero: swap the 4th stat (manufacturer warranty) for the Google rating
    h, n = re.subn(r'(<div class="stats">.*?)<div><b>30[^<]*</b><span>[^<]*</span></div>', lambda m: m.group(1) + t["stat"], h, count=1, flags=re.S)
    assert n == 1, f
    # 2. cut bills + voices out of #projects
    s = h.index('<div class="sub" id="bills">')
    e = h.index('</div></section>', h.index('<div class="sub" id="voices">'))
    block = h[s:e]
    h = h[:s] + h[e:]
    block = block.replace('<div class="sub" id="bills">', '<div class="sub first" id="bills">', 1)
    sec = ('<section class="band light" id="results"><div class="wrap">\n'
           f'<p class="eyebrow">{t["eb"]}</p>\n<h2>{t["h2"]}</h2>\n'
           f'<p class="lede" style="margin-top:18px">{t["lede"]}</p>\n'
           + block +
           f'\n<div class="cta" style="margin-top:44px"><a class="btn" href="#consult">{t["cta"]}</a>'
           f'<a class="btn ghost" href="tel:+66631516694">{t["call"]}</a></div>\n'
           '</div></section>\n\n')
    # 3. place it straight after the calculator
    i = h.index('<section class="band light" id="services">')
    h = h[:i] + sec + h[i:]
    # small CSS: no top rule on the first block
    h = h.replace('.sub{margin-top:72px;', '.sub.first{margin-top:40px;border-top:0;padding-top:0}\n.sub{margin-top:72px;', 1) if '.sub.first' not in h else h
    # .sub.first must come after .sub to win; move rule after
    h = h.replace('.sub.first{margin-top:40px;border-top:0;padding-top:0}\n.sub{margin-top:72px;padding-top:40px;border-top:1.5px solid var(--navy)}',
                  '.sub{margin-top:72px;padding-top:40px;border-top:1.5px solid var(--navy)}\n.sub.first{margin-top:40px;border-top:0;padding-top:0}', 1)
    open(f, "w", encoding="utf-8").write(h)
    print("ok", f)
