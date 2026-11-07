# -*- coding: utf-8 -*-
"""Build netlify/functions/itest/bank.json: 125 questions in 5 levels of 25 (easiest to hardest), Thai + English.
Levels 1–4 use questions_a.py + questions_bcd.py (assigned below) plus brand questions (questions_brands.py) in levels 2–3; level 5 is questions_e.py.
Each level mixes all four sections. Option order is shuffled once (fixed seed).
Run from the repo root:  python3 tools/itest/build_bank.py"""
import json, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from questions_a import A
from questions_bcd import B, C, D
from questions_e import E
from questions_brands import BRANDS2, BRANDS3
from questions_ds import DS2, DS3, DS4

SECTIONS = [("A", "ไฟฟ้าในระบบโซลาร์: สาย เบรกเกอร์ อินเวอร์เตอร์ แผง อนุกรม/ขนาน", "Solar electrical: cables, breakers, inverters, panels, series/parallel"),
            ("B", "การเดินสายและชนิดสายไฟ", "Wiring methods and cable types"),
            ("C", "โครงสร้าง แรงลม และการติดตั้งแผง", "Mounting, wind load and panel installation"),
            ("D", "ความต้องการและความพึงพอใจของลูกค้า", "Customer needs and satisfaction")]
LEVELS = [(1, "Solar Enterer", "ผู้เริ่มต้นเข้าสู่โซลาร์"), (2, "Solar Enthusiast", "ผู้สนใจโซลาร์"), (3, "Solar in Practice", "ผู้ปฏิบัติงานโซลาร์"),
          (4, "Solar Professional", "มืออาชีพด้านโซลาร์"), (5, "Solar Expert", "ผู้เชี่ยวชาญด้านโซลาร์")]
# index in the 100-question list (A 0–49, B 50–69, C 70–89, D 90–99) -> level 1–4
ASSIGN = {1: [0, 1, 2, 3, 9, 12, 13, 19, 23, 25, 46, 47, 50, 51, 52, 56, 57, 76, 77, 82, 84, 89, 90, 91, 99],
          2: [7, 8, 14, 31, 33, 38, 44, 48, 54, 58, 60, 64, 70, 71, 74, 92, 95, 97],
          3: [4, 6, 17, 18, 24, 27, 35, 36, 39, 40, 43, 45, 49, 61, 62, 63, 72, 93, 96],
          4: [5, 10, 16, 21, 22, 26, 28, 29, 32, 37, 41, 42, 68, 69, 78, 80, 85, 87, 88, 94, 98]}
base = [("A",) + q for q in A] + [("B",) + q for q in B] + [("C",) + q for q in C] + [("D",) + q for q in D]
# Nov 2026 review: DC-safety items (4, 39, 40, 45, 62, 63) moved 4 -> 3; design items (11, 15, 29, 73) moved 3 -> 4,
# (22, 26) moved 2 -> 4; Sigenergy and Solis brand questions moved 3 -> 2.
# Datasheet/site questions (questions_ds.py) replaced 20, 34, 65 (L2), 30, 53, 66, 79 (L3), 11, 15, 67, 73 (L4).
# Nov 2026: the Sigenergy '5-in-1' question left Level 2 for the Sigenergy brand set (questions_brands.SIGENERGY); 58 came back in its place.
# Nov 2026: the Enphase microinverter question left Level 2 for the Enphase brand set (questions_brands.ENPHASE); 60 came back in its place.
# 55, 58, 59, 60, 75, 81, 83, 86 were retired to make room for the brand questions (levels 2–3)
EXTRA = {2: BRANDS2 + DS2, 3: BRANDS3 + DS3, 4: DS4}
used = sum(ASSIGN.values(), [])
assert len(used) == len(set(used)), "no question twice"
assert all(len(ASSIGN[l]) + len(EXTRA.get(l, [])) == 25 for l in ASSIGN), "25 per level"
assert len(E) == 25
rnd = random.Random(20261106)
out = {"pass_pct": 100, "work_level": 3,
       "sections": [{"id": s, "th": th, "en": en} for s, th, en in SECTIONS],
       "levels": [{"n": n, "en": en, "th": th, "count": 25} for n, en, th in LEVELS],
       "questions": []}

def add(level, sec, th, en, opts, expl):
    o = [x if isinstance(x, tuple) else (x, x) for x in opts]
    order = list(range(4)); rnd.shuffle(order)
    out["questions"].append({"level": level, "sec": sec, "th": th, "en": en,
                             "options": [{"th": o[k][0], "en": o[k][1]} for k in order],
                             "answer": order.index(0), "explain": expl})

for lv in (1, 2, 3, 4):
    qs = [base[i] for i in ASSIGN[lv]] + list(EXTRA.get(lv, []))
    rnd.shuffle(qs)                                  # mix sections within the level
    for q in qs:
        add(lv, *q)
e = E[:]; rnd.shuffle(e)
for q in e:
    add(5, *q)
Path("netlify/functions/itest/bank.json").write_text(json.dumps(out, ensure_ascii=False, indent=0), encoding="utf-8")
from collections import Counter
print(len(out["questions"]), "questions", Counter(q["level"] for q in out["questions"]), Counter((q["level"], q["sec"]) for q in out["questions"]))
