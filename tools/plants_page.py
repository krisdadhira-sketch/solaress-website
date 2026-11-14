"""Build the public "Plants by Province" pages (plants.html, th/plants.html) and data/plant-index.json.

Plants come from data/plant-codes.json and are clustered by province (Thai postcode, first 2 digits).
Each plant card lists the reports that cite its code (technical-notes.html) and the jobs that cite it
(job.html). Jobs without a plant code are listed under their province when the province name appears
in the job's search text. No customer names: the public pages use plant codes only.

Run from the repo root:  python3 tools/plants_page.py
"""
import html, json, re
from collections import defaultdict

CODE = re.compile(r'\b[A-Z]{2}-\d{5}-\d+-\d{2}\b')

PROV_TH = {"Chiang Rai": "เชียงราย", "Songkhla": "สงขลา", "Chiang Mai": "เชียงใหม่", "Pathum Thani": "ปทุมธานี",
           "Lamphun": "ลำพูน", "Surat Thani": "สุราษฎร์ธานี", "Trang": "ตรัง", "Shan State": "รัฐฉาน (เมียนมา)",
           "Lampang": "ลำปาง", "Bangkok": "กรุงเทพมหานคร", "Samut Songkhram": "สมุทรสงคราม", "Krabi": "กระบี่",
           "Samut Prakan": "สมุทรปราการ", "Vientiane": "เวียงจันทน์ (ลาว)", "Tak": "ตาก", "Phetchabun": "เพชรบูรณ์"}
PROV_Q = {"Chiang Rai": ["chiang rai", "เชียงราย"], "Songkhla": ["songkhla", "hat yai", "สงขลา", "หาดใหญ่"],
          "Chiang Mai": ["chiang mai", "เชียงใหม่"], "Pathum Thani": ["pathum thani", "ปทุมธานี"],
          "Lamphun": ["lamphun", "ลำพูน"], "Surat Thani": ["surat thani", "koh samui", "สุราษฎร์ธานี", "สมุย"],
          "Trang": ["trang", "ตรัง"], "Lampang": ["lampang", "ลำปาง"], "Bangkok": ["bangkok", "กรุงเทพ"],
          "Samut Songkhram": ["samut songkhram", "สมุทรสงคราม"], "Krabi": ["krabi", "กระบี่"],
          "Samut Prakan": ["samut prakan", "สมุทรปราการ"], "Tak": ["tak ", "ตาก"], "Phetchabun": ["phetchabun", "เพชรบูรณ์"],
          "Shan State": ["shan", "tachileik"], "Vientiane": ["vientiane"]}
TYPE = {"en": {"Hybrid with battery": "Hybrid with battery", "Grid-tied, no battery": "Grid-tied, no battery"},
        "th": {"Hybrid with battery": "ไฮบริด มีแบตเตอรี่", "Grid-tied, no battery": "ออนกริด ไม่มีแบตเตอรี่"}}
