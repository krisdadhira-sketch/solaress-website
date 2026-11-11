# Solar ESS website

Static site for www.solaress.org. `index.html` is the home page; `thanks.html` is shown after the consultation form is sent (Netlify Forms).

## Vocabulary tests (/vocabulary)

100 English synonym tests x 20 questions (test 1 easiest, test 100 hardest), plus 10 solar electrical vocabulary tests (S1–S10, stored as tests 101–110): terms in `tools/vocab/solar_terms.py`, build with `python3 tools/vocab/build_solar.py`. Direct link: www.solaress.org/vocabulary.html?track=solar (the tests are no longer in the menu).
- Pages: `vocabulary.html` (students: register, log in, take tests, see scores) and `vocab-admin.html` (teacher dashboard, noindex). Both are built from `tools/vocab/*.html` with `python3 tools/vocab_page.py`.
- Backend: `netlify/functions/vocab/vocab.mjs` at `/api/vocab`. Accounts, attempts and scores are stored in Netlify Blobs (store `vocab`). The answer key is `netlify/functions/vocab/bank.json` and is only sent to students after they submit.
- Email: every finished test is also posted to the Netlify form `vocab-results`. Add a form notification for that form in Netlify (Forms > Form notifications > Email) to receive results by email.
- Teacher password: set `VOCAB_ADMIN_PASSWORD` in Netlify environment variables to change it.

## Installer partners (/partners, /th/partners)

Regional directory of approved subcontract installers, a registration form (`installer-partner`) and a job-request form (`installer-request`), both Netlify Forms.
- Directory data: `data/installer-partners.json` (public file: never put phone, email, LINE, address or ID numbers in it). Add one object per approved registration; `_example` shows the fields. Photos go in `images/partners/`.
- Page text and forms: edit `tools/partners_page.py`, then run `python3 tools/partners_page.py`. Card rendering: `partners.js`.
- Add form notifications for `installer-partner` and `installer-request` in Netlify (Forms > Form notifications > Email) to get each submission by email.

## TSIA members & installer partners: review and publish (/members-admin.html)

- Every TSIA membership (`tsia-membership`) and installer-partner (`installer-partner`) submission is saved as *pending* by `netlify/functions/submission-created.mjs` (Netlify Blobs store `members`); uploaded photos are copied at the same time.
- Review at **/members-admin.html** (noindex). Approve → the profile appears at once on /team.html#network (TSIA, via `tsia.js`) or /partners.html (via `partners.js`). Reject, hide or move back to review at any time.
- Public API `/api/members?a=public&type=tsia|partner` returns only public fields; phone, email, LINE, address, tax/ID numbers and documents are never returned.
- Delete: a rejected or hidden entry can be removed for good with "Delete permanently" (click twice); its photos are deleted too. Published or waiting entries cannot be deleted.
- Admin password: `MEMBERS_ADMIN_PASSWORD` in Netlify environment variables; if unset, the vocabulary teacher password is used.

## Google Analytics (GA4)

Every public page carries the GA4 tag for stream "solaress.org" (`G-46HG0JWSZV`, property "Solar ESS Co. Ltd."), between `<!--ga4-->` markers. **After adding or regenerating any page, run `python3 tools/analytics_tag.py`** (idempotent), then `python3 tools/form_ink.py` (white form boxes with black text on every page that has a form). Custom events: `book_consultation_click`, `phone_click`, `line_click`, `facebook_click`, `form_sent` (with `form_name`) and `generate_lead` (consultation / installer-request forms). Mark `generate_lead` as a Key event in GA (Admin > Data display > Events).

## Job admin: installer report, customer feedback, payment release & team record (/feedback-admin.html)

