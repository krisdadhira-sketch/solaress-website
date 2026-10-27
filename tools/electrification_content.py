"""Content for /electrification-who-pays (EN/TH). Built by tools/electrification_page.py."""

def T(head, rows):
    h = ''.join(f'<th>{c}</th>' for c in head)
    r = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in row) + '</tr>' for row in rows)
    return f'RAW:<div class="tw"><table><tr>{h}</tr>{r}</table></div>'

SRC = [
 ('IEA – Energy and AI: energy demand from AI', 'https://www.iea.org/reports/energy-and-ai/energy-demand-from-ai'),
 ('DCD – Google plans 24/7 carbon-free energy for data centers by 2030 (15 Sep 2020)', 'https://datacenterdynamics.com/en/news/google-plans-move-247-carbon-free-energy-data-centers-and-offices-2030'),
 ('Mayer Brown – German Energy Efficiency Act and data centers (Feb 2024)', 'https://www.mayerbrown.com/en/insights/publications/2024/02/sustainable-data-centers-the-german-energy-efficiency-act-what-data-center-operators-need-to-consider-now-and-in-the-future'),
 ('Hunton – Thailand’s draft direct PPA regulation for data centers (Oct 2025)', 'https://www.hunton.com/insights/legal/thailands-draft-regulation-on-direct-power-purchase-agreements-via-third-party-access-for-data-centers'),
 ('Green Tech Festival – Thailand gives data centres their own power tariff (14 Aug 2026)', 'https://greentechfestival.com/network/story/thailand-data-centre-power-tariff-direct-ppa-2026/'),
 ('BOI – Utility Green Tariff (UGT1/UGT2) presentation (Jul 2024)', 'https://www.boi.go.th/upload/content/20240730%20EN%20UGT.pdf'),
 ('SolarQuarter – Thailand launches UGT2 (20 Mar 2026)', 'https://solarquarter.com/2026/03/20/thailand-launches-ugt2-program-to-boost-corporate-access-to-renewable-energy/'),
 ('MEA MyEnergy – People’s Solar notices', 'https://myenergy.mea.or.th/'),
 ('PEA – โซลาร์ภาคประชาชน registration site', 'https://peoplesolar.pea.co.th'),
 ('Watson Farley & Williams – Thailand’s 5 GW renewable FiT scheme 2022–2030 (Oct 2022)', 'https://www.wfw.com/articles/thailands-5-gw-renewable-ppa-fit-scheme-2022-2030/'),
 ('Reccessary – 25-year solar PPAs for 12 projects, 644.8 MW (Dec 2023)', 'https://reccessary.com/en/news/gulf-energy-egat-sign-for-12-solar-power-projects'),
 ('Oxpeckers – Wired for waste: Thailand’s energy surplus (Oct 2025)', 'https://oxpeckers.org/?p=14090'),
 ('The Nation – September 2026 household tariff, first 200 units capped at 3 baht', 'https://www.nationthailand.com/news/general/40069705'),
 ('Thansettakij – Royal decree on the 200,000-baht solar tax deduction (4 Mar 2026)', 'https://www.thansettakij.com/economy/energy/652936'),
 ('SCB EIC – Solar rooftop tax benefits (Jul 2025)', 'https://www.scbeic.com/en/detail/file/product/9833/h90rysnt5x/Flash-Solar-rooftop-tax-benefits-ENG-20250708.pdf'),
 ('Prachachat – PEA plan for the 50,000-baht scheme (21 Oct 2026)', 'https://www.prachachat.net/economic/news-2083575'),
 ('Asia News Network / The Nation – The true price of the cloud (Sep 2026)', 'https://asianews.network/the-true-price-of-the-cloud-inside-thailands-battle-for-water-and-power/'),
 ('Brookings – New evidence on data center employment effects (2026)', 'https://www.brookings.edu/articles/new-evidence-on-data-center-employment-effects/'),
 ('IEEFA – PJM capacity prices and data centers (Jul 2025)', 'https://ieefa.org/resources/projected-data-center-growth-spurs-pjm-capacity-prices-factor-10'),
 ('The Conversation – AI’s invisible and exploited workforce', 'https://theconversation.com/ai-is-a-multi-billion-dollar-industry-its-underpinned-by-an-invisible-and-exploited-workforce-240568'),
]

