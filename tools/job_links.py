# -*- coding: utf-8 -*-
"""Add 'Rate this job' (customer) and 'Send job report' (installer team) links to the end of every
project job post on the Jobs page (EN + TH). Idempotent: lives between <!--jl--> and <!--/jl--> markers.
Run from the repo root after the Jobs page changes:  python3 tools/job_links.py"""
import re, html
from urllib.parse import quote

L = {"job.html": ("", "Customer: rate this job ★", "Installer: send job report"),
     "th/job.html": ("/th", "ลูกค้า: ประเมินงานนี้ ★", "ช่าง: ส่งรายงานจบงาน")}
CSS = ('<style id="jl-css">.jl{display:flex;flex-wrap:wrap;gap:6px 14px;margin-top:10px;padding-top:10px;border-top:1px dashed var(--line,#DEE3ED);font-size:13px}'
       '.jl a{color:var(--mute,#3E548E);font-weight:600;text-decoration:none}.jl a:hover{text-decoration:underline}</style>')
for f, (pre, rate, rep) in L.items():
    h = open(f, encoding="utf-8").read()
    h = re.sub(r"<!--jl-->.*?<!--/jl-->", "", h, flags=re.S)
    def add(m):
        art = m.group(0)
        j = re.search(r'<div class="go"><a [^>]*data-job="([^"]*)"', art)
        if j:
            job = html.unescape(j.group(1))
        else:  # closed / completed job: take the name from its heading
            hd = re.search(r"<h3>(.*?)</h3>", art, re.S)
            if not hd:
                return art
            job = html.unescape(re.sub(r"<[^>]+>", "", hd.group(1))).strip()
        links = (f'<!--jl--><div class="jl"><a href="{pre}/feedback.html">{rate}</a>'
                 f'<a href="{pre}/job-report.html?job={quote(job)}">{rep}</a></div><!--/jl-->')
        return art.replace("</div></div></article>", "</div>" + links + "</div></article>", 1) if art.endswith("</div></div></article>") else art
    h, n = re.subn(r'<article class="card p".*?</article>', add, h, flags=re.S)
    if 'id="jl-css"' not in h:
        h = h.replace("</head>", CSS + "\n</head>", 1)
    open(f, "w", encoding="utf-8").write(h)
    print(f, n, "posts,", h.count('<div class="jl">'), "with links")
