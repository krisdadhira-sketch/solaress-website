#!/usr/bin/env python3
"""News topics: News dropdown menu on every page, topic tags + filter bar on the
news pages, and the topic articles. Idempotent. Run: python3 tools/news_topics.py
To tag a new article, add its id to TOPICS below and re-run."""
import glob, html, os, re
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'); os.chdir(ROOT)

LABELS = {
 'en': [('subsidy', '50,000 for Solar Homeowner', '/solar-subsidy-50000.html'), ('datacenter', 'Data Center', None),
        ('innovation', 'Innovation', None), ('adoption', 'Global Adoption of Solar Installation', None),
        ('consumption', 'Global Energy Consumption', None)],
 'th': [('subsidy', 'โซลาร์ 50,000 บาท สำหรับเจ้าของบ้าน', '/th/solar-subsidy-50000.html'), ('datacenter', 'ดาต้าเซ็นเตอร์', None),
        ('innovation', 'นวัตกรรม', None), ('adoption', 'การติดตั้งโซลาร์ทั่วโลก', None),
        ('consumption', 'การใช้พลังงานของโลก', None)],
 'zh': [('subsidy', '5万泰铢家庭光伏补贴', '/solar-subsidy-50000.html'), ('datacenter', '数据中心', None),
        ('innovation', '创新', None), ('adoption', '全球光伏普及', None), ('consumption', '全球能源消费', None)],
}
NEWS = {'en': ('/news.html', 'News'), 'th': ('/th/news.html', 'ข่าวสาร'), 'zh': ('/zh/news.html', '新闻')}
ALL = {'en': 'All news', 'th': 'ข่าวทั้งหมด', 'zh': '全部新闻'}
TOPICS = {
 'subsidy': ['public-reaction-50000-subsidy', 'thailand-50000-baht-solar-subsidy', 'thai-rooftop-solar-policy', 'thailand-mandatory-panel-standard',
             'thailand-ocpb-faulty-solar', 'solar-disadvantages-honest'],
 'datacenter': ['data-centre-impacts-guide', 'data-centres-power-water', 'data-centres-thailand-power', 'global-energy-review-2025'],
 'innovation': ['fraunhofer-silicon-anode-cells', 'tongwei-93-bifaciality', 'risen-anti-glare', 'mova-lumegret-s5000',
                'solis-s6-eh3p50k-v38-vs-21a', 'thailand-solar-battery-recycling-estate'],
 'adoption': ['global-energy-review-2025', 'china-solar-down-rest-up', 'module-prices-october-2026', 'nz-solar-complaints-surge',
              'thai-rooftop-solar-policy'],
 'consumption': ['data-centre-impacts-guide', 'data-centres-power-water', 'global-energy-review-2025', 'data-centres-thailand-power', 'tni-state-of-power-2024', 'ucs-solar-environmental-impacts'],
}
GUIDE = {
 'en': ('Full guide: Thailand\'s 50,000-baht solar subsidy', 'Who qualifies, when to register, what you still pay, loans and sell-back – updated as rules are announced.', '/solar-subsidy-50000.html', 'Read the guide →'),
 'th': ('สรุปฉบับเต็ม: โซลาร์ 50,000 บาท', 'ใครได้สิทธิ์ ลงทะเบียนเมื่อไร ต้องจ่ายเองเท่าไร สินเชื่อ และการขายไฟคืน อัปเดตทุกครั้งที่มีประกาศใหม่', '/th/solar-subsidy-50000.html', 'อ่านสรุป →'),
 'zh': ('完整指南：泰国 5 万泰铢家庭光伏补贴（英文）', '谁有资格、何时登记、自付多少、贷款与余电回购——随新规公布持续更新。', '/solar-subsidy-50000.html', '阅读指南 →'),
}
SEP = 'style="max-width:760px;margin-top:64px;padding-top:48px;border-top:1.5px solid var(--navy)"'

def cmpk(items):
    return '<div class="cmpk">' + ''.join(f'<div><small>{a}</small><b>{b}</b></div>' for a, b in items) + '</div>\n'

def art(aid, eyebrow, h2, lede, kp, paras, src):
    return (f'<article id="{aid}" {SEP}>\n<p class="eyebrow">{eyebrow}</p><h2 style="font-size:clamp(26px,3.6vw,40px)">{h2}</h2>\n'
            f'<p class="lede" style="margin-top:16px;opacity:1">{lede}</p>\n' + cmpk(kp) +
            ''.join(f'<p style="margin-top:{22 if i == 0 else 14}px">{p}</p>\n' for i, p in enumerate(paras)) +
            '<p style="margin-top:28px">' + '<br>'.join(f'<a href="{u}" rel="noopener">{t}</a>' for t, u in src) + '</p>\n</article>\n')

S_DC = [('https://www.thestar.com.my/aseanplus/aseanplus-news/2026/08/22/thailand039s-data-centre-boom-tests-the-grid-the-rules-and-the-workforce', {'en': 'Source: The Nation via The Star, 22 August 2026 (English)', 'th': 'ที่มา: The Nation ผ่าน The Star 22 สิงหาคม 2026 (ภาษาอังกฤษ)', 'zh': '来源：The Nation（经 The Star 转载），2026年8月22日（英文）'}),
        ('https://ourworldindata.org/how-much-energy-do-data-centers-and-artificial-intelligence-use', {'en': 'Source: Our World in Data, using IEA estimates, 20 July 2026 (English)', 'th': 'ที่มา: Our World in Data ใช้ตัวเลขประมาณการของ IEA 20 กรกฎาคม 2026 (ภาษาอังกฤษ)', 'zh': '来源：Our World in Data，采用 IEA 估算，2026年7月20日（英文）'})]
S_GE = [('https://www.iea.org/reports/global-energy-review-2026/key-findings', {'en': 'Source: IEA, Global Energy Review 2026 – key findings (English)', 'th': 'ที่มา: IEA รายงาน Global Energy Review 2026 (ภาษาอังกฤษ)', 'zh': '来源：国际能源署（IEA）《全球能源回顾 2026》主要结论（英文）'})]
src = lambda S, l: [(d[l], u) for u, d in S]

