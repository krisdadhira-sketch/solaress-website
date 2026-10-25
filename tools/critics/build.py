#!/usr/bin/env python3
"""Rebuild the video section of critics.html (EN/TH/ZH) from the summary JSON files."""
import json, re, glob, html, sys

import os
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', '..')
WORK = HERE

TH_MONTHS = {'ม.ค.':1,'ก.พ.':2,'มี.ค.':3,'เม.ย.':4,'พ.ค.':5,'มิ.ย.':6,'ก.ค.':7,'ส.ค.':8,'ก.ย.':9,'ต.ค.':10,'พ.ย.':11,'ธ.ค.':12}
EN_M = ['January','February','March','April','May','June','July','August','September','October','November','December']
TH_M = ['มกราคม','กุมภาพันธ์','มีนาคม','เมษายน','พฤษภาคม','มิถุนายน','กรกฎาคม','สิงหาคม','กันยายน','ตุลาคม','พฤศจิกายน','ธันวาคม']

meta = {}
for line in open(f'{WORK}/meta.txt', encoding='utf-8'):
    line = line.strip()
    if not line: continue
    vid, d, dur, th_title = line.split('|', 3)
    day, mon, yr = d.split(' ')
    meta[vid] = dict(day=int(day), mon=TH_MONTHS[mon], yr=int(yr), dur=dur, title_th=th_title)

videos = []
for f in sorted(glob.glob(f'{WORK}/sum_*.json')):
    videos += json.load(open(f, encoding='utf-8'))
order = [l.split('|')[0] for l in open(f'{WORK}/meta.txt', encoding='utf-8') if l.strip()]
byid = {v['id']: v for v in videos}
missing = [i for i in order if i not in byid]
if missing:
    print('MISSING summaries:', missing); sys.exit(1)

TOPICS = ['solar', 'prices', 'lng', 'climate', 'ev', 'governance']
L = {
 'en': dict(all='All', solar='Solar & batteries', prices='Electricity prices & policy', lng='LNG, gas & oil',
            climate='Climate', ev='EVs & transport', governance='Society & governance',
            search='Search the summaries', ph='e.g. LNG, battery, Australia', summary='Summary',
            more='Show more videos', shown='Showing {n} of {t} videos', none='No video matches. Try another word or topic.',
            play='Play video', credit='Summary written by Solar ESS from the video and its description.',
            intro='The videos are in Thai. Each one has a short English summary first; press play to watch. Newest first.'),
 'th': dict(all='ทั้งหมด', solar='โซลาร์และแบตเตอรี่', prices='ค่าไฟและนโยบายพลังงาน', lng='LNG ก๊าซและน้ำมัน',
            climate='โลกร้อน', ev='รถยนต์ไฟฟ้า', governance='ธรรมาภิบาลและสังคม',
            search='ค้นหาในสรุป', ph='เช่น LNG แบตเตอรี่ ออสเตรเลีย', summary='สรุปเนื้อหา',
            more='ดูคลิปเพิ่มเติม', shown='แสดง {n} จาก {t} คลิป', none='ไม่พบคลิปที่ตรงกัน ลองคำอื่นหรือหัวข้ออื่น',
            play='เล่นคลิป', credit='สรุปโดยบริษัท โซลาร์ เอสส์ จำกัด จากคลิปและคำอธิบายคลิป',
            intro='แต่ละคลิปมีสรุปเนื้อหาสั้น ๆ ก่อน กดเล่นเพื่อดูคลิป เรียงจากคลิปล่าสุด'),
 'zh': dict(all='全部', solar='太阳能与储能', prices='电价与能源政策', lng='LNG、天然气与石油',
            climate='气候', ev='电动车与交通', governance='治理与社会',
            search='搜索摘要', ph='例如：LNG、电池、澳大利亚', summary='摘要',
            more='显示更多视频', shown='显示 {n} / {t} 个视频', none='没有匹配的视频，请换个关键词或主题。',
            play='播放视频', credit='摘要由 Solar ESS 根据视频及其说明撰写。',
            intro='视频为泰语。每个视频先附中文摘要，点击播放即可观看。按最新排序。'),
}

def date_str(lang, m):
    if lang == 'en': return f"{m['day']} {EN_M[m['mon']-1]} {m['yr']}"
    if lang == 'th': return f"{m['day']} {TH_M[m['mon']-1]} {m['yr']}"
    return f"{m['yr']}年{m['mon']}月{m['day']}日"

def dur_str(lang, d):
    return {'en': f'{d} · in Thai', 'th': f'{d} นาที', 'zh': f'{d} · 泰语'}[lang]

esc = lambda s: html.escape(s, quote=True)

