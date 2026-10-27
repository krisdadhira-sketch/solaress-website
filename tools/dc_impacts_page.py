#!/usr/bin/env python3
"""Build /data-centre-impacts.html and /th/data-centre-impacts.html (long-form explainer)
from the news page shell. Edit C below and run: python3 tools/dc_impacts_page.py"""
import html, json, os, re
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'); os.chdir(ROOT)
UPDATED_ISO = '2026-10-27'

SRC = [
 ('DataReportal – Digital 2026: Thailand (8 Nov 2025)', 'https://datareportal.com/reports/digital-2026-thailand'),
 ('Telecom Lead – Ericsson Mobility Report, June 2026 edition', 'https://telecomlead.com/5g/ericsson-mobility-report-2026-global-mobile-data-traffic-to-reach-515-eb-by-2031-as-india-leads-smartphone-data-consumption-126290'),
 ('Profile Books – Hyperscale by Paris Marx', 'https://profilebooks.com/work/hyperscale/'),
 ('Wikipedia – Empire of AI (publication details and water-figure correction)', 'https://en.wikipedia.org/wiki/Empire_of_AI'),
 ('Kate Crawford – Atlas of AI', 'https://katecrawford.net/atlas'),
 ('LBNL / Science (Masanet et al., 28 Feb 2020) – Data centers successful in energy efficiency measures', 'https://energyanalysis.lbl.gov/news/data-centers-successful-energy'),
 ('LowCarbonPower – Thailand electricity per person, 2025', 'https://www.lowcarbonpower.org/region/Thailand'),
 ('Pattaya Mail – Bangkok uses roughly 4–5 million m³ of water a day (21 Jul 2015)', 'https://www.pattayamail.com/thailandnews/dwr-urges-thais-to-reduce-daily-water-consumption-by-1l-49211'),
 ('IEA – Energy and AI: energy demand from AI', 'https://www.iea.org/reports/energy-and-ai/energy-demand-from-ai'),
 ('Bangkok Post – AI surge to double data centre power demand by 2030 (IEA: 180 Mt CO₂ today, ~300 Mt by 2035; coal ~30%)', 'https://bangkokpost.com/business/general/3000142/ai-surge-to-double-data-centre-power-demand-by-2030'),
 ('Lincoln Institute of Land Policy – Land and water impacts of data centers (17 Oct 2025)', 'https://www.lincolninst.edu/publications/land-lines-magazine/articles/land-water-impacts-data-centers/'),
 ('eWeek – Caltech / UC Riverside study “The Unpaid Toll” on AI air pollution (16 Jan 2025)', 'https://www.eweek.com/news/ai-boom-environmental-impact/'),
 ('IEEE Spectrum – Nature Computational Science study on generative-AI e-waste', 'https://spectrum.ieee.org/e-waste'),
 ('Brookings – New evidence on data center employment effects (May 2026, updated Aug 2026)', 'https://www.brookings.edu/articles/new-evidence-on-data-center-employment-effects/'),
 ('IEEFA – Projected data center growth spurs PJM capacity prices by factor of 10 (30 Jul 2025)', 'https://ieefa.org/resources/projected-data-center-growth-spurs-pjm-capacity-prices-factor-10'),
 ('Fortune – Data centers: millions in investment, billions in tax revenue lost (2 Sep 2026)', 'https://fortune.com/2026/09/02/data-center-millions-investment-billions-tax-revenue-loss/'),
 ('The Nation / Asia News Network – The true price of the cloud: Thailand’s battle for water and power (3 Sep 2026)', 'https://asianews.network/the-true-price-of-the-cloud-inside-thailands-battle-for-water-and-power/'),
 ('The Nation via The Star – Thailand’s data centre boom tests the grid, the rules and the workforce (22 Aug 2026)', 'https://www.thestar.com.my/aseanplus/aseanplus-news/2026/08/22/thailand039s-data-centre-boom-tests-the-grid-the-rules-and-the-workforce'),
]

