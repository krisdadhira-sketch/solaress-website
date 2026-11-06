# -*- coding: utf-8 -*-
"""Search box for the Project Based Jobs on /job.html and /th/job.html.
- Under the region chips: a text box (province, district, place or any word) + a "Type of work" select.
- Every project card gets data-work (work types, from keyword rules below) and data-q (its location in
  English AND Thai, taken from the same card on the other-language page, plus province names in both languages),
  so a Thai name finds jobs on the English page and the other way round.
- Works together with the region chips (region AND text AND type).
Idempotent (markers <!--jsearch-->, <!--jsearchjs-->). Re-run after adding or editing jobs:  python3 tools/job_search.py"""
import html, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = {"en": ROOT / "job.html", "th": ROOT / "th/job.html"}

# work type -> (EN label, TH label)
TYPES = [
    ("electrical", "Electrical work", "งานไฟฟ้า"),
    ("solar", "Solar installation", "งานติดตั้งโซลาร์"),
    ("cleaning", "PV cleaning & maintenance (O&M)", "ล้างแผงและบำรุงรักษา (O&M)"),
    ("repair", "Repair & troubleshooting", "ซ่อมและแก้ไขปัญหา"),
    ("civil", "Civil & structure (welding, steel, mounting)", "งานโยธาและโครงสร้าง (เชื่อม เหล็ก ยึดติดตั้ง)"),
    ("supply", "Supply & fabrication", "จัดหาและผลิตชิ้นงาน"),
]
RULES = {  # matched on the English card id + kind + title (lower case)
    "electrical": r"wiring|electrical|cable|feeder|\bats\b|\bct\b|meter|voltage|breaker|load wiring",
    "solar": r"install|mount the|battery wall|\bpv\b|solar",
    "cleaning": r"cleaning|o&amp;m|o&m|maintenance",
    "repair": r"^fix-|fault|not working|offline|error|missing|not reaching|trips|troubleshoot",
    "civil": r"weld|steel|frame|base plate|fabricat|structure|screw pile|mount",
    "supply": r"^supply|supply |fabricat|bolt",
}

PROV = {  # English -> Thai, all 77 provinces + neighbours used on the page
 "Bangkok": "กรุงเทพมหานคร", "Amnat Charoen": "อำนาจเจริญ", "Ang Thong": "อ่างทอง", "Bueng Kan": "บึงกาฬ", "Buriram": "บุรีรัมย์",
 "Chachoengsao": "ฉะเชิงเทรา", "Chai Nat": "ชัยนาท", "Chaiyaphum": "ชัยภูมิ", "Chanthaburi": "จันทบุรี", "Chiang Mai": "เชียงใหม่",
 "Chiang Rai": "เชียงราย", "Chonburi": "ชลบุรี", "Chumphon": "ชุมพร", "Kalasin": "กาฬสินธุ์", "Kamphaeng Phet": "กำแพงเพชร",
 "Kanchanaburi": "กาญจนบุรี", "Khon Kaen": "ขอนแก่น", "Krabi": "กระบี่", "Lampang": "ลำปาง", "Lamphun": "ลำพูน", "Loei": "เลย",
 "Lopburi": "ลพบุรี", "Mae Hong Son": "แม่ฮ่องสอน", "Maha Sarakham": "มหาสารคาม", "Mukdahan": "มุกดาหาร", "Nakhon Nayok": "นครนายก",
 "Nakhon Pathom": "นครปฐม", "Nakhon Phanom": "นครพนม", "Nakhon Ratchasima": "นครราชสีมา", "Nakhon Sawan": "นครสวรรค์",
 "Nakhon Si Thammarat": "นครศรีธรรมราช", "Nan": "น่าน", "Narathiwat": "นราธิวาส", "Nong Bua Lamphu": "หนองบัวลำภู", "Nong Khai": "หนองคาย",
 "Nonthaburi": "นนทบุรี", "Pathum Thani": "ปทุมธานี", "Pattani": "ปัตตานี", "Phang Nga": "พังงา", "Phatthalung": "พัทลุง", "Phayao": "พะเยา",
 "Phetchabun": "เพชรบูรณ์", "Phetchaburi": "เพชรบุรี", "Phichit": "พิจิตร", "Phitsanulok": "พิษณุโลก", "Phra Nakhon Si Ayutthaya": "พระนครศรีอยุธยา",
 "Ayutthaya": "อยุธยา", "Phrae": "แพร่", "Phuket": "ภูเก็ต", "Prachinburi": "ปราจีนบุรี", "Prachuap Khiri Khan": "ประจวบคีรีขันธ์", "Ranong": "ระนอง",
 "Ratchaburi": "ราชบุรี", "Rayong": "ระยอง", "Roi Et": "ร้อยเอ็ด", "Sa Kaeo": "สระแก้ว", "Sakon Nakhon": "สกลนคร", "Samut Prakan": "สมุทรปราการ",
 "Samut Sakhon": "สมุทรสาคร", "Samut Songkhram": "สมุทรสงคราม", "Saraburi": "สระบุรี", "Satun": "สตูล", "Sing Buri": "สิงห์บุรี",
 "Sisaket": "ศรีสะเกษ", "Songkhla": "สงขลา", "Sukhothai": "สุโขทัย", "Suphan Buri": "สุพรรณบุรี", "Surat Thani": "สุราษฎร์ธานี", "Surin": "สุรินทร์",
 "Tak": "ตาก", "Trang": "ตรัง", "Trat": "ตราด", "Ubon Ratchathani": "อุบลราชธานี", "Udon Thani": "อุดรธานี", "Uthai Thani": "อุทัยธานี",
 "Uttaradit": "อุตรดิตถ์", "Yala": "ยะลา", "Yasothon": "ยโสธร", "Hat Yai": "หาดใหญ่", "Koh Samui": "เกาะสมุย", "Laos": "ลาว",
 "Myanmar": "เมียนมา พม่า", "Vientiane": "เวียงจันทน์", "Tachileik": "ท่าขี้เหล็ก", "Shan State": "รัฐฉาน",
}

