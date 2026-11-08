# -*- coding: utf-8 -*-
"""Accessibility (WCAG 2.1 AA) and reach for every page of www.solaress.org. Idempotent.
- "Skip to content" link and a <main id="main"> landmark (between the header and the footer).
- Contrast fixes: accent text on dark bands in light violet, share/LINE/WhatsApp/Facebook buttons in darker
  brand shades so white text is readable, a few low-contrast greys.
- Respects "reduce motion"; clearer keyboard focus.
- /js/a11y.js: "More languages" (Google machine translation: Lao, Burmese, Khmer, Vietnamese, ... ) in the
  language switcher, and a one-time suggestion to switch to the visitor's own language (EN / TH / ZH).
The site accent colour is violet-blue #5B5BD6 (was red-pink #FF2D55).
Run after adding or regenerating pages:  python3 tools/accessibility.py"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {"googlef2e2bf45e07052f3.html"}
LABEL = {"en": "Skip to content", "th": "ข้ามไปยังเนื้อหา", "zh": "跳到正文"}

CSS = """<style id="a11y-css">
.skip{position:absolute;left:12px;top:-60px;z-index:1000;background:#fff;color:#0A1230;padding:10px 16px;border-radius:8px;font:600 15px system-ui,sans-serif;text-decoration:none;box-shadow:0 4px 14px rgba(0,0,0,.3)}
.skip:focus{top:12px;outline:3px solid #5B5BD6;outline-offset:2px}
main#main:focus{outline:0}
:focus-visible{outline:3px solid #5B5BD6;outline-offset:3px}
.dark :focus-visible,.nav :focus-visible,footer :focus-visible{outline-color:#A5B4FC}
.dark .eyebrow,.dark .k,.dark legend,.nav nav a:hover,footer a:hover,.dark [style*="color:var(--hot)"],.dark [style*="color:#5B5BD6"]{color:#A5B4FC!important}
.about .eyebrow,[style*="background:var(--sky)"] .eyebrow{color:#4338CA}
.ssh a[aria-label*="LINE"],.fab a[href*="line.me"]{background:#0B7A3E!important}
.ssh a[aria-label*="WhatsApp"]{background:#0B7A3E!important}
.ssh a[aria-label*="Facebook"],.fab a[href*="facebook.com"]{background:#1460C8!important}
.jl a,.facts .fact,.card details li,.card .fit,#bills .note{color:#4B5A85!important;opacity:1!important}
.pf-num,.about .eyebrow{color:#4338CA!important}
.dark .pf-num{color:#A5B4FC!important}
.dark .hint,.evpromo .eyebrow,.alliance .eyebrow,[style*="background:var(--navy)"] .eyebrow,[style*="background:#0A1230"] .eyebrow{color:#A5B4FC!important}
.langsw .ml-sel{font:inherit;font-size:11px;letter-spacing:.06em;background:transparent;color:inherit;border:1px solid rgba(255,255,255,.35);border-radius:6px;padding:3px 4px;max-width:150px;cursor:pointer}
.langsw .ml-sel option{color:#0A0E2E;background:#fff;text-transform:none}
.lang-sug{position:fixed;left:50%;transform:translateX(-50%);bottom:84px;z-index:60;display:flex;gap:12px;align-items:center;flex-wrap:wrap;max-width:min(560px,calc(100vw - 24px));background:#0A1230;color:#fff;border:1px solid #5B5BD6;border-radius:14px;padding:12px 14px 12px 18px;box-shadow:0 10px 30px rgba(0,0,0,.35);font:15px/1.4 system-ui,sans-serif}
.lang-sug a{color:#C7D2FE;font-weight:700}
.lang-sug button{margin-left:auto;background:transparent;border:0;color:#fff;font-size:22px;line-height:1;cursor:pointer;padding:2px 6px}
@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important;scroll-behavior:auto!important}}
</style>"""
JS = '<script src="/js/a11y.js?v=1" defer></script>'


def lang_of(rel):
    return "th" if rel.startswith("th/") else "zh" if rel.startswith("zh/") else "en"


n_main = n_all = 0
for p in sorted(ROOT.glob("*.html")) + sorted((ROOT / "th").glob("*.html")) + sorted((ROOT / "zh").glob("*.html")):
    if p.name in SKIP:
        continue
    rel = p.relative_to(ROOT).as_posix()
    s = p.read_text(encoding="utf-8")
    orig = s
    s = re.sub(r"<!--a11y-->.*?<!--/a11y-->\n?", "", s, flags=re.S)
    s = re.sub(r'<!--skip--><a class="skip"[^>]*>.*?</a><!--/skip-->', "", s)
    s = s.replace("</head>", "<!--a11y-->" + CSS + JS + "<!--/a11y-->\n</head>", 1)
    m = re.search(r"<body[^>]*>", s)
    if m:
        s = s[: m.end()] + f'<!--skip--><a class="skip" href="#main">{LABEL[lang_of(rel)]}</a><!--/skip-->' + s[m.end():]
    if "<main" not in s and "</header>" in s and "<footer" in s:
        h = s.index("</header>")
        sec = s.find("<section", h)
        f = s.rfind("<footer")
        if 0 < sec < f:
            s = s[:sec] + '<main id="main" tabindex="-1"><!--main-->' + s[sec:f] + "<!--/main--></main>\n" + s[f:]
            n_main += 1
    elif "<main" in s and 'id="main"' not in s:
        s = re.sub(r"<main(\s|>)", r'<main id="main"\1', s, count=1)
    if s != orig:
        p.write_text(s, encoding="utf-8")
        n_all += 1
print(f"accessibility: {n_all} pages updated, {n_main} given a <main> landmark")