C = {
'en': dict(
 out='data-centre-impacts.html', url='https://solaress.org/data-centre-impacts', news='/news.html', home='/',
 title='Data Centres: Environmental and Socio-economic Impacts, and What They Mean for Thailand | Solar ESS',
 desc='A plain-language guide to the environmental and socio-economic impacts of data centres: electricity, emissions, water, air pollution, e-waste, jobs, power bills and tax breaks, with what Thailand is doing about them.',
 crumb_home='Home', crumb_news='News', updated='Updated 27 October 2026',
 h1='Data centres:<br>the real costs<br>and benefits',
 lede='Every photo, message and AI answer runs through a data centre. As AI grows, these buildings are becoming some of the biggest users of electricity and water anywhere. This guide sets out what the evidence says about their environmental and socio-economic impacts, and what Thailand is doing about them.',
 kf=[('415 TWh', 'world data-centre electricity, 2024 (≈1.5%)'), ('945 TWh', 'IEA forecast for 2030'), ('≈180 Mt', 'CO₂ a year today'), ('19 m litres', 'water a day, large site (max)')],
 toc='On this page',
 sections=[
  ('cmp', 'Before and after: how big is this?', [
   ('Electricity: the decade before AI', [
    'For most of the 2010s, data centres grew without using much more power. A study in <i>Science</i> found they used about 205 TWh in 2018, only about 6% more than in 2010, even though computing work grew about 550%, because each server became far more efficient. That was about 1% of the world’s electricity.',
    'AI changed this. Use roughly doubled to about 415 TWh by 2024 (1.5%), and the IEA expects about 945 TWh by 2030 (just under 3%).']),
   ('Compared with things we know', [
    'RAW:<div class="tw"><table><tr><th>Item</th><th>Electricity a year</th><th>Compared with Thailand</th></tr>'
    '<tr><td>All of Thailand (2025)</td><td>≈ 205 TWh*</td><td>1×</td></tr>'
    '<tr><td>World data centres, 2018 (before AI)</td><td>≈ 205 TWh</td><td>≈ 1×</td></tr>'
    '<tr><td>World data centres, 2024</td><td>≈ 415 TWh</td><td>≈ 2×</td></tr>'
    '<tr><td>World data centres, 2030 (IEA forecast)</td><td>≈ 945 TWh</td><td>≈ 4.5×</td></tr>'
    '<tr><td>Thailand’s planned data centres, 2.87 GW</td><td>≈ 20 TWh**</td><td>≈ 10% of today’s use</td></tr>'
    '<tr><td>One 100 MW data centre</td><td>≈ 0.7 TWh**</td><td>as much as ≈ 220,000 Thais use in total</td></tr></table></div>',
    '<small>* Our calculation: 3,134 kWh per person in 2025 (LowCarbonPower) × about 66 million people. ** Our estimate, assuming the sites run at 80% of capacity all year; real use depends on how full they are.</small>']),
   ('Water', [
    'A large data centre can use up to about 19 million litres a day, similar to a town of 50,000 people. Bangkok uses roughly 4–5 billion litres a day, so one such site would equal about 0.4–0.5% of the whole city’s supply, drawn from one location, every day, much of it evaporated rather than returned.',
    'Before AI, most data centres were smaller, often 10–50 MW, and many used air cooling. AI chips run far hotter and are packed more densely, which is why water-based cooling has become common again.']),
  ]),
  ('env', 'Environmental impacts', [
   ('Electricity and emissions', [
    'The IEA estimates data centres used about 415 TWh in 2024, about 1.5% of the world’s electricity, growing about 12% a year over the past five years. In its base case this reaches about 945 TWh by 2030, just under 3% of world demand. AI is the main driver: its specialised chips draw far more power than ordinary servers.',
    'Inside a modern data centre the servers take about 60% of the electricity; cooling takes about 7% in the most efficient large sites and more than 30% in older or less efficient ones; storage and networking take most of the rest.',
    'About 30% of data-centre electricity still comes from coal. The IEA puts their emissions at about 180 million tonnes of CO₂ today, rising to about 300 million tonnes by 2035. That is still under 1% of world emissions (41.6 billion tonnes in 2024), but very fast demand growth can keep older fossil plants running longer and use up clean power that would otherwise replace them.']),
   ('Water', [
    'Much of the heat is removed by evaporative cooling: water absorbs heat and evaporates, so it does not come back. The Lincoln Institute reports that a large data centre can need up to 5 million US gallons a day (about 19 million litres), roughly what a town of 50,000 people uses.',
    'There is also hidden water use. About half of the electricity used by US data centres comes from fossil-fuel plants, which boil water to drive their turbines. Operators face a trade-off: closed-loop or air cooling saves water but uses more electricity; evaporative cooling saves electricity but uses more water.']),
   ('Air pollution and health', [
    'Data centres keep large banks of diesel generators for power cuts and test them regularly. A study by researchers at Caltech and UC Riverside estimates that, in the United States, air pollution linked to AI data centres and the power plants that feed them could cause about 1,300 premature deaths and up to US$20 billion in health costs a year by 2030. Diesel backup generators emit 200–600 times more nitrogen dioxide than gas power plants per unit of power; in Northern Virginia alone their pollution is estimated to cost US$190–260 million a year in public health.']),
   ('Electronic waste', [
    'AI hardware is replaced quickly as new chips arrive. A study in Nature Computational Science estimates large language models alone could produce 1.2–5 million tonnes of e-waste between 2023 and 2030, and up to about 2.5 million tonnes a year by 2030 in the aggressive scenario, against about 62 million tonnes of all e-waste worldwide in 2022. Chips, boards and batteries contain valuable and hazardous materials, so recycling matters.']),
   ('Land, noise and heat', [
    'Large campuses take up a lot of land. Cooling towers run day and night, testing night-time noise limits of 50–55 dB(A) near homes, and waste heat adds to the urban heat-island effect, as reported for sites near Bangkok.']),
  ]),
  ('soc', 'Socio-economic impacts', [
   ('Investment and growth', [
    'Data centres bring very large investments. Thailand’s Board of Investment approved 26 data-centre projects worth almost 500 billion baht in 2025, and applications passed 1 trillion baht by early 2026; reports also list 36 projects worth 728 billion baht before the BOI paused new data-centre promotion applications in April 2026, with 42 data centres already operating. Hyperscale sites also bring better telecoms and cloud services, and keep data closer to users.']),
   ('Jobs', [
    'They create far fewer permanent jobs than their size suggests. A Brookings study of about 1,500 US facilities found roughly 100–200 extra jobs in a county that gets a large data centre, with data-processing employment up about 56% over a decade but no change in local wages, and home prices up 2–5%. In Thailand, TDRI estimates a 100 MW data centre creates about 50 direct jobs. Construction brings a temporary boost.']),
   ('Electricity bills', [
    'Where many data centres arrive at once, everyone can pay for the extra power plants and lines. In the PJM grid in the eastern United States, the capacity price jumped from US$28.92 to US$269.92 per MW-day for 2025/26; the market monitor attributed 63% of the increase, about US$9.3 billion, to data centres. Residential bills rose by about US$16–21 a month in some areas. A Georgia Tech study found local electricity prices about 5% higher where data centres open.',
    'In Thailand, data centres are reported to pay about 5–6 baht per unit against roughly 3–4 baht for homes, and a new “Category 9” user class has been proposed so that large data centres running on fossil-fuel power bear the true cost of imported LNG. How grid upgrades are paid for will decide whether households share the cost.']),
   ('Tax breaks', [
    'Governments compete with incentives. In the US, 36 of 50 states offer data-centre tax breaks; states have given up billions in revenue, and at least 14 do not disclose how much. Some require jobs in return, such as Virginia’s minimum of 50 jobs paying above 150% of the local average wage.']),
   ('Water competition and local communities', [
    'Farming and fishing communities in Chonburi and Rayong fear for their water. In a Federation of Thai Industries survey of 160 executives, 68.8% named insufficient water supply as their top concern. Investigators have also found “phantom demand”: overlapping water-reservation contracts that make shortages look worse on paper.']),
  ]),
  ('info', 'How we consume information', [
   ('', [
    'Every scroll, video and AI answer is served from a data centre. In Thailand, 67.8 million people (94.7%) were online in late 2025, with 56.6 million social-media identities; LINE has about 56 million monthly users, and TikTok, Facebook and YouTube each reach about 47–57 million.',
    'Video dominates. Ericsson reports that video is about 75% of all mobile data. The average smartphone used about 22 GB a month at the end of 2025 (about 23 GB in South-East Asia and Oceania), heading for about 42 GB worldwide and 50 GB in our region by 2031. World mobile traffic is about 210 exabytes a month.',
    'AI adds a new layer on top: instead of fetching a stored page, a chatbot or image tool computes a fresh answer each time, which takes far more energy per request than an ordinary search or message.',
    'Small habits help: download over Wi-Fi rather than streaming the same video again, choose a lower resolution on small screens, turn off autoplay, and clear out cloud storage you no longer need.']),
  ]),
  ('th', 'What Thailand is doing', [
   ('Rules being prepared', [
    'A four-pillar screening framework (energy security, water limits, environmental impact and domestic benefit) is being finalised by the BOI, the Office of National Water Resources and the NESDC.',
    'Joint power and water mapping would limit new data centres to areas with proven surplus and keep new water-cooled sites out of vulnerable river basins; new projects must use closed-loop or liquid cooling.',
    'A direct power-purchase pilot capped at 2,000 MW would let data centres buy renewable electricity directly; EGAT plans a 31-billion-baht transmission upgrade in the EEC.',
    'The NESDC has proposed mandatory reporting of resource use, local-content rules, workforce training and a formal public-participation process.']),
  ]),
  ('you', 'What it means for homes and businesses', [
   ('', [
    'Data centres are part of a modern economy, and the question in Thailand is no longer whether to have them but on what terms. For households and businesses, three things are worth watching: whether grid-upgrade costs are passed on to ordinary users, whether water allocation protects farms and towns, and how quickly clean power is added.',
    'Solar panels make electricity without burning fuel or using cooling water. Making some of your own daytime power on your roof is one way to be less exposed to whatever happens to grid prices, and every unit made on a roof is a unit the grid does not have to supply. Read our guide to <a href="/solar-subsidy-50000.html">Thailand’s 50,000-baht solar subsidy</a>.']),
  ]),
  ('books', 'Further reading: books on AI, data centres and their impacts', [
   ('', [
    'RAW:<ol class="books">' + '<li><b><i>Atlas of AI</i></b> – Kate Crawford (Yale University Press, 2021). AI as an industry that extracts minerals, energy, labour and data – the classic starting point.</li><li><b><i>Empire of AI</i></b> – Karen Hao (Penguin Press, May 2025). The rise of OpenAI, the data workers behind it and the resources it uses. The author corrected an overstated Chilean data-centre water figure in November 2025.</li><li><b><i>Hyperscale: Ambition, Power and the Relentless Rise of Data Empires</i></b> – Paris Marx (Profile Books, 20 October 2026). The physical footprint of data centres and who bears the cost; longlisted for the FT Business Book of the Year 2026.</li><li><b><i>A Prehistory of the Cloud</i></b> – Tung-Hui Hu (MIT Press, 2015). The cables, buildings and history hidden behind the word “cloud”.</li><li><b><i>Cloud Empires</i></b> – Vili Lehdonvirta (MIT Press, 2022). How digital platforms came to act like governments.</li><li><b><i>Power and Progress</i></b> – Daron Acemoglu & Simon Johnson (PublicAffairs, 2023). Who gains from new technology, from the Middle Ages to AI.</li><li><b><i>Code Dependent</i></b> – Madhumita Murgia (Henry Holt / Picador, 2024). How AI already affects workers and ordinary people around the world.</li><li><b><i>AI Snake Oil</i></b> – Arvind Narayanan & Sayash Kapoor (Princeton University Press, 2024). How to tell what AI can and cannot really do.</li><li><b><i>The Coming Wave</i></b> – Mustafa Suleyman with Michael Bhaskar (Crown, 2023). An industry insider on the risks and governance of AI.</li><li><b><i>The Datacenter as a Computer (3rd ed.)</i></b> – Luiz André Barroso, Urs Hölzle & Parthasarathy Ranganathan (Morgan & Claypool, 2018). The technical design of large data centres and why efficiency matters.</li><li><b><i>The Shallows</i></b> – Nicholas Carr (W. W. Norton, 2010). What constant online reading does to attention and memory.</li><li><b><i>Stolen Focus</i></b> – Johann Hari (Crown / Bloomsbury, 2022). Why attention is shrinking in the age of endless feeds.</li>' + '</ol>',
   ]),
  ]),
 ],
 src_h='Sources', note='Solar ESS is always happy to share up-to-date information and our first-hand experience. Figures are from the sources listed; where sources differ we give both. This page is updated as new evidence appears.',
 back='All data-centre news', backurl='/news.html#topic-datacenter'),
'th': dict(
 out='th/data-centre-impacts.html', url='https://solaress.org/th/data-centre-impacts', news='/th/news.html', home='/th/',
 title='ดาต้าเซ็นเตอร์: ผลกระทบต่อสิ่งแวดล้อม เศรษฐกิจและสังคม และความหมายต่อประเทศไทย | Solar ESS',
 desc='สรุปผลกระทบของดาต้าเซ็นเตอร์ต่อสิ่งแวดล้อม เศรษฐกิจและสังคม แบบอ่านง่าย ทั้งไฟฟ้า การปล่อยคาร์บอน น้ำ มลพิษอากาศ ขยะอิเล็กทรอนิกส์ การจ้างงาน ค่าไฟ และสิทธิประโยชน์ทางภาษี พร้อมมาตรการของประเทศไทย',
 crumb_home='หน้าแรก', crumb_news='ข่าวสาร', updated='อัปเดต 27 ตุลาคม 2569',
 h1='ดาต้าเซ็นเตอร์:<br>ต้นทุนที่แท้จริง<br>และประโยชน์',
 lede='ทุกภาพ ทุกข้อความ และทุกคำตอบจาก AI ล้วนวิ่งผ่านดาต้าเซ็นเตอร์ เมื่อ AI เติบโต อาคารเหล่านี้กำลังกลายเป็นผู้ใช้ไฟและน้ำรายใหญ่ที่สุดแห่งหนึ่ง หน้านี้สรุปว่าหลักฐานบอกอะไรเกี่ยวกับผลกระทบต่อสิ่งแวดล้อม เศรษฐกิจและสังคม และประเทศไทยกำลังรับมืออย่างไร',
 kf=[('415 TWh', 'ไฟที่ดาต้าเซ็นเตอร์ทั่วโลกใช้ ปี 2024 (≈1.5%)'), ('945 TWh', 'คาดการณ์ของ IEA ปี 2030'), ('≈180 ล้านตัน', 'CO₂ ต่อปี ในปัจจุบัน'), ('19 ล้านลิตร', 'น้ำต่อวัน ศูนย์ขนาดใหญ่ (สูงสุด)')],
 toc='ในหน้านี้',
 sections=[
  ('cmp', 'ก่อนและหลัง: ใหญ่แค่ไหน?', [
   ('ไฟฟ้า: ทศวรรษก่อนยุค AI', [
    'ตลอดช่วงปี 2010 ดาต้าเซ็นเตอร์เติบโตโดยแทบไม่ใช้ไฟเพิ่ม งานวิจัยในวารสาร <i>Science</i> พบว่าใช้ไฟราว 205 TWh ในปี 2018 เพิ่มจากปี 2010 เพียงราว 6% ทั้งที่งานประมวลผลเพิ่มราว 550% เพราะเซิร์ฟเวอร์แต่ละเครื่องประหยัดไฟขึ้นมาก ขณะนั้นคิดเป็นราว 1% ของไฟฟ้าโลก',
    'AI เปลี่ยนภาพนี้ การใช้ไฟเพิ่มเกือบเท่าตัวเป็นราว 415 TWh ในปี 2024 (1.5%) และ IEA คาดว่าจะถึงราว 945 TWh ในปี 2030 (เกือบ 3%)']),
   ('เทียบกับสิ่งที่เรารู้จัก', [
    'RAW:<div class="tw"><table><tr><th>รายการ</th><th>ไฟฟ้าต่อปี</th><th>เทียบกับประเทศไทย</th></tr>'
    '<tr><td>ทั้งประเทศไทย (2025)</td><td>≈ 205 TWh*</td><td>1 เท่า</td></tr>'
    '<tr><td>ดาต้าเซ็นเตอร์ทั่วโลก ปี 2018 (ก่อนยุค AI)</td><td>≈ 205 TWh</td><td>≈ 1 เท่า</td></tr>'
    '<tr><td>ดาต้าเซ็นเตอร์ทั่วโลก ปี 2024</td><td>≈ 415 TWh</td><td>≈ 2 เท่า</td></tr>'
    '<tr><td>ดาต้าเซ็นเตอร์ทั่วโลก ปี 2030 (คาดการณ์ของ IEA)</td><td>≈ 945 TWh</td><td>≈ 4.5 เท่า</td></tr>'
    '<tr><td>ดาต้าเซ็นเตอร์ที่วางแผนในไทย 2.87 GW</td><td>≈ 20 TWh**</td><td>≈ 10% ของการใช้ไฟปัจจุบัน</td></tr>'
    '<tr><td>ดาต้าเซ็นเตอร์ 100 MW หนึ่งแห่ง</td><td>≈ 0.7 TWh**</td><td>เท่ากับการใช้ไฟทั้งหมดของคนไทย ≈ 220,000 คน</td></tr></table></div>',
    '<small>* คำนวณโดยเรา: 3,134 kWh ต่อคนในปี 2025 (LowCarbonPower) × ประชากรราว 66 ล้านคน ** ประมาณการของเรา โดยสมมติว่าเดินเครื่อง 80% ของกำลังตลอดปี การใช้จริงขึ้นกับอัตราการใช้งาน</small>']),
   ('น้ำ', [
    'ดาต้าเซ็นเตอร์ขนาดใหญ่อาจใช้น้ำถึงราว 19 ล้านลิตรต่อวัน ใกล้เคียงเมืองที่มีประชากร 50,000 คน กรุงเทพฯ ใช้น้ำราว 4,000–5,000 ล้านลิตรต่อวัน ศูนย์หนึ่งแห่งจึงเท่ากับราว 0.4–0.5% ของน้ำทั้งเมือง ดึงจากจุดเดียวทุกวัน และส่วนใหญ่ระเหยไปไม่กลับคืน',
    'ก่อนยุค AI ดาต้าเซ็นเตอร์ส่วนใหญ่เล็กกว่า มักอยู่ที่ 10–50 MW และหลายแห่งระบายความร้อนด้วยอากาศ ชิป AI ร้อนกว่ามากและติดตั้งหนาแน่นกว่า การระบายความร้อนด้วยน้ำจึงกลับมาใช้แพร่หลาย']),
  ]),
  ('env', 'ผลกระทบต่อสิ่งแวดล้อม', [
   ('ไฟฟ้าและการปล่อยคาร์บอน', [
    'IEA ประเมินว่าดาต้าเซ็นเตอร์ใช้ไฟราว 415 TWh ในปี 2024 หรือประมาณ 1.5% ของไฟฟ้าทั้งโลก เพิ่มขึ้นราว 12% ต่อปีในห้าปีที่ผ่านมา และในกรณีฐานจะเพิ่มเป็นราว 945 TWh ภายในปี 2030 หรือเกือบ 3% ของความต้องการไฟฟ้าโลก ตัวขับเคลื่อนหลักคือ AI เพราะชิปเฉพาะทางกินไฟมากกว่าเซิร์ฟเวอร์ทั่วไปมาก',
    'ภายในดาต้าเซ็นเตอร์สมัยใหม่ เซิร์ฟเวอร์ใช้ไฟราว 60% ระบบระบายความร้อนใช้ราว 7% ในศูนย์ขนาดใหญ่ที่มีประสิทธิภาพสูงสุด และมากกว่า 30% ในศูนย์ที่เก่าหรือประสิทธิภาพต่ำ ที่เหลือส่วนใหญ่เป็นระบบจัดเก็บข้อมูลและเครือข่าย',
    'ไฟที่ดาต้าเซ็นเตอร์ใช้ราว 30% ยังมาจากถ่านหิน IEA ประเมินการปล่อย CO₂ ราว 180 ล้านตันต่อปีในปัจจุบัน และเพิ่มเป็นราว 300 ล้านตันภายในปี 2035 ยังน้อยกว่า 1% ของการปล่อยทั้งโลก (41,600 ล้านตันในปี 2024) แต่ความต้องการที่โตเร็วมากอาจทำให้โรงไฟฟ้าฟอสซิลเก่าต้องเดินเครื่องนานขึ้น และแย่งไฟสะอาดที่ควรจะมาแทนที่โรงไฟฟ้าเหล่านั้น']),
   ('น้ำ', [
    'ความร้อนส่วนใหญ่ถูกระบายด้วยระบบหล่อเย็นแบบระเหย น้ำดูดความร้อนแล้วระเหยไป ไม่กลับคืนมา Lincoln Institute รายงานว่าดาต้าเซ็นเตอร์ขนาดใหญ่อาจใช้น้ำถึง 5 ล้านแกลลอนสหรัฐต่อวัน (ราว 19 ล้านลิตร) ใกล้เคียงเมืองที่มีประชากร 50,000 คน',
    'ยังมีการใช้น้ำแฝงอยู่ ไฟที่ดาต้าเซ็นเตอร์ในสหรัฐฯ ใช้ราวครึ่งหนึ่งมาจากโรงไฟฟ้าเชื้อเพลิงฟอสซิลที่ต้มน้ำเพื่อหมุนกังหัน ผู้ประกอบการต้องเลือก ระบบวงจรปิดหรือระบายความร้อนด้วยอากาศประหยัดน้ำแต่ใช้ไฟมากขึ้น ส่วนระบบระเหยประหยัดไฟแต่ใช้น้ำมากขึ้น']),
   ('มลพิษทางอากาศและสุขภาพ', [
    'ดาต้าเซ็นเตอร์มีเครื่องปั่นไฟดีเซลจำนวนมากไว้ใช้ตอนไฟดับ และต้องเดินเครื่องทดสอบเป็นประจำ งานวิจัยของ Caltech และ UC Riverside ประเมินว่าในสหรัฐฯ มลพิษทางอากาศจากดาต้าเซ็นเตอร์ AI และโรงไฟฟ้าที่ป้อนไฟให้ อาจทำให้มีผู้เสียชีวิตก่อนวัยอันควรราว 1,300 คน และค่าใช้จ่ายด้านสุขภาพสูงถึง 20,000 ล้านดอลลาร์สหรัฐต่อปีภายในปี 2030 เครื่องปั่นไฟดีเซลปล่อยไนโตรเจนไดออกไซด์มากกว่าโรงไฟฟ้าก๊าซ 200–600 เท่าต่อหน่วยไฟ เฉพาะเวอร์จิเนียตอนเหนือ ประเมินว่ามลพิษจากเครื่องปั่นไฟสำรองสร้างต้นทุนด้านสาธารณสุข 190–260 ล้านดอลลาร์ต่อปี']),
   ('ขยะอิเล็กทรอนิกส์', [
    'ฮาร์ดแวร์ AI ถูกเปลี่ยนเร็วเมื่อมีชิปรุ่นใหม่ งานวิจัยในวารสาร Nature Computational Science ประเมินว่าเฉพาะโมเดลภาษาขนาดใหญ่อาจสร้างขยะอิเล็กทรอนิกส์ 1.2–5 ล้านตันระหว่างปี 2023–2030 และสูงถึงราว 2.5 ล้านตันต่อปีภายในปี 2030 ในกรณีขยายตัวเร็ว เทียบกับขยะอิเล็กทรอนิกส์ทั้งโลกราว 62 ล้านตันในปี 2022 ชิป แผงวงจร และแบตเตอรี่มีทั้งวัสดุมีค่าและสารอันตราย การรีไซเคิลจึงสำคัญ']),
   ('ที่ดิน เสียง และความร้อน', [
    'โครงการขนาดใหญ่ใช้พื้นที่มาก หอระบายความร้อนทำงานทั้งวันทั้งคืน ทดสอบเพดานเสียงกลางคืน 50–55 dB(A) ใกล้บ้านเรือน และความร้อนที่ปล่อยออกมาเพิ่มปรากฏการณ์เกาะความร้อนในเมือง ตามที่มีรายงานในพื้นที่ใกล้กรุงเทพฯ']),
  ]),
  ('soc', 'ผลกระทบทางเศรษฐกิจและสังคม', [
   ('การลงทุนและการเติบโต', [
    'ดาต้าเซ็นเตอร์มาพร้อมเงินลงทุนมหาศาล บีโอไออนุมัติโครงการดาต้าเซ็นเตอร์ 26 โครงการ มูลค่าเกือบ 5 แสนล้านบาทในปี 2025 และคำขอใหม่เกิน 1 ล้านล้านบาทในต้นปี 2026 อีกรายงานระบุ 36 โครงการ มูลค่า 7.28 แสนล้านบาท ก่อนบีโอไอหยุดรับคำขอส่งเสริมดาต้าเซ็นเตอร์ใหม่ในเดือนเมษายน 2026 และมีดาต้าเซ็นเตอร์เปิดดำเนินการแล้ว 42 แห่ง ศูนย์ขนาดใหญ่ยังช่วยให้บริการโทรคมนาคมและคลาวด์ดีขึ้น และเก็บข้อมูลไว้ใกล้ผู้ใช้']),
   ('การจ้างงาน', [
    'ดาต้าเซ็นเตอร์สร้างงานประจำน้อยกว่าขนาดของมันมาก งานวิจัยของ Brookings จากราว 1,500 แห่งในสหรัฐฯ พบว่ามณฑลที่มีดาต้าเซ็นเตอร์ขนาดใหญ่มีงานเพิ่มราว 100–200 ตำแหน่ง การจ้างงานด้านประมวลผลข้อมูลเพิ่มราว 56% ในสิบปี แต่ค่าจ้างในพื้นที่ไม่เปลี่ยน และราคาบ้านเพิ่ม 2–5% ในไทย TDRI ประเมินว่าดาต้าเซ็นเตอร์ 100 MW สร้างงานโดยตรงราว 50 ตำแหน่ง ช่วงก่อสร้างช่วยกระตุ้นเศรษฐกิจเพียงชั่วคราว']),
   ('ค่าไฟ', [
    'ในที่ที่มีดาต้าเซ็นเตอร์เข้ามาพร้อมกันจำนวนมาก ทุกคนอาจต้องร่วมจ่ายค่าโรงไฟฟ้าและสายส่งที่เพิ่มขึ้น ในระบบไฟฟ้า PJM ทางตะวันออกของสหรัฐฯ ราคากำลังผลิตพุ่งจาก 28.92 เป็น 269.92 ดอลลาร์ต่อ MW ต่อวันในปี 2025/26 หน่วยงานกำกับตลาดระบุว่า 63% ของส่วนที่เพิ่มขึ้น หรือราว 9,300 ล้านดอลลาร์ มาจากดาต้าเซ็นเตอร์ ค่าไฟบ้านในบางพื้นที่เพิ่มราว 16–21 ดอลลาร์ต่อเดือน งานวิจัยของ Georgia Tech พบว่าค่าไฟในพื้นที่ที่มีดาต้าเซ็นเตอร์สูงขึ้นราว 5%',
    'ในไทย มีรายงานว่าดาต้าเซ็นเตอร์จ่ายค่าไฟราว 5–6 บาทต่อหน่วย เทียบกับบ้านเรือนราว 3–4 บาท และมีข้อเสนอผู้ใช้ไฟ "ประเภทที่ 9" ให้ดาต้าเซ็นเตอร์ขนาดใหญ่ที่ใช้ไฟจากเชื้อเพลิงฟอสซิลรับต้นทุนจริงของ LNG นำเข้า วิธีจ่ายค่าปรับปรุงระบบไฟฟ้าจะเป็นตัวตัดสินว่าบ้านเรือนต้องร่วมแบกต้นทุนหรือไม่']),
   ('สิทธิประโยชน์ทางภาษี', [
    'รัฐบาลแข่งกันให้สิทธิประโยชน์ ในสหรัฐฯ 36 จาก 50 รัฐมีมาตรการลดภาษีให้ดาต้าเซ็นเตอร์ รัฐต่าง ๆ สูญรายได้ภาษีหลายพันล้านดอลลาร์ และอย่างน้อย 14 รัฐไม่เปิดเผยตัวเลข บางรัฐกำหนดเงื่อนไขการจ้างงาน เช่น เวอร์จิเนียกำหนดอย่างน้อย 50 ตำแหน่ง ค่าจ้างเกิน 150% ของค่าเฉลี่ยในพื้นที่']),
   ('การแย่งน้ำและชุมชน', [
    'ชุมชนเกษตรและประมงในชลบุรีและระยองกังวลเรื่องความมั่นคงทางน้ำ ผลสำรวจผู้บริหาร 160 คนของสภาอุตสาหกรรมแห่งประเทศไทยพบว่า 68.8% กังวลเรื่องน้ำไม่พอมากที่สุด การตรวจสอบยังพบ "ความต้องการผี" คือสัญญาจองน้ำซ้อนกันที่ทำให้การขาดแคลนดูรุนแรงกว่าความจริงบนกระดาษ']),
  ]),
  ('info', 'เราบริโภคข้อมูลอย่างไร', [
   ('', [
    'ทุกการเลื่อนฟีด ทุกวิดีโอ และทุกคำตอบจาก AI ถูกส่งมาจากดาต้าเซ็นเตอร์ ปลายปี 2025 คนไทย 67.8 ล้านคน (94.7%) ใช้อินเทอร์เน็ต มีบัญชีโซเชียลมีเดีย 56.6 ล้านบัญชี LINE มีผู้ใช้ราว 56 ล้านคนต่อเดือน ส่วน TikTok, Facebook และ YouTube เข้าถึงคนราว 47–57 ล้านคนต่อแพลตฟอร์ม',
    'วิดีโอครองส่วนใหญ่ Ericsson รายงานว่าวิดีโอคิดเป็นราว 75% ของข้อมูลมือถือทั้งหมด สมาร์ตโฟนใช้ข้อมูลเฉลี่ยราว 22 GB ต่อเดือนเมื่อปลายปี 2025 (ราว 23 GB ในเอเชียตะวันออกเฉียงใต้และโอเชียเนีย) และจะเพิ่มเป็นราว 42 GB ทั่วโลก และ 50 GB ในภูมิภาคของเราภายในปี 2031 ปริมาณข้อมูลมือถือทั้งโลกอยู่ที่ราว 210 เอกซะไบต์ต่อเดือน',
    'AI เพิ่มอีกชั้นหนึ่ง แทนที่จะดึงหน้าเว็บที่เก็บไว้แล้ว แชตบอตหรือเครื่องมือสร้างภาพต้องประมวลผลคำตอบใหม่ทุกครั้ง จึงใช้พลังงานต่อครั้งมากกว่าการค้นหาหรือส่งข้อความทั่วไปมาก',
    'นิสัยเล็ก ๆ ช่วยได้ ดาวน์โหลดผ่าน Wi-Fi แทนการสตรีมวิดีโอเดิมซ้ำ เลือกความละเอียดต่ำลงบนจอเล็ก ปิดเล่นอัตโนมัติ และลบไฟล์บนคลาวด์ที่ไม่ใช้แล้ว']),
  ]),
  ('th', 'ประเทศไทยกำลังทำอะไร', [
   ('มาตรการที่กำลังเตรียม', [
    'กรอบคัดกรอง 4 เสาหลัก (ความมั่นคงทางพลังงาน ขีดจำกัดของน้ำ ผลกระทบสิ่งแวดล้อม และประโยชน์ต่อประเทศ) กำลังจัดทำโดยบีโอไอ สำนักงานทรัพยากรน้ำแห่งชาติ และสภาพัฒน์',
    'แผนที่ไฟฟ้าและน้ำร่วมกัน จะจำกัดดาต้าเซ็นเตอร์ใหม่ไว้ในพื้นที่ที่มีส่วนเกินจริง และไม่ให้ศูนย์ที่ใช้น้ำหล่อเย็นแห่งใหม่ตั้งในลุ่มน้ำเปราะบาง โครงการใหม่ต้องใช้ระบบหล่อเย็นวงจรปิดหรือของเหลว',
    'โครงการนำร่องซื้อไฟโดยตรง (Direct PPA) จำกัด 2,000 MW ให้ดาต้าเซ็นเตอร์ซื้อไฟพลังงานหมุนเวียนได้โดยตรง และ กฟผ. วางแผนลงทุนปรับปรุงสายส่งใน EEC 3.1 หมื่นล้านบาท',
    'สภาพัฒน์เสนอให้รายงานการใช้ทรัพยากรภาคบังคับ กำหนดสัดส่วนการใช้ของในประเทศ ฝึกอบรมแรงงาน และกระบวนการรับฟังความคิดเห็นของประชาชนอย่างเป็นทางการ']),
  ]),
  ('you', 'มีความหมายอย่างไรกับบ้านและธุรกิจ', [
   ('', [
    'ดาต้าเซ็นเตอร์เป็นส่วนหนึ่งของเศรษฐกิจสมัยใหม่ คำถามในไทยจึงไม่ใช่ว่าจะมีหรือไม่ แต่จะมีภายใต้เงื่อนไขอะไร สำหรับบ้านเรือนและธุรกิจ มีสามเรื่องที่ควรติดตาม คือ ต้นทุนปรับปรุงระบบไฟฟ้าจะถูกส่งต่อมาที่ผู้ใช้ทั่วไปหรือไม่ การจัดสรรน้ำจะปกป้องเกษตรกรและชุมชนหรือไม่ และไฟสะอาดจะเพิ่มขึ้นเร็วแค่ไหน',
    'แผงโซลาร์ผลิตไฟได้โดยไม่ต้องเผาเชื้อเพลิงหรือใช้น้ำหล่อเย็น การผลิตไฟใช้เองตอนกลางวันบนหลังคาเป็นทางหนึ่งที่ทำให้คุณได้รับผลกระทบน้อยลงจากการเปลี่ยนแปลงของค่าไฟ และทุกหน่วยที่ผลิตบนหลังคาคือหน่วยที่ระบบไฟฟ้าไม่ต้องจ่าย อ่าน <a href="/th/solar-subsidy-50000.html">สรุปโซลาร์ 50,000 บาท</a>']),
  ]),
  ('books', 'หนังสือแนะนำ: AI ดาต้าเซ็นเตอร์ และผลกระทบ (ภาษาอังกฤษ)', [
   ('', [
    'RAW:<ol class="books">' + '<li><b><i>Atlas of AI</i></b> – Kate Crawford (Yale University Press, 2021). มอง AI เป็นอุตสาหกรรมที่ใช้แร่ พลังงาน แรงงาน และข้อมูล จุดเริ่มต้นที่ดีที่สุด</li><li><b><i>Empire of AI</i></b> – Karen Hao (Penguin Press, May 2025). เบื้องหลังการเติบโตของ OpenAI แรงงานข้อมูล และทรัพยากรที่ใช้ ผู้เขียนแก้ตัวเลขการใช้น้ำของดาต้าเซ็นเตอร์ในชิลีที่สูงเกินจริงเมื่อ พ.ย. 2025</li><li><b><i>Hyperscale: Ambition, Power and the Relentless Rise of Data Empires</i></b> – Paris Marx (Profile Books, 20 October 2026). รอยเท้าทางกายภาพของดาต้าเซ็นเตอร์ และใครต้องแบกรับต้นทุน ติดรายชื่อยาวรางวัล FT Business Book of the Year 2026</li><li><b><i>A Prehistory of the Cloud</i></b> – Tung-Hui Hu (MIT Press, 2015). สายเคเบิล อาคาร และประวัติศาสตร์ที่ซ่อนอยู่หลังคำว่า "คลาวด์"</li><li><b><i>Cloud Empires</i></b> – Vili Lehdonvirta (MIT Press, 2022). แพลตฟอร์มดิจิทัลกลายเป็นผู้มีอำนาจคล้ายรัฐได้อย่างไร</li><li><b><i>Power and Progress</i></b> – Daron Acemoglu & Simon Johnson (PublicAffairs, 2023). ใครได้ประโยชน์จากเทคโนโลยีใหม่ ตั้งแต่ยุคกลางจนถึง AI</li><li><b><i>Code Dependent</i></b> – Madhumita Murgia (Henry Holt / Picador, 2024). AI ส่งผลต่อแรงงานและคนธรรมดาทั่วโลกแล้วอย่างไร</li><li><b><i>AI Snake Oil</i></b> – Arvind Narayanan & Sayash Kapoor (Princeton University Press, 2024). แยกให้ออกว่า AI ทำอะไรได้จริงและทำอะไรไม่ได้</li><li><b><i>The Coming Wave</i></b> – Mustafa Suleyman with Michael Bhaskar (Crown, 2023). คนในวงการพูดถึงความเสี่ยงและการกำกับดูแล AI</li><li><b><i>The Datacenter as a Computer (3rd ed.)</i></b> – Luiz André Barroso, Urs Hölzle & Parthasarathy Ranganathan (Morgan & Claypool, 2018). การออกแบบดาต้าเซ็นเตอร์ขนาดใหญ่เชิงเทคนิค และทำไมประสิทธิภาพจึงสำคัญ</li><li><b><i>The Shallows</i></b> – Nicholas Carr (W. W. Norton, 2010). การอ่านออนไลน์ตลอดเวลาส่งผลต่อสมาธิและความจำอย่างไร</li><li><b><i>Stolen Focus</i></b> – Johann Hari (Crown / Bloomsbury, 2022). ทำไมสมาธิของเราสั้นลงในยุคฟีดไม่รู้จบ</li>' + '</ol>',
   ]),
  ]),
 ],
 src_h='แหล่งข้อมูล', note='โซลาร์ เอสส์ ยินดีแบ่งปันข้อมูลที่อัปเดตและประสบการณ์ตรงจากหน้างานจริงเสมอ ตัวเลขมาจากแหล่งข้อมูลด้านล่าง หากแหล่งข้อมูลต่างกัน เราแสดงทั้งสองค่า หน้านี้จะอัปเดตเมื่อมีหลักฐานใหม่',
 back='ข่าวดาต้าเซ็นเตอร์ทั้งหมด', backurl='/th/news.html#topic-datacenter'),
}

