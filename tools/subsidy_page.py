#!/usr/bin/env python3
"""Build /th/solar-subsidy-50000 and /solar-subsidy-50000 from the news page shell.
Edit CONTENT below and re-run: python3 tools/subsidy_page.py"""
import re, json, os, html
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
UPDATED_ISO = '2026-10-27'

C = {
'th': dict(
 shell='th/news.html', out='th/solar-subsidy-50000.html', url='https://solaress.org/th/solar-subsidy-50000',
 title='โซลาร์ 50,000 บาท: ใครได้สิทธิ์ ลงทะเบียนเมื่อไร ต้องจ่ายเองเท่าไร | Solar ESS',
 desc='สรุปโครงการโซลาร์ภาคประชาชน อุดหนุน 50,000 บาทต่อครัวเรือน 1 ล้านสิทธิ์: เงื่อนไข การลงทะเบียนผ่าน กฟภ./กฟน. ค่าใช้จ่ายที่ต้องจ่ายเอง สินเชื่อ และการขายไฟคืน 2.20 บาท อัปเดต 27 ต.ค. 2569',
 updated='อัปเดต 27 ตุลาคม 2569', crumb_news='ข่าวสาร', crumb_home='หน้าแรก',
 h1='โซลาร์ 50,000 บาท<br>ใครได้ ลงทะเบียนเมื่อไร<br>ต้องจ่ายเองเท่าไร',
 lede='สรุปโครงการ "โซลาร์ภาคประชาชน" ที่รัฐบาลอุดหนุนค่าติดตั้งโซลาร์เซลล์ครัวเรือนละ 50,000 บาท จำนวน 1 ล้านสิทธิ์ เขียนให้อ่านง่าย และจะอัปเดตทุกครั้งที่มีประกาศใหม่',
 status_h='สถานะล่าสุด',
 status=['คณะกรรมการกลั่นกรองการใช้จ่ายเงินกู้เห็นชอบแล้ว (19–20 ต.ค. 2569) วงเงิน 50,000 ล้านบาท',
         'เสนอคณะรัฐมนตรีพิจารณาวันที่ <b>27 ตุลาคม 2569</b> มีรายงานว่าจะเปิดลงทะเบียนทันทีหลัง ครม. อนุมัติ ผ่าน กฟภ. และ กฟน.',
         '<b>เว็บลงทะเบียนทางการ:</b> กฟภ. <a href="https://peoplesolar.pea.co.th" rel="noopener">peoplesolar.pea.co.th</a> (ขึ้นข้อความ "เตรียมเปิดให้บริการ เริ่มใช้งานได้ภายในวันที่ 27 ตุลาคม 2569" ตรวจเมื่อ 27 ต.ค. 06:00 น.) · กฟน. <a href="https://myenergy.mea.or.th/" rel="noopener">myenergy.mea.or.th</a> ระวังเว็บปลอม ลงทะเบียนผ่านสองเว็บนี้เท่านั้น',
         'หลักเกณฑ์ฉบับทางการยังไม่ประกาศ รายละเอียดด้านล่างมาจากการแถลงข่าวและรายงานข่าว จึงอาจเปลี่ยนได้'],
 kf=[('50,000 บาท','เงินอุดหนุนต่อครัวเรือน'),('1 ล้าน','สิทธิ์ ระยะแรก'),('2.20 บาท','ต่อหน่วย ขายไฟส่วนเกิน')],
 sections=[
  ('ใครได้สิทธิ์ และติดตั้งแบบไหนได้',
   ['ครัวเรือนละ 1 สิทธิ์ ผู้สมัครควรเป็นผู้ใช้ไฟที่มีมิเตอร์ในชื่อของตนเอง',
    'ติดตั้งได้ทั้งบนหลังคา บนพื้นดิน และแบบลอยน้ำในบ่อ สำหรับบ้านที่หลังคาไม่เหมาะ',
    'มีรายงานว่าขนาดระบบ 5–10 kW และส่งไฟออกขายได้ไม่เกิน 5 kW',
    'การไฟฟ้าเปลี่ยนเป็นสมาร์ตมิเตอร์ให้ โดยผู้ใช้ไฟไม่ต้องจ่ายค่าเปลี่ยนมิเตอร์']),
  ('เงิน 50,000 บาทจ่ายอย่างไร',
   ['แนวทางเบื้องต้นของ กฟภ.: เมื่อติดตั้งเสร็จและการไฟฟ้าตรวจสอบว่าใช้งานได้ รัฐจะโอนเงินอุดหนุนให้<b>ผู้ติดตั้ง</b>โดยตรง ไม่ได้โอนให้เจ้าของบ้าน',
    'ผู้ติดตั้งต้องอยู่ในรายชื่อผู้ประกอบการ (Vendor List) ของการไฟฟ้า ซึ่ง กฟภ. มีผู้ลงทะเบียนแล้วกว่า 1,000 ราย คุณสมบัติอย่างเป็นทางการยังไม่ประกาศ',
    'ดังนั้นเจ้าของบ้านจ่ายเฉพาะส่วนที่เหลือหลังหักเงินอุดหนุน ทั้งนี้วิธีจ่ายเงินยังไม่เป็นทางการ บางรายงานระบุว่ารัฐจะจ่ายตรงให้ประชาชน']),
  ('ตัวอย่างค่าใช้จ่าย',
   ['ตัวอย่างจาก กฟภ.: ระบบ 5 kW ราคาประมาณ 140,000 บาท หักเงินอุดหนุน 50,000 บาท เหลือจ่ายเองประมาณ <b>90,000 บาท</b>',
    'เงินอุดหนุนจึงช่วยราวหนึ่งในสามของระบบ 5 kW ไม่ใช่ทั้งหมด ราคาจริงขึ้นกับขนาดระบบ อุปกรณ์ และหน้างาน',
    'ส่วนที่เหลือจ่ายเป็นเงินสด หรือใช้สินเชื่อดอกเบี้ยต่ำจากธนาคารออมสิน ธอส. และ ธ.ก.ส. ซึ่งผ่อนคืนจากรายได้การขายไฟ มีรายงานดอกเบี้ยราว 2.5% ต่อปี ระยะประมาณ 7 ปี (ยังไม่เป็นทางการ)']),
  ('ขายไฟคืนได้เท่าไร',
   ['รับซื้อไฟส่วนเกินแบบ net billing ที่ <b>2.20 บาทต่อหน่วย</b> มีรายงานว่าคณะกรรมการนโยบายพลังงานแห่งชาติขยายเป้ารับซื้อเป็น 10,000 MW และระยะเวลารับซื้อเป็น 20 ปี แต่ประกาศปัจจุบันบนเว็บ กฟน. ยังระบุ 10 ปี (เป้า 500 MW) จึงต้องรอหลักเกณฑ์ใหม่',
    'ไฟที่ใช้เองตอนกลางวันมีค่ามากกว่าไฟที่ขาย เพราะทดแทนไฟที่ซื้อในราคาเต็ม บ้านที่ใช้ไฟกลางวันมากจึงคุ้มกว่า',
    'ผู้ที่ติดตั้งเองโดยไม่เข้าโครงการ ยังลดหย่อนภาษีได้สูงสุด 200,000 บาท']),
  ('สิ่งที่ควรทำตอนนี้',
   ['ตรวจว่ามิเตอร์ไฟอยู่ในชื่อของคุณ และเก็บบิลค่าไฟ 3 เดือนล่าสุด',
    'ดูว่าบ้านใช้ไฟ 1 เฟสหรือ 3 เฟส และใช้ไฟช่วงกลางวันมากแค่ไหน',
    'ถ้าไฟดับบ่อย พิจารณาระบบไฮบริดพร้อมแบตเตอรี่ (ถามให้ชัดว่าโครงการครอบคลุมแบตเตอรี่หรือไม่)',
    '<b>อย่าจ่ายมัดจำ</b>ให้ใครที่อ้างว่าได้สิทธิ์แล้ว ก่อนมีประกาศหลักเกณฑ์และช่องทางสมัครอย่างเป็นทางการ']),
 ],
 faq_h='คำถามที่พบบ่อย',
 faq=[('ลงทะเบียนโซลาร์ 50,000 บาทได้ที่ไหน','ต่างจังหวัด: กฟภ. ที่ peoplesolar.pea.co.th กรุงเทพฯ นนทบุรี สมุทรปราการ: กฟน. ที่ myenergy.mea.or.th มีรายงานว่าจะเปิดทันทีหลัง ครม. อนุมัติ ให้ใช้ช่องทางทางการของการไฟฟ้าเท่านั้น'),
      ('เงินอุดหนุนโอนเข้าบัญชีเจ้าของบ้านหรือไม่','ตามแนวทางเบื้องต้นของ กฟภ. เงินอุดหนุนจ่ายให้ผู้ติดตั้งโดยตรงหลังการไฟฟ้าตรวจสอบระบบแล้ว เจ้าของบ้านจ่ายเฉพาะส่วนที่เหลือ'),
      ('ระบบ 5 kW ต้องจ่ายเองเท่าไร','ตัวอย่างจาก กฟภ. ระบบประมาณ 140,000 บาท หักเงินอุดหนุนแล้วเหลือประมาณ 90,000 บาท ราคาจริงขึ้นกับอุปกรณ์และหน้างาน'),
      ('ขายไฟคืนได้หน่วยละเท่าไร','2.20 บาทต่อหน่วย แบบ net billing ส่งไฟออกได้ไม่เกิน 5 kW'),
      ('ติดตั้งบนพื้นหรือบนบ่อได้ไหม','ได้ โครงการขยายให้ครอบคลุมการติดตั้งบนพื้นดินและแบบลอยน้ำ สำหรับบ้านที่หลังคาไม่เหมาะ')],
 cta_h='อยากรู้ว่าบ้านคุณควรติดขนาดเท่าไร',
 cta='ดูตัวอย่างใบเสนอราคาจริงของเรา แล้วขอใบเสนอราคาสำหรับบ้านของคุณ เราออกแบบให้ใช้ไฟเองตอนกลางวันก่อน และแจ้งคุณทันทีเมื่อหลักเกณฑ์การสมัครออกมา',
 cta_btn='ดูตัวอย่างใบเสนอราคา', cta_btn2='นัดปรึกษาฟรี',
 src_h='แหล่งข้อมูล',
 note='โซลาร์ เอสส์ ยินดีแบ่งปันข้อมูลที่อัปเดตและประสบการณ์ตรงจากหน้างานจริงเสมอ หน้านี้สรุปจากรายงานข่าวและการแถลงของหน่วยงาน ไม่ใช่ประกาศทางการ',
 news='/th/news', home='/th/', quote='/th/quotation', consult='/th/#consult'),
'en': dict(
 shell='news.html', out='solar-subsidy-50000.html', url='https://solaress.org/solar-subsidy-50000',
 title="Thailand's 50,000-Baht Solar Subsidy: Who Qualifies, When to Register, What You Pay | Solar ESS",
 desc="Plain-English guide to Thailand's 50,000-baht household solar subsidy for 1 million homes: eligibility, PEA/MEA registration, what you still pay, loans and the 2.20-baht sell-back rate. Updated 27 Oct 2026.",
 updated='Updated 27 October 2026', crumb_news='News', crumb_home='Home',
 h1="Thailand's 50,000-baht<br>solar subsidy",
 lede='A plain-language guide to the "People\'s Solar" scheme: a 50,000-baht installation subsidy for each of 1 million households. We update this page whenever new rules are announced.',
 status_h='Latest status',
 status=['The loan screening committee approved the 50-billion-baht plan (19–20 Oct 2026).',
         'It goes to Cabinet on <b>27 October 2026</b>. Registration is reported to open right after approval, through PEA and MEA.',
         '<b>Official registration sites:</b> PEA <a href="https://peoplesolar.pea.co.th" rel="noopener">peoplesolar.pea.co.th</a> (showing "opening soon, available by 27 October 2026" when checked at 06:00 on 27 Oct) · MEA <a href="https://myenergy.mea.or.th/" rel="noopener">myenergy.mea.or.th</a>. Beware of fake sites: register only through these two.',
         'The official rules have not been published yet. Details below come from government briefings and news reports and may change.'],
 kf=[('50,000 baht','subsidy per household'),('1 million','rights in phase 1'),('2.20 baht','per unit for surplus power')],
 sections=[
  ('Who qualifies and what can be installed',
   ['One right per household; applicants should be the electricity account holder with a meter in their own name.',
    'Rooftop, ground-mounted and floating (pond) systems are all allowed, for homes whose roofs are unsuitable.',
    'Systems are reported at 5–10 kW, with no more than 5 kW exported.',
    'The utility installs a smart meter free of charge.']),
  ('How the 50,000 baht is paid',
   ["PEA's preliminary plan: once the system is installed and the utility confirms it works, the subsidy is paid <b>directly to the installer</b>, not to the homeowner.",
    'Installers must be on the utility vendor list; PEA already has more than 1,000 registered vendors. Official qualifications are not yet published.',
    'The homeowner pays only the remainder. The payment method is not final; some reports say the government will pay households directly.']),
  ('Example cost',
   ['PEA example: a 5 kW system costs about 140,000 baht. After the 50,000-baht subsidy, the owner pays about <b>90,000 baht</b>.',
    'So the subsidy covers roughly a third of a 5 kW system, not most of it. Real prices depend on size, equipment and site.',
    'The remainder can be paid in cash or with low-interest loans from GSB, GH Bank and BAAC, repaid from sell-back income. Reports mention about 2.5% a year over about 7 years (not yet official).']),
  ('How much you get for selling power',
   ['Surplus power is bought by net billing at <b>2.20 baht per unit</b>. The national energy policy council is reported to have raised the target to 10,000 MW and the contract to 20 years, but MEA\'s current notice still says 10 years (500 MW target), so check the new rules.',
    'Power you use yourself in the daytime is worth much more than power you sell, because it replaces electricity bought at the full price.',
    'Homeowners who install without the scheme can still claim a tax deduction of up to 200,000 baht.']),
  ('What to do now',
   ['Check that the electricity meter is in your name and keep your last three bills.',
    'Find out whether your home is single-phase or three-phase and how much power you use in the daytime.',
    'If you have frequent power cuts, consider a hybrid system with battery (ask whether the scheme covers batteries).',
    '<b>Do not pay a deposit</b> to anyone who claims you already have a right before the official rules and application channel are announced.']),
 ],
 faq_h='Frequently asked questions',
 faq=[('Where do I register for the 50,000-baht solar subsidy?','Outside Bangkok: PEA at peoplesolar.pea.co.th. Bangkok, Nonthaburi and Samut Prakan: MEA at myenergy.mea.or.th. Registration is reported to open right after Cabinet approval. Use only these official sites.'),
      ('Is the subsidy paid to the homeowner?',"Under PEA's preliminary plan, the subsidy is paid directly to the installer after the utility has inspected the system. The homeowner pays the remainder."),
      ('How much do I pay for a 5 kW system?','PEA\'s example: about 140,000 baht, so about 90,000 baht after the subsidy. Actual prices depend on equipment and site.'),
      ('How much do I get for power I sell back?','2.20 baht per unit under net billing, with exports limited to 5 kW.'),
      ('Can I install on the ground or on a pond?','Yes. The scheme was widened to cover ground-mounted and floating systems for homes with unsuitable roofs.')],
 cta_h='Not sure what size your home needs?',
 cta='See our real sample quotations, then request one for your home. We design for daytime self-use first and will let you know as soon as the application rules are published.',
 cta_btn='See sample quotations', cta_btn2='Book a free consultation',
 src_h='Sources',
 note='Solar ESS is always happy to share up-to-date information and our first-hand experience. This page summarises news reports and government briefings; it is not an official announcement.',
 news='/news', home='/', quote='/quotation', consult='/#consult'),
}
SOURCES = [('PEA – โซลาร์ภาคประชาชน registration site', 'https://peoplesolar.pea.co.th'),
           ('MEA – MyEnergy registration site and notices', 'https://myenergy.mea.or.th/'),
           ('Thansettakij – PEA plan: subsidy paid to installer after inspection; 140,000-baht example (22 Oct 2026)', 'https://www.thansettakij.com/economy/energy/671963'),
           ('Thansettakij – screening board approves 50bn baht; 5–10 kW, 2.20 baht, 20 years, loans (20 Oct 2026)', 'https://www.thansettakij.com/economy/671800'),
           ('Daily News – conditions: rooftop, ground and floating; free smart meter (26 Oct 2026)', 'https://www.dailynews.co.th/news/6305233/'),
           ('The Nation – Cabinet review on 27 Oct, registration via MEA/PEA after approval (26 Oct 2026)', 'https://www.nationthailand.com/news/policy/40072746'),
           ('Bangkok Biz News – One Stop Service and app registration (22 Oct 2026)', 'https://www.bangkokbiznews.com/economics/1257535')]

