#!/usr/bin/env python3
"""Make the downloadable PDFs of the data-centre impacts guide (EN/TH/ZH) from the same
content as the web pages. Solar ESS logo top-left and company address top-right on every page.
Needs Playwright (Chromium) and the Sarabun font in tools/fonts/ (Thai) and Noto Sans CJK SC (system).
Run: python3 tools/dc_impacts_pdf.py"""
import base64, html, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dc_impacts_page import C, SRC, PDF, ROOT
os.chdir(ROOT)

FONTS = os.path.join(ROOT, 'tools', 'fonts')
LOGO = 'data:image/jpeg;base64,' + base64.b64encode(open('images/solar-ess-report-logo.jpg', 'rb').read()).decode()
ADDR = {
 'en': 'Solar ESS Co. Ltd.<br>53 Moo 2 Tambon Nanglae, Amphoe Muang, Chiang Rai 57100<br>Tel 063 151 6694, 089 632 5829 · LINE solaress1<br>www.solaress.org · www.โซลาร์เอสส์.com',
 'th': 'บริษัท โซลาร์ เอสส์ จำกัด<br>53 หมู่ 2 ต.นางแล อ.เมือง จ.เชียงราย 57100<br>โทร 063 151 6694, 089 632 5829 · LINE solaress1<br>www.solaress.org · www.โซลาร์เอสส์.com',
 'zh': 'Solar ESS Co. Ltd.<br>53 Moo 2 Tambon Nanglae, Amphoe Muang, Chiang Rai 57100<br>电话 063 151 6694, 089 632 5829 · LINE solaress1<br>www.solaress.org · www.โซลาร์เอสส์.com',
}
FAM = {'en': "'Sarabun', sans-serif", 'th': "'Sarabun', sans-serif", 'zh': "'Noto Sans CJK SC', 'Sarabun', sans-serif"}
PAGE = {'en': 'Page', 'th': 'หน้า', 'zh': '第'}

def strip_links(x):
    # keep link text, show internal links as full URLs so they work in print
    return re.sub(r'<a href="(/[^"]*)">([^<]*)</a>', lambda m: f'{m.group(2)} (solaress.org{m.group(1).replace(".html", "")})', x)

def doc(lang):
    c = C[lang]
    css = f"""@font-face{{font-family:'Sarabun';src:url('file://{FONTS}/Sarabun-Regular.ttf')}}
@font-face{{font-family:'Sarabun';font-weight:bold;src:url('file://{FONTS}/Sarabun-Bold.ttf')}}
body{{font-family:{FAM[lang]};font-size:10.5pt;line-height:1.55;color:#141a33;margin:0}}
h1{{font-size:24pt;line-height:1.15;margin:0 0 8px;color:#0b1433}} h2{{font-size:15pt;margin:22px 0 4px;padding-top:10px;border-top:1.5px solid #0b1433;color:#0b1433;page-break-after:avoid}}
h3{{font-size:11.5pt;margin:12px 0 2px;page-break-after:avoid}} p{{margin:5px 0}} .eyebrow{{color:#e8304f;font-size:9pt;letter-spacing:.05em}}
.lede{{font-size:11.5pt}} .kf{{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:12px 0}} .kf div{{border:1px solid #c9cdd8;padding:8px}}
.kf b{{display:block;font-size:14pt;color:#0b1433}} .kf span{{font-size:8.5pt;color:#555}}
table{{width:100%;border-collapse:collapse;margin:8px 0;font-size:9.5pt;page-break-inside:avoid}} th,td{{border:1px solid #c9cdd8;padding:5px 7px;text-align:left;vertical-align:top}} th{{background:#0b1433;color:#fff}}
ol{{padding-left:20px}} ol.src{{font-size:8.5pt}} ol.src a{{color:#141a33;word-break:break-all}} small{{color:#555;font-size:8.5pt}} .note{{color:#555;font-size:9pt;margin-top:14px}}"""
    b = [f'<p class="eyebrow">{c["updated"]}</p><h1>{re.sub("<br>", " ", c["h1"])}</h1><p class="lede">{c["lede"]}</p>',
         '<div class="kf">' + ''.join(f'<div><b>{a}</b><span>{s}</span></div>' for a, s in c['kf']) + '</div>']
    for sid, h, subs in c['sections']:
        b.append(f'<h2>{h}</h2>')
        for sh, paras in subs:
            if sh: b.append(f'<h3>{sh}</h3>')
            for p in paras:
                p = strip_links(p)
                b.append(p[4:] if p.startswith('RAW:') else f'<p>{p}</p>')
    b.append(f'<p class="note">{c["note"]}</p>')
    b.append(f'<h2>{c["src_h"]}</h2><ol class="src">' + ''.join(f'<li>{html.escape(t)} – <a href="{u}">{u}</a></li>' for t, u in SRC) + '</ol>')
    b.append(f'<p class="note">{c["url"]}</p>')
    return f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><style>{css}</style></head><body>{"".join(b)}</body></html>'

def header(lang):
    return (f'<div style="width:100%;padding:0 14mm;display:flex;justify-content:space-between;align-items:flex-start;font-family:{FAM[lang]};font-size:7.5px;color:#333">'
            f'<img src="{LOGO}" style="height:15mm"><div style="text-align:right;line-height:1.35">{ADDR[lang]}</div></div>')

def footer(lang):
    pg = '第 <span class="pageNumber"></span> 页' if lang == 'zh' else f'{PAGE[lang]} <span class="pageNumber"></span> / <span class="totalPages"></span>'
    return f'<div style="width:100%;padding:0 14mm;font-family:{FAM[lang]};font-size:7.5px;color:#666;display:flex;justify-content:space-between"><span>{html.escape(C[lang]["title"].split(" | ")[0])}</span><span>{pg}</span></div>'

if __name__ == '__main__':
    from playwright.sync_api import sync_playwright
    tmp = os.path.join(ROOT, 'tools', '.pdf_tmp'); os.makedirs(tmp, exist_ok=True)
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        for lang in ('en', 'th', 'zh'):
            f = os.path.join(tmp, f'{lang}.html'); open(f, 'w', encoding='utf-8').write(doc(lang))
            pg = br.new_page(); pg.goto('file://' + f); pg.wait_for_timeout(500)
            out = PDF[lang]
            if os.path.exists(out): sys.exit(f'{out} exists – bump the revision number in PDF (never overwrite)')
            pg.pdf(path=out, format='A4', print_background=True, display_header_footer=True,
                   header_template=header(lang), footer_template=footer(lang),
                   margin={'top': '30mm', 'bottom': '16mm', 'left': '14mm', 'right': '14mm'})
            print('wrote', out, os.path.getsize(out) // 1024, 'KB')
        br.close()
    import shutil; shutil.rmtree(tmp)
