# -*- coding: utf-8 -*-
"""Add a small "Admin" icon to the end of every project job post on the Jobs page (EN + TH). It opens
/feedback-admin.html?job=<job> where Solar ESS signs in and issues the one-time codes for that job:
one for the installer's job report, one for the customer's feedback. Idempotent: lives between <!--jl--> and <!--/jl--> markers.
Run from the repo root after the Jobs page changes:  python3 tools/job_links.py"""
import re, html
from urllib.parse import quote

L = {"job.html": ("Admin: issue job report & customer feedback"),
     "th/job.html": ("ผู้ดูแล: ออกแบบรายงานจบงานและแบบประเมินลูกค้า")}
CSS = ('<style id="jl-css">.jl{display:flex;justify-content:flex-end;margin-top:8px;font-size:12px}'
       '.card.is-closed{filter:grayscale(1);opacity:.6}.card.is-closed:hover{opacity:.85}.card.is-closed .go a{display:none!important}.closed-tag{display:inline-block;padding:10px 14px;background:#475569;color:#fff;font-weight:700;border-radius:6px}.jl a{display:inline-flex;align-items:center;gap:4px;color:var(--mute,#3E548E);opacity:.55;text-decoration:none}.jl a:hover{opacity:1}.jl a:hover{text-decoration:underline}</style>')
for f, title in L.items():
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
        pid = (re.search(r'<article class="card p" id="([^"]+)"', art) or [None, ""])[1]
        links = (f'<!--jl--><div class="jl"><a href="/feedback-admin.html?job={quote(job)}&amp;post={quote(pid)}" title="{title}" aria-label="{title}" rel="nofollow">'
                 '<svg viewBox="0 0 24 24" width="15" height="15" aria-hidden="true"><path fill="currentColor" d="M19.4 13a7.5 7.5 0 0 0 0-2l2-1.6-2-3.4-2.4 1a7.6 7.6 0 0 0-1.7-1L15 3.5h-4l-.4 2.5a7.6 7.6 0 0 0-1.7 1l-2.4-1-2 3.4L6.6 11a7.5 7.5 0 0 0 0 2l-2 1.6 2 3.4 2.4-1c.5.4 1.1.7 1.7 1l.4 2.5h4l.4-2.5c.6-.3 1.2-.6 1.7-1l2.4 1 2-3.4zM13 15.5a3.5 3.5 0 1 1 0-7 3.5 3.5 0 0 1 0 7z" transform="translate(-1 0)"/></svg> Admin</a></div><!--/jl-->')
        return art.replace("</div></div></article>", "</div>" + links + "</div></article>", 1) if art.endswith("</div></div></article>") else art
    h, n = re.subn(r'<article class="card p".*?</article>', add, h, flags=re.S)
    h = re.sub(r'<style id="jl-css">.*?</style>\n?', '', h, flags=re.S)
    if True:
        h = h.replace("</head>", CSS + "\n</head>", 1)
    # live status of each post (closed = greyed with a label, hidden = removed), set from the job admin page
    h = re.sub(r"<!--jls-->.*?<!--/jls-->\n?", "", h, flags=re.S)
    tag = "ปิดรับแล้ว – งานเสร็จสิ้น" if f.startswith("th/") else "Closed – job completed"
    js = ("<!--jls--><script>(function(){fetch('/api/feedback?a=posts').then(function(r){return r.ok?r.json():{posts:{}}}).then(function(d){var P=d.posts||{};"
          "Object.keys(P).forEach(function(id){var a=document.getElementById(id);if(!a||!a.classList.contains('card'))return;"
          "var name=(a.querySelector('.go a[data-job]')||{}).getAttribute?a.querySelector('.go a[data-job]').getAttribute('data-job'):'';"
          "if(P[id].state==='hidden'){a.style.display='none'}else{a.classList.add('is-closed');var g=a.querySelector('.go');"
          "if(g&&!g.querySelector('.closed-tag,.closed')){var t=document.createElement('span');t.className='closed-tag';t.textContent=" + repr(tag) + ";g.appendChild(t)}}"
          "if(name){[].forEach.call(document.querySelectorAll('#j-role option'),function(o){if(o.textContent===name)o.disabled=true})}})}).catch(function(){})})();</script><!--/jls-->\n")
    h = h.replace("</body>", js + "</body>", 1)
    open(f, "w", encoding="utf-8").write(h)
    print(f, n, "posts,", h.count('<div class="jl">'), "with links")