def existing_first(lang_html):
    """Keep the existing UV8XIDNeP_w article's content (already summarised by hand)."""
    m = re.search(r'<article id="v-UV8XIDNeP_w".*?</article>', lang_html, re.S)
    a = m.group(0)
    title = re.search(r'<h3[^>]*>(.*?)</h3>', a, re.S).group(1)
    thai = re.search(r'<p lang="th"[^>]*>(.*?)</p>', a, re.S)
    lis = re.findall(r'<li>(.*?)</li>', a, re.S)
    return dict(title=title, thai=thai.group(1) if thai else '', lis=lis)

def article(lang, vid, title, thai_sub, bullets_html, m, topic, first=False):
    t = L[lang]
    sub = f'<p lang="th" class="vth">{thai_sub}</p>' if thai_sub else ''
    search = re.sub(r'<[^>]+>', ' ', title + ' ' + thai_sub + ' ' + ' '.join(bullets_html)).lower()
    return (f'<article id="v-{vid}" class="vid" data-topic="{topic}" data-s="{esc(search)}">'
            f'<p class="eyebrow">{date_str(lang, m)} · {dur_str(lang, m["dur"])} · <span class="tag">{t[topic]}</span></p>'
            f'<h3>{title}</h3>{sub}'
            f'<h4>{t["summary"]}</h4><ul>' + ''.join(f'<li>{b}</li>' for b in bullets_html) + '</ul>'
            f'<button type="button" class="yt" data-id="{vid}" aria-label="{t["play"]}: {esc(re.sub("<[^>]+>","",title))}">'
            f'<img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="" loading="lazy" width="480" height="360"><span class="pl" aria-hidden="true"></span></button>'
            '</article>')

CSS = """<style id="vid-css">
.vbar{padding:14px 0 12px;margin-top:28px;border-bottom:1px solid var(--line)}
.vbar label{display:block;font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--mute);margin-bottom:6px}
.vbar input{width:100%;font:inherit;font-size:16px;padding:11px 14px;border:1.5px solid var(--line);background:var(--white);color:var(--ink)}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
.chips button{font-family:var(--mono);font-size:12px;letter-spacing:.06em;padding:7px 12px;border:1.5px solid var(--line);background:var(--white);color:var(--ink);cursor:pointer}
.chips button[aria-pressed="true"]{background:var(--navy);border-color:var(--navy);color:var(--white)}
.vcount{font-family:var(--mono);font-size:12px;color:var(--mute);margin-top:10px}
.vid{margin-top:36px;padding-top:30px;border-top:1px solid var(--line)}
.vbar+.vid{border-top:0;margin-top:12px}
.vid h3{font-size:clamp(21px,2.8vw,28px)}
.vid .vth{margin-top:6px;opacity:.7;font-family:var(--thai)}
.vid h4{margin:20px 0 8px;font-family:var(--mono);font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--mute)}
.vid ul{margin:0;padding-left:20px;display:grid;gap:8px;max-width:70ch}
.vid .tag{color:var(--mute)}
.yt{position:relative;display:block;width:100%;aspect-ratio:16/9;margin-top:20px;padding:0;border:0;background:#000;cursor:pointer;overflow:hidden}
.yt img{width:100%;height:100%;object-fit:cover;opacity:.85;display:block}
.yt:hover img{opacity:1}
.yt .pl{position:absolute;left:50%;top:50%;width:72px;height:50px;margin:-25px 0 0 -36px;background:var(--hot);border-radius:12px}
.yt .pl::after{content:"";position:absolute;left:29px;top:15px;border-style:solid;border-width:10px 0 10px 17px;border-color:transparent transparent transparent #fff}
.yt iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.vid[hidden]{display:none}
#vmore{margin-top:32px}
.vnone{margin-top:28px;opacity:.75}
</style>"""

