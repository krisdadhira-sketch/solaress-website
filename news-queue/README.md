# News queue (nightly publishing)

Branch `news-queue` only. Every Solar ESS news PDF made during the day is added here with an entry in `queue.json`
(pdf, publish_on YYYY-MM-DD Asia/Bangkok, id, topics, eyebrow, title, lede, bullets, thailand_note, sources).

At 23:00 Asia/Bangkok a scheduled task publishes every entry with publish_on <= today to `main`:
EN article in news.html, Thai article in th/news.html (newest first, same style as existing articles, sources credited),
PDF copied to downloads/ and linked, tools/build_share.py run, one commit + push = one Netlify deploy.
Published entries are then removed from this queue.