PDF = {'en': 'downloads/Data_Centre_Impacts_Guide_EN_Rev01_20261027.pdf', 'th': 'downloads/Data_Centre_Impacts_Guide_TH_Rev01_20261027.pdf', 'zh': 'downloads/Data_Centre_Impacts_Guide_ZH_Rev01_20261027.pdf'}
DLH = {'en': ('Download the full guide (PDF)', ['English', 'ไทย', '中文']), 'th': ('ดาวน์โหลดฉบับเต็ม (PDF)', ['English', 'ไทย', '中文']), 'zh': ('下载完整指南（PDF）', ['English', 'ไทย', '中文'])}
def dl_block(lang):
    h, labs = DLH[lang]
    return ('<div class="dl" style="margin-top:22px;border-left:4px solid var(--hot);background:var(--white);padding:14px 18px"><b>' + h + '</b><p style="margin-top:8px">' +
            ' '.join(f'<a class="btn{"" if k == lang else " ghost"}" href="/{PDF[k]}" download style="margin:4px 6px 4px 0">{lab} ↓</a>' for k, lab in zip(('en', 'th', 'zh'), labs)) + '</p></div>')

def build(lang):
    c = C[lang]; e = lambda x: html.escape(x, quote=True)
    shell = open({'th': 'th/news.html', 'zh': 'zh/news.html'}.get(lang, 'news.html'), encoding='utf-8').read()
    he = shell.find('</head>'); bs = shell.find('<section', shell.find('<body')); ft = shell.find('<footer')
    head = shell[:he]
    head = re.sub(r'<title>.*?</title>', f'<title>{e(c["title"])}</title>', head, flags=re.S)
    head = re.sub(r'(<meta (?:property|name)="(?:og:title|twitter:title)" content=")[^"]*"', lambda m: m.group(1) + e(c['title']) + '"', head)
    head = re.sub(r'(<meta (?:property|name)="(?:description|og:description|twitter:description)" content=")[^"]*"', lambda m: m.group(1) + e(c['desc']) + '"', head)
    head = re.sub(r'<meta property="og:type" content="[^"]*">', '<meta property="og:type" content="article">', head)
    head = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{c["url"]}">', head)
    head = re.sub(r'<link rel="canonical"[^>]*>', f'<link rel="canonical" href="{c["url"]}">', head)
    head = re.sub(r'<link rel="alternate" hreflang="[^"]*"[^>]*>\n?', '', head)
    head = re.sub(r'<script type="application/ld\+json"[^>]*>.*?</script>\n?', '', head, flags=re.S)
    head = re.sub(r'<style id="(ntopics|poll)-css">.*?</style>\n?', '', head, flags=re.S)
    head += ('<link rel="alternate" hreflang="th" href="https://solaress.org/th/data-centre-impacts">\n'
             '<link rel="alternate" hreflang="en" href="https://solaress.org/data-centre-impacts">\n'
             '<link rel="alternate" hreflang="zh-Hans" href="https://solaress.org/zh/data-centre-impacts">\n'
             '<link rel="alternate" hreflang="x-default" href="https://solaress.org/data-centre-impacts">\n')
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": c['title'].split(' | ')[0], "description": c['desc'],
           "inLanguage": lang, "datePublished": "2026-10-27", "dateModified": UPDATED_ISO, "mainEntityOfPage": c['url'],
           "author": {"@type": "Organization", "name": "Solar ESS", "url": "https://solaress.org/"},
           "publisher": {"@type": "Organization", "name": "Solar ESS Co. Ltd.", "url": "https://solaress.org/"},
           "citation": [u for t, u in SRC]},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": c['crumb_home'], "item": "https://solaress.org" + c['home']},
              {"@type": "ListItem", "position": 2, "name": c['crumb_news'], "item": "https://solaress.org" + c['news']},
              {"@type": "ListItem", "position": 3, "name": c['title'].split(' | ')[0], "item": c['url']}]}]
    for d in ld:
        head += '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False).replace('</', '<\\/') + '</script>\n'
    head += ('<style>.lf h2{font-size:clamp(26px,3.6vw,38px);margin-top:56px;padding-top:28px;border-top:1.5px solid var(--navy)}'
             '.lf h3{font-size:20px;margin-top:28px}.lf p{margin-top:12px}.lf .kf{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin-top:8px}'
             '.lf .kf div{border:1.5px solid var(--line);background:var(--white);padding:14px 16px}.lf .kf b{display:block;font-family:var(--display);font-size:26px;color:var(--navy)}'
             '.lf .kf span{font-size:14px;color:var(--mute)}.lf .toc{margin-top:24px;display:flex;flex-wrap:wrap;gap:8px}.lf .toc a{border:1.5px solid var(--navy);padding:6px 12px;font-size:14px;text-decoration:none}'
             '.lf table{width:100%;border-collapse:collapse;margin-top:14px;font-size:15px;background:var(--white)}.lf th,.lf td{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}.lf th{background:var(--navy);color:var(--white)}.lf .tw{overflow-x:auto}'
             '.lf .crumb{font-family:var(--mono);font-size:12px;opacity:.75;margin-bottom:12px}.lf .crumb a{text-decoration:none}.lf ol.books{font-size:16px;gap:10px}.lf ol{padding-left:22px;font-size:14px;display:grid;gap:6px;margin-top:12px}</style>\n')
    out = [head, shell[he:bs]]
    out.append(f'<section class="dark band" style="padding-block:64px"><div class="wrap lf"><p class="crumb"><a href="{c["home"]}">{c["crumb_home"]}</a> › <a href="{c["news"]}">{c["crumb_news"]}</a></p>'
               f'<p class="eyebrow">{c["updated"]}</p><h1 style="font-size:clamp(34px,5.6vw,60px)">{c["h1"]}</h1>'
               f'<p class="lede" style="margin-top:18px">{c["lede"]}</p></div></section>\n')
    b = ['<section class="band light" style="padding-block:56px"><div class="wrap lf"><article style="max-width:760px">',
         '<div class="kf">' + ''.join(f'<div><b>{a}</b><span>{s}</span></div>' for a, s in c['kf']) + '</div>',
         f'<nav class="toc" aria-label="{e(c["toc"])}">' + ''.join(f'<a href="#{sid}">{h}</a>' for sid, h, _ in c['sections']) + '</nav>', dl_block(lang)]
    for sid, h, subs in c['sections']:
        b.append(f'<h2 id="{sid}">{h}</h2>')
        for sh, paras in subs:
            if sh: b.append(f'<h3>{sh}</h3>')
            b += [p[4:] if p.startswith('RAW:') else f'<p>{p}</p>' for p in paras]
    b.append(f'<p style="margin-top:36px;font-size:14px;color:var(--mute)">{c["note"]}</p>')
    b.append(f'<h2 style="font-size:22px">{c["src_h"]}</h2><ol>' + ''.join(f'<li><a href="{u}" rel="noopener">{e(t)}</a></li>' for t, u in SRC) + '</ol>')
    b.append(f'<p style="margin-top:28px"><a class="btn ghost" href="{c["backurl"]}">← {c["back"]}</a></p>')
    b.append('</article></div></section>\n')
    out += b
    tail = shell[ft:]
    tail = re.sub(r'<script id="(ntopics|poll)-js">.*?</script>\n?', '', tail, flags=re.S)
    out.append(tail)
    open(c['out'], 'w', encoding='utf-8').write(''.join(out)); print('wrote', c['out'])

from dc_impacts_zh import ZH
C['zh'] = ZH

if __name__ == '__main__':
    for l in C: build(l)
