# Complicated World video page

`critics.html`, `th/critics.html` and `zh/critics.html` list every video from the YouTube channel
โลกที่ซับซ้อน โดย ประสาท มีแต้ม, each with a short summary (EN / TH / ZH).

- `meta.txt` — one line per video: `videoId|date (Thai short month)|duration|Thai title`, newest first.
- `sum_*.json` — summaries per video: `title_en`, `title_zh`, `topic`, `sum_en`, `sum_th`, `sum_zh`.
- `build.py` — rewrites the video section of the three pages from these files: `python3 tools/critics/build.py`

To add a new video: add its line at the top of `meta.txt`, add its summary object to a `sum_*.json` file, run `build.py`, commit.
Topics: solar, prices, lng, climate, ev, governance.