def build(lang):
    c = C[lang]; shell = open(os.path.join(ROOT, c['shell']), encoding='utf-8').read()
    head_end = shell.find('</head>'); body_start = shell.find('<section', shell.find('<body')); foot = shell.find('<footer')
    head = shell[:head_end]
    e = lambda x: html.escape(x, quote=True)
    # title / meta
    head = re.sub(r'<title>.*?</title>', f'<title>{e(c["title"])}</title>', head, flags=re.S)
    head = re.sub(r'(<meta (?:property|name)="(?:og:title|twitter:title)" content=")[^"]*"', lambda m: m.group(1) + e(c['title']) + '"', head)
    head = re.sub(r'(<meta (?:property|name)="(?:description|og:description|twitter:description)" content=")[^"]*"', lambda m: m.group(1) + e(c['desc']) + '"', head)
    head = re.sub(r'<meta property="og:type" content="[^"]*">', '<meta property="og:type" content="article">', head)
    head = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{c["url"]}">', head)
    head = re.sub(r'<link rel="canonical"[^>]*>', f'<link rel="canonical" href="{c["url"]}">', head)
    head = re.sub(r'<link rel="alternate" hreflang="[^"]*"[^>]*>\n?', '', head)
    head += ('<link rel="alternate" hreflang="th" href="https://solaress.org/th/solar-subsidy-50000">\n'
             '<link rel="alternate" hreflang="en" href="https://solaress.org/solar-subsidy-50000">\n'
             '<link rel="alternate" hreflang="x-default" href="https://solaress.org/solar-subsidy-50000">\n')
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": c['title'].split(' | ')[0], "description": c['desc'],
           "inLanguage": lang, "datePublished": "2026-10-27", "dateModified": UPDATED_ISO, "mainEntityOfPage": c['url'],
           "image": "https://solaress.org/images/news-combiner-mdb-front.jpg",
           "author": {"@type": "Organization", "name": "Solar ESS", "url": "https://solaress.org/"},
           "publisher": {"@type": "Organization", "name": "Solar ESS Co. Ltd.", "url": "https://solaress.org/"}},
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in c['faq']]},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": c['crumb_home'], "item": "https://solaress.org" + c['home']},
              {"@type": "ListItem", "position": 2, "name": c['crumb_news'], "item": "https://solaress.org" + c['news']},
              {"@type": "ListItem", "position": 3, "name": c['title'].split(' | ')[0], "item": c['url']}]}]
    for d in ld:
        head += '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False).replace('</', '<\\/') + '</script>\n'
    head += ('<style>.sp ul{margin:12px 0 0;padding-left:22px;display:grid;gap:8px}.sp h2{font-size:clamp(24px,3.2vw,34px);margin-top:40px}'
             '.sp .kf{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin-top:26px}'
             '.sp .kf div{border:1.5px solid var(--line);background:var(--white);padding:14px 16px}'
             '.sp .kf b{display:block;font-family:var(--display);font-size:28px;color:var(--navy)}.sp .kf span{font-size:14px;color:var(--mute)}'
             '.sp .st{border-left:4px solid var(--hot);background:var(--white);padding:14px 18px;margin-top:22px}'
             '.sp .qa{margin-top:16px}.sp .qa h3{font-size:18px}.sp .qa p{margin-top:4px}'
             '.sp .crumb{font-family:var(--mono);font-size:12px;opacity:.75;margin-bottom:12px}.sp .crumb a{text-decoration:none}</style>\n')
    nav = shell[head_end:body_start]
    out = [head, nav]
    out.append(f'<section class="dark band" style="padding-block:64px"><div class="wrap sp"><p class="crumb"><a href="{c["home"]}">{c["crumb_home"]}</a> › <a href="{c["news"]}">{c["crumb_news"]}</a></p>'
               f'<p class="eyebrow">{c["updated"]}</p><h1 style="font-size:clamp(34px,5.6vw,60px)">{c["h1"]}</h1>'
               f'<p class="lede" style="margin-top:18px">{c["lede"]}</p></div></section>\n')
    body = [f'<section class="band light" style="padding-block:56px"><div class="wrap sp"><article style="max-width:760px">',
            '<div class="kf">' + ''.join(f'<div><b>{a}</b><span>{b}</span></div>' for a, b in c['kf']) + '</div>',
            f'<div class="st"><h2 style="margin-top:0;font-size:22px">{c["status_h"]}</h2><ul>' + ''.join(f'<li>{x}</li>' for x in c['status']) + '</ul></div>']
    for h, items in c['sections']:
        body.append(f'<h2>{h}</h2><ul>' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>')
    body.append(f'<h2>{c["faq_h"]}</h2>' + ''.join(f'<div class="qa"><h3>{e(q)}</h3><p>{e(a)}</p></div>' for q, a in c['faq']))
    body.append(f'<div class="st" style="margin-top:40px"><h2 style="margin-top:0;font-size:24px">{c["cta_h"]}</h2><p style="margin-top:8px">{c["cta"]}</p>'
                f'<p style="margin-top:16px"><a class="btn" href="{c["quote"]}">{c["cta_btn"]}</a> <a class="btn ghost" href="{c["consult"]}" style="margin-left:8px">{c["cta_btn2"]}</a></p></div>')
    body.append(f'<p style="margin-top:28px;font-size:14px;color:var(--mute)">{c["note"]}</p>')
    body.append(f'<h2 style="font-size:20px">{c["src_h"]}</h2><ul style="font-size:14px">' + ''.join(f'<li><a href="{u}" rel="noopener">{e(t)}</a></li>' for t, u in SOURCES) + '</ul>')
    body.append('</article></div></section>\n')
    out += body
    out.append(shell[foot:])
    open(os.path.join(ROOT, c['out']), 'w', encoding='utf-8').write(''.join(out))
    print('wrote', c['out'])

for l in C: build(l)
