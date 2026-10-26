#!/usr/bin/env python3
"""Add/refresh FAQPage JSON-LD on faq pages from their <details><summary>Q</summary><div class="a">A</div></details> blocks.
Run after editing any FAQ: python3 tools/faq_schema.py"""
import re, json, html, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
def clean(x):
    x = re.sub(r'<br\s*/?>', ' ', x); x = re.sub(r'<[^>]+>', '', x)
    return re.sub(r'\s+', ' ', html.unescape(x)).strip()
for p in ('faq.html', 'th/faq.html', 'zh/faq.html'):
    f = os.path.join(ROOT, p); s = open(f, encoding='utf-8').read()
    qa = re.findall(r'<details[^>]*>\s*<summary[^>]*>(.*?)</summary>\s*<div class="a"[^>]*>(.*?)</div>\s*</details>', s, re.S)
    data = {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": clean(q), "acceptedAnswer": {"@type": "Answer", "text": clean(a)}} for q, a in qa]}
    tag = '<script type="application/ld+json" id="faq-ld">' + json.dumps(data, ensure_ascii=False).replace('</', '<\\/') + '</script>'
    s = re.sub(r'<script type="application/ld\+json" id="faq-ld">.*?</script>\n?', '', s, flags=re.S)
    s = s.replace('</head>', tag + '\n</head>', 1)
    open(f, 'w', encoding='utf-8').write(s); print(p, len(qa), 'questions')
