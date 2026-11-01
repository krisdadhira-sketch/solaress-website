# Solar ESS website

Static site for www.solaress.org. `index.html` is the home page; `thanks.html` is shown after the consultation form is sent (Netlify Forms).

## Vocabulary tests (/vocabulary)

100 English synonym tests x 20 questions (test 1 easiest, test 100 hardest).
- Pages: `vocabulary.html` (students: register, log in, take tests, see scores) and `vocab-admin.html` (teacher dashboard, noindex). Both are built from `tools/vocab/*.html` with `python3 tools/vocab_page.py`.
- Backend: `netlify/functions/vocab/vocab.mjs` at `/api/vocab`. Accounts, attempts and scores are stored in Netlify Blobs (store `vocab`). The answer key is `netlify/functions/vocab/bank.json` and is only sent to students after they submit.
- Email: every finished test is also posted to the Netlify form `vocab-results`. Add a form notification for that form in Netlify (Forms > Form notifications > Email) to receive results by email.
- Teacher password: set `VOCAB_ADMIN_PASSWORD` in Netlify environment variables to change it.
