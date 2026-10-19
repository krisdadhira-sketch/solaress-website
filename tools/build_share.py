"""Build per-topic share pages so social previews show the topic's own photo.

For every share topic (job card, technical note, news article, FAQ section, pick)
this writes s/<lang>/<page>/<id>.html with its own Open Graph title, description and
image, then sends human visitors on to the real page#id. Topics with a photo use
that photo; topics without one get a generated title card (images/og/...).
Also sets each page's own og:image to the first photo on that page.
Run from the repo root after editing content:  python3 tools/build_share.py
"""
import glob, html, os, re, shutil, hashlib
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from PIL import Image

SITE = 'https://solaress.org'
SEL = '.tnote[id], article[id], section.fsec[id], .cards.fl .card[id], section.pick[id], section.wide[id]'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
LOC = {'en': 'en_US', 'th': 'th_TH', 'zh': 'zh_CN'}
OPEN = {'en': 'Open on solaress.org', 'th': 'เปิดบน solaress.org', 'zh': '在 solaress.org 打开'}

def txt(el):
    return re.sub(r'\s+', ' ', el.get_text(' ', strip=True)).strip() if el else ''

def clip(s, n=200):
    return s if len(s) <= n else s[:n - 1].rsplit(' ', 1)[0] + '…'

def lang_of(path):
    return path.split('/')[0] if '/' in path else 'en'

def page_url(path):
    return SITE + '/' + path

shutil.rmtree('s', ignore_errors=True)
os.makedirs('images/og', exist_ok=True)
cards = []      # (outfile, dict) for title cards to render
made = set()
logo = None

for path in sorted(glob.glob('*.html') + glob.glob('th/*.html') + glob.glob('zh/*.html')):
    raw = open(path, encoding='utf-8').read()
    soup = BeautifulSoup(raw, 'lxml')
    if logo is None:
        li = soup.select_one('header img')
        logo = li['src'] if li else ''
    lang = lang_of(path)
    page = os.path.basename(path)[:-5]
    purl = page_url(path)
    topics = soup.select(SEL)
    first_photo = None
    for el in topics:
        tid = el['id']
        h = el.find(['h2', 'h3'])
        title = txt(h) or txt(soup.title)
        img = el.find('img')
        if el.select_one('.where'):          # job card
            kind = txt(el.select_one('.kind'))
            where = txt(el.select_one('.where'))
            factlist = [(txt(b), txt(b.parent).replace(txt(b), '', 1).strip()) for b in el.select('.facts .fact b')]
            facts = ' · '.join(f'{a} {z}'.strip() for a, z in factlist)
            # job description: scope / deliverables / duties list
            lst = el.select_one('details ul') or el.select_one('.body ul')
            items = [txt(li) for li in lst.find_all('li')] if lst else []
            lbl = el.select_one('details summary')
            lbl = re.sub(r'\s*\(\d+\)\s*$', '', txt(lbl)) if lbl else txt(el.select_one('.lbl'))
            fit = txt(el.select_one('.fit'))
            parts = [f'{title} – {where}' + (f' · {facts}' if facts else '')]
            if fit: parts.append(fit)
            if items: parts.append(f'{lbl}: ' + '; '.join(items))
            desc = clip('. '.join(p.rstrip('.') for p in parts) + '.', 600)
        else:
            p = el.select_one('p.lede') or next((q for q in el.find_all('p') if len(txt(q)) > 40), None)
            desc = txt(p)
            ey = el.select_one('.eyebrow, .kind, .tag')
            kind, where, factlist = txt(ey), '', []
        md = soup.find('meta', attrs={'name': 'description'})
        if not desc: desc = clip(md.get('content', '') if md else '')
        elif not el.select_one('.where'): desc = clip(desc)
        if img and img.get('src') and not img['src'].startswith('data:'):
            iurl = urljoin(purl, img['src'])
            local = iurl.replace(SITE + '/', '')
            try: w, hgt = Image.open(local).size
            except Exception: w = hgt = None
            first_photo = first_photo or (iurl, w, hgt)
        else:
            items = items if el.select_one('.where') else []
            key = hashlib.md5(f'{lang}|{page}|{tid}|{title}|{kind}|{where}|{factlist}|{items[:3]}'.encode()).hexdigest()[:8]
            fn = f'images/og/{lang}-{page}-{tid}-{key}.jpg'
            made.add(fn)
            if not os.path.exists(fn):
                cards.append((fn, dict(lang=lang, title=title, kind=kind, where=where, facts=factlist, desc=desc if not where else '', items=items[:3])))
            iurl, w, hgt = SITE + '/' + fn, 1200, 630
        surl = f'{SITE}/s/{lang}/{page}/{tid}.html'
        target = f'{purl}#{tid}'
        t = html.escape(f'{title} | Solar ESS'); d = html.escape(desc)
        dims = f'<meta property="og:image:width" content="{w}"><meta property="og:image:height" content="{hgt}">' if w else ''
        out = f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t}</title><meta name="description" content="{d}"><meta name="robots" content="noindex,follow"><link rel="canonical" href="{html.escape(target)}">
