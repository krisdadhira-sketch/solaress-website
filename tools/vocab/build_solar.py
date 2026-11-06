# -*- coding: utf-8 -*-
"""Write the 10 solar electrical vocabulary tests into the answer bank as tests 101-110.
Tests 1-100 (English synonyms) are kept as they are. Idempotent. Run: python3 tools/vocab/build_solar.py"""
import json, random, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from solar_terms import TESTS, TOPICS, GROUPS

bank_p = pathlib.Path(__file__).resolve().parents[2] / "netlify/functions/vocab/bank.json"
bank = json.loads(bank_p.read_text(encoding="utf-8"))[:100]
near = {}
for g in GROUPS:
    for a in g:
        near.setdefault(a, set()).update(g)
for k, t in enumerate(TESTS):
    rnd = random.Random(f"solar-{k}")
    out = []
    for term, meaning in t:
        pool = [d for w, d in t if w != term and w not in near.get(term, ())]
        out.append({"word": term, "pos": TOPICS[k][0], "answer": meaning, "distractors": rnd.sample(pool, 3)})
    bank.append(out)
bank_p.write_text(json.dumps(bank, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print("bank tests:", len(bank))
