# -*- coding: utf-8 -*-
"""Write the 5 Word Power tests (100 advanced synonym questions) into the answer bank as tests 111-115.
Tests 1-110 are kept as they are. Idempotent. Run: python3 tools/vocab/build_word_power.py"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from word_power import TESTS

bank_p = pathlib.Path(__file__).resolve().parents[2] / "netlify/functions/vocab/bank.json"
bank = json.loads(bank_p.read_text(encoding="utf-8"))[:110]
assert len(bank) == 110, "run build_solar.py first"
for t in TESTS:
    assert len(t) == 20
    out = []
    for word, pos, answer, wrong in t:
        assert len(wrong) == 3 and answer not in wrong and len(set(wrong)) == 3, word
        out.append({"word": word, "pos": pos, "answer": answer, "distractors": wrong})
    bank.append(out)
bank_p.write_text(json.dumps(bank, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print("bank tests:", len(bank))
