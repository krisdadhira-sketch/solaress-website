# -*- coding: utf-8 -*-
"""Clean a customer quotation/proposal PDF for publishing on solaress.org (Nov 2026 rules):
no prices, no personal names, no customer details, no exact locations; Solar ESS watermark on every page.
Usage: python3 tools/clean_quote_pdf.py IN.pdf OUT.pdf [--name "text to hide=replacement" ...] [--noprice  (drawings without prices: names only)]
Prices: every amount with 2 decimals, every per-watt / per-metre rate, and any "N บาท" whose value also appears
as a 2-decimal price in the document or that sits on a price line. PEA buy-back rate and savings figures stay.
Also fixes the old Krabi branch address (761 → 140/2 หมู่ 4)."""
import re, sys
import pymupdf as fitz

FONT = "/home/claude/solaress-website/tools/fonts/Sarabun-Regular.ttf"
A = re.compile(r"[-+]?\d{1,3}(?:,\d{3})+\.\d{2}")
BARE = re.compile(r"^\s*[-+]?\d[\d,]*\.\d{2}(?:\s*/\s*\S.*)?\s*$")
RATE = re.compile(r"\d+(?:\.\d+)?(?=\s*บาท\s*(?:/|ต่อ)\s*(?:วัตต์|W|ม\.|\s*$))|(?<=× )\d+(?=\s*บาท)")
BAHT = re.compile(r"[-+]?\d[\d,]*(?:\.\d+)?(?=\s*บาท)")
PRICE_LINE = re.compile(r"ราคา|ลงทุน|เหมา|ชุดละ|แผงละ|MCCB|สายแบต|แพ็กเกจ|ยื่นขอ|VAT|ค่าเผื่อ|ค่าธรรมเนียม|รวมอยู่")


NOTE_P = "ตัวอย่าง · ตัดข้อมูลลูกค้าและราคาออกแล้ว · Sample: customer details and prices removed"
NOTE_N = "Sample: site and customer names removed · www.solaress.org"


def lines(page):
    for b in page.get_text("rawdict")["blocks"]:
        for l in b.get("lines", []):
            chars = [(c, s) for s in l["spans"] for c in s["chars"]]
            if chars:
                yield "".join(c["c"] for c, _ in chars), chars


def clean(src, dst, names, prices=True):
    d = fitz.open(src)
    known = set()
    for p in d:
        for t, _ in lines(p):
            known |= {m.group(0).lstrip("+-").split(".")[0] for m in A.finditer(t)}
    for pno, p in enumerate(d):
        todo = []
        for t, chars in lines(p):
            spans = []
            for old, new in names:
                for m in re.finditer(re.escape(old), t):
                    spans.append((m.start(), m.end(), new))
            if "761 หมู่ 4" in t:
                m = re.search(r"761", t); spans.append((m.start(), m.end(), "140/2"))
            for m in (A.finditer(t) if prices else []):
                spans.append((m.start(), m.end(), "–"))
            if prices and BARE.match(t):
                m = re.search(r"[-+]?\d[\d,]*\.\d{2}(?:\s*/\s*\S.*)?", t); spans.append((m.start(), m.end(), "–"))
            for m in (RATE.finditer(t) if prices else []):
                spans.append((m.start(), m.end(), "–"))
            for m in (BAHT.finditer(t) if prices else []):
                v = m.group(0).lstrip("+-").split(".")[0]
                if "ล้านบาท" in t[m.end():m.end() + 8]:
                    continue
                if v in known or (PRICE_LINE.search(t) and not re.search(r"หน่วยละ|ประหยัด|ผลประโยชน์|รายได้", t)):
                    if len(v.replace(",", "")) >= 3:
                        spans.append((m.start(), m.end(), "–"))
            spans.sort()
            merged = []
            for s in spans:
                if merged and s[0] < merged[-1][1]:
                    continue
                merged.append(s)
            for a, b, new in merged:
                cs = chars[a:b]
                r = fitz.Rect(cs[0][0]["bbox"])
                for c, _ in cs[1:]:
                    r |= fitz.Rect(c["bbox"])
                sp = cs[0][1]
                h = r.height
                r2 = fitz.Rect(r.x0, r.y0 + h * 0.18, r.x1, r.y1 - h * 0.12)
                todo.append((r2, r, new, sp["size"], sp["color"], "Bold" in sp["font"], cs[0][0]["origin"]))
        for r2, *_ in todo:
            p.add_redact_annot(r2, fill=None)
        p.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_NONE)
        for r2, r, new, size, color, bold, origin in todo:
            col = "#%06x" % color
            w = "bold" if bold else "normal"
            box = fitz.Rect(r.x0, r.y0 - 0.5, max(r.x1, r.x0 + size * 0.6 * len(new)) + 4, r.y1 + 4)
            p.insert_htmlbox(box, f'<span style="font-family:sans-serif;font-size:{size}px;color:{col};font-weight:{w};white-space:nowrap">{new}</span>',
                             css="* {margin:0;padding:0}")
        # watermark
        pr = p.rect
        c = fitz.Point(pr.width / 2, pr.height / 2)
        mat = fitz.Matrix(-30)
        p.insert_text(fitz.Point(c.x - 170, c.y + 20), "SOLAR ESS", fontsize=64, fontname="helv", color=(0.45, 0.45, 0.55),
                      fill_opacity=0.10, stroke_opacity=0.10, morph=(c, mat), overlay=True)
        p.insert_text(fitz.Point(c.x - 85, c.y + 55), "www.solaress.org", fontsize=20, fontname="helv", color=(0.36, 0.36, 0.84),
                      fill_opacity=0.14, stroke_opacity=0.14, morph=(c, mat), overlay=True)
        if pno == 0:
            note = fitz.Rect(36, 8, pr.width * 0.55, 20)
            p.insert_htmlbox(note, '<div style="font-family:sans-serif;font-size:8px;color:#5B5BD6;text-align:left">' +
                             (NOTE_P if prices else NOTE_N) + '</div>')
    d.set_metadata({"title": "Solar ESS sample", "author": "Solar ESS Co. Ltd.", "subject": "www.solaress.org"})
    d.save(dst, garbage=4, deflate=True)
    print("saved", dst)


if __name__ == "__main__":
    a = sys.argv[1:]
    names = []
    while "--name" in a:
        i = a.index("--name"); o, n = a[i + 1].split("=", 1); names.append((o, n)); del a[i:i + 2]
    pr = "--noprice" not in a
    a = [x for x in a if x != "--noprice"]
    clean(a[0], a[1], names, pr)
