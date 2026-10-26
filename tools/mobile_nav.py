# -*- coding: utf-8 -*-
"""Inject the mobile navigation (Menu button + accordion panel) into every page.

Idempotent: the block lives between <!--mnav--> and <!--/mnav--> right after </header>
and is replaced on each run.  Run from the repo root:  python3 tools/mobile_nav.py
"""
import glob, re, os

LABEL = {"en": ("Menu", "Close"), "th": ("เมนู", "ปิด"), "zh": ("菜单", "关闭")}

CSS = """
.mnav-btn,.mnav-tg{display:none}
@media (max-width:900px){
.nav .wrap{flex-wrap:nowrap;gap:12px;padding-block:8px}
.nav img{height:40px}
.mnav-btn{display:inline-flex;align-items:center;gap:9px;margin-left:auto;height:44px;padding:0 14px;border:1px solid rgba(255,255,255,.35);border-radius:10px;background:transparent;color:#fff;font-family:inherit;font-size:15px;font-weight:600;line-height:1;cursor:pointer;-webkit-tap-highlight-color:transparent}
.mnav-btn i{position:relative;display:block;width:18px;height:2px;background:currentColor;border-radius:2px;transition:background .15s}
.mnav-btn i::before,.mnav-btn i::after{content:"";position:absolute;left:0;width:18px;height:2px;background:currentColor;border-radius:2px;transition:transform .2s}
.mnav-btn i::before{top:-6px}.mnav-btn i::after{top:6px}
.nav.mopen .mnav-btn i{background:transparent}
.nav.mopen .mnav-btn i::before{transform:translateY(6px) rotate(45deg)}
.nav.mopen .mnav-btn i::after{transform:translateY(-6px) rotate(-45deg)}
.nav nav{display:none!important}
.nav.mopen nav{display:flex!important;position:fixed;left:0;right:0;top:var(--mnav-top,64px);bottom:0;z-index:30;overflow-y:auto;-webkit-overflow-scrolling:touch;overscroll-behavior:contain;flex-direction:column;flex-wrap:nowrap;gap:0;margin:0;padding:6px 20px calc(28px + env(safe-area-inset-bottom,0px));background:var(--navy);border-top:1px solid rgba(255,255,255,.14);font-family:inherit;font-size:17px;letter-spacing:0;text-transform:none}
.nav.mopen nav>a{display:flex;align-items:center;min-height:54px;font-weight:600;opacity:1;border-bottom:1px solid rgba(255,255,255,.1)}
.nav.mopen nav .dd{display:flex;flex-wrap:wrap;align-items:center;gap:0;border-bottom:1px solid rgba(255,255,255,.1)}
.nav.mopen nav .dd>a{flex:1;display:flex;align-items:center;min-height:54px;font-weight:600;opacity:1}
.nav.mopen nav .dd>a::after{content:none}
.mnav-tg{display:inline-flex;align-items:center;justify-content:center;width:48px;height:48px;margin-right:-10px;border:0;background:none;color:#fff;cursor:pointer;-webkit-tap-highlight-color:transparent}
.mnav-tg::before{content:"";width:9px;height:9px;border-right:2px solid currentColor;border-bottom:2px solid currentColor;transform:translateY(-3px) rotate(45deg);transition:transform .2s}
.dd.mx>.mnav-tg::before{transform:translateY(2px) rotate(-135deg)}
.nav.mopen nav .ddm{display:none!important}
.nav.mopen nav .dd.mx .ddm{display:flex!important;position:static;flex-direction:column;flex-wrap:nowrap;width:100%;min-width:0;margin:0;padding:0 0 12px 14px;gap:0;background:none;border:0;border-left:2px solid var(--hot,#f2a516);box-shadow:none}
.nav.mopen nav .ddm a{display:flex;align-items:center;min-height:44px;padding:4px 0;font-size:15.5px;line-height:1.35;opacity:.86;white-space:normal}
.nav.mopen nav .ddm a::before{content:none}
.nav.mopen nav .langsw{display:flex;gap:10px;margin:22px 0 0;font-size:16px}
.nav.mopen nav .langsw a{flex:1;display:flex;align-items:center;justify-content:center;min-height:46px;border:1px solid rgba(255,255,255,.28);border-radius:10px;opacity:.85}
.nav.mopen nav .langsw a[aria-current]{background:rgba(255,255,255,.12);opacity:1;font-weight:700}
html.mnav-lock,html.mnav-lock body{overflow:hidden}
html.mnav-lock .fab{display:none!important}
}
"""

JS = r"""
(function(){var h=document.querySelector('header.nav');if(!h||h.dataset.mnav)return;h.dataset.mnav=1;
var w=h.querySelector('.wrap'),n=h.querySelector('nav');if(!w||!n)return;n.id=n.id||'site-nav';
var L=%s,b=document.createElement('button');b.type='button';b.className='mnav-btn';
b.setAttribute('aria-controls',n.id);b.setAttribute('aria-expanded','false');b.innerHTML='<i aria-hidden="true"></i><span>'+L[0]+'</span>';
w.insertBefore(b,n);
function top(){h.style.setProperty('--mnav-top',Math.round(h.getBoundingClientRect().bottom)+'px')}
function set(o){h.classList.toggle('mopen',o);document.documentElement.classList.toggle('mnav-lock',o);b.setAttribute('aria-expanded',o);b.lastChild.textContent=o?L[1]:L[0];if(o)top()}
b.addEventListener('click',function(){set(!h.classList.contains('mopen'))});
n.querySelectorAll('.dd').forEach(function(d){var a=d.querySelector('a'),m=d.querySelector('.ddm');if(!a||!m)return;
 var t=document.createElement('button');t.type='button';t.className='mnav-tg';t.setAttribute('aria-expanded','false');t.setAttribute('aria-label',a.textContent);
 a.after(t);t.addEventListener('click',function(){var x=!d.classList.contains('mx');d.classList.toggle('mx',x);t.setAttribute('aria-expanded',x)})});
n.addEventListener('click',function(e){if(e.target.closest('a'))set(false)});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&h.classList.contains('mopen')){set(false);b.focus()}});
addEventListener('resize',function(){if(innerWidth>900&&h.classList.contains('mopen'))set(false);else if(h.classList.contains('mopen'))top()});
})();
"""

def lang_of(path, html):
    m = re.search(r'<html[^>]*\blang="([a-zA-Z]+)', html)
    l = (m.group(1).lower() if m else "en")
    return l if l in LABEL else ("th" if "/th/" in path else "zh" if "/zh/" in path else "en")

def block(lang):
    lab = LABEL[lang]
    js = JS % ('["%s","%s"]' % lab)
    return "<!--mnav--><style id=\"mnav-css\">%s</style><script>%s</script><!--/mnav-->" % (CSS.strip(), js.strip())

n = 0
for f in sorted(glob.glob("*.html") + glob.glob("th/*.html") + glob.glob("zh/*.html")):
    s = open(f, encoding="utf-8").read()
    if '<header class="nav">' not in s or "<nav" not in s:
        continue
    s = re.sub(r"<!--mnav-->.*?<!--/mnav-->", "", s, flags=re.S)
    s = s.replace("</header>", "</header>" + block(lang_of(f, s)), 1)
    open(f, "w", encoding="utf-8").write(s)
    n += 1
print("pages updated:", n)