S_FB = [('https://www.facebook.com/sondhitalk/posts/pfbid0CvqEsNWv6xiPDiboohHHZY27s9pfsj5d6u6oatmSnQLqdHHrsjAZmgjsjrn39GH8l', {'en':'Facebook: คุยทุกเรื่องกับสนธิ (about 90 of 374 comments read)','th':'Facebook: คุยทุกเรื่องกับสนธิ (อ่านราว 90 จาก 374 ความคิดเห็น)','zh':'Facebook：คุยทุกเรื่องกับสนธิ（阅读约 90/374 条评论）'}),
        ('https://www.facebook.com/jarm/posts/pfbid02Zvk2SJRPrBiRQTuTWcVo16ARnKm7gzkkiUAvdKdjPaLWYgLyrMCswCkjWL8T5YkDl', {'en':'Facebook: Jarm – จาม (about 38 comments read)','th':'Facebook: Jarm – จาม (อ่านราว 38 ความคิดเห็น)','zh':'Facebook：Jarm – จาม（阅读约 38 条评论）'}),
        ('https://www.facebook.com/thestandardth/posts/pfbid0t56JcRws3qzh2LA2LEVwsnpBLfAuwBqhiPkwfB3SPpMLF5wgQnfUxZWz3zbvmzhTl', {'en':'Facebook: THE STANDARD (about 37 comments read)','th':'Facebook: THE STANDARD (อ่านราว 37 ความคิดเห็น)','zh':'Facebook：THE STANDARD（阅读约 37 条评论）'}),
        ('https://www.facebook.com/thairath/posts/pfbid0313AjX5ZpapoqfSmLjKnxd4QfezdSSA8Vp1cFNdqwt7ZRAqR7UUWy4NvUoM8SSC7Ll', {'en':'Facebook: Thairath (about 12 comments read)','th':'Facebook: ไทยรัฐออนไลน์ (อ่านราว 12 ความคิดเห็น)','zh':'Facebook：Thairath（阅读约 12 条评论）'})]

S_DW = [('https://www.iea.org/reports/energy-and-ai/energy-demand-from-ai', {'en':'Source: IEA, Energy and AI – energy demand from AI (English)','th':'ที่มา: IEA รายงาน Energy and AI (ภาษาอังกฤษ)','zh':'来源：国际能源署（IEA）《能源与人工智能》（英文）'}),
        ('https://www.lincolninst.edu/publications/land-lines-magazine/articles/land-water-impacts-data-centers/', {'en':'Source: Lincoln Institute of Land Policy, 17 October 2025 (English)','th':'ที่มา: Lincoln Institute of Land Policy 17 ตุลาคม 2025 (ภาษาอังกฤษ)','zh':'来源：林肯土地政策研究院，2025年10月17日（英文）'})]

S_DI = [('/data-centre-impacts.html', {'en':'Read the full guide: Data centres – the real costs and benefits','th':'อ่านฉบับเต็ม: ดาต้าเซ็นเตอร์ ต้นทุนที่แท้จริงและประโยชน์ (ภาษาไทย)','zh':'阅读完整指南：数据中心的真实成本与收益（英文）'})]

