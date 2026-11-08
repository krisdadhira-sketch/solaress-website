# -*- coding: utf-8 -*-
"""'Jobs near me' on /job.html and /th/job.html.
- Every project card gets data-lat/data-lng: the APPROXIMATE centre of its area (district level, never the site),
  matched from the card's "where" line with PLACES below. Cards that can be done anywhere get no coordinates.
- Adds a bar under the job search: GPS button, province select, distance select. Cards are sorted nearest first,
  each shows "≈ N km", and cards beyond the chosen distance are hidden (works with region chips + search).
- Uses the location an installer saved on /location.html (same browser) automatically.
Idempotent (markers <!--jnear-->, <!--jnearjs-->). Re-run after adding jobs:  python3 tools/job_near.py
Add a new place to PLACES if a new job's area is not matched (the script prints unmatched cards)."""
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
PAGES = {"en": ROOT / "job.html", "th": ROOT / "th/job.html"}
NOWHERE = re.compile(r"anywhere in thailand|your workshop")
PLACES = [  # (regex on the English "where" text, lower case) -> approx. area centre
 (r"hat yai.*airport|airport.*hat yai", 6.93, 100.39), (r"ban pru", 6.93, 100.44), (r"khlong hae", 7.04, 100.49),
 (r"lam phlai", 6.98, 100.55), (r"singhanakhon", 7.24, 100.55), (r"hat yai", 7.007, 100.474), (r"songkhla", 7.19, 100.595),
 (r"nang lae", 20.03, 99.88), (r"rop wiang", 19.91, 99.83), (r"tha sai", 19.86, 99.84), (r"ban du", 19.97, 99.85),
 (r"si kham, mae fa luang", 20.17, 99.75), (r"si kham", 20.10, 99.80), (r"mae chan", 20.15, 99.85),
 (r"wiang phang kham|mae sai", 20.43, 99.88), (r"mae suai", 19.65, 99.54), (r"chiang rai", 19.91, 99.84),
 (r"mueang ngai", 19.53, 98.97), (r"chiang dao", 19.37, 98.96), (r"huai ?lan", 18.86, 99.15), (r"hang dong", 18.69, 98.92),
 (r"san kamphaeng", 18.75, 99.12), (r"san sai", 18.86, 99.04), (r"chiang mai", 18.788, 98.985),
 (r"ban ueam", 18.37, 99.49), (r"mae mo", 18.28, 99.66), (r"lampang", 18.289, 99.49),
 (r"ban hong", 18.31, 98.82), (r"lamphun", 18.574, 99.008),
 (r"tha duang|nong phai", 16.0, 101.06), (r"phetchabun", 16.419, 101.16),
 (r"mae pa|mae sot", 16.71, 98.57), (r"tak\b", 16.884, 99.126),
 (r"khlong chet|thanyaburi", 14.03, 100.73), (r"khlong sam|khlong luang", 14.06, 100.65), (r"pathum thani", 14.021, 100.525),
 (r"bangkok", 13.756, 100.502), (r"bang khonthi", 13.45, 99.98), (r"samut songkhram", 13.409, 100.002),
 (r"ao nang", 8.03, 98.82), (r"khlong thom", 7.92, 99.15), (r"krabi", 8.086, 98.906),
 (r"samui", 9.50, 100.00), (r"surat thani", 9.139, 99.33),
 (r"thung yao|palian|pa lian", 7.17, 99.69), (r"trang", 7.556, 99.611),
 (r"vientiane", 17.97, 102.60), (r"tachileik", 20.45, 99.88), (r"shan state", 20.79, 97.04),
]
CARD = re.compile(r'<article class="card p" id="([^"]+)"([^>]*)>')

def where_text(s, start):
    m = re.compile(r'<div class="where">.*?<span>(.*?)(?: · <span|</span>)', re.S).search(s, start)
    return re.sub(r"<[^>]+>", "", m.group(1)).lower() if m else ""

def geo_from_en():
    s = PAGES["en"].read_text(encoding="utf-8"); out = {}
    for m in CARD.finditer(s):
        w = where_text(s, m.end())
        if NOWHERE.search(w): out[m.group(1)] = None; continue
        for rx, la, ln in PLACES:
            if re.search(rx, w): out[m.group(1)] = (la, ln); break
        else: print("UNMATCHED:", m.group(1), "|", w)
    return out

