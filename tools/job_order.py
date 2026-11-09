# -*- coding: utf-8 -*-
"""Jobs page order (Nov 2026): newest job first, closed jobs last, on job.html and th/job.html.
Each job card carries data-posted="YYYY-MM-DD" (first published) and shows it in its kind line.
New job cards: add data-posted (today) when you insert them, then run:  python3 tools/job_order.py
(Cards without data-posted are dated from git history the first time this runs.)"""
import re, subprocess, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TH_M = ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."]
EN_M = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
ART = re.compile(r'<article class="card[^"]*" id="([^"]+)".*?</article>\n?', re.S)


def first_seen(jid):
    out = subprocess.run(["git", "log", "--reverse", "--format=%at", f'-Sid="{jid}"', "--", "job.html"],
                         cwd=ROOT, capture_output=True, text=True).stdout.split()
    return int(out[0]) if out else int(datetime.datetime.now().timestamp())


def label(lang, d):
    y, m, dd = map(int, d.split("-"))
    return f" · ลงประกาศ {dd} {TH_M[m-1]} {y + 543}" if lang == "th" else f" · Posted {dd} {EN_M[m-1]} {y}"


def run(path, lang, stamps):
    p = ROOT / path
    s = p.read_text(encoding="utf-8")
    arts = list(ART.finditer(s))
    # group contiguous runs of articles (one run per cards container)
    runs, cur = [], [arts[0]]
    for a in arts[1:]:
        if s[cur[-1].end():a.start()].strip() == "":
            cur.append(a)
        else:
            runs.append(cur); cur = [a]
    runs.append(cur)
    out, pos = [], 0
    for r in runs:
        items = []
        for i, a in enumerate(r):
            jid, block = a.group(1), a.group(0)
            m = re.search(r'data-posted="(\d{4}-\d{2}-\d{2})"', block)
            if m:
                d = m.group(1); ts = stamps.get(jid) or int(datetime.datetime.fromisoformat(d).timestamp())
            else:
                ts = stamps.get(jid) or first_seen(jid)
                d = datetime.datetime.fromtimestamp(ts, datetime.timezone(datetime.timedelta(hours=7))).date().isoformat()
                block = block.replace(f'id="{jid}"', f'id="{jid}" data-posted="{d}"', 1)
            block = re.sub(r'<span class="posted">.*?</span>', "", block)
            block = re.sub(r'(<div class="kind">)(.*?)(</div>)', lambda mm: mm.group(1) + mm.group(2) + f'<span class="posted">{label(lang, d)}</span>' + mm.group(3), block, count=1, flags=re.S)
            closed = 'class="closed"' in block
            if not block.endswith("\n"):
                block += "\n"
            items.append((closed, -ts, i, block))
        items.sort()
        out.append(s[pos:r[0].start()]); out.append("".join(b for *_, b in items)); pos = r[-1].end()
    out.append(s[pos:])
    s = "".join(out)
    if ".kind .posted" not in s:
        s = s.replace("</head>", "<style id=\"posted-css\">.kind .posted{font-weight:400;opacity:.75;white-space:nowrap}</style></head>", 1)
    p.write_text(s, encoding="utf-8")
    print(path, sum(len(r) for r in runs), "cards in", len(runs), "lists")


if __name__ == "__main__":
    import sys
    stamps = {}
    if len(sys.argv) > 1:  # optional "id timestamp" file to skip git lookups
        for line in Path(sys.argv[1]).read_text().split("\n"):
            if line.strip():
                k, v = line.split(); stamps[k] = int(v)
    run("job.html", "en", stamps)
    run("th/job.html", "th", stamps)