NEW = {
'en': [
 art('data-centre-impacts-guide', '27 October 2026 · Data centres', 'Data centres: the real environmental and socio-economic costs, and the benefits',
     'Our new guide pulls together the evidence on what data centres mean for electricity, emissions, water, air quality, e-waste, jobs, power bills and tax revenue, and what Thailand is doing about it.',
     [('CO₂ a year today', '≈ 180 Mt'), ('Jobs per large site (US county)', '≈ 100–200'), ('Thai execs naming water top concern', '68.8%')],
     ['<b>Environment.</b> About 415 TWh of electricity in 2024, heading for 945 TWh by 2030; about 30% still from coal; up to 19 million litres of water a day at a large site; diesel backup generators and e-waste from fast chip upgrades.',
      '<b>Economy and society.</b> Huge investment but few permanent jobs; in one US grid, data centres drove most of a ninefold jump in capacity prices that reached household bills; billions in tax breaks; and competition for water with farms and towns.',
      '<b>Thailand.</b> A four-pillar screening framework, power and water mapping, closed-loop cooling for new projects, a 2,000 MW direct renewable-power pilot and proposed rules so large users bear the true cost of imported gas.'],
     [(d['en'], u) for u, d in S_DI]),
 art('data-centres-power-water', '27 October 2026 · Data centres', 'Why data centres use so much electricity and water',
     'Data centres used about <b>415 TWh</b> of electricity in 2024, about 1.5% of the world’s total, and the IEA expects this to more than double to about <b>945 TWh</b> by 2030. AI is the main reason: its chips are far more power-hungry, and they run hot.',
     [('World use, 2024', '415 TWh'), ('Forecast, 2030', '945 TWh'), ('Large site, water per day', 'up to 19 million litres')],
     ['<b>Why so much electricity.</b> AI runs on clusters of specialised chips (GPUs) that draw far more power than ordinary servers. The servers themselves use about 60% of a modern data centre’s electricity, according to the IEA. Cooling uses about 7% in the most efficient large sites and more than 30% in less efficient ones; storage and networking take most of the rest.',
      '<b>Why so much water.</b> Much of the heat is removed by evaporative cooling, where water soaks up heat and evaporates. The Lincoln Institute reports that a large data centre can need up to 5 million US gallons a day (about 19 million litres), similar to a town of 50,000 people. There is also an indirect water cost: about half of the electricity US data centres use comes from fossil-fuel plants, which use water to make steam.',
      '<b>The trade-off.</b> Operators can save water by cooling with more electricity (closed-loop and air systems), or save electricity by using more water. Because AI chips run so hot, many lean on water.',
      '<b>Why it matters in Thailand.</b> Thailand has approved large data centre investments, and in a Federation of Thai Industries survey most executives named water supply as their top concern (see <a href="#data-centres-thailand-power">Thailand’s data centre boom</a>). Solar panels make electricity without burning fuel or boiling water, which is one reason data centres are asking to buy renewable power directly.'],
     src(S_DW, 'en')),
 art('public-reaction-50000-subsidy', '27 October 2026 · Public reaction', 'What people on Facebook are saying about the 50,000-baht solar subsidy',
     'We read about <b>175 public comments</b> under four widely shared Facebook posts about the scheme (25–26 October). Clear worries outnumbered clear support by roughly six to one. Most worries were about money and trust, not about whether solar works.',
     [('Comments read', '≈ 175'), ('Mainly concerns', '≈ 70%'), ('Mainly supportive', '≈ 12%')],
     ['<b>What supporters say.</b> It pays off for homes that use power in the daytime: retirees, home offices, shops and cafés with air-conditioning. One owner of a 5 kW system for three years says it saves about 2,000 baht a month when the bill is above about 5,000 baht. Others welcome help for people who could not afford solar in one go, say energy will only get dearer, and note that more rooftop solar means less imported gas.',
      '<b>What worries people.</b> The biggest theme by far is debt: the 50,000 baht is seen as bait for a much bigger loan. Next come distrust of who supplies the equipment and who profits; the low 2.20-baht buy-back price against the 4-plus baht people pay; fears that installers will raise prices; long payback against inverter and battery life; no help at night without a battery; and safety and quality (fire, roof leaks, poor installers, panels without the Thai standard mark, e-waste). Some think the money should go to fuel prices, flood relief, farmers or the elderly instead, or that only people who already have money will benefit.',
      '<b>Common questions.</b> How many years will power be bought back? Where do the panels come from, and what is the warranty? Can homes that already have solar use the subsidy to expand? Must people use an installer chosen by the government? What does a battery cost on top?',
      '<b>A note on the sample.</b> Two of the four posts were framed critically, so this is not an opinion poll. Comments were read on 27 October 2026, before the official rules were published; we have not recorded any names. Our answers to the five biggest concerns are in the <a href="/solar-subsidy-50000.html">50,000-baht subsidy guide</a>.'],
     src(S_FB, 'en')),
 art('data-centres-thailand-power', '27 October 2026 · Data centres', 'Thailand’s data centre boom: what it means for the grid',
     'Thailand’s Board of Investment approved <b>26 data centre projects</b> worth almost 500 billion baht in 2025, and new applications passed <b>1 trillion baht</b> by the first quarter of 2026. The planned pipeline is about <b>2.87 GW</b>, mostly in the Eastern Economic Corridor.',
     [('Planned pipeline', '2.87 GW'), ('Approved in 2025', '≈ ฿500 bn'), ('World data centres, 2025', '≈ 485 TWh')],
     ['<b>Worldwide.</b> The IEA estimates data centres used about 485 TWh in 2025, roughly 1.5% of the world’s electricity, and expects this to reach about 945 TWh (around 3%) by 2030. Centres built for AI used about a third of it.',
      '<b>In Thailand.</b> Reports say the country has enough generating capacity (a reserve margin above 25%); the bottleneck is transmission. EGAT plans a 31-billion-baht transmission upgrade in the EEC. A pilot letting data centres buy renewable power directly is capped at 2,000 MW, with final rules still pending in mid-2026. Data centres are reported to pay about 5–6 baht per unit, against roughly 3–4 baht for homes. Water is the other worry: in a Federation of Thai Industries survey, 68.8% of executives named water supply as their top concern.',
      '<b>What it means for you:</b> very large new users will compete with everyone else for grid upgrades over the next few years. The reports do not say this will raise household tariffs, so we are not predicting that. What you can control is how much of your daytime power you make yourself, on your own roof.'],
     src(S_DC, 'en')),
 art('global-energy-review-2025', '27 October 2026 · Global energy', 'World energy use in 2025: electricity grew twice as fast, and solar led the growth',
     'The IEA’s Global Energy Review 2026 says world energy demand grew <b>1.3%</b> in 2025, below the average of the past decade, while electricity demand grew by nearly <b>3%</b>. Solar was the largest single source of new supply.',
     [('Energy demand 2025', '+1.3%'), ('Electricity demand', '≈ +3%'), ('New solar generation', '600 TWh')],
     ['<b>Electricity is the fast-growing part.</b> Electricity demand grew more than twice as fast as energy use overall. In the United States, data centres accounted for half of all electricity demand growth; worldwide, data centres and electric vehicles grew quickly from a small base.',
      '<b>Solar led the growth.</b> Solar PV met over a quarter of the increase in total energy demand and added about 600 TWh of generation, about 70% of the growth in electricity generation. The world added a record 800 GW of renewable capacity, 75% of it solar. Low-emission sources covered nearly 60% of demand growth, and CO₂ emissions rose about 0.4%.',
      '<b>What it means for you:</b> the panels on your roof are now the world’s main source of new electricity, not an experiment. For how installations are shifting between countries, see <a href="#china-solar-down-rest-up">Solar installs fall in China, rise everywhere else</a>.'],
     src(S_GE, 'en')),
],
'th': [
 art('data-centre-impacts-guide', '27 ตุลาคม 2026 · ดาต้าเซ็นเตอร์', 'ดาต้าเซ็นเตอร์: ต้นทุนที่แท้จริงต่อสิ่งแวดล้อม เศรษฐกิจและสังคม และประโยชน์',
     'คู่มือฉบับใหม่ของเรารวบรวมหลักฐานว่าดาต้าเซ็นเตอร์ส่งผลอย่างไรต่อไฟฟ้า การปล่อยคาร์บอน น้ำ คุณภาพอากาศ ขยะอิเล็กทรอนิกส์ การจ้างงาน ค่าไฟ และรายได้ภาษี และประเทศไทยกำลังรับมืออย่างไร',
     [('CO₂ ต่อปีในปัจจุบัน', '≈ 180 ล้านตัน'), ('งานต่อศูนย์ขนาดใหญ่ (สหรัฐฯ)', '≈ 100–200'), ('ผู้บริหารไทยที่กังวลเรื่องน้ำที่สุด', '68.8%')],
     ['<b>สิ่งแวดล้อม</b> ใช้ไฟราว 415 TWh ในปี 2024 และกำลังไปสู่ 945 TWh ในปี 2030 ราว 30% ยังมาจากถ่านหิน ศูนย์ขนาดใหญ่ใช้น้ำได้ถึง 19 ล้านลิตรต่อวัน มีเครื่องปั่นไฟดีเซลสำรอง และขยะอิเล็กทรอนิกส์จากการเปลี่ยนชิปเร็ว',
      '<b>เศรษฐกิจและสังคม</b> เงินลงทุนมหาศาลแต่งานประจำน้อย ในระบบไฟฟ้าหนึ่งของสหรัฐฯ ดาต้าเซ็นเตอร์เป็นสาเหตุหลักที่ราคากำลังผลิตพุ่งเกือบเก้าเท่าจนกระทบค่าไฟบ้าน สิทธิประโยชน์ภาษีหลายพันล้าน และการแย่งน้ำกับเกษตรกรและชุมชน',
      '<b>ประเทศไทย</b> กรอบคัดกรอง 4 เสาหลัก แผนที่ไฟฟ้าและน้ำ ระบบหล่อเย็นวงจรปิดสำหรับโครงการใหม่ โครงการนำร่องซื้อไฟพลังงานหมุนเวียนโดยตรง 2,000 MW และข้อเสนอให้ผู้ใช้ไฟรายใหญ่รับต้นทุนจริงของก๊าซนำเข้า'],
     [(d['th'], '/th/data-centre-impacts.html') for u, d in S_DI]),
 art('data-centres-power-water', '27 ตุลาคม 2026 · ดาต้าเซ็นเตอร์', 'ทำไมดาต้าเซ็นเตอร์ใช้ไฟและน้ำมากขนาดนี้',
     'ปี 2024 ดาต้าเซ็นเตอร์ทั่วโลกใช้ไฟราว <b>415 TWh</b> หรือประมาณ 1.5% ของไฟฟ้าทั้งโลก และ IEA คาดว่าจะเพิ่มขึ้นกว่าเท่าตัวเป็นราว <b>945 TWh</b> ภายในปี 2030 สาเหตุหลักคือ AI เพราะชิปใช้ไฟมากกว่าเดิมมากและร้อนจัด',
     [('ใช้ไฟทั่วโลก 2024', '415 TWh'), ('คาดการณ์ 2030', '945 TWh'), ('น้ำของศูนย์ขนาดใหญ่ต่อวัน', 'สูงสุด 19 ล้านลิตร')],
     ['<b>ทำไมใช้ไฟมาก</b> AI ทำงานบนชิปเฉพาะทาง (GPU) จำนวนมากที่กินไฟมากกว่าเซิร์ฟเวอร์ทั่วไปหลายเท่า IEA ระบุว่าตัวเซิร์ฟเวอร์ใช้ไฟราว 60% ของดาต้าเซ็นเตอร์สมัยใหม่ ส่วนระบบระบายความร้อนใช้ราว 7% ในศูนย์ขนาดใหญ่ที่มีประสิทธิภาพสูง และมากกว่า 30% ในศูนย์ที่ประสิทธิภาพต่ำ ที่เหลือส่วนใหญ่เป็นระบบจัดเก็บข้อมูลและเครือข่าย',
      '<b>ทำไมใช้น้ำมาก</b> ความร้อนส่วนใหญ่ถูกระบายด้วยระบบหล่อเย็นแบบระเหย คือให้น้ำดูดความร้อนแล้วระเหยออกไป Lincoln Institute รายงานว่าดาต้าเซ็นเตอร์ขนาดใหญ่อาจใช้น้ำถึง 5 ล้านแกลลอนสหรัฐต่อวัน (ราว 19 ล้านลิตร) ใกล้เคียงเมืองที่มีประชากร 50,000 คน ยังมีการใช้น้ำทางอ้อมด้วย เพราะไฟที่ดาต้าเซ็นเตอร์ในสหรัฐฯ ใช้ราวครึ่งหนึ่งมาจากโรงไฟฟ้าเชื้อเพลิงฟอสซิล ซึ่งต้องใช้น้ำทำไอน้ำ',
      '<b>ต้องเลือกระหว่างน้ำกับไฟ</b> ผู้ประกอบการประหยัดน้ำได้ด้วยการใช้ไฟมากขึ้น (ระบบวงจรปิดหรือระบบลม) หรือประหยัดไฟได้ด้วยการใช้น้ำมากขึ้น เมื่อชิป AI ร้อนจัด หลายแห่งจึงหันไปใช้น้ำ',
      '<b>เกี่ยวกับไทยอย่างไร</b> ไทยอนุมัติการลงทุนดาต้าเซ็นเตอร์มูลค่าสูง และผลสำรวจของสภาอุตสาหกรรมฯ พบว่าผู้บริหารส่วนใหญ่กังวลเรื่องน้ำมากที่สุด (ดู <a href="#data-centres-thailand-power">ดาต้าเซ็นเตอร์บูมในไทย</a>) โซลาร์ผลิตไฟได้โดยไม่ต้องเผาเชื้อเพลิงหรือต้มน้ำ ซึ่งเป็นเหตุผลหนึ่งที่ดาต้าเซ็นเตอร์ขอซื้อไฟพลังงานหมุนเวียนโดยตรง'],
     src(S_DW, 'th')),
 art('public-reaction-50000-subsidy', '27 ตุลาคม 2026 · เสียงประชาชน', 'คนบน Facebook พูดถึงโซลาร์ 50,000 บาทว่าอย่างไร',
     'เราอ่านความคิดเห็นสาธารณะราว <b>175 ความคิดเห็น</b> ใต้โพสต์ Facebook ที่มีคนแชร์มาก 4 โพสต์ (25–26 ตุลาคม) ความกังวลมีมากกว่าความเห็นสนับสนุนราวหกต่อหนึ่ง และส่วนใหญ่เป็นเรื่องเงินและความไว้ใจ ไม่ใช่เรื่องว่าโซลาร์ใช้ได้จริงหรือไม่',
     [('ความคิดเห็นที่อ่าน', '≈ 175'), ('ส่วนใหญ่กังวล', '≈ 70%'), ('ส่วนใหญ่สนับสนุน', '≈ 12%')],
     ['<b>ฝ่ายที่สนับสนุนพูดว่า</b> คุ้มสำหรับบ้านที่ใช้ไฟตอนกลางวัน เช่น ผู้เกษียณ โฮมออฟฟิศ ร้านค้า และร้านกาแฟที่เปิดแอร์ ผู้ที่ติดระบบ 5 kW มา 3 ปีเล่าว่าประหยัดได้ราว 2,000 บาทต่อเดือนเมื่อค่าไฟเกินราว 5,000 บาท บางคนยินดีที่รัฐช่วยคนที่ไม่มีเงินก้อน มองว่าพลังงานจะแพงขึ้นเรื่อย ๆ และถ้าติดกันมากจะลดการนำเข้าก๊าซได้',
      '<b>สิ่งที่คนกังวล</b> อันดับหนึ่งคือหนี้ มองว่าเงิน 50,000 บาทเป็นเหยื่อล่อให้กู้ก้อนใหญ่กว่า รองลงมาคือความไม่ไว้ใจว่าใครเป็นผู้จัดหาอุปกรณ์และใครได้ประโยชน์ ราคารับซื้อ 2.20 บาทต่ำเมื่อเทียบกับค่าไฟที่จ่ายกว่า 4 บาท กลัวผู้ติดตั้งขึ้นราคา ระยะคืนทุนนานเมื่อเทียบอายุอินเวอร์เตอร์และแบตเตอรี่ กลางคืนใช้ไม่ได้ถ้าไม่มีแบตเตอรี่ และเรื่องความปลอดภัยและคุณภาพ (ไฟไหม้ หลังคารั่ว ช่างไม่ได้มาตรฐาน แผงที่ไม่มี มอก. ขยะอิเล็กทรอนิกส์) บางคนเห็นว่าควรนำเงินไปลดราคาน้ำมัน ช่วยน้ำท่วม เกษตรกร หรือผู้สูงอายุแทน หรือกังวลว่าคนที่มีเงินอยู่แล้วเท่านั้นจะได้ประโยชน์',
      '<b>คำถามที่พบบ่อย</b> รัฐจะรับซื้อไฟกี่ปี แผงมาจากไหน รับประกันกี่ปี บ้านที่ติดโซลาร์แล้วใช้สิทธิ์ขยายระบบได้ไหม ต้องใช้ผู้ติดตั้งที่รัฐกำหนดหรือไม่ และแบตเตอรี่ต้องจ่ายเพิ่มเท่าไร',
      '<b>หมายเหตุเรื่องกลุ่มตัวอย่าง</b> โพสต์ 2 ใน 4 นำเสนอในเชิงวิจารณ์ ผลนี้จึงไม่ใช่โพล อ่านความคิดเห็นเมื่อ 27 ตุลาคม 2026 ก่อนมีหลักเกณฑ์ทางการ และไม่ได้บันทึกชื่อผู้แสดงความคิดเห็น คำตอบของเราต่อ 5 ข้อกังวลหลักอยู่ใน <a href="/th/solar-subsidy-50000.html">สรุปโซลาร์ 50,000 บาท</a>'],
     src(S_FB, 'th')),
 art('data-centres-thailand-power', '27 ตุลาคม 2026 · ดาต้าเซ็นเตอร์', 'ดาต้าเซ็นเตอร์บูมในไทย: มีผลกับระบบไฟฟ้าอย่างไร',
     'บีโอไออนุมัติ <b>โครงการดาต้าเซ็นเตอร์ 26 โครงการ</b> มูลค่าเกือบ 5 แสนล้านบาทในปี 2025 และคำขอใหม่เกิน <b>1 ล้านล้านบาท</b> ภายในไตรมาสแรกของปี 2026 โครงการที่วางแผนไว้รวมราว <b>2.87 GW</b> ส่วนใหญ่อยู่ในเขตพัฒนาพิเศษภาคตะวันออก (EEC)',
     [('โครงการที่วางแผน', '2.87 GW'), ('อนุมัติปี 2025', '≈ 5 แสนล้านบาท'), ('ดาต้าเซ็นเตอร์ทั่วโลก 2025', '≈ 485 TWh')],
     ['<b>ทั่วโลก</b> IEA ประเมินว่าดาต้าเซ็นเตอร์ใช้ไฟราว 485 TWh ในปี 2025 หรือประมาณ 1.5% ของไฟฟ้าทั้งโลก และคาดว่าจะเพิ่มเป็นราว 945 TWh (ประมาณ 3%) ภายในปี 2030 โดยศูนย์ที่สร้างเพื่อ AI ใช้ไฟราวหนึ่งในสาม',
      '<b>ในประเทศไทย</b> รายงานระบุว่าไทยมีกำลังผลิตเพียงพอ (กำลังผลิตสำรองเกิน 25%) แต่คอขวดอยู่ที่ระบบสายส่ง กฟผ. วางแผนลงทุนปรับปรุงสายส่งใน EEC 3.1 หมื่นล้านบาท โครงการนำร่องให้ดาต้าเซ็นเตอร์ซื้อไฟพลังงานหมุนเวียนโดยตรงจำกัดไว้ที่ 2,000 MW และหลักเกณฑ์ยังไม่ออก ณ กลางปี 2026 มีรายงานว่าดาต้าเซ็นเตอร์จ่ายค่าไฟราว 5–6 บาทต่อหน่วย เทียบกับบ้านเรือนราว 3–4 บาท อีกเรื่องที่น่ากังวลคือน้ำ ผลสำรวจของสภาอุตสาหกรรมฯ พบว่าผู้บริหาร 68.8% กังวลเรื่องน้ำมากที่สุด',
      '<b>สิ่งนี้มีความหมายกับคุณอย่างไร:</b> ผู้ใช้ไฟรายใหญ่รายใหม่จะใช้งบปรับปรุงระบบไฟฟ้าร่วมกับทุกคนในอีกไม่กี่ปีข้างหน้า รายงานไม่ได้บอกว่าค่าไฟบ้านจะขึ้นเพราะเรื่องนี้ เราจึงไม่คาดการณ์เช่นนั้น สิ่งที่คุณควบคุมได้คือสัดส่วนไฟตอนกลางวันที่คุณผลิตใช้เองบนหลังคาบ้าน'],
     src(S_DC, 'th')),
 art('global-energy-review-2025', '27 ตุลาคม 2026 · พลังงานโลก', 'การใช้พลังงานของโลกปี 2025: ไฟฟ้าโตเร็วกว่าสองเท่า และโซลาร์นำการเติบโต',
     'รายงาน Global Energy Review 2026 ของ IEA ระบุว่าความต้องการพลังงานของโลกเพิ่มขึ้น <b>1.3%</b> ในปี 2025 ต่ำกว่าค่าเฉลี่ยสิบปีที่ผ่านมา ขณะที่ความต้องการไฟฟ้าเพิ่มเกือบ <b>3%</b> และโซลาร์เป็นแหล่งพลังงานใหม่ที่ใหญ่ที่สุด',
     [('ความต้องการพลังงาน 2025', '+1.3%'), ('ความต้องการไฟฟ้า', '≈ +3%'), ('ไฟจากโซลาร์ที่เพิ่มขึ้น', '600 TWh')],
     ['<b>ไฟฟ้าคือส่วนที่โตเร็ว</b> ความต้องการไฟฟ้าโตเร็วกว่าการใช้พลังงานโดยรวมมากกว่าสองเท่า ในสหรัฐฯ ดาต้าเซ็นเตอร์คิดเป็นครึ่งหนึ่งของการเติบโตของความต้องการไฟฟ้า ส่วนทั่วโลก ดาต้าเซ็นเตอร์และรถยนต์ไฟฟ้าโตเร็วจากฐานที่ยังเล็ก',
      '<b>โซลาร์นำการเติบโต</b> โซลาร์ตอบสนองความต้องการพลังงานที่เพิ่มขึ้นได้มากกว่าหนึ่งในสี่ และผลิตไฟเพิ่มราว 600 TWh หรือประมาณ 70% ของการผลิตไฟฟ้าที่เพิ่มขึ้น ทั่วโลกติดตั้งพลังงานหมุนเวียนใหม่เป็นสถิติ 800 GW โดย 75% เป็นโซลาร์ แหล่งพลังงานคาร์บอนต่ำตอบสนองความต้องการที่เพิ่มขึ้นเกือบ 60% และการปล่อย CO₂ เพิ่มราว 0.4%',
      '<b>สิ่งนี้มีความหมายกับคุณอย่างไร:</b> แผงโซลาร์บนหลังคาบ้านคุณคือแหล่งไฟฟ้าใหม่หลักของโลกแล้ว ไม่ใช่เทคโนโลยีทดลอง ดูการเปลี่ยนแปลงการติดตั้งในแต่ละประเทศได้ที่ <a href="#china-solar-down-rest-up">ติดตั้งโซลาร์ในจีนลดลง แต่ทั่วโลกที่เหลือเพิ่มขึ้น</a>'],
     src(S_GE, 'th')),
],
'zh': [
 art('data-centre-impacts-guide', '2026年10月27日 · 数据中心', '数据中心：对环境和社会经济的真实成本与收益',
     '我们的新指南汇总了数据中心对电力、碳排放、水、空气质量、电子垃圾、就业、电费和税收的影响证据，以及泰国的应对措施。',
     [('当前年 CO₂ 排放', '≈ 1.8 亿吨'), ('大型数据中心带来的岗位（美国县）', '≈ 100–200'), ('泰国高管首要担忧为缺水', '68.8%')],
     ['<b>环境。</b>2024 年用电约 415 TWh，2030 年将达 945 TWh；约 30% 仍来自煤电；大型数据中心每天用水最高约 1900 万升；还有柴油备用发电机和芯片快速换代产生的电子垃圾。',
      '<b>经济与社会。</b>投资巨大但长期岗位少；在美国一个电网区域，数据中心是容量电价上涨近九倍的主因，并传导到家庭电费；数十亿美元税收优惠；与农民和城镇争水。',
      '<b>泰国。</b>四大支柱审查框架、电力与水资源联合规划、新项目须采用闭环冷却、2,000 MW 可再生电力直购试点，以及让大用户承担进口天然气真实成本的拟议规则。'],
     [(d['zh'], u) for u, d in S_DI]),
 art('data-centres-power-water', '2026年10月27日 · 数据中心', '数据中心为何如此耗电耗水',
     '2024 年全球数据中心用电约 <b>415 TWh</b>，约占全球电力的 1.5%；IEA 预计到 2030 年将翻倍以上，达到约 <b>945 TWh</b>。主要原因是 AI：其芯片耗电量大得多，而且发热严重。',
     [('2024 年全球用电', '415 TWh'), ('2030 年预测', '945 TWh'), ('大型数据中心日用水', '最高约 1900 万升')],
     ['<b>为何耗电。</b>AI 运行在大量专用芯片（GPU）集群上，耗电远超普通服务器。IEA 指出，服务器本身约占现代数据中心用电的 60%；冷却在最高效的大型数据中心约占 7%，在效率较低的数据中心超过 30%；其余主要是存储和网络设备。',
      '<b>为何耗水。</b>大部分热量通过蒸发冷却带走：水吸收热量后蒸发。林肯土地政策研究院报告称，大型数据中心每天可能需要多达 500 万美制加仑（约 1900 万升）水，相当于 5 万人口城镇的用水量。此外还有间接用水：美国数据中心约一半电力来自化石燃料电厂，而这些电厂需要用水产生蒸汽。',
      '<b>水与电的取舍。</b>运营方可以多用电（闭环或风冷系统）来省水，也可以多用水来省电。由于 AI 芯片发热极高，许多数据中心倾向于用水。',
      '<b>与泰国的关系。</b>泰国已批准大额数据中心投资，泰国工业联合会的调查显示多数高管最担心供水（见<a href="#data-centres-thailand-power">泰国数据中心热潮</a>）。光伏发电无需燃烧燃料或烧水，这也是数据中心要求直接购买可再生电力的原因之一。'],
     src(S_DW, 'zh')),
 art('public-reaction-50000-subsidy', '2026年10月27日 · 公众反应', 'Facebook 网友如何评价 5 万泰铢家庭光伏补贴',
     '我们阅读了 4 篇广泛转发的 Facebook 帖子下约 <b>175 条公开评论</b>（10 月 25–26 日）。明确担忧的评论约为明确支持的六倍，且大多关于钱和信任，而非光伏本身是否有效。',
     [('阅读评论', '≈ 175'), ('以担忧为主', '≈ 70%'), ('以支持为主', '≈ 12%')],
     ['<b>支持者的观点。</b>白天用电多的家庭划算：退休人士、家庭办公、开空调的商店和咖啡馆。一位已安装 5 kW 系统 3 年的用户表示，月电费超过约 5,000 泰铢时每月可省约 2,000 泰铢。也有人欢迎政府帮助无法一次性付款的家庭，认为能源只会越来越贵，屋顶光伏越多，进口天然气就越少。',
      '<b>人们担心什么。</b>最大的担忧是负债：认为 5 万泰铢是诱导人们借更多钱的诱饵。其次是不信任设备由谁供应、谁获利；2.20 泰铢的回购价远低于每度 4 泰铢以上的电价；担心安装商涨价；回本期长于逆变器和电池寿命；没有电池夜间无法使用；以及安全与质量（火灾、屋顶漏水、安装不规范、无泰国标准标志的组件、电子垃圾）。也有人认为这笔钱应用于降低油价、救灾、农民或老人，或担心只有本来有钱的人受益。',
      '<b>常见问题。</b>电力回购多少年？组件来自哪里、保修多久？已装光伏的家庭能否用补贴扩容？是否必须使用政府指定的安装商？电池另需多少钱？',
      '<b>关于样本。</b>4 篇帖子中有 2 篇立场偏批评，因此这不是民意调查。评论于 2026 年 10 月 27 日、官方细则公布前阅读，未记录任何评论者姓名。我们对五大担忧的回答见<a href="/solar-subsidy-50000.html">5 万泰铢补贴指南（英文）</a>。'],
     src(S_FB, 'zh')),
 art('data-centres-thailand-power', '2026年10月27日 · 数据中心', '泰国数据中心热潮：对电网意味着什么',
     '泰国投资促进委员会（BOI）在 2025 年批准了 <b>26 个数据中心项目</b>，总值近 5000 亿泰铢；到 2026 年第一季度，新申请已超过 <b>1 万亿泰铢</b>。规划项目约 <b>2.87 GW</b>，主要位于东部经济走廊（EEC）。',
     [('规划容量', '2.87 GW'), ('2025 年获批', '≈ 5000 亿泰铢'), ('2025 年全球数据中心用电', '≈ 485 TWh')],
     ['<b>全球。</b>IEA 估计，2025 年数据中心用电约 485 TWh，约占全球电力的 1.5%，预计到 2030 年将增至约 945 TWh（约 3%）。其中为 AI 建设的数据中心约占三分之一。',
      '<b>泰国。</b>报道称泰国发电容量充足（备用率超过 25%），瓶颈在输电。泰国电力局（EGAT）计划在 EEC 投资 310 亿泰铢升级输电网。允许数据中心直接购买可再生电力的试点上限为 2,000 MW，截至 2026 年年中细则仍未出台。据报道，数据中心电价约每度 5–6 泰铢，家庭约 3–4 泰铢。另一个担忧是用水：泰国工业联合会的调查中，68.8% 的高管将供水列为首要担忧。',
      '<b>对您意味着什么：</b>未来几年，大型新用户将与所有人共同分享电网升级资源。报道并未说家庭电价会因此上涨，我们也不作此预测。您能掌控的，是白天用电中有多少由自家屋顶自发自用。'],
     src(S_DC, 'zh')),
 art('global-energy-review-2025', '2026年10月27日 · 全球能源', '2025 年全球能源消费：电力增速是总量的两倍，光伏领跑',
     'IEA《全球能源回顾 2026》指出，2025 年全球能源需求增长 <b>1.3%</b>，低于过去十年平均水平；电力需求增长近 <b>3%</b>。光伏是最大的单一新增来源。',
     [('2025 年能源需求', '+1.3%'), ('电力需求', '≈ +3%'), ('光伏新增发电量', '600 TWh')],
     ['<b>电力是增长最快的部分。</b>电力需求增速是能源总需求的两倍多。在美国，数据中心占电力需求增长的一半；在全球，数据中心和电动汽车从较小基数快速增长。',
      '<b>光伏领跑增长。</b>光伏满足了能源总需求增量的四分之一以上，新增发电约 600 TWh，约占发电增量的 70%。全球新增可再生能源装机创纪录达 800 GW，其中 75% 为光伏。低排放能源满足了近 60% 的需求增长，二氧化碳排放上升约 0.4%。',
      '<b>对您意味着什么：</b>您屋顶上的光伏板已是全球新增电力的主要来源，而不是试验性技术。各国装机变化请见<a href="#china-solar-down-rest-up">中国光伏装机下降，其他地区持续增长</a>。'],
     src(S_GE, 'zh')),
],
}

