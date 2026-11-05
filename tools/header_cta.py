# -*- coding: utf-8 -*-
"""Add a 'Book consultation' button to the top bar of every page (EN/TH/ZH), visible on desktop and mobile.
Idempotent: lives between <!--hcta--> and <!--/hcta--> right after </nav> inside header.nav. Run: python3 tools/header_cta.py"""
import glob, re
L = {"en": ("/#consult", "Book consultation", "Book"),
     "th": ("/th/#consult", "ขอคำปรึกษา", "ปรึกษา"),
     "zh": ("/zh/#consult", "预约咨询", "咨询")}
CSS = ('<style id="hcta-css">.hcta{display:inline-flex;align-items:center;margin-left:4px;padding:10px 16px;background:var(--hot,#FF2D55);'
       'color:#fff!important;font-family:var(--mono,monospace);font-size:12px;letter-spacing:.1em;text-transform:uppercase;text-decoration:none;'
       'white-space:nowrap;border:1.5px solid var(--hot,#FF2D55)}.hcta:hover{background:transparent}.hcta .s{display:none}'
       '@media (max-width:900px){.hcta{order:3;margin-left:0;height:44px;padding:0 14px;border-radius:10px;font-size:13px}.mnav-btn{order:2}.hcta .l{display:none}.hcta .s{display:inline}}'
       '</style>')
n = 0
for f in sorted(glob.glob("*.html") + glob.glob("th/*.html") + glob.glob("zh/*.html")):
    h = open(f, encoding="utf-8").read()
    if '<header class="nav">' not in h or "</nav>" not in h:
        continue
    lang = "th" if f.startswith("th/") else "zh" if f.startswith("zh/") else "en"
    href, long_, short = L[lang]
    if f.endswith("index.html"):
        href = "#consult"
    blk = f'<!--hcta--><a class="hcta" href="{href}"><span class="l">{long_}</span><span class="s">{short}</span></a><!--/hcta-->'
    h = re.sub(r"<!--hcta-->.*?<!--/hcta-->", "", h, flags=re.S)
    hs = h.index('<header class="nav">'); ne = h.index("</nav>", hs) + len("</nav>")
    h = h[:ne] + blk + h[ne:]
    if 'id="hcta-css"' not in h:
        h = h.replace("</head>", CSS + "\n</head>", 1)
    open(f, "w", encoding="utf-8").write(h); n += 1
print(n, "pages")