T = {
 "en": dict(title="Solar Plants by Province – Plant Codes, Jobs and Reports | Solar ESS",
   desc="Solar ESS plants grouped by province: plant codes, plant reports and installer jobs near each plant.",
   h1="Plants by Province", lede="Every plant Solar ESS installs or looks after has a code instead of a customer name. Plants are grouped here by province, so installers can see the work near them and owners can find the reports for their plant.",
   how="How to read a code", howtxt="<code>[Platform][Type]-[Postcode]-[Inverter kW]-[No.]</code> – e.g. <code>SG-52000-20-01</code> is a SolisCloud grid-tied plant in postcode area 52000 (Lampang) with a 20 kW inverter, the first such plant. The first two postcode digits give the province.",
   near="Installers: register your location to be matched with jobs near these plants", nearbtn="Register my location",
   plants="plants", reports="Reports", jobs="Jobs", none="No published report yet", nojob="No job posted for this plant",
   area_jobs="Other jobs in this province", kwp="kWp", inv="kW inverter", since="Since", top="All provinces",
   tech="technical-notes.html", job="job.html", loc="location.html", prefix=""),
 "th": dict(title="โรงไฟฟ้าโซลาร์ตามจังหวัด – รหัสโรงไฟฟ้า งาน และรายงาน | Solar ESS",
   desc="โรงไฟฟ้าโซลาร์ของ Solar ESS แยกตามจังหวัด พร้อมรหัสโรงไฟฟ้า รายงาน และงานสำหรับช่างใกล้แต่ละโรงไฟฟ้า",
   h1="โรงไฟฟ้าตามจังหวัด", lede="ทุกโรงไฟฟ้าที่ บริษัท โซลาร์ เอสส์ จำกัด ติดตั้งหรือดูแล ใช้รหัสแทนชื่อลูกค้า หน้านี้จัดกลุ่มโรงไฟฟ้าตามจังหวัด เพื่อให้ช่างเห็นงานใกล้ตัว และเจ้าของระบบหารายงานของโรงไฟฟ้าตนเองได้",
   how="วิธีอ่านรหัส", howtxt="<code>[แพลตฟอร์ม][ประเภท]-[รหัสไปรษณีย์]-[ขนาดอินเวอร์เตอร์ kW]-[ลำดับ]</code> เช่น <code>SG-52000-20-01</code> คือโรงไฟฟ้าออนกริดบน SolisCloud ในเขตรหัสไปรษณีย์ 52000 (ลำปาง) อินเวอร์เตอร์ 20 kW เป็นโรงแรกของกลุ่มนี้ เลขสองหลักแรกของรหัสไปรษณีย์บอกจังหวัด",
   near="ช่าง: ลงทะเบียนตำแหน่งของคุณ เพื่อรับงานใกล้โรงไฟฟ้าเหล่านี้", nearbtn="ลงทะเบียนตำแหน่ง",
   plants="โรงไฟฟ้า", reports="รายงาน", jobs="งาน", none="ยังไม่มีรายงานที่เผยแพร่", nojob="ยังไม่มีงานสำหรับโรงไฟฟ้านี้",
   area_jobs="งานอื่นในจังหวัดนี้", kwp="kWp", inv="kW อินเวอร์เตอร์", since="เริ่มใช้งาน", top="ทุกจังหวัด",
   tech="/th/technical-notes.html", job="/th/job.html", loc="/th/location.html", prefix="/"),
}

def articles(path, pat):
    s = open(path, encoding="utf-8").read()
    out = []
    for m in re.finditer(pat, s, re.S):
        head, body = m.group(1), m.group(2)
        i = re.search(r'id="([^"]+)"', head)
        h = re.search(r'<h[23][^>]*>(.*?)</h[23]>', body, re.S)
        if not i or not h:
            continue
        title = re.sub(r"<[^>]+>", "", h.group(1)).strip()
        out.append(dict(id=i.group(1), title=html.unescape(title), codes=sorted(set(CODE.findall(head + body))),
                        q=(re.search(r'data-q="([^"]*)"', head) or [None, ""])[1].lower(),
                        posted=(re.search(r'data-posted="([^"]*)"', head) or [None, ""])[1]))
    return out