CSS = ('<style id="ntopics-css">.ntopics{display:flex;flex-wrap:wrap;gap:8px;max-width:960px;margin-bottom:8px}'
       '.ntopics a{border:1.5px solid var(--navy);padding:7px 14px;font-size:14px;text-decoration:none;color:var(--navy);background:var(--white)}'
       '.ntopics a[aria-current="true"]{background:var(--navy);color:var(--white)}'
       '.ntcard{display:none;max-width:760px;margin-top:40px;border-left:4px solid var(--hot);background:var(--white);padding:16px 20px}'
       '.ntcard h2{font-size:22px}.ntcard p{margin-top:6px}</style>\n')
JS = ('<script id="ntopics-js">(function(){function ap(){var h=decodeURIComponent(location.hash.slice(1)),t=h.indexOf("topic-")===0?h.slice(6):"";'
      'document.querySelectorAll("#ntopics a").forEach(function(a){a.setAttribute("aria-current",String(a.getAttribute("data-t")===t))});'
      'document.querySelectorAll("article[id],.ntcard").forEach(function(e){var ts=(e.getAttribute("data-topics")||"").split(" ");'
      'var show=e.classList.contains("ntcard")?t==="subsidy":(!t||ts.indexOf(t)>=0);e.style.display=show?(e.classList.contains("ntcard")?"block":""):"none"});'
      'if(t){var b=document.getElementById("ntopics");if(b)scrollTo(0,b.getBoundingClientRect().top+scrollY-96)}}addEventListener("hashchange",ap);ap()})();</script>\n')