1. **Admin issues codes**: every project job post on the Jobs page ends with a small ⚙ Admin icon (`tools/job_links.py`, re-run after editing the Jobs page) → `/feedback-admin.html?job=<job>`. Sign in (same password as members-admin), enter the team, click *Create codes* → two one-time codes: installer and customer. *Copy message* gives a ready LINE message (Thai + English) with the link.
2. **Installer** opens `/job-report.html?c=<code>` (EN/TH) and sends the report (Netlify form `job-report`); `submission-created.mjs` attaches it only for a valid, unused installer code.
3. **Customer** opens `/feedback.html?c=<code>` (EN/TH) and rates once: 10 questions 5 / 4 / 2 / 1 (no middle score) + NPS 0–10, checked by `/api/feedback` (`netlify/functions/feedback/feedback.mjs`).
4. **Release payment**: possible only when both are in; the admin checks both and clicks *Release payment*. Team record = customer feedback on issued jobs only.

Post status from the ⚙ Admin icon: Open for quotes, On hold (waiting for customer confirmation: amber badge, no Apply button), Close (grey), Hide. Page text: `tools/feedback_page.py`, then `tools/analytics_tag.py`. Data: Blobs store `feedback` (`job/`, `code/`, `fb/`, `file/`).

## TSIA and Installer Partners (one category)

