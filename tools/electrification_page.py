#!/usr/bin/env python3
"""Build /electrification-who-pays (EN/TH) from tools/electrification_content.py. Run: python3 tools/electrification_page.py"""
import html, json, os, re
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'); os.chdir(ROOT)
UPDATED_ISO = '2026-10-27'
import sys; sys.path.insert(0, os.path.join(ROOT, "tools"))
from electrification_content import EN, TH, SRC
C = {"en": EN, "th": TH}

def build(lang):
    c = C[lang]; e = lambda x: html.escape(x, quote=True)
    shell = open({'th': 'th/news.html', 'zh': 'zh/news.html'}.get(lang, 'news.html'), encoding='utf-8').read()
    he = shell.find('</head>'); bs = shell.find('<section', shell.find('<body')); ft = shell.find('<footer')
    head = shell[:he]
    head = re.sub(r'<title>.*?</title>', f'<title>{e(c["title"])}</title>', head, flags=re.S)
    head = re.sub(r'(<meta (?:property|name)="(?:og:title|twitter:title)" content=")[^"]*"', lambda m: m.group(1) + e(c['title']) + '"', head)
    head = re.sub(r'(<meta (?:property|name)="(?:description|og:description|twitter:description)" content=")[^"]*"', lambda m: m.group(1) + e(c['desc']) + '"', head)
    head = re.sub(r'<meta property="og:type" content="[^"]*">', '<meta property="og:type" content="article">', head)
    head = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{c["url"]}">', head)
    head = re.sub(r'<link rel="canonical"[^>]*>', f'<link rel="canonical" href="{c["url"]}">', head)
    head = re.sub(r'<link rel="alternate" hreflang="[^"]*"[^>]*>\n?', '', head)
    head = re.sub(r'<script type="application/ld\+json"[^>]*>.*?</script>\n?', '', head, flags=re.S)
    head = re.sub(r'<style id="(ntopics|poll)-css">.*?</style>\n?', '', head, flags=re.S)
    head += ('<link rel="alternate" hreflang="th" href="https://solaress.org/th/electrification-who-pays">\n'
             '<link rel="alternate" hreflang="en" href="https://solaress.org/electrification-who-pays">\n'
             '<link rel="alternate" hreflang="x-default" href="https://solaress.org/electrification-who-pays">\n')
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": c['title'].split(' | ')[0], "description": c['desc'],
           "inLanguage": lang, "datePublished": "2026-10-27", "dateModified": UPDATED_ISO, "mainEntityOfPage": c['url'],
           "author": {"@type": "Organization", "name": "Solar ESS", "url": "https://solaress.org/"},
           "publisher": {"@type": "Organization", "name": "Solar ESS Co. Ltd.", "url": "https://solaress.org/"},
           "citation": [u for t, u in SRC]},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": c['crumb_home'], "item": "https://solaress.org" + c['home']},
              {"@type": "ListItem", "position": 2, "name": c['crumb_news'], "item": "https://solaress.org" + c['news']},
              {"@type": "ListItem", "position": 3, "name": c['title'].split(' | ')[0], "item": c['url']}]}]
    for d in ld:
        head += '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False).replace('</', '<\\/') + '</script>\n'
    head += ('<style>.lf h2{font-size:clamp(26px,3.6vw,38px);margin-top:56px;padding-top:28px;border-top:1.5px solid var(--navy)}'
             '.lf h3{font-size:20px;margin-top:28px}.lf p{margin-top:12px}.lf .kf{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin-top:8px}'
             '.lf .kf div{border:1.5px solid var(--line);background:var(--white);padding:14px 16px}.lf .kf b{display:block;font-family:var(--display);font-size:26px;color:var(--navy)}'
             '.lf .kf span{font-size:14px;color:var(--mute)}.lf .toc{margin-top:24px;display:flex;flex-wrap:wrap;gap:8px}.lf .toc a{border:1.5px solid var(--navy);padding:6px 12px;font-size:14px;text-decoration:none}'
             '.lf table{width:100%;border-collapse:collapse;margin-top:14px;font-size:15px;background:var(--white)}.lf th,.lf td{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}.lf th{background:var(--navy);color:var(--white)}.lf .tw{overflow-x:auto}'
             '.lf ul.check{list-style:none;padding-left:0;display:grid;gap:8px;margin-top:12px}.lf ul.check li:before{content:"☐ ";color:var(--hot)}'
             '.lf .crumb{font-family:var(--mono);font-size:12px;opacity:.75;margin-bottom:12px}.lf .crumb a{text-decoration:none}.lf ol.books{font-size:16px;gap:10px}.lf ol{padding-left:22px;font-size:14px;display:grid;gap:6px;margin-top:12px}</style>\n')
    out = [head, shell[he:bs]]
    out.append(f'<section class="dark band" style="padding-block:64px"><div class="wrap lf"><p class="crumb"><a href="{c["home"]}">{c["crumb_home"]}</a> › <a href="{c["news"]}">{c["crumb_news"]}</a></p>'
               f'<p class="eyebrow">{c["updated"]}</p><h1 style="font-size:clamp(34px,5.6vw,60px)">{c["h1"]}</h1>'
               f'<p class="lede" style="margin-top:18px">{c["lede"]}</p></div></section>\n')
    b = ['<section class="band light" style="padding-block:56px"><div class="wrap lf"><article style="max-width:760px">',
         '<div class="kf">' + ''.join(f'<div><b>{a}</b><span>{s}</span></div>' for a, s in c['kf']) + '</div>',
         f'<nav class="toc" aria-label="{e(c["toc"])}">' + ''.join(f'<a href="#{sid}">{h}</a>' for sid, h, _ in c['sections']) + '</nav>']
    for sid, h, subs in c['sections']:
        b.append(f'<h2 id="{sid}">{h}</h2>')
        for sh, paras in subs:
            if sh: b.append(f'<h3>{sh}</h3>')
            b += [p[4:] if p.startswith('RAW:') else f'<p>{p}</p>' for p in paras]
    b.append(f'<p style="margin-top:36px;font-size:14px;color:var(--mute)">{c["note"]}</p>')
    b.append(f'<h2 style="font-size:22px">{c["src_h"]}</h2><ol>' + ''.join(f'<li><a href="{u}" rel="noopener">{e(t)}</a></li>' for t, u in SRC) + '</ol>')
    b.append(f'<p style="margin-top:28px"><a class="btn ghost" href="{c["backurl"]}">← {c["back"]}</a></p>')
    b.append('</article></div></section>\n')
    out += b
    tail = shell[ft:]
    tail = re.sub(r'<script id="(ntopics|poll)-js">.*?</script>\n?', '', tail, flags=re.S)
    out.append(tail)
    open(c['out'], 'w', encoding='utf-8').write(''.join(out)); print('wrote', c['out'])

if __name__ == "__main__":
    for l in C: build(l)