BOOKS = [
 ('Atlas of AI', 'Kate Crawford', 'Yale University Press, 2021', 'AI as an extractive industry', 'AI ในฐานะอุตสาหกรรมที่ดึงทรัพยากร'),
 ('Hyperscale', 'Paris Marx', 'Profile Books, 2026', 'The physical footprint of data centres and who bears it', 'รอยเท้าของดาต้าเซ็นเตอร์ และใครแบกรับ'),
 ('Power and Progress', 'Daron Acemoglu & Simon Johnson', 'PublicAffairs, 2023', 'Who gains from new technology', 'ใครได้ประโยชน์จากเทคโนโลยีใหม่'),
 ('Agnotology: The Cultural Production of Ignorance', 'Robert N. Proctor & Londa Schiebinger (eds.)', 'Stanford University Press, 2008', 'How confusion and doubt are produced on purpose', 'ความสับสนและความสงสัยถูกสร้างขึ้นโดยเจตนาอย่างไร'),
 ('Merchants of Doubt', 'Naomi Oreskes & Erik M. Conway', 'Bloomsbury, 2010', 'How doubt is used to delay action', 'การใช้ความสงสัยเพื่อถ่วงเวลา'),
 ('The Shock Doctrine', 'Naomi Klein', 'Metropolitan Books, 2007', 'How a crisis is used to rush policy through', 'การใช้วิกฤตเพื่อเร่งผลักดันนโยบาย'),
 ('Code Dependent', 'Madhumita Murgia', 'Henry Holt / Picador, 2024', 'AI’s effect on ordinary people and workers', 'AI กับคนธรรมดาและแรงงาน'),
]

def books(lang):
    i = 3 if lang == 'en' else 4
    return 'RAW:<ol class="books">' + ''.join(f'<li><b><i>{b[0]}</i></b> – {b[1]} ({b[2]}). {b[i]}.</li>' for b in BOOKS) + '</ol>'