<meta property="og:type" content="article"><meta property="og:site_name" content="Solar ESS"><meta property="og:title" content="{t}"><meta property="og:description" content="{d}">
<meta property="og:url" content="{surl}"><meta property="og:image" content="{html.escape(iurl)}">{dims}<meta property="og:locale" content="{LOC[lang]}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{t}"><meta name="twitter:description" content="{d}"><meta name="twitter:image" content="{html.escape(iurl)}">
<script>location.replace({target!r})</script></head>
<body style="font-family:sans-serif;padding:24px"><p><a href="{html.escape(target)}">{html.escape(title)} – {OPEN[lang]}</a></p></body></html>'''
        os.makedirs(f's/{lang}/{page}', exist_ok=True)
        open(f's/{lang}/{page}/{tid}.html', 'w', encoding='utf-8').write(out)
    # page-level preview image: first photo on the page (hero stays for pages without one)
    if not first_photo:
        im = next((i for i in soup.select('main img, section img') if i.get('src') and not i['src'].startswith('data:')), None)
        if im:
            u = urljoin(purl, im['src'])
            try: first_photo = (u,) + Image.open(u.replace(SITE + '/', '')).size
            except Exception: first_photo = (u, None, None)
    if first_photo and page not in ('index',):
        new = re.sub(r'<meta property="og:image" content="[^"]*">(<meta property="og:image:(width|height)" content="[^"]*">)*',
                     f'<meta property="og:image" content="{first_photo[0]}">' + (f'<meta property="og:image:width" content="{first_photo[1]}"><meta property="og:image:height" content="{first_photo[2]}">' if first_photo[1] else ''), raw, count=1)
        if new != raw: open(path, 'w', encoding='utf-8').write(new)

# remove stale cards
for f in glob.glob('images/og/*.jpg'):
    if f not in made: os.remove(f)

if cards:
    from playwright.sync_api import sync_playwright
    CSS = '''*{margin:0;box-sizing:border-box}body{width:1200px;height:630px;background:#0A1230;color:#fff;font-family:"Inter","Sarabun","Noto Sans CJK SC","Noto Sans CJK TC",sans-serif;position:relative;overflow:hidden}
    .bar{position:absolute;left:0;top:0;bottom:0;width:14px;background:#FF2D55}.lg{position:absolute;left:64px;top:52px;height:84px;border-radius:10px;background:#fff;padding:6px}
    .lg img{height:72px;display:block}.in{position:absolute;left:64px;right:64px;top:180px}.k{color:#FF2D55;font:600 24px/1.2 "IBM Plex Mono","Inter","Sarabun","Noto Sans CJK SC",monospace;letter-spacing:.08em;text-transform:uppercase}
    h1{font-size:60px;line-height:1.18;font-weight:700;margin-top:18px;max-height:216px;overflow:hidden}.w{font-size:34px;margin-top:22px;opacity:.95}.w:before{content:"";display:inline-block;width:18px;height:18px;border-radius:50%;background:#FF2D55;margin-right:14px}
    .f{display:flex;gap:16px;margin-top:26px}.f div{border:2px solid rgba(255,255,255,.35);border-radius:12px;padding:10px 18px;font-size:26px}.f b{font-size:30px;margin-right:8px}
    .d{font-size:28px;line-height:1.45;margin-top:22px;opacity:.85;max-height:122px;overflow:hidden}.s{margin-top:24px;padding-left:0;list-style:none;font-size:25px;line-height:1.4;opacity:.9}.s li:before{content:"✓  ";color:#FF2D55;font-weight:700}.s li{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:1040px}.u{position:absolute;right:64px;bottom:44px;font-size:26px;opacity:.75;letter-spacing:.04em}'''
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1200, 'height': 630})
        for fn, c in cards:
            facts = ''.join(f'<div><b>{html.escape(a)}</b>{html.escape(z)}</div>' for a, z in c['facts'][:3])
            body = (f'<div class="bar"></div><div class="lg"><img src="{logo}"></div><div class="in">'
                    + (f'<div class="k">{html.escape(c["kind"])}</div>' if c['kind'] else '')
                    + f'<h1>{html.escape(c["title"])}</h1>'
                    + (f'<div class="w">{html.escape(c["where"])}</div>' if c['where'] else '')
                    + (f'<div class="f">{facts}</div>' if facts else '')
                    + (f'<div class="d">{html.escape(c["desc"])}</div>' if c['desc'] else '')
                    + (('<ul class="s">' + ''.join(f'<li>{html.escape(i)}</li>' for i in c['items']) + '</ul>') if c.get('items') else '')
                    + '</div><div class="u">solaress.org</div>')
            pg.set_content(f'<html lang="{c["lang"]}"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>')
            pg.screenshot(path=fn, type='jpeg', quality=80)
        b.close()
print('topics done; cards rendered:', len(cards))