UI = {
 "en": dict(ph="Search province, district or place (e.g. Chiang Mai, Hat Yai, เชียงราย)", lab="Search jobs", type="Type of work",
            all="All types of work", clear="Clear", n="{n} jobs shown", none="No job matches your search yet. Try another area or type of work, or post your availability with the form below."),
 "th": dict(ph="ค้นหาจังหวัด อำเภอ หรือสถานที่ (เช่น เชียงใหม่ หาดใหญ่ Chiang Rai)", lab="ค้นหางาน", type="ประเภทงาน",
            all="ทุกประเภทงาน", clear="ล้างการค้นหา", n="แสดง {n} งาน", none="ยังไม่มีงานที่ตรงกับการค้นหา ลองเปลี่ยนพื้นที่หรือประเภทงาน หรือส่งใบสมัครไว้ด้วยแบบฟอร์มด้านล่าง"),
}

CARD = re.compile(r'<article class="card[^"]*" id="([^"]+)"[^>]*>.*?</article>', re.S)


def text(h):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h))).strip()


def info(s):
    """card id -> (where, kind, title) for the project cards (.cards.fl)."""
    i = s.index('<div class="cards fl">'); j = s.index('<section class="finder perm"', i)
    out = {}
    for m in CARD.finditer(s, i, j):
        c = m.group(0)
        w = re.search(r'<div class="where">.*?<span>(.*?)(?:·\s*<span style="white-space:nowrap">|</span></div>)', c, re.S)
        k = re.search(r'<div class="kind">(.*?)</div>', c, re.S); t = re.search(r"<h3>(.*?)</h3>", c, re.S)
        out[m.group(1)] = (text(w.group(1)) if w else "", text(k.group(1)) if k else "", text(t.group(1)) if t else "")
    return out


src = {l: p.read_text(encoding="utf-8") for l, p in PAGES.items()}
cards = {l: info(s) for l, s in src.items()}


def work_of(cid):
    e = cards["en"].get(cid, ("", "", ""))
    hay = (cid + " " + e[1] + " " + e[2]).lower()
    w = [k for k, r in RULES.items() if re.search(r, hay)]
    if "cleaning" in w and "repair" not in w and "solar" in w and "install" not in hay:
        w.remove("solar")  # O&M cards are maintenance, not installation
    return w or ["solar"]


def q_of(cid):
    parts = [cards[l].get(cid, ("",))[0] for l in ("en", "th")]
    loc = " ".join(parts)
    extra = [f"{en} {th}" for en, th in PROV.items() if re.search(r"\b" + re.escape(en) + r"\b", loc, re.I) or th in loc]
    return re.sub(r"\s+", " ", (loc + " " + " ".join(extra)).replace('"', "")).strip().lower()


def bar(lang):
    u = UI[lang]; th = lang == "th"
    opts = "".join(f'<option value="{k}">{(t if th else e)}</option>' for k, e, t in TYPES)
    return (f'<!--jsearch--><div class="jsearch" role="search">'
            f'<label class="jsq"><span class="sr">{u["lab"]}</span><svg width="18" height="18" viewBox="0 0 20 20" aria-hidden="true"><circle cx="8.5" cy="8.5" r="6" fill="none" stroke="currentColor" stroke-width="2"/><path d="M13 13l5 5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
            f'<input id="js-q" type="search" placeholder="{u["ph"]}" autocomplete="off"></label>'
            f'<label class="jst"><span class="sr">{u["type"]}</span><select id="js-t"><option value="">{u["all"]}</option>{opts}</select></label>'
            f'<button type="button" id="js-x">{u["clear"]}</button><span id="js-n" aria-live="polite"></span></div>'
            f'<style>.jsearch{{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:-12px 0 28px}}'
            f'.jsearch .sr{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}}'
            f'.jsq{{flex:1 1 340px;display:flex;align-items:center;gap:10px;border:1.5px solid var(--navy);background:var(--white);padding:0 14px;color:var(--navy)}}'
            f'.jsq input{{flex:1;border:0;outline:0;font:inherit;font-size:16px;padding:13px 0;background:transparent;color:var(--ink);min-width:0}}'
            f'.jsq:focus-within{{border-color:var(--hot)}}'
            f'.jst select{{font:inherit;font-size:15px;padding:13px 12px;border:1.5px solid var(--navy);background:var(--white);color:var(--navy);border-radius:0;max-width:100%}}'
            f'#js-x{{font-family:var(--mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;padding:14px 14px;border:1.5px solid var(--navy);background:transparent;color:var(--navy);cursor:pointer}}'
            f'#js-n{{font-family:var(--mono);font-size:12px;letter-spacing:.06em;color:var(--mute);flex-basis:100%}}</style><!--/jsearch-->')