EN = dict(
 out='electrification-who-pays.html', url='https://solaress.org/electrification-who-pays', news='/news.html', home='/',
 title='Thailand’s Electrification: Who Pays, Who Gains? | Solar ESS',
 desc='An evidence-graded look at Thailand’s energy policy as data centres arrive: clean-power rules, who can sell green power, the 200,000-baht tax deduction, the 50,000-baht solar scheme, and what to check before you sign.',
 crumb_home='Home', crumb_news='News', updated='Analysis · 27 October 2026',
 h1='Thailand’s electrification:<br>who pays,<br>who gains?',
 lede='Thailand needs much more electricity, and much of the new demand comes from data centres that want clean power. Whether this journey narrows or widens the gap between rich and poor depends on rules that are still being written. We grade each claim by its evidence, so you can see what is known and what is still a question.',
 kf=[('1,000 kVA', 'minimum plant size to sell green power directly to a data centre'), ('2.20 baht', 'what a household is paid per unit, up to 5 kW'), ('4.56 baht', 'what companies pay for certified green power (UGT2)'), ('0–50,000 baht', 'tax saved from the 200,000-baht deduction, by income')],
 toc='On this page',
 sections=[
  ('grades', 'How to read this page', [('', [
   'Each finding carries a grade. <b>Supported</b>: official data or documents back it. <b>Partly supported</b>: the facts exist but the conclusion is one reading among several. <b>Not yet evidenced</b>: a fair question, but no public evidence yet. Figures are as of 27 October 2026, before the official rules of the 50,000-baht scheme were published. This page names no person or company as acting in bad faith; it shows where to look.'])]),
  ('demand', 'Rising demand, and data centres', [('', [
   '<b>Supported.</b> Data centres worldwide used about 415 TWh in 2024, roughly twice Thailand’s total use, and the IEA expects about 945 TWh by 2030. Thailand’s planned data centres (about 2.87 GW) could add roughly 10% to national demand at 80% use (our estimate). Few permanent jobs come with them, and they compete for water and grid upgrades. Full detail: <a href="/data-centre-impacts.html">Data centres: the real costs and benefits</a>.'])]),
  ('clean', 'Why data centres want clean power', [('', [
   '<b>Partly supported.</b> Thailand has no general law that every data centre must use a set share of clean power. The expectation comes from three places:',
   T(['Source', 'What it says'], [
    ['Company pledges', 'Large cloud firms buy renewable power equal to their yearly use; Google aims for carbon-free power every hour by 2030 (about 65% hour by hour in 2020)'],
    ['Germany', 'Data centres of 300 kW or more: 50% unsubsidised renewable power from 2024, 100% from 2027'],
    ['Thailand, direct PPA (draft, Oct 2025)', 'Buyer: a BOI-promoted data centre of at least 50 MW that intends 100% renewable power. Seller: a new renewable plant of at least 1,000 kVA. Opened to all industries in Aug 2026 (reported)'],
    ['Thailand, green tariffs', 'UGT1 adds certificates from existing hydro plants; UGT2 costs about 4.56 baht/kWh for 10 years from new solar, wind and biogas']]),
   'The reasons: climate pledges and emissions reporting, customers’ supply-chain rules (including EU carbon rules for exporters), long-term price stability, and competition between countries for investment. The gap to watch: about 30% of data-centre power worldwide still comes from coal, and Thailand’s Energy Minister has said operators publicly demand 100% clean energy yet often ask for “any power immediately”.'])]),
  ('share', 'A fair share: who gets to sell clean power?', [('', [
   '<b>Supported on access; partly supported on profit.</b> The direct-sale rules are written for large plants, so a household rooftop cannot take part. Per unit, households and big solar farms are paid about the same; the difference is scale and contract length.',
   T(['Who', 'Price (baht/kWh)', 'Terms'], [
    ['Household rooftop sells surplus', '2.20', 'up to 5 kW export; 10 years per MEA’s current notice (20 years reported for the new scheme)'],
    ['Large ground solar sells to EGAT (2022 scheme)', '2.1679', 'regulator-set price, no price bidding; 2,368 MW'],
    ['Large solar + battery (same scheme)', '2.8331', '1,000 MW'],
    ['Households buy (Sept 2026 average)', 'about 3.89', 'first 200 units capped at 3 baht'],
    ['Companies buy certified green power (UGT2)', 'about 4.56', '10 years'],
    ['Data centres buy (new tariff, reported)', 'about 5–6', 'separate class']]),
   'One large listed company signed 25-year contracts with EGAT for 12 solar projects totalling 644.8 MW under the 2022 scheme; a household gets at most 5 kW. The larger money is in fossil capacity: Thailand’s reserve margin was 34–38% in 2025 against a 15% norm, and under some private contracts availability payments are made even when plants are not used, costs that TDRI says flow into tariffs.',
   '<b>What a fairer system could look like:</b> reserve a share of data-centre green-power demand for households, cooperatives and community solar; let aggregators pool many rooftops to reach the 1,000 kVA threshold; publish the full chain of prices; and give households contracts as long as large producers get.'])]),
  ('tax', 'The 200,000-baht tax deduction: who benefits?', [('', [
   '<b>Supported: it favours higher incomes.</b> It reduces taxable income, so its value rises with the tax bracket: about 6,100–50,000 baht saved on the full 200,000 baht (SCB EIC). Rules: new on-grid systems up to 10 kWp, installed 3 March 2026 – 31 December 2028, claimant must own the meter and hold an e-tax invoice from a VAT-registered seller.',
   T(['Effect', 'Who gains or loses'], [
    ['Tax saved grows with income', 'Top earners gain most; people below the tax threshold gain nothing'],
    ['Meter must be in the claimant’s name', 'Renters and families with the meter in a parent’s name are left out'],
    ['VAT-registered sellers only', 'Formal companies gain; small local installers without VAT lose work'],
    ['Lower bills, less peak demand', 'Positive for owners and a little for the grid']]),
   'Side effects to watch: a 2026–2028 rush means panels reaching end of life together while recycling is still being planned, and deadline pressure invites poor installations.'])]),
  ('fifty', 'The 50,000-baht scheme: what is still unclear', [('', [
   '<b>“Unclear” is supported; a 25-year debt trap is not supported by the terms reported so far; hidden intent is not yet evidenced.</b> Reported terms: 50,000 baht for each of 1 million homes; PEA’s example of a 5 kW system at about 140,000 baht leaves about 90,000 baht; loans at 2.5% for 7 years; surplus bought at 2.20 baht. Still unclear: the vendor list and its criteria; the interest rate after the promotion and the penalty for missed payments; whether the subsidy goes to the installer or the household; the buy-back term (10 or 20 years); how the 90,000-baht balance is financed; and whether batteries and ground-mounted systems get the same terms.',
   '<b>Does a loan pay for itself?</b> Our arithmetic: 90,000 baht at 2.5% over 7 years ≈ 1,169 baht a month. A 5 kW system makes about 600 units a month.',
   T(['Household', 'Use per month', 'Value of solar per month', 'Margin over the loan'], [
    ['Low user (half in daytime, 3 baht/unit)', '150 units', '≈ 1,380 baht', '≈ +210 baht'],
    ['Middle user (60% daytime, 3.89 baht)', '400 units', '≈ 1,730 baht', '≈ +560 baht'],
    ['High daytime user (70%, 4.20 baht)', '800 units', '≈ 2,440 baht', '≈ +1,270 baht']]),
   'The poorest households pay the lowest tariff, use little power in the day and depend on selling at 2.20 baht, so their margin is thin; a cloudy month, a rate rise or an inverter fault can push them below zero. Why the rules are unclear has ordinary explanations (Cabinet approves money first, then regulators write rules; political timing), and the vendor list, once published, will show who benefits.'])]),
  ('people', 'What people say', [('', [
   'We read about 175 public Facebook comments on four widely shared posts: clear worries outnumbered support about six to one. The main worries were debt, distrust of who supplies the equipment, the low 2.20-baht buy-back price and rising installation prices; supporters said it pays for homes that use power in the daytime. Full summary and a reader poll: <a href="/news.html#public-reaction-50000-subsidy">What people on Facebook are saying</a>.'])]),
  ('divide', 'Who carries the costs?', [('', [
   T(['Strand', 'Evidence', 'Grade'], [
    ['Poorer homes sell small amounts on thin margins', '5 kW cap at 2.20 baht; low-use homes clear about 200 baht a month over a loan', 'Supported'],
    ['Water and resources near data centres', 'Farming and fishing communities in Chonburi and Rayong fear for water; 68.8% of surveyed executives name water as their top concern', 'Supported as a risk'],
    ['Living costs rise', 'Home prices up 2–5% near large US data centres; household power bills up about US$16–21 a month in parts of one US grid; not yet measured in Thailand', 'Supported abroad'],
    ['Work without contracts or welfare', 'About 50 direct jobs per 100 MW in Thailand (TDRI); AI data labellers abroad paid about US$0.90–2 an hour, often without health care', 'Supported for AI data work']])])]),
  ('real', 'Agnotology, and being realistic', [('', [
   'A flood of complex detail – panel types, IEC and Thai standards, sizes and scales, the positive published and the negative left out – can leave the public confused enough to give up. Researchers call the deliberate production of confusion <b>agnotology</b>. The answer is not to be negative or positive, but realistic: ask who pays, who gains, for how long, and who checks. There is no free lunch: the 50,000 baht is borrowed public money, the deduction is tax given up, and grid upgrades are paid through tariffs.',
   'RAW:<ul class="check"><li>Is the full rulebook published, with dates?</li><li>Can I choose my own installer, and is the vendor list public?</li><li>What is the loan rate after the promotion, and the penalty if I miss a payment?</li><li>Is the buy-back price fixed, and for how many years?</li><li>Does my daytime use make the numbers work without relying on selling power?</li><li>Who supplies the equipment, and is the warranty in writing?</li></ul>'])]),
  ('books', 'Further reading', [('', [books('en')])]),
 ],
 src_h='Sources', note='This is an analysis by Solar ESS, based on the public sources listed below. Where the evidence is thin we say so. We will update it when the official rules of the 50,000-baht scheme are published.',
 back='All news on the 50,000-baht scheme', backurl='/news.html#topic-subsidy')