POLL = {
 'en': ('Do you agree with the 50,000-baht household solar subsidy?', [('agree','Agree'),('disagree','Disagree'),('undecided','Undecided')], 'Vote', 'Thank you for voting. You can change your vote.', '{n} votes so far', 'One vote per device/network. Results show after you vote.', 'The poll is not available right now. Please try again later.'),
 'th': ('คุณเห็นด้วยกับโครงการโซลาร์ 50,000 บาทหรือไม่?', [('agree','เห็นด้วย'),('disagree','ไม่เห็นด้วย'),('undecided','ยังไม่ตัดสินใจ')], 'โหวต', 'ขอบคุณที่ร่วมโหวต เปลี่ยนคำตอบได้', 'โหวตแล้ว {n} คน', 'โหวตได้ 1 ครั้งต่ออุปกรณ์/เครือข่าย ผลโหวตจะแสดงหลังคุณโหวต', 'ระบบโหวตไม่พร้อมใช้งานขณะนี้ กรุณาลองใหม่ภายหลัง'),
 'zh': ('您是否赞同 5 万泰铢家庭光伏补贴计划？', [('agree','赞同'),('disagree','不赞同'),('undecided','未决定')], '投票', '感谢投票，您可以更改选择。', '已有 {n} 票', '每个设备/网络限投一票，投票后显示结果。', '投票暂时不可用，请稍后再试。'),
}
POLL_CSS = ('<style id="poll-css">.poll{margin-top:32px;border:1.5px solid var(--navy);background:var(--white);padding:20px 22px}'
            '.poll h3{font-size:20px}.poll .opts{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px}'
            '.poll .opts button{font:inherit;cursor:pointer;border:1.5px solid var(--navy);background:var(--white);color:var(--navy);padding:9px 18px}'
            '.poll .opts button[aria-pressed="true"]{background:var(--navy);color:var(--white)}'
            '.poll .res{margin-top:16px;display:grid;gap:8px}.poll .res[hidden]{display:none}.poll .row{display:grid;grid-template-columns:120px 1fr 56px;gap:10px;align-items:center;font-size:15px}'
            '.poll .bar{height:14px;background:rgba(0,0,0,.08)}.poll .bar i{display:block;height:100%;background:var(--hot)}'
            '.poll small{display:block;margin-top:12px;color:var(--mute)}</style>\n')
