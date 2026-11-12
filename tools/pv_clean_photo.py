"""Add the PV-cleaning example photo to every PV cleaning job (data-work="cleaning")
on job.html and th/job.html. Idempotent: cards already carrying the photo are skipped.
Placeholder thumbs (thumb ph) are replaced by the photo; cards with a site photo get it
as a second picture under the site photo."""
import re, pathlib
IMG = "images/job-pv-cleaning-in-action.jpg"
TXT = {"en": ("Solar ESS team cleaning panels with a soft rotating brush and clean water",
              "PV cleaning in progress (example)"),
       "th": ("ทีม Solar ESS ล้างแผงด้วยแปรงหมุนขนนุ่มและน้ำสะอาด",
              "ตัวอย่างงานล้างแผงโซลาร์")}
ROOT = pathlib.Path(__file__).resolve().parent.parent

def fig(lang, cap):
    alt, _ = TXT[lang]
    return (f'<figure class="pvc" style="margin:0"><img src="/{IMG}" alt="{alt}" loading="lazy">'
            f'<figcaption>{cap}</figcaption></figure>')

def run(path, lang):
    s = path.read_text(encoding="utf-8")
    out, pos, n_ph, n_add = [], 0, 0, 0
    for m in re.finditer(r'<article class="card p[^"]*"[^>]*data-work="cleaning"[^>]*>', s):
        a = m.end(); e = s.index("</article>", a)
        card = s[a:e]
        if IMG in card:
            continue
        top = card.index('<div class="top">')
        thumb = card[:top]
        if 'class="thumb ph"' in thumb:
            loc = re.search(r"<span>(.*?)</span></div>\s*$", thumb)
            cap = (loc.group(1) + " · " if loc else "") + TXT[lang][1]
            new = f'<div class="thumb"><div class="pics">{fig(lang, cap)}</div></div>'
            n_ph += 1
        else:
            k = thumb.rindex("</div></div>")
            new = thumb[:k] + fig(lang, TXT[lang][1]) + thumb[k:]
            n_add += 1
        out.append((a, a + top, new))
    for a, b, new in reversed(out):
        s = s[:a] + new + s[b:]
    path.write_text(s, encoding="utf-8")
    print(f"{path.name} ({lang}): placeholder replaced {n_ph}, photo added {n_add}")

run(ROOT / "job.html", "en")
run(ROOT / "th" / "job.html", "th")