TH = dict(
 out='th/electrification-who-pays.html', url='https://solaress.org/th/electrification-who-pays', news='/th/news.html', home='/th/',
 title='การเดินทางสู่ไฟฟ้าของไทย: ใครจ่าย ใครได้? | Solar ESS',
 desc='วิเคราะห์นโยบายพลังงานไทยในยุคดาต้าเซ็นเตอร์ พร้อมระดับหลักฐาน: กฎพลังงานสะอาด ใครขายไฟสีเขียวได้ ลดหย่อนภาษี 200,000 บาท โซลาร์ 50,000 บาท และสิ่งที่ต้องตรวจก่อนเซ็น',
 crumb_home='หน้าแรก', crumb_news='ข่าวสาร', updated='บทวิเคราะห์ · 27 ตุลาคม 2569',
 h1='การเดินทางสู่ไฟฟ้าของไทย:<br>ใครจ่าย<br>ใครได้?',
 lede='ไทยต้องการไฟฟ้าเพิ่มอีกมาก และความต้องการใหม่ส่วนใหญ่มาจากดาต้าเซ็นเตอร์ที่ต้องการไฟสะอาด การเดินทางนี้จะลดหรือเพิ่มช่องว่างระหว่างคนรวยกับคนจน ขึ้นกับกติกาที่ยังเขียนไม่เสร็จ เราให้ระดับหลักฐานกับทุกข้อสรุป เพื่อให้เห็นว่าอะไรรู้แล้ว และอะไรยังเป็นคำถาม',
 kf=[('1,000 kVA', 'ขนาดโรงไฟฟ้าขั้นต่ำที่ขายไฟสีเขียวตรงให้ดาต้าเซ็นเตอร์ได้'), ('2.20 บาท', 'ราคาที่บ้านได้รับต่อหน่วย สูงสุด 5 kW'), ('4.56 บาท', 'ราคาที่บริษัทจ่ายซื้อไฟสีเขียวมีใบรับรอง (UGT2)'), ('0–50,000 บาท', 'ภาษีที่ประหยัดได้จากลดหย่อน 200,000 บาท ตามรายได้')],
 toc='ในหน้านี้',
 sections=[
  ('grades', 'อ่านหน้านี้อย่างไร', [('', [
   'ทุกข้อสรุปมีระดับหลักฐาน <b>มีหลักฐานรองรับ</b>: มีข้อมูลหรือเอกสารทางการ <b>มีหลักฐานบางส่วน</b>: ข้อเท็จจริงมีอยู่ แต่ข้อสรุปเป็นเพียงการตีความหนึ่ง <b>ยังไม่มีหลักฐาน</b>: เป็นคำถามที่ควรถาม แต่ยังไม่มีหลักฐานสาธารณะ ตัวเลข ณ 27 ตุลาคม 2569 ก่อนประกาศหลักเกณฑ์ทางการของโครงการ 50,000 บาท หน้านี้ไม่กล่าวหาบุคคลหรือบริษัทใดว่าทำโดยไม่สุจริต แต่ชี้ว่าควรตรวจสอบที่ใด'])]),
  ('demand', 'ความต้องการไฟที่พุ่งขึ้น และดาต้าเซ็นเตอร์', [('', [
   '<b>มีหลักฐานรองรับ</b> ดาต้าเซ็นเตอร์ทั่วโลกใช้ไฟราว 415 TWh ในปี 2024 หรือราวสองเท่าของการใช้ไฟทั้งประเทศไทย และ IEA คาดว่าจะถึงราว 945 TWh ในปี 2030 ดาต้าเซ็นเตอร์ที่วางแผนในไทย (ราว 2.87 GW) อาจเพิ่มความต้องการไฟราว 10% ของประเทศหากเดินเครื่อง 80% (ประมาณการของเรา) สร้างงานประจำน้อย และแย่งน้ำกับงบปรับปรุงระบบไฟฟ้า รายละเอียด: <a href="/th/data-centre-impacts.html">ดาต้าเซ็นเตอร์: ต้นทุนที่แท้จริงและประโยชน์</a>'])]),
  ('clean', 'ทำไมดาต้าเซ็นเตอร์ต้องการไฟสะอาด', [('', [
   '<b>มีหลักฐานบางส่วน</b> ไทยไม่มีกฎหมายทั่วไปที่บังคับให้ดาต้าเซ็นเตอร์ใช้ไฟสะอาดตามสัดส่วนที่กำหนด ความคาดหวังมาจากสามแหล่ง:',
   T(['แหล่งที่มา', 'สาระสำคัญ'], [
    ['คำมั่นของบริษัท', 'บริษัทคลาวด์รายใหญ่ซื้อไฟหมุนเวียนเท่ากับการใช้ทั้งปี Google ตั้งเป้าใช้ไฟปลอดคาร์บอนทุกชั่วโมงภายในปี 2030 (ปี 2020 ทำได้ราว 65% รายชั่วโมง)'],
    ['เยอรมนี', 'ดาต้าเซ็นเตอร์ 300 kW ขึ้นไป ต้องใช้ไฟหมุนเวียนที่ไม่ได้รับเงินอุดหนุน 50% ตั้งแต่ปี 2024 และ 100% ตั้งแต่ปี 2027'],
    ['ไทย ซื้อขายไฟตรง Direct PPA (ร่าง ต.ค. 2568)', 'ผู้ซื้อ: ดาต้าเซ็นเตอร์ที่ได้ BOI ขนาดอย่างน้อย 50 MW ที่ตั้งใจใช้ไฟหมุนเวียน 100% ผู้ขาย: โรงไฟฟ้าหมุนเวียนใหม่ขนาดอย่างน้อย 1,000 kVA มีรายงานว่าเปิดให้ทุกอุตสาหกรรมเมื่อ ส.ค. 2569'],
    ['ไทย อัตราค่าไฟสีเขียว', 'UGT1 เพิ่มใบรับรองจากเขื่อนพลังน้ำเดิม UGT2 ราว 4.56 บาท/หน่วย 10 ปี จากโครงการโซลาร์ ลม และชีวภาพใหม่']]),
   'เหตุผล: คำมั่นด้านสภาพภูมิอากาศและการรายงานการปล่อยคาร์บอน กฎห่วงโซ่อุปทานของลูกค้า (รวมกฎคาร์บอนของ EU สำหรับผู้ส่งออก) ราคาที่คงที่ระยะยาว และการแข่งขันดึงการลงทุนระหว่างประเทศ ช่องว่างที่ต้องจับตา: ไฟของดาต้าเซ็นเตอร์ทั่วโลกราว 30% ยังมาจากถ่านหิน และรัฐมนตรีพลังงานไทยเคยกล่าวว่าผู้ประกอบการเรียกร้องไฟสะอาด 100% ต่อสาธารณะ แต่มักขอ "ไฟอะไรก็ได้ทันที" เพื่อเริ่มดำเนินการ'])]),
  ('share', 'ส่วนแบ่งที่เป็นธรรม: ใครได้ขายไฟสะอาด?', [('', [
   '<b>มีหลักฐานรองรับเรื่องการเข้าถึง มีหลักฐานบางส่วนเรื่องกำไร</b> กติกาการขายไฟตรงเขียนไว้สำหรับโรงไฟฟ้าขนาดใหญ่ หลังคาบ้านจึงเข้าร่วมไม่ได้ ราคาต่อหน่วยของบ้านกับโซลาร์ฟาร์มใกล้เคียงกัน ความต่างอยู่ที่ขนาดและอายุสัญญา',
   T(['ใคร', 'ราคา (บาท/หน่วย)', 'เงื่อนไข'], [
    ['บ้านขายไฟส่วนเกิน', '2.20', 'ส่งออกไม่เกิน 5 kW 10 ปีตามประกาศ กฟน. ปัจจุบัน (มีรายงาน 20 ปีสำหรับโครงการใหม่)'],
    ['โซลาร์ภาคพื้นดินขนาดใหญ่ขายให้ กฟผ. (โครงการ 2565)', '2.1679', 'ราคากำหนดโดยผู้กำกับ ไม่มีการประมูลราคา 2,368 MW'],
    ['โซลาร์ + แบตเตอรี่ขนาดใหญ่ (โครงการเดียวกัน)', '2.8331', '1,000 MW'],
    ['บ้านซื้อไฟ (เฉลี่ย ก.ย. 2569)', 'ราว 3.89', '200 หน่วยแรกไม่เกิน 3 บาท'],
    ['บริษัทซื้อไฟสีเขียวมีใบรับรอง (UGT2)', 'ราว 4.56', '10 ปี'],
    ['ดาต้าเซ็นเตอร์ซื้อไฟ (อัตราใหม่ ตามรายงาน)', 'ราว 5–6', 'ประเภทผู้ใช้แยก']]),
   'บริษัทจดทะเบียนขนาดใหญ่แห่งหนึ่งลงนามสัญญา 25 ปีกับ กฟผ. สำหรับโซลาร์ 12 โครงการ รวม 644.8 MW ในโครงการปี 2565 ขณะที่บ้านหนึ่งหลังขายได้ไม่เกิน 5 kW เงินก้อนใหญ่จริงอยู่ที่โรงไฟฟ้าฟอสซิล ปี 2568 กำลังผลิตสำรองของไทยอยู่ที่ 34–38% เทียบเกณฑ์ 15% และบางสัญญาเอกชนมีการจ่ายค่าความพร้อมจ่ายแม้ไม่ได้เดินเครื่อง ซึ่ง TDRI ระบุว่าต้นทุนเหล่านี้ส่งผ่านมาที่ค่าไฟ',
   '<b>ระบบที่เป็นธรรมกว่าอาจเป็นอย่างไร:</b> กันส่วนหนึ่งของความต้องการไฟสีเขียวจากดาต้าเซ็นเตอร์ให้บ้านเรือน สหกรณ์ และโซลาร์ชุมชน ให้ผู้รวบรวมรวมหลังคาหลายหลังให้ถึงเกณฑ์ 1,000 kVA เปิดเผยราคาทั้งห่วงโซ่ และให้บ้านเรือนได้สัญญายาวเท่าผู้ผลิตรายใหญ่'])]),
  ('tax', 'ลดหย่อนภาษี 200,000 บาท: ใครได้ประโยชน์?', [('', [
   '<b>มีหลักฐานรองรับ: เอื้อคนรายได้สูง</b> เป็นการลดเงินได้สุทธิ มูลค่าจึงเพิ่มตามขั้นภาษี ประหยัดภาษีราว 6,100–50,000 บาทจากยอดเต็ม 200,000 บาท (SCB EIC) เงื่อนไข: ระบบออนกริดใหม่ไม่เกิน 10 kWp ติดตั้ง 3 มี.ค. 2569 – 31 ธ.ค. 2571 ผู้ใช้สิทธิต้องเป็นเจ้าของมิเตอร์ และมี e-Tax Invoice จากผู้ประกอบการจด VAT',
   T(['ผลกระทบ', 'ใครได้หรือเสีย'], [
    ['ภาษีที่ประหยัดเพิ่มตามรายได้', 'คนรายได้สูงได้มากที่สุด คนที่ไม่ถึงเกณฑ์เสียภาษีไม่ได้อะไร'],
    ['มิเตอร์ต้องเป็นชื่อผู้ใช้สิทธิ', 'ผู้เช่าและครอบครัวที่มิเตอร์เป็นชื่อพ่อแม่ใช้สิทธิไม่ได้'],
    ['เฉพาะผู้ขายที่จด VAT', 'บริษัทในระบบได้ประโยชน์ ช่างท้องถิ่นที่ไม่จด VAT เสียงาน'],
    ['ค่าไฟลด ความต้องการช่วงพีคลด', 'บวกต่อเจ้าของบ้าน และต่อระบบไฟฟ้าเล็กน้อย']]),
   'ผลข้างเคียงที่ต้องจับตา: การเร่งติดตั้งช่วง 2569–2571 ทำให้แผงหมดอายุพร้อมกันขณะที่ระบบรีไซเคิลยังอยู่ในแผน และแรงกดดันจากเส้นตายเปิดช่องให้งานติดตั้งคุณภาพต่ำ'])]),
  ('fifty', 'โครงการ 50,000 บาท: อะไรยังไม่ชัด', [('', [
   '<b>"ไม่ชัดเจน" มีหลักฐานรองรับ "กับดักหนี้ 25 ปี" ยังไม่มีหลักฐานจากเงื่อนไขที่รายงาน "เจตนาแอบแฝง" ยังไม่มีหลักฐาน</b> เงื่อนไขที่มีรายงาน: 50,000 บาทต่อบ้าน 1 ล้านสิทธิ ตัวอย่าง กฟภ. ระบบ 5 kW ราว 140,000 บาท เหลือราว 90,000 บาท สินเชื่อ 2.5% 7 ปี รับซื้อไฟ 2.20 บาท สิ่งที่ยังไม่ชัด: รายชื่อและเกณฑ์ผู้ติดตั้ง ดอกเบี้ยหลังโปรและบทลงโทษเมื่อผิดนัด เงินอุดหนุนจ่ายให้ผู้ติดตั้งหรือเจ้าของบ้าน ระยะรับซื้อไฟ (10 หรือ 20 ปี) ยอด 90,000 บาทจ่ายด้วยอะไร และแบตเตอรี่หรือระบบบนพื้นได้เงื่อนไขเดียวกันหรือไม่',
   '<b>กู้แล้วคุ้มไหม?</b> คำนวณของเรา: กู้ 90,000 บาท 2.5% 7 ปี ≈ 1,169 บาทต่อเดือน ระบบ 5 kW ผลิตราว 600 หน่วยต่อเดือน',
   T(['บ้าน', 'ใช้ไฟต่อเดือน', 'มูลค่าโซลาร์ต่อเดือน', 'เหลือหลังหักค่างวด'], [
    ['ใช้ไฟน้อย (กลางวันครึ่งหนึ่ง 3 บาท/หน่วย)', '150 หน่วย', '≈ 1,380 บาท', '≈ +210 บาท'],
    ['ใช้ไฟปานกลาง (กลางวัน 60% 3.89 บาท)', '400 หน่วย', '≈ 1,730 บาท', '≈ +560 บาท'],
    ['ใช้ไฟกลางวันมาก (70% 4.20 บาท)', '800 หน่วย', '≈ 2,440 บาท', '≈ +1,270 บาท']]),
   'บ้านที่ยากจนที่สุดจ่ายค่าไฟอัตราต่ำสุด ใช้ไฟกลางวันน้อย และพึ่งการขายไฟ 2.20 บาท กำไรจึงบางมาก เดือนที่ฟ้าครึ้ม ดอกเบี้ยขึ้น หรืออินเวอร์เตอร์เสีย อาจทำให้ติดลบ เหตุที่กติกายังไม่ชัดมีคำอธิบายปกติ (ครม. อนุมัติเงินก่อน แล้วผู้กำกับจึงออกกติกา จังหวะทางการเมือง) และรายชื่อผู้ติดตั้งเมื่อประกาศจะบอกได้ว่าใครได้ประโยชน์'])]),
  ('people', 'เสียงประชาชน', [('', [
   'เราอ่านความคิดเห็นสาธารณะบน Facebook ราว 175 ความคิดเห็นใน 4 โพสต์ที่มีคนแชร์มาก ความกังวลมากกว่าความเห็นสนับสนุนราวหกต่อหนึ่ง เรื่องหลักคือหนี้ ความไม่ไว้ใจว่าใครเป็นผู้จัดหาอุปกรณ์ ราคารับซื้อ 2.20 บาทที่ต่ำ และราคาติดตั้งที่อาจขึ้น ฝ่ายสนับสนุนบอกว่าคุ้มสำหรับบ้านที่ใช้ไฟกลางวัน สรุปเต็มและโพลความเห็น: <a href="/th/news.html#public-reaction-50000-subsidy">คนบน Facebook พูดถึงโซลาร์ 50,000 บาทว่าอย่างไร</a>'])]),
  ('divide', 'ใครแบกรับต้นทุน?', [('', [
   T(['ประเด็น', 'หลักฐาน', 'ระดับ'], [
    ['บ้านยากจนขายไฟจำนวนน้อย กำไรบาง', 'ส่งออกได้ 5 kW ที่ 2.20 บาท บ้านใช้ไฟน้อยเหลือราว 200 บาทต่อเดือนหลังหักค่างวด', 'มีหลักฐานรองรับ'],
    ['น้ำและทรัพยากรใกล้ดาต้าเซ็นเตอร์', 'ชุมชนเกษตรและประมงในชลบุรีและระยองกังวลเรื่องน้ำ ผู้บริหาร 68.8% กังวลเรื่องน้ำมากที่สุด', 'มีหลักฐานในฐานะความเสี่ยง'],
    ['ค่าครองชีพสูงขึ้น', 'ราคาบ้านเพิ่ม 2–5% ใกล้ดาต้าเซ็นเตอร์ใหญ่ในสหรัฐฯ ค่าไฟบ้านเพิ่มราว 16–21 ดอลลาร์ต่อเดือนในบางพื้นที่ ยังไม่มีการวัดในไทย', 'มีหลักฐานในต่างประเทศ'],
    ['งานไม่มีสัญญาหรือสวัสดิการ', 'ราว 50 ตำแหน่งต่อ 100 MW ในไทย (TDRI) ผู้ติดป้ายข้อมูล AI ในต่างประเทศได้ราว 0.90–2 ดอลลาร์ต่อชั่วโมง มักไม่มีประกันสุขภาพ', 'มีหลักฐานสำหรับงานข้อมูล AI']])])]),
  ('real', 'Agnotology และการมองตามความจริง', [('', [
   'ข้อมูลซับซ้อนจำนวนมหาศาล ทั้งชนิดแผง มาตรฐาน IEC และ มอก. ขนาดและสเกล เผยแพร่ด้านบวก เก็บด้านลบ อาจทำให้ประชาชนสับสนจนยอมแพ้ นักวิชาการเรียกการสร้างความสับสนโดยเจตนาว่า <b>agnotology</b> ทางออกไม่ใช่มองแง่ลบหรือแง่บวก แต่มองตามความจริง ถามว่าใครจ่าย ใครได้ นานแค่ไหน และใครตรวจสอบ ไม่มีของฟรีในโลก เงิน 50,000 บาทคือเงินกู้สาธารณะ ลดหย่อนภาษีคือรายได้ภาษีที่รัฐสละ และการปรับปรุงระบบไฟฟ้าจ่ายผ่านค่าไฟ',
   'RAW:<ul class="check"><li>หลักเกณฑ์ฉบับเต็มประกาศแล้วหรือยัง มีวันที่ชัดเจนไหม</li><li>เลือกผู้ติดตั้งเองได้ไหม รายชื่อผู้ติดตั้งเปิดเผยหรือไม่</li><li>ดอกเบี้ยหลังโปรเท่าไร ผิดนัดชำระแล้วจะเป็นอย่างไร</li><li>ราคารับซื้อไฟคงที่ไหม กี่ปี</li><li>การใช้ไฟกลางวันของบ้านเราคุ้มโดยไม่ต้องพึ่งการขายไฟหรือไม่</li><li>ใครเป็นผู้จัดหาอุปกรณ์ และมีการรับประกันเป็นลายลักษณ์อักษรไหม</li></ul>'])]),
  ('books', 'หนังสือแนะนำ (ภาษาอังกฤษ)', [('', [books('th')])]),
 ],
 src_h='แหล่งข้อมูล', note='บทวิเคราะห์นี้จัดทำโดยบริษัท โซลาร์ เอสส์ จำกัด จากแหล่งข้อมูลสาธารณะด้านล่าง หากหลักฐานยังไม่พอเราจะบอกตรง ๆ และจะปรับปรุงเมื่อมีประกาศหลักเกณฑ์ทางการของโครงการ 50,000 บาท',
 back='ข่าวโซลาร์ 50,000 บาททั้งหมด', backurl='/th/news.html#topic-subsidy')