def script(lang):
    u = UI[lang]
    return ("<!--jsearchjs--><script>(function(){var q=document.getElementById('js-q'),t=document.getElementById('js-t'),x=document.getElementById('js-x'),n=document.getElementById('js-n'),"
            "em=document.getElementById('jobs-empty'),cs=document.querySelectorAll('.cards.fl .card'),bs=document.querySelectorAll('#projects .chip');if(!q)return;"
            "var N=" + repr(u["n"]) + ",NONE=" + repr(u["none"]) + ",EM0=em?em.innerHTML:'';"
            "function run(){var b=document.querySelector('#projects .chip[aria-pressed=\"true\"]'),f=b?b.getAttribute('data-f'):'all',"
            "w=q.value.toLowerCase().trim().replace(/\\s+/g,' ').split(/\\s*[,;]\\s*|\\s+(?=จังหวัด|อำเภอ|ตำบล|จ\\.|อ\\.|ต\\.)/).map(function(s){return s.replace(/^(จังหวัด|อำเภอ|ตำบล|จ\\.|อ\\.|ต\\.)\\s*/,'').trim()}).filter(Boolean),ty=t.value,k=0;"
            "cs.forEach(function(c){var tg=(c.getAttribute('data-tags')||'').split(' '),h3=c.querySelector('h3'),kd=c.querySelector('.kind'),hay=((c.getAttribute('data-q')||'')+' '+(h3?h3.textContent:'')+' '+(kd?kd.textContent:'')).toLowerCase(),"
            "ok=(f==='all'||tg.indexOf(f)>-1)&&(!ty||(' '+(c.getAttribute('data-work')||'')+' ').indexOf(' '+ty+' ')>-1)&&w.every(function(s){return hay.indexOf(s)>-1});"
            "c.hidden=!ok;if(ok)k++});n.textContent=(w.length||ty)?N.replace('{n}',k):'';"
            "if(em){em.style.display=k?'none':'block';if(w.length||ty)em.textContent=NONE;else em.innerHTML=EM0}}"
            "q.addEventListener('input',run);t.addEventListener('change',run);bs.forEach(function(b){b.addEventListener('click',function(){setTimeout(run,0)})});"
            "x.addEventListener('click',function(){q.value='';t.value='';run();q.focus()});"
            "var p=new URLSearchParams(location.search);if(p.get('q')){q.value=p.get('q')}if(p.get('type')){t.value=p.get('type')}if(p.get('q')||p.get('type')){run();var s=document.getElementById('projects');if(s)s.scrollIntoView()}"
            "})();</script><!--/jsearchjs-->")


for lang, path in PAGES.items():
    s = src[lang]
    s = re.sub(r"<!--jsearch-->.*?<!--/jsearch-->", "", s, flags=re.S)
    s = re.sub(r"<!--jsearchjs-->.*?<!--/jsearchjs-->", "", s, flags=re.S)
    # data attributes on the project cards
    i = s.index('<div class="cards fl">'); j = s.index('<section class="finder perm"', i)
    def tag(m):
        a = re.sub(r'\s(?:data-work|data-q)="[^"]*"', "", m.group(0))
        cid = re.search(r'id="([^"]+)"', a).group(1)
        return a[:-1] + f' data-work="{" ".join(work_of(cid))}" data-q="{html.escape(q_of(cid))}">'
    s = s[:i] + re.sub(r'<article class="card[^"]*" id="[^"]+"[^>]*>', tag, s[i:j]) + s[j:]
    # search bar right after the region chips of Project Based Jobs
    k = s.index('<div class="chips"', s.index('id="projects"')); k = s.index("</div>", k) + len("</div>")
    s = s[:k] + bar(lang) + s[k:]
    s = s.replace("</body>", script(lang) + "</body>", 1) if "</body>" in s else s + script(lang)
    path.write_text(s, encoding="utf-8")
    from collections import Counter
    print(lang, Counter(w for c in cards[lang] for w in work_of(c)))