POLL_JS = (r"""<script id="poll-js">(function(){document.querySelectorAll('.poll[data-poll]').forEach(function(el){var id=el.getAttribute('data-poll'),msg=el.querySelector('.msg'),res=el.querySelector('.res');
function show(d){var t=d.total||0;el.querySelectorAll('.row').forEach(function(r){var k=r.getAttribute('data-k'),n=(d.counts||{})[k]||0,p=t?Math.round(100*n/t):0;r.querySelector('i').style.width=p+'%';r.querySelector('b').textContent=p+'%'});
el.querySelector('.tot').textContent=el.getAttribute('data-tot').replace('{n}',t);el.querySelectorAll('.opts button').forEach(function(b){b.setAttribute('aria-pressed',String(b.value===d.mine))});
if(d.mine){res.hidden=false;msg.textContent=el.getAttribute('data-thanks')}}
function fail(){msg.textContent=el.getAttribute('data-fail')}
fetch('/api/poll?id='+id,{cache:'no-store'}).then(function(r){if(!r.ok)throw 0;return r.json()}).then(show).catch(function(){});
el.querySelectorAll('.opts button').forEach(function(b){b.addEventListener('click',function(){fetch('/api/poll?id='+id,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({choice:b.value})}).then(function(r){if(!r.ok)throw 0;return r.json()}).then(show).catch(fail)})})})})();</script>
""")

