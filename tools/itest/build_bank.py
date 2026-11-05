# -*- coding: utf-8 -*-
"""Build netlify/functions/itest/bank.json from questions_a.py + questions_bcd.py.
Option order is shuffled once (fixed seed) so the correct answer is not always first.
Run from the repo root:  python3 tools/itest/build_bank.py"""
import json, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from questions_a import A
from questions_bcd import B, C, D

SECTIONS = [("A", "ไฟฟ้าในระบบโซลาร์: สาย เบรกเกอร์ อินเวอร์เตอร์ แผง อนุกรม/ขนาน", "Solar electrical: cables, breakers, inverters, panels, series/parallel", A),
            ("B", "การเดินสายและชนิดสายไฟ", "Wiring methods and cable types", B),
            ("C", "โครงสร้าง แรงลม และการติดตั้งแผง", "Mounting, wind load and panel installation", C),
            ("D", "ความต้องการและความพึงพอใจของลูกค้า", "Customer needs and satisfaction", D)]
rnd = random.Random(20261106)
out = {"sections": [{"id": s, "th": th, "en": en, "count": len(qs)} for s, th, en, qs in SECTIONS], "questions": []}
for s, _, _, qs in SECTIONS:
    for th, en, opts, expl in qs:
        o = [x if isinstance(x, tuple) else (x, x) for x in opts]
        order = list(range(4)); rnd.shuffle(order)
        out["questions"].append({"sec": s, "th": th, "en": en,
                                 "options": [{"th": o[k][0], "en": o[k][1]} for k in order],
                                 "answer": order.index(0), "explain": expl})
Path("netlify/functions/itest/bank.json").write_text(json.dumps(out, ensure_ascii=False, indent=0), encoding="utf-8")
from collections import Counter
print(len(out["questions"]), "questions; answer positions", Counter(q["answer"] for q in out["questions"]))