def build():
    plants = json.load(open("data/plant-codes.json", encoding="utf-8"))["plants"]
    known = {p["code"] for p in plants}
    rep = {"en": articles("technical-notes.html", r'(<article class="tnote"[^>]*>)(.*?)</article>'),
           "th": articles("th/technical-notes.html", r'(<article class="tnote"[^>]*>)(.*?)</article>')}
    jobs = {"en": articles("job.html", r'(<article class="card p"[^>]*>)(.*?)</article>'),
            "th": articles("th/job.html", r'(<article class="card p"[^>]*>)(.*?)</article>')}
    # Thai job titles keyed by id (fall back to English)
    index = {"updated": None, "plants": {}}
    for p in plants:
        c = p["code"]
        index["plants"][c] = {"province": p["province"], "postcode": p["postcode"],
                              "reports": [a["id"] for a in rep["en"] if c in a["codes"]],
                              "jobs": [a["id"] for a in jobs["en"] if c in a["codes"]]}
    json.dump(index, open("data/plant-index.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    for lang in ("en", "th"):
        t = T[lang]
        rt = {a["id"]: a["title"] for a in rep[lang]}
        jt = {a["id"]: a["title"] for a in jobs[lang]}
        groups = defaultdict(list)
        for p in plants:
            groups[(p["country"] != "TH", p["postcode"][:2] if p["country"] == "TH" else p["country"], p["province"])].append(p)
        order = sorted(groups, key=lambda k: (k[0], -len(groups[k]), k[2]))
        name = (lambda pr: PROV_TH.get(pr, pr)) if lang == "th" else (lambda pr: pr)
        chips = "".join(f'<a href="#prov-{re.sub(r"[^a-z]+","-",k[2].lower())}">{html.escape(name(k[2]))} <span>{len(groups[k])}</span></a>' for k in order)
        secs = []
        for k in order:
            pr = k[2]; ps = sorted(groups[k], key=lambda p: p["code"])
            pid = re.sub(r"[^a-z]+", "-", pr.lower())
            used_jobs = set()
            cards = []
            for p in ps:
                c = p["code"]; ix = index["plants"][c]
                rl = "".join(f'<li><a href="{t["tech"]}#{r}">{html.escape(rt.get(r, r))}</a></li>' for r in ix["reports"])
                jl = "".join(f'<li><a href="{t["job"]}#{j}">{html.escape(jt.get(j, j))}</a></li>' for j in ix["jobs"])
                used_jobs.update(ix["jobs"])
                comm = p["commissioned"] or ""
                cards.append(f'''<div class="pcard" id="plant-{c}"><div class="pc-h"><code>{c}</code><span class="pc-t">{html.escape(TYPE[lang][p["type"]])}</span></div>
<div class="pc-f">{f'<b>{p["pv_kwp"]:g} {t["kwp"]}</b> · ' if p["pv_kwp"] else ""}{p["inverter_kw"]:g} {t["inv"]} · {p["phase"]} · {p["platform"]}{f' · {t["since"]} {comm}' if comm else ''}</div>
<div class="pc-l"><b>{t["reports"]}</b>{f"<ul>{rl}</ul>" if rl else f'<p class="pc-n">{t["none"]}</p>'}</div>
<div class="pc-l"><b>{t["jobs"]}</b>{f"<ul>{jl}</ul>" if jl else f'<p class="pc-n">{t["nojob"]}</p>'}</div></div>''')
            keys = PROV_Q.get(pr, [pr.lower()])
            aj = [a for a in jobs[lang] if a["id"] not in used_jobs and any(q in a["q"] for q in keys)]
            aj = sorted(aj, key=lambda a: a["posted"], reverse=True)
            ajl = "".join(f'<li><a href="{t["job"]}#{a["id"]}">{html.escape(a["title"])}</a></li>' for a in aj)
            pc = f'{k[1]}xxx' if not k[0] else k[1]
            secs.append(f'''<section class="prov" id="prov-{pid}"><h2>{html.escape(name(pr))} <small>{pc} · {len(ps)} {t["plants"]}</small></h2>
<div class="pgrid">{"".join(cards)}</div>{f'<details class="ajobs"><summary>{t["area_jobs"]} ({len(aj)})</summary><ul>{ajl}</ul></details>' if aj else ''}</section>''')
        style = """<style>
.pl-wrap{max-width:1180px;margin:0 auto;padding:40px 22px 70px}
.pl-wrap h1{margin:0 0 10px}.pl-lede{max-width:820px;font-size:17px;line-height:1.6}
.pl-how{background:#eef0fb;border-left:4px solid #4a4fd8;padding:12px 16px;border-radius:8px;margin:18px 0;font-size:15px;line-height:1.6}
.pl-chips{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 8px}.pl-chips a{border:1px solid #d9dcef;border-radius:999px;padding:6px 12px;text-decoration:none;color:#101a3a;font-weight:600;font-size:14px;background:#fff}
.pl-chips a span{color:#4a4fd8;margin-left:4px}.pl-near{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin:14px 0 6px;font-size:15px}
.pl-near a{background:#101a3a;color:#fff;border-radius:999px;padding:8px 16px;text-decoration:none;font-weight:600}
.prov{margin-top:40px;scroll-margin-top:90px}.prov h2{margin:0 0 14px;color:#101a3a}.prov h2 small{font-size:15px;color:#6b7280;font-weight:500;margin-left:6px}
.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}
.pcard{border:1px solid #d9dcef;border-radius:14px;padding:14px 16px;background:#fff;scroll-margin-top:90px}.pcard:target{outline:3px solid #4a4fd8}
.pc-h{display:flex;justify-content:space-between;align-items:center;gap:8px}.pc-h code{font-size:16px;font-weight:700;color:#101a3a;background:#eef0fb;padding:3px 8px;border-radius:6px}
.pc-t{font-size:12.5px;color:#4a4fd8;font-weight:600}.pc-f{font-size:14px;color:#374151;margin:8px 0 6px}
.pc-l{font-size:14px;margin-top:6px}.pc-l b{font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:#6b7280}.pc-l ul{margin:4px 0 0;padding-left:18px}.pc-l li{margin:2px 0}
.pc-n{margin:2px 0 0;color:#9ca3af;font-size:13.5px}.ajobs{margin-top:12px;font-size:14.5px}.ajobs summary{cursor:pointer;font-weight:600;color:#101a3a}.ajobs ul{columns:2;column-gap:28px;margin-top:8px}
@media(max-width:700px){.ajobs ul{columns:1}}
</style>"""
        main = f'''<main id="main" tabindex="-1">{style}<div class="pl-wrap"><h1>{t["h1"]}</h1><p class="pl-lede">{t["lede"]}</p>
<div class="pl-how"><b>{t["how"]}:</b> {t["howtxt"]}</div>
<div class="pl-near"><span>{t["near"]}</span><a href="{t["loc"]}">{t["nearbtn"]}</a></div>
<nav class="pl-chips" aria-label="{t["top"]}">{chips}</nav>{"".join(secs)}</div></main>'''
        src = "technical-notes.html" if lang == "en" else "th/technical-notes.html"
        s = open(src, encoding="utf-8").read()
        a, b = s.index('<main id="main"'), s.index("</main>") + len("</main>")
        page = s[:a] + main + s[b:]
        page = re.sub(r"<title>.*?</title>", f"<title>{html.escape(t['title'])}</title>", page, count=1, flags=re.S)
        page = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{html.escape(t["desc"])}">', page, count=1)
        url = "https://solaress.org/plants" if lang == "en" else "https://solaress.org/th/plants"
        page = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', page, count=1)
        page = re.sub(r'(<meta property="og:url" content=")[^"]*', r"\g<1>" + url, page)
        page = re.sub(r'(<meta property="og:title" content=")[^"]*', r"\g<1>" + html.escape(t["title"]), page)
        page = re.sub(r'(<meta (?:property="og:description"|name="twitter:description") content=")[^"]*', r"\g<1>" + html.escape(t["desc"]), page)
        page = re.sub(r'(<meta name="twitter:title" content=")[^"]*', r"\g<1>" + html.escape(t["title"]), page)
        page = re.sub(r'<link rel="alternate" hreflang="zh-Hans"[^>]*>\n?', "", page)
        page = re.sub(r'(<link rel="alternate" hreflang="[^"]*" href="https://solaress.org/(?:th/)?)technical-notes"', r'\1plants"', page)
        page = re.sub(r'<span class="langsw">.*?</span>', lambda m: re.sub(r'<a href="/zh/technical-notes.html"[^>]*>[^<]*</a>', "", m.group(0)).replace("technical-notes.html", "plants.html"), page, count=1, flags=re.S)
        # drop JSON-LD blocks copied from the technical page (they describe that page, not this one)
        page = re.sub(r'<script type="application/ld\+json">.*?</script>', "", page, flags=re.S)
        open("plants.html" if lang == "en" else "th/plants.html", "w", encoding="utf-8").write(page)
    print("plants:", len(plants), "| reports linked:", sum(len(v["reports"]) for v in index["plants"].values()),
          "| jobs linked:", sum(len(v["jobs"]) for v in index["plants"].values()))

if __name__ == "__main__":
    build()