T = {
 "en": dict(gps="📍 Jobs near me", prov="…or choose your province", any="Any distance", km="within {} km", sorted="Nearest jobs first, from", mine="your location", none="No jobs within this distance yet. Choose a larger distance, or keep your location updated and we will tell you when one opens near you.", upd="Update my location", no="Could not get your location. Choose your province instead.", aw="≈ {} km away", anyw="can be done anywhere"),
 "th": dict(gps="📍 งานใกล้ฉัน", prov="…หรือเลือกจังหวัดของท่าน", any="ทุกระยะทาง", km="ภายใน {} กม.", sorted="เรียงงานที่ใกล้ที่สุดก่อน จาก", mine="ตำแหน่งของท่าน", none="ยังไม่มีงานในระยะนี้ เลือกระยะที่ไกลขึ้น หรืออัปเดตตำแหน่งไว้ เราจะแจ้งท่านเมื่อมีงานใกล้", upd="อัปเดตตำแหน่งของฉัน", no="ไม่สามารถอ่านตำแหน่งได้ กรุณาเลือกจังหวัดแทน", aw="ห่าง ≈ {} กม.", anyw="ทำได้จากทุกที่"),
}

def build(lang, geo):
    p = PAGES[lang]; s = p.read_text(encoding="utf-8"); t = T[lang]
    def fix(m):
        attrs = re.sub(r' data-(lat|lng)="[^"]*"', "", m.group(2)); g = geo.get(m.group(1), "missing")
        if g == "missing": print(lang, "no EN geo for", m.group(1)); return m.group(0)
        add = f' data-lat="{g[0]}" data-lng="{g[1]}"' if g else ' data-lat="" data-lng=""'
        return f'<article class="card p" id="{m.group(1)}"{attrs}{add}>'
    s = CARD.sub(fix, s)
    s = re.sub(r"<!--jnear-->.*?<!--/jnear-->", "", s, flags=re.S); s = re.sub(r"<!--jnearjs-->.*?<!--/jnearjs-->", "", s, flags=re.S)
    loc = "/th/location.html" if lang == "th" else "/location.html"
    bar = (f'<!--jnear--><div class="jnear"><button type="button" id="jn-gps">{t["gps"]}</button><label><span class="sr">{t["prov"]}</span><select id="jn-p"><option value="">{t["prov"]}</option></select></label>'
           f'<label><span class="sr">km</span><select id="jn-r"><option value="99999">{t["any"]}</option>' + "".join(f'<option value="{k}"{" selected" if k==200 else ""}>{t["km"].format(k)}</option>' for k in (50,100,200,400)) + '</select></label>'
           f'<a href="{loc}" id="jn-upd">{t["upd"]} →</a><span id="jn-n" aria-live="polite"></span></div>'
           '<style>.jnear{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:-16px 0 28px}.jnear .sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}'
           '#jn-gps{font:inherit;font-size:15px;font-weight:600;padding:12px 16px;border:1.5px solid var(--navy);background:var(--navy);color:#fff;cursor:pointer}'
           '.jnear select{font:inherit;font-size:15px;padding:12px;border:1.5px solid var(--navy);background:var(--white);color:var(--navy);border-radius:0;max-width:100%}'
           '#jn-upd{font-size:14px;color:var(--navy);font-weight:600}#jn-n{font-family:var(--mono);font-size:12px;letter-spacing:.04em;color:var(--mute);flex-basis:100%}'
           '.jdist{display:inline-block;margin-left:8px;font-size:12px;font-weight:700;padding:2px 8px;border-radius:999px;background:#E7EBFF;color:#2E3AA8;white-space:nowrap}.jdist.near{background:#DCFCE7;color:#067647}</style><!--/jnear-->')
    assert s.count("<!--/jsearch-->") == 1; s = s.replace("<!--/jsearch-->", "<!--/jsearch-->" + bar, 1)
    js = ('<!--jnearjs--><script src="/js/th-provinces.js"></script><script>(function(){var TH=' + ("true" if lang == "th" else "false") +
      ',T=' + __import__("json").dumps(t, ensure_ascii=False) + ',$=function(i){return document.getElementById(i)},box=document.querySelector(".cards.fl"),cs=[].slice.call(document.querySelectorAll(".cards.fl .card")),P=$("jn-p"),R=$("jn-r"),N=$("jn-n"),q=$("js-q"),HOME=null,LBL="",ORD=cs.slice();if(!box||!P)return;'
      'TH_PROV.slice().sort(function(a,b){return(TH?a[1]:a[0]).localeCompare(TH?b[1]:b[0],TH?"th":"en")}).forEach(function(p){var o=document.createElement("option");o.value=p[0];o.textContent=TH?p[1]:p[0];P.appendChild(o)});'
      'function km(a,b,c,d){var r=Math.PI/180,x=Math.sin((c-a)*r/2),y=Math.sin((d-b)*r/2);return 12742*Math.asin(Math.sqrt(x*x+Math.cos(a*r)*Math.cos(c*r)*y*y))}'
      'function base(){if(q)q.dispatchEvent(new Event("input"))}'
      'function apply(){if(!HOME)return;var max=+R.value,k=0;cs.forEach(function(c){var la=parseFloat(c.getAttribute("data-lat")),ln=parseFloat(c.getAttribute("data-lng")),d=isNaN(la)?null:km(HOME[0],HOME[1],la,ln);c._d=d;var w=c.querySelector(".where span"),b=c.querySelector(".jdist");if(!b&&w){b=document.createElement("span");b.className="jdist";w.appendChild(b)}if(b){b.textContent=d==null?T.anyw:(d<5?T.aw.replace("≈ ","").replace("{}","< 5"):T.aw.replace("{}",Math.round(d/5)*5));b.className="jdist"+(d!=null&&d<=50?" near":"")}if(d!=null&&d>max)c.hidden=true;if(!c.hidden)k++});'
      'cs.slice().sort(function(a,b){return(a._d==null?5e4:a._d)-(b._d==null?5e4:b._d)}).forEach(function(c){box.appendChild(c)});var em=$("jobs-empty");if(em){em.style.display=k?"none":"block";if(!k)em.textContent=T.none}N.textContent=T.sorted+" "+LBL+(max<9999?" · "+T.km.replace("{}",max):"")+" · "+k}'
      'function set(la,ln,l){HOME=[la,ln];LBL=l;base();apply()}'
      '$("jn-gps").onclick=function(){if(!navigator.geolocation){N.textContent=T.no;return}N.textContent="…";navigator.geolocation.getCurrentPosition(function(p){P.value="";set(p.coords.latitude,p.coords.longitude,T.mine);try{var s=JSON.parse(localStorage.getItem("sess-installer-loc")||"{}");s.lat=p.coords.latitude.toFixed(5);s.lng=p.coords.longitude.toFixed(5);localStorage.setItem("sess-installer-loc",JSON.stringify(s))}catch(e){}},function(){N.textContent=T.no},{timeout:12000})};'
      'P.onchange=function(){var p=TH_PROV_FIND(P.value);if(p)set(p[2],p[3],TH?p[1]:p[0]);else{HOME=null;N.textContent="";ORD.forEach(function(c){box.appendChild(c);var b=c.querySelector(".jdist");if(b)b.remove()});base()}};R.onchange=function(){base();apply()};'
      'if(q){q.addEventListener("input",function(){setTimeout(apply,0)});var t=$("js-t");if(t)t.addEventListener("change",function(){setTimeout(apply,0)});var x=$("js-x");if(x)x.addEventListener("click",function(){setTimeout(apply,0)})}'
      'document.querySelectorAll("#projects .chip").forEach(function(b){b.addEventListener("click",function(){setTimeout(apply,5)})});'
      'var u=new URLSearchParams(location.search),s={};try{s=JSON.parse(localStorage.getItem("sess-installer-loc")||"{}")}catch(e){}'
      'if(s.lat&&s.lng)set(+s.lat,+s.lng,T.mine);else if(s.province){P.value=s.province;P.onchange()}if(u.get("near")){var pr=document.getElementById("projects");if(pr)pr.scrollIntoView();if(!HOME)$("jn-gps").click()}})();</script><!--/jnearjs-->')
    assert s.count("<!--/jsearchjs-->") == 1; s = s.replace("<!--/jsearchjs-->", "<!--/jsearchjs-->" + js, 1)
    p.write_text(s, encoding="utf-8"); print(lang, "ok")

if __name__ == "__main__":
    g = geo_from_en()
    for l in PAGES: build(l, g)