JS = """<script id="vid-js">
(function(){
var PAGE=15,shown=PAGE,topic='all',q='';
var list=[].slice.call(document.querySelectorAll('.vid')),more=document.getElementById('vmore'),cnt=document.getElementById('vcount'),none=document.getElementById('vnone'),inp=document.getElementById('vq');
var tpl=cnt.getAttribute('data-t');
function render(){var m=list.filter(function(a){return (topic==='all'||a.getAttribute('data-topic')===topic)&&(!q||a.getAttribute('data-s').indexOf(q)>-1)});
 var lim=(q||topic!=='all')?m.length:shown;
 list.forEach(function(a){a.hidden=true});m.slice(0,lim).forEach(function(a){a.hidden=false});
 more.hidden=lim>=m.length;none.hidden=m.length>0;cnt.textContent=tpl.replace('{n}',Math.min(lim,m.length)).replace('{t}',m.length);}
more.addEventListener('click',function(){shown+=PAGE;render()});
inp.addEventListener('input',function(){q=inp.value.trim().toLowerCase();render()});
[].forEach.call(document.querySelectorAll('.chips button'),function(b){b.addEventListener('click',function(){topic=b.getAttribute('data-t');[].forEach.call(document.querySelectorAll('.chips button'),function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});render()})});
document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.yt');if(!b||b.querySelector('iframe'))return;var f=document.createElement('iframe');f.src='https://www.youtube-nocookie.com/embed/'+b.getAttribute('data-id')+'?autoplay=1&rel=0';f.title=b.getAttribute('aria-label');f.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';f.referrerPolicy='strict-origin-when-cross-origin';f.allowFullscreen=true;b.appendChild(f);});
var h=location.hash.match(/^#v-([\\w-]{11})$/);if(h){var a=document.getElementById('v-'+h[1]);if(a){shown=list.indexOf(a)+1;render();a.scrollIntoView();return}}
render();})();
</script>"""

def build(lang, path):
    src = open(path, encoding='utf-8').read()
    t = L[lang]
    first = existing_first(src)
    arts = []
    # existing hand-written first video (24/25 Oct 2026)
    m0 = dict(day=24, mon=10, yr=2026, dur='5:41')
    arts.append(article(lang, 'UV8XIDNeP_w', first['title'], first['thai'], first['lis'], m0, 'solar'))
    for vid in order:
        v, m = byid[vid], meta[vid]
        if lang == 'en': title, sub = esc(v['title_en']), esc(m['title_th'])
        elif lang == 'zh': title, sub = esc(v['title_zh']), esc(m['title_th'])
        else: title, sub = esc(m['title_th']), ''
        bl = [esc(b) for b in v['sum_' + lang]]
        arts.append(article(lang, vid, title, sub, bl, m, v['topic']))
    total = len(arts)
    chips = f'<button type="button" data-t="all" aria-pressed="true">{t["all"]}</button>' + ''.join(
        f'<button type="button" data-t="{k}" aria-pressed="false">{t[k]}</button>' for k in TOPICS)
    bar = (f'<div class="vbar"><label for="vq">{t["search"]}</label><input id="vq" type="search" placeholder="{esc(t["ph"])}" autocomplete="off">'
           f'<div class="chips" role="group" aria-label="Topics">{chips}</div>'
           f'<p class="vcount" id="vcount" data-t="{esc(t["shown"])}" aria-live="polite"></p></div>')
    section_m = re.search(r'(<section class="band light"[^>]*><div class="wrap"[^>]*>\s*<h2.*?</h2>)<p[^>]*>.*?</p>.*?(<p style="margin-top:24px"><a class="btn")', src, re.S)
    head, tail_start = section_m.group(1), section_m.start(2)
    intro = f'<p style="margin-top:10px;opacity:.8">{t["intro"]}</p><p style="margin-top:6px;font-size:13px;opacity:.65">{t["credit"]}</p>'
    body = (head + intro + bar + '\n' + '\n'.join(arts) + '\n'
            + f'<p class="vnone" id="vnone" hidden>{t["none"]}</p>'
            + f'<button type="button" class="btn ghost" id="vmore">{t["more"]}</button>\n')
    out = src[:section_m.start(1)] + body + src[tail_start:]
    # styles + script (idempotent)
    out = re.sub(r'<style id="vid-css">.*?</style>', '', out, flags=re.S)
    out = re.sub(r'<script id="vid-js">.*?</script>', '', out, flags=re.S)
    out = out.replace('</head>', CSS + '\n</head>', 1)
    out = out.replace('</body>', JS + '\n</body>', 1)
    # fix canonical / hreflang (were pointing at /news)
    pre = {'en': '', 'th': '/th', 'zh': '/zh'}[lang]
    out = out.replace(f'<link rel="canonical" href="https://solaress.org{pre}/news">', f'<link rel="canonical" href="https://solaress.org{pre}/critics">')
    for p, hl in (('', 'en'), ('/th', 'th'), ('/zh', 'zh-Hans'), ('', 'x-default')):
        out = out.replace(f'<link rel="alternate" hreflang="{hl}" href="https://solaress.org{p}/news">', f'<link rel="alternate" hreflang="{hl}" href="https://solaress.org{p}/critics">')
    out = out.replace(f'content="https://solaress.org{pre}/critics.html"', f'content="https://solaress.org{pre}/critics"')
    open(path, 'w', encoding='utf-8').write(out)
    return total

for lang, p in (('en', 'critics.html'), ('th', 'th/critics.html'), ('zh', 'zh/critics.html')):
    print(lang, build(lang, f'{SITE}/{p}'), 'videos')
