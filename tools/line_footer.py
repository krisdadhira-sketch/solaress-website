"""Add a LINE Official Account 'Add friend' block (QR + button) to every page footer.
Idempotent: content between <!--linefoot--> markers is replaced."""
import pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent.parent
TXT = {"en": ("Add us on LINE", "@441hmruu"), "th": ("เพิ่มเพื่อน LINE", "@441hmruu"), "zh": ("加我们 LINE 好友", "@441hmruu")}
def block(lang):
    t, i = TXT[lang]
    return ('<!--linefoot--><a href="https://line.me/R/ti/p/@441hmruu" target="_blank" rel="noopener" '
            'style="display:inline-flex;align-items:center;gap:10px;background:#fff;color:#0B1736;padding:6px 12px 6px 6px;border-radius:10px;text-decoration:none;opacity:1">'
            '<img src="/images/line-oa-qr.png" alt="LINE QR @441hmruu" width="56" height="56" loading="lazy" style="display:block;border-radius:4px">'
            f'<span style="line-height:1.35"><b style="color:#06C755">LINE</b> {t}<br>{i}</span></a><!--/linefoot-->')
n = 0
for p in ROOT.rglob("*.html"):
    if any(x in p.parts for x in ("node_modules", ".git")): continue
    s = p.read_text(encoding="utf-8")
    if "<footer" not in s: continue
    rel = p.relative_to(ROOT).as_posix()
    lang = "th" if rel.startswith("th/") else "zh" if rel.startswith("zh/") else "en"
    s2 = re.sub(r"<!--linefoot-->.*?<!--/linefoot-->", "", s, flags=re.S)
    s2 = re.sub(r"(<footer><div class=\"wrap\">.*?)(</div></footer>)", lambda m: m.group(1) + block(lang) + m.group(2), s2, count=1, flags=re.S)
    if s2 != s: p.write_text(s2, encoding="utf-8"); n += 1
print("pages updated:", n)
