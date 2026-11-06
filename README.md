# Solar ESS website

Static site for www.solaress.org. `index.html` is the home page; `thanks.html` is shown after the consultation form is sent (Netlify Forms).

## Vocabulary tests (/vocabulary)

100 English synonym tests x 20 questions (test 1 easiest, test 100 hardest).
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

Every public page carries the GA4 tag for stream "solaress.org" (`G-46HG0JWSZV`, property "Solar ESS Co. Ltd."), between `<!--ga4-->` markers. **After adding or regenerating any page, run `python3 tools/analytics_tag.py`** (idempotent). Custom events: `book_consultation_click`, `phone_click`, `line_click`, `facebook_click`, `form_sent` (with `form_name`) and `generate_lead` (consultation / installer-request forms). Mark `generate_lead` as a Key event in GA (Admin > Data display > Events).

## Job admin: installer report, customer feedback, payment release & team record (/feedback-admin.html)

1. **Admin issues codes**: every project job post on the Jobs page ends with a small ⚙ Admin icon (`tools/job_links.py`, re-run after editing the Jobs page) → `/feedback-admin.html?job=<job>`. Sign in (same password as members-admin), enter the team, click *Create codes* → two one-time codes: installer and customer. *Copy message* gives a ready LINE message (Thai + English) with the link.
2. **Installer** opens `/job-report.html?c=<code>` (EN/TH) and sends the report (Netlify form `job-report`); `submission-created.mjs` attaches it only for a valid, unused installer code.
3. **Customer** opens `/feedback.html?c=<code>` (EN/TH) and rates once: 10 questions 5 / 4 / 2 / 1 (no middle score) + NPS 0–10, checked by `/api/feedback` (`netlify/functions/feedback/feedback.mjs`).
4. **Release payment**: possible only when both are in; the admin checks both and clicks *Release payment*. Team record = customer feedback on issued jobs only.

Page text: `tools/feedback_page.py`, then `tools/analytics_tag.py`. Data: Blobs store `feedback` (`job/`, `code/`, `fb/`, `file/`).

## Installer test (/installer-test, /certificate.html, /itest-admin.html)

- 5 levels × 25 questions (Thai + English): 1 Solar Enterer, 2 Solar Enthusiast, 3 Solar in Practice, 4 Solar Professional, 5 Solar Expert. Pass = 100% (25/25); only a pass gives a certificate and unlocks the next level. Solar ESS accepts installation work from Level 3.
- Level 1 is open to anyone. Levels 2–5 need a TSIA or installer-partner registration (individual, team or company) with the same phone (members store, any status except rejected/hidden), plus the level below passed.
- Name, phone, email and company/team are required (checked on the page and in the API).
- Questions: `tools/itest/questions_a.py`, `questions_bcd.py` (levels 1–4, assigned in `build_bank.py`), `questions_brands.py` (brand questions in levels 2–3), `questions_e.py` (level 5 fault cases) → `python3 tools/itest/build_bank.py` → `netlify/functions/itest/bank.json` (answer key stays server-side).
- Pages: `python3 tools/itest/page.py`, `python3 tools/itest/cert_page.py`, `python3 tools/test_menu.py` (the "Solar Test" nav dropdown on every page), then `tools/analytics_tag.py`.
- API `netlify/functions/itest/itest.mjs` at `/api/itest`: `status`, `start`, `submit`, `cert` (public); `list`, `attempt`, `delete` (admin). Blobs store `itest`: `att/<id>`, `cert/<SESS-Ln-XXXXXXXX>`.
- Certificate: `/certificate.html?id=…`, A4 landscape, metal tier per level (Bronze, Silver, Gold, Platinum, Diamond), QR to the verify link; Level 3+ shows "Accepted for Solar ESS installation work". No phone number is shown.
- Results: **/itest-admin.html** (same admin password): filter by level, certificate numbers, wrong answers with the key and explanation, CSV.