def poll_html(lang, pid):
    q, opts, vote, thanks, tot, note, fail = POLL[lang]
    return (f'<div class="poll" data-poll="{pid}" data-thanks="{html.escape(thanks)}" data-tot="{html.escape(tot)}" data-fail="{html.escape(fail)}">'
            f'<h3>{q}</h3><div class="opts" role="group" aria-label="{html.escape(q)}">' +
            ''.join(f'<button type="button" value="{k}" aria-pressed="false">{lab}</button>' for k, lab in opts) +
            '</div><div class="res" hidden>' +
            ''.join(f'<div class="row" data-k="{k}"><span>{lab}</span><div class="bar"><i style="width:0"></i></div><b>0%</b></div>' for k, lab in opts) +
            f'<p class="tot" style="font-size:14px"></p></div><p class="msg" aria-live="polite" style="margin-top:10px;font-size:15px"></p><small>{note}</small></div>\n')

def nav_dd(lang):
    url, name = NEWS[lang]
    items = ''.join(f'<a href="{u or url + "#topic-" + k}">{lab}</a>' for k, lab, u in LABELS[lang])
    return f'<span class="dd"><a href="{url}">{name}</a><span class="ddm">{items}</span></span>'

# 1. nav on every page
n = 0
for f in glob.glob('*.html') + glob.glob('th/*.html') + glob.glob('zh/*.html'):
    s = open(f, encoding='utf-8').read(); o = s
    for lang, (url, name) in NEWS.items():
        plain = f'<nav><a href="{url}">{name}</a>'
        if plain in s:
            s = s.replace(plain, '<nav>' + nav_dd(lang))
        else:  # refresh existing dropdown
            s = re.sub(r'<nav><span class="dd"><a href="' + re.escape(url) + r'">[^<]*</a><span class="ddm">.*?</span></span>',
                       lambda m: '<nav>' + nav_dd(lang), s, count=1)
    if s != o:
        open(f, 'w', encoding='utf-8').write(s); n += 1