- Every Installer Partner is a TSIA member. TSIA has two kinds of member: Installer Partner (individual, team or company; form `installer-partner` on /partners.html, which now says it is a TSIA application and carries `joins-tsia=yes`) and company member (form `tsia-membership` on /team.html#join-tsia).
- `/api/members?a=public&type=tsia` lists approved company members and approved partners (`category`), shown by `tsia.js` on the team page.
- `python3 tools/tsia_partner.py` (run after `tools/job_links.py` and `tools/partners_page.py`): "Two ways to join TSIA" box on the team pages, Solar Test button texts, the single "TSIA & Partners" menu item (no separate partners link), the "Who is TSIA, and who can be a partner?" block (domestic / global partners) and the partner-type select on the TSIA form.

## Admin hub (/admin)

- **www.solaress.org/admin**: one sign-in (MEMBERS_ADMIN_PASSWORD) with a menu: Jobs & payment release, TSIA & partner applications, Installer test & certificates, Vocabulary test results, plus links to public pages. Overview shows counts.
- Each admin page opens inside the hub without asking again (shared sessionStorage `members-admin-pw`); opened on its own it shows an "Admin home" button.
- Build: `python3 tools/admin_hub.py` (also re-adds the bridge script to the 4 admin pages; run it after `tools/vocab_page.py`). The vocabulary API also accepts the main admin password.

## Installer test (/installer-test, /certificate.html, /itest-admin.html)

- 5 levels × 25 questions (Thai + English): 1 Solar Enterer, 2 Solar Enthusiast, 3 Solar in Practice, 4 Solar Professional, 5 Solar Expert. Pass = 100% (25/25); only a pass gives a certificate and unlocks the next level. Solar ESS accepts installation work from Level 3.
- Time limit (Nov 2026): Levels 1–2 and brand/product tests 10 min, Level 3 12 min, Levels 4–5 15 min (`LEVEL_MINUTES` / `PRODUCT_MINUTES` in `itest.mjs`; sent to the page as `limit` and per level as `minutes`). The page shows a countdown and auto-submits when time runs out; only answers given in time are scored. A submission arriving more than 2 minutes after the limit (`GRACE_MS`) is scored 0 and marked `late` in the attempt.
- Open to everyone (Nov 2026): any level can be taken without registration and the score is shown at once; only name and phone are required (email, team and province optional). A certificate number is issued only for 100%. Opening or downloading the certificate needs a TSIA or installer-partner registration with the same phone (any status except rejected/hidden). One click from the result or the certificate link opens **/join.html** (`tools/itest/join_page.py`): type, name, phone, province and certificate number; `/api/itest?a=register` checks the certificate belongs to that phone, saves a pending Installer Partner registration (members store) and the certificate opens at once. Kris still approves profiles before they are published. Certificates issued before this change stay open.
- Every start shuffles question and answer order (server session `ses/<id>`, valid 3 h). After an attempt the same phone or email waits 30 days for that level. Certificates are valid 1 year; an expired level can be renewed, and any pass counts as the prerequisite.
- Datasheet and site-measurement questions: `tools/itest/questions_ds.py` (levels 2–4).
- Questions: `tools/itest/questions_a.py`, `questions_bcd.py` (levels 1–4, assigned in `build_bank.py`), `questions_brands.py` (brand questions in levels 2–3; brand-specific sets such as `SIGENERGY` and `ENPHASE` are kept out of the levels), `questions_e.py` (level 5 fault cases) → `python3 tools/itest/build_bank.py` → `netlify/functions/itest/bank.json` (answer key stays server-side).
- Pages: `python3 tools/itest/page.py`, `python3 tools/itest/cert_page.py`, `python3 tools/test_menu.py` (Solar Test levels 1–5 + vocabulary test at the end of the Solar ESS dropdown on every page), then `tools/analytics_tag.py`.
- API `netlify/functions/itest/itest.mjs` at `/api/itest`: `status`, `start`, `submit`, `cert` (public); `list`, `attempt`, `delete` (admin). Blobs store `itest`: `att/<id>`, `cert/<SESS-Ln-XXXXXXXX>`.
- Certificate: `/certificate.html?id=…`, A4 landscape, metal tier per level (Bronze, Silver, Gold, Platinum, Diamond), QR to the verify link; Level 3+ shows "Accepted for Solar ESS installation work". No phone number is shown.
- Results: **/itest-admin.html** (same admin password): filter by level, certificate numbers, wrong answers with the key and explanation, CSV.

## Job search (/job.html, /th/job.html)

Search box under the region chips of Project Based Jobs: province / district / place (English or Thai, on either page) + "Type of work" (electrical, solar installation, PV cleaning & O&M, repair, civil & structure, supply). Built by `python3 tools/job_search.py`: it tags each project card with `data-work` (keyword rules in the script) and `data-q` (location in both languages). **Re-run it after adding or editing jobs.** Links can pre-fill it: `/job.html?q=Hat%20Yai&type=cleaning`.

## Projects menu, Solar Package and Preventive Maintenance (Nov 2026)

- Projects dropdown (all pages, EN/TH/ZH): Solar Package (Quotation indented), EV Charger, Preventive Maintenance, Consultation (FAQ indented), Solar ESS Care. Set by `python3 tools/projects_menu.py` (idempotent).
- Pages `package.html`, `maintenance.html` (+ `th/`) are built by `python3 tools/service_pages.py` from the quotation page shell. No prices on them (sent on request). After building: `tools/projects_menu.py`, then `tools/analytics_tag.py`.

## All Risks insurance (profile + menu badge)

`python3 tools/insurance.py` (idempotent): profile pages (EN/TH/ZH) get the "Insured · All Risks cover" section (`#insurance`, EAR open cover, Dhipaya Insurance, 16 Oct 2026 – 16 Oct 2027); every page gets a blinking shield on the top "Solar ESS" menu link and an "All Risks Insured" dropdown item. Never publish the policy PDF or policy number (certificate furnished on request). Update the policy period in the script at renewal.


## Solar Enthusiast community (/community.html, /th/community.html)
- Built by `python3 tools/community_page.py` (then `python3 tools/form_ink.py`), using members.html as the page shell.
- Anyone registers free (`/api/members?a=enthusiast`, saved as type "enthusiast", status pending).
- Approve members in /members-admin.html, tab "Solar Enthusiasts". Approved members then get the member price-list password from Solar ESS (by LINE or phone).
- Approved members ask questions (`a=ask`, matched by phone). Questions appear in the admin tab "Questions"; write the answer and click "Save & publish". Only answered + published questions show on the page (`a=qa`), with the member's first name and province only.

## Site search (home pages) and reader NPS (Nov 2026)

- **Search box** in the hero of `/`, `/th/`, `/zh/` (`js/site-search.js`): searches every public page, each section/card with an id and heading (news, jobs, technical notes, FAQ…) and every linked PDF. Own language first; if nothing is found, the other languages. `?q=` pre-fills it, e.g. `/?q=battery`. GA event `search`.
- Index: `data/search-en.json`, `search-th.json`, `search-zh.json`, built by **`python3 tools/site_search.py`**. Pages with `noindex` are left out. **Re-run it after adding or editing any page or job**, or new content will not be found.
- **Reader NPS** band above the footer of the three home pages (`js/nps-widget.js`): "How likely are you to recommend Solar ESS…?" 1–10 + optional reason. One score per IP per calendar month (Bangkok time); the IP is stored only as a salted hash. API `netlify/functions/nps/nps.mjs` at `/api/nps`, Blobs store `nps`. GA event `nps_score`.
- Results: **/nps-admin.html** (also in the admin hub as "Reader NPS"): NPS = % promoters (9–10) − % detractors (1–6), by month, comments, delete, CSV.
- Markup and texts (EN/TH/ZH): `python3 tools/home_search_nps.py` (idempotent), then `tools/site_search.py`.
- **NPS on almost every page** (Nov 2026): `python3 tools/nps_everywhere.py` (idempotent) puts the same band above the footer of every public page except home pages, admin/noindex pages, share redirects, the timed tests and one-step forms (list in `SKIP`). Re-run after adding pages.
- **Blinking score on the home pages**: badge `#npsscore` under the hero search (`js/nps-score.js`) shows NPS for the last 12 months from the public `GET /api/nps?a=score` (CDN-cached 5 min), with the average and number of ratings; it links to the rating band.

## Accessibility and reach (Nov 2026)

`python3 tools/accessibility.py` (idempotent; **re-run after adding or regenerating any page**) adds to every page:
- a "Skip to content" link and a `<main id="main">` landmark; clearer keyboard focus; "reduce motion" respected;
- WCAG AA contrast fixes. The site accent is now violet-blue **#5B5BD6** (the red-pink #FF2D55 was replaced everywhere, including in `tools/`); on dark bands accent text uses #A5B4FC (CSS + a runtime check in `js/a11y.js`). LINE / WhatsApp / Facebook buttons use darker brand shades so white text is readable;
- `js/a11y.js`: **🌐 More languages** in the language switcher (Google machine translation of the same page: Lao, Burmese, Khmer, Vietnamese, Malay, Indonesian, Japanese, Korean, Hindi, French, German, Spanish, Russian, Arabic), and a one-time suggestion bar offering the visitor's own language (EN / TH / 中文) when that version exists.
Audit: axe-core (WCAG 2 A/AA) on 14 key pages went from about 2,400 contrast failures to 40 (the remaining ones are the deliberately faded "job closed" cards).

## Jobs apply form: job picker and job proposal (Nov 2026)

`python3 tools/job_apply_box.py` (idempotent) on `/job.html` and `/th/job.html`, script `js/job-apply.js`:
- **Job picker**: filter box + list built live from the open job posts on the page (closed jobs left out, on-hold jobs shown but not selectable), grouped Project jobs / Permanent roles / Open application, with a count of open jobs. The chosen job's title, location and a link back to the post are shown; hidden field `job-id` = post id. "Quote for this job →" buttons pre-select it. New job posts appear in the list automatically.
- **Job proposal** box (project jobs only; hidden and not required for permanent roles): `price-labour-only`, `price-labour-materials`, `proposal`, `start-date`, `days-needed`. Hidden `quoted-price` is filled on submit ("Labour only: … / Labour + materials: …") so the inbox keeps working.

## Ongoing projects page (Nov 2026)

`python3 tools/ongoing_page.py` builds `/ongoing.html` and `/th/ongoing.html` (project overview from the News article `#upcoming-projects-nov2026` + the My Park CAR section, whose original is kept in `data/ongoing-mypark-{en,th}.html`). It puts "Ongoing Projects" first in the **News** dropdown on every page (EN/TH/ZH), removes it from the Solar ESS dropdown, repoints links to `profile#ongoing`, leaves a short pointer band on the profile page and adds the pages to `sitemap.xml`. To update the projects, edit the News article, then re-run it.

## Free System Check (Nov 2026)

- `/system-check.html`, `/th/system-check.html`: free remote check for any solar system (any brand, any installer). Netlify form `system-check` (name, phone, LINE, province, kWp, inverter brand, monitoring app, battery, installer, concern, 3 optional screenshots, optional monitoring access, consent); copied to the admin inbox as "Free system check". Reply target: within 3 working days.
- Green "FREE" promo band under the hero of `/` and `/th/`; first item of the Services menu (EN/TH/ZH).
- Build: `python3 tools/system_check_page.py` (then the post-processors listed in its docstring).

## Homeowner test: Self-Appointed Electrician (Nov 2026)

- Test 19, key `home-electrician` (`tools/itest/questions_home.py`, 15 questions, section H "Home electrics for owners"), group "Homeowner Test", 10 minutes, certificate at 100%. Shown first on the test page under "For homeowners". Direct link: `/th/installer-test.html?test=home-electrician`.
- Rule (Nov 2026): every new test question is based on what solaress.org already publishes (FAQ, Our Picks, service pages, Technical notes); each explanation names the page it comes from.

## More topic tests (Nov 2026)

- Tests 20–25 (`tools/itest/questions_protect.py`), all from solaress.org content: 20 RCBO & Earth Leakage (10), 21 MCCB & Main Boards (10), 22 One-way or Two-way breakers (8), 23 Cable Sizing (10), 24 AC Cable (8), 25 Solar Issues & Troubleshooting (15).
- Display order = `PRODUCTS` in `questions_products.py`; the page groups product tests under Troubleshooting, Inverters, Solar panels, Battery, Breakers & protection, Cables. Build/shuffle order is fixed (`LEGACY` in `build_bank.py`) so existing tests never change when tests are added or reordered.

## Jobs page order (Nov 2026)

- Newest job first, closed jobs last, in both lists of `job.html` and `th/job.html`. Every card has `data-posted="YYYY-MM-DD"` (first published) shown as "Posted 9 Nov 2026" / "ลงประกาศ 9 พ.ย. 2569" in its kind line.
- When adding a job: give the new `<article>` a `data-posted` with today's date, then run `python3 tools/job_order.py` (idempotent), then `tools/build_share.py`.

## Job application: candidate information and score (Nov 2026)

- Every job application (`job-application`, /job.html#apply and /th/job.html#apply) asks for 4 parts: 1) personal information (name and last name, contact address, phone, ID card upload, company name), 2) numbers (age, years of experience in this job, largest project value, 3-year project value), 3) certificates (academic/institute and product, name required, file optional), 4) references (a person and a company), plus a PDPA consent box. Form text: `tools/job_candidate_form.py` (idempotent; run after `tools/job_apply_box.py`, then `tools/form_ink.py` and `tools/accessibility.py`).
- `jobScore()` in `netlify/functions/submission-created.mjs` adds `candidate-score` (out of 100) and `score-breakdown` to each application in the inbox: experience 30, largest project 25, 3-year value 10, academic 15, product 10, references 10. Age is an eligibility check only (18+). ≥ 60 with ID card, address and company = "Qualified – send contract"; 40–59 = Review. The score shows as a coloured ★ badge in /inbox-admin.html.
- ID cards and personal details stay in the private inbox (Blobs store `inbox`) and are never published.

## Services menu: free offers (Nov 2026)

Services dropdown order: Free System Check, Free Consultation, Free Quotation, Free Plant Design, then Solar Package, Quotation, EV Charger, Preventive Maintenance, FAQ, Solar ESS Care (`tools/projects_menu.py`). The three new free items open the home-page consultation form at `/?free=consultation|quotation|design#consult`; `tools/consult_free.py` adds the "What would you like?" select (`free_service`) and preselects it from `?free=`.

## Installer hiring contract (/contract.html, /th/contract.html)

Read-only pages of the contract every selected installer signs; no download. The PDF is sent by Solar ESS only after the price is agreed (master copy: Claude Docs "Installer Hiring Contract – Solar ESS", English and Thai tabs). Text in `tools/contract/en.md` and `th.md`; build with `python3 tools/contract_page.py`. Linked from the Jobs page apply box.

## Free System Check example report (Nov 2026)

The Free System Check pages show a real, anonymised report (6.48 kWp hybrid + 16 kWh battery, eastern Bangkok) before the request form: `python3 tools/system_check_example.py`. PDFs in `downloads/Solar-ESS-Free-System-Check-Example-Report*_Rev03_WM_20261111.pdf` (watermarked, no customer name or address), previews `images/system-check-example*.jpg`.

## Candidate ranking (/candidates-admin.html, Nov 2026)

- The job application form is mostly numbers and tick boxes (`tools/job_candidate_form.py`): installs in 3 years, largest kWp, team size, Work-at-Height workers, electrical licence, Solar ESS test level, distance to site, job types done (`jt-*`), tools owned (`tl-*`), own insurance, plus the 4 required parts (personal info, numbers, certificates, references).
- `netlify/functions/candidates/score.mjs`: candidate score 0–100 (`jobScore`, weights in `MAX`) and per-job ranking (`rankJob`): 80% candidate score + 20% price (cheapest labour-only price for that job = 100) + optional AI adjustment −5…+5. Tiers: Top pick (top 3, rank ≥ 55, ID/address/company present), Still in the running (rank ≥ 40, or top 5 with ≥ 30), Not now.
- `/api/candidates` (admin password): `list` groups job applications from the inbox by job and ranks them; `set` marks contacted/declined; `ai` asks Claude to read up to 8 new written proposals (needs `ANTHROPIC_API_KEY` in Netlify; model `CANDIDATES_AI_MODEL`, default claude-haiku-5-5).
- Admin page **/candidates-admin.html** (also in /admin): opens on "Top picks only"; Call / Contacted / Decline buttons per candidate.

## Free Plant Design (/design.html, /th/design.html, Nov 2026)

Services > Free Plant Design now opens its own page: real design drawings (equipment frame front/rear, ground-mount section, array layout, screw piles, corner detail) with a short description each, the 4 steps, and a button to the consultation form with "Free Plant Design" preselected (`/?free=design#consult`). Build: `python3 tools/plant_design_page.py` (watermarks originals placed in `tools/design_src/1..6.jpg` into `images/design-*_Rev01_20261111.jpg`), then the post-processors in its docstring.

## Sample documents, EV drawings and maintenance photos (11 Nov 2026)

- `python3 tools/clean_quote_pdf.py IN.pdf OUT.pdf --name "hide=replace" [--noprice]`: removes prices (2-decimal amounts, per-watt/metre rates, "N บาท" on price lines), names given with `--name`, fixes the old Krabi address (761 → 140/2), adds the Solar ESS watermark and a "sample" note. Savings, payback and the PEA 2.20 THB rate stay.
- `python3 tools/sample_docs_nov11.py`: quotation pages (EN/TH) get the 16.9 kWp + 32 kWh proposal and the general 10 kW / 16 kWh package at the top (`<!--q1111-->`); EV pages get "Samples and drawings" (`<!--evdocs-->`): EV 2nd circuit Option A/B (Thai Rev02), and SLD + construction plan for four DC charging stations (site names generalised).
- `python3 tools/maintenance_photos.py`: "On site" photo band (cleaning, torque checks) on the Preventive Maintenance pages (`<!--mphotos-->`).
