# -*- coding: utf-8 -*-
"""Consultation form (home page EN/TH/ZH): "What would you like?" select (field free_service), Nov 2026.
The Services menu items Free Consultation / Free Quotation / Free Plant Design link to /?free=<key>#consult and the
small script preselects the matching option. Idempotent.  Run:  python3 tools/consult_free.py (then tools/form_ink.py)"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
T = {
    "en": ("What would you like? (all free)", ["Free consultation", "Free quotation", "Free plant design", "Free system check"]),
    "th": ("ต้องการบริการใด (ฟรีทั้งหมด)", ["ปรึกษาฟรี", "ใบเสนอราคาฟรี", "ออกแบบระบบฟรี", "ตรวจระบบฟรี"]),
    "zh": ("您需要哪项服务？（全部免费）", ["免费咨询", "免费报价", "免费系统设计", "免费系统检查"]),
}
KEYS = ["consultation", "quotation", "design", "check"]


def block(lang):
    label, opts = T[lang]
    o = "".join(f'<option value="{v}" data-k="{k}">{v}</option>' for k, v in zip(KEYS, opts))
    return (f'<!--cfree--><label for="f-free" style="margin-bottom:10px">{label}<select id="f-free" name="free_service">{o}</select></label>'
            '<script>(function(){try{var k=new URLSearchParams(location.search).get("free"),s=document.getElementById("f-free");'
            'if(!k||!s)return;for(var i=0;i<s.options.length;i++)if(s.options[i].dataset.k===k){s.selectedIndex=i;break}}catch(e){}})();</script><!--/cfree-->')


for lang, path in (("en", ROOT / "index.html"), ("th", ROOT / "th" / "index.html"), ("zh", ROOT / "zh" / "index.html")):
    s = path.read_text(encoding="utf-8")
    s = re.sub(r"<!--cfree-->.*?<!--/cfree-->", "", s, flags=re.S)
    a = s.index('<form id="cform"')
    i = s.index('<p class="fsnote"', a)
    s = s[:i] + block(lang) + s[i:]
    path.write_text(s, encoding="utf-8")
    print("updated", path.relative_to(ROOT))