print('nav updated in', n, 'files')

# 2. news pages
for lang, f in (('en', 'news.html'), ('th', 'th/news.html'), ('zh', 'zh/news.html')):
    s = open(f, encoding='utf-8').read()
    first = s.find('<article id=')
    for a in reversed(NEW[lang]):
        aid = re.search(r'id="([^"]+)"', a).group(1)
        if f'<article id="{aid}"' not in s:
            first = s.find('<article id=')
            # previous first article gets the separator style
            m = re.compile(r'<article id="([^"]+)"((?: data-topics="[^"]*")?) style="max-width:760px">').match(s, first)
            if m:
                s = s[:first] + f'<article id="{m.group(1)}"{m.group(2)} {SEP}>' + s[m.end():]
            s = s[:first] + a.replace(f' {SEP}>', ' style="max-width:760px">', 1) + s[first:]
    # tags
    for aid in set(re.findall(r'<article id="([^"]+)"', s)):
        ts = [k for k, ids in TOPICS.items() if aid in ids]
        s = re.sub(r'(<article id="' + re.escape(aid) + r'")(?: data-topics="[^"]*")?', lambda m: m.group(1) + (f' data-topics="{" ".join(ts)}"' if ts else ''), s, count=1)
    # filter bar + guide card
    s = re.sub(r'<nav class="ntopics".*?</nav>\n<div class="ntcard".*?</div>\n', '', s, flags=re.S)
    url = NEWS[lang][0]
    bar = (f'<nav class="ntopics" id="ntopics" aria-label="Topics"><a href="{url}#all" data-t="">{ALL[lang]}</a>' +
           ''.join(f'<a href="{url}#topic-{k}" data-t="{k}">{lab}</a>' for k, lab, u in LABELS[lang]) + '</nav>\n')
    g = GUIDE[lang]
    card = f'<div class="ntcard" data-topics="subsidy"><h2>{g[0]}</h2><p>{g[1]}</p><p><a class="btn" href="{g[2]}">{g[3]}</a></p></div>\n'
    first = s.find('<article id=')
    s = s[:first] + bar + card + s[first:]
    if 'id="ntopics-css"' not in s:
        s = s.replace('</head>', CSS + '</head>', 1)
    s = re.sub(r'<script id="ntopics-js">.*?</script>\n', '', s, flags=re.S)
    i = s.rfind('</body>'); s = s[:i] + JS + s[i:]
    # poll after the public-reaction article
    s = re.sub(r'<div class="poll" data-poll="subsidy-50000".*?</small></div>\n', '', s, flags=re.S)
    m = re.search(r'<article id="public-reaction-50000-subsidy".*?(</article>)', s, re.S)
    if m:
        s = s[:m.start(1)] + poll_html(lang, 'subsidy-50000') + s[m.start(1):]
    if 'id="poll-css"' not in s:
        s = s.replace('</head>', POLL_CSS + '</head>', 1)
    s = re.sub(r'<script id="poll-js">.*?</script>\n', '', s, flags=re.S)
    i = s.rfind('</body>'); s = s[:i] + POLL_JS + s[i:]
    open(f, 'w', encoding='utf-8').write(s)
    print(f, 'articles', s.count('<article id='), 'tagged', s.count('data-topics=') - 1)
