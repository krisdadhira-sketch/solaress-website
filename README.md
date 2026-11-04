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
- Admin password: `MEMBERS_ADMIN_PASSWORD` in Netlify environment variables; if unset, the vocabulary teacher password is used.
