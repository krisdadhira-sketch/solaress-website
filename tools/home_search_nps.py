# -*- coding: utf-8 -*-
"""Home pages (EN /, TH /th/, ZH /zh/): site search box in the hero and the reader NPS band above the footer.
Idempotent (markup between <!--sitesearch--> and <!--nps--> markers). Scripts: /js/site-search.js, /js/nps-widget.js.
Run from the repo root:  python3 tools/home_search_nps.py   (then python3 tools/site_search.py for the index)"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

T = {
    "en": dict(
        label="Search solaress.org", ph="Search anything: jobs, battery, Hat Yai, 50,000 subsidy…", go="Search",
        js=dict(none="Nothing found. Try another word, or ask us on LINE: solaress1.", other="Nothing in English; results in other languages:",
                loading="Loading…", err="Search is not available right now."),
        eyebrow="Your opinion", h="How likely are you to recommend Solar ESS to a friend or colleague?",
        lo="1 = Not at all likely", hi="10 = Extremely likely", why="What is the main reason for your score? (optional)",
        send="Send my score", note="One score per month from each internet connection. Your IP address is never stored.",
        sc=dict(lbl="Reader score (NPS)", of="average {avg}/10 · {n} ratings in the last 12 months", none="No ratings yet: be the first to rate us", rate="Rate us"),
        njs=dict(thanks="Thank you! Your score has been recorded.", done="You have already given us a score this month. Thank you, and see you again next month.",
                 err="Sorry, it could not be sent. Please try again.", sending="Sending…")),
    "th": dict(
        label="ค้นหาในเว็บไซต์ solaress.org", ph="ค้นหาได้ทุกอย่าง: งาน, แบตเตอรี่, หาดใหญ่, เงินอุดหนุน 50,000…", go="ค้นหา",
        js=dict(none="ไม่พบผลลัพธ์ ลองคำอื่น หรือสอบถามทาง LINE: solaress1", other="ไม่พบในภาษาไทย ผลลัพธ์จากภาษาอื่น:",
                loading="กำลังโหลด…", err="ระบบค้นหาไม่พร้อมใช้งานในขณะนี้"),
        eyebrow="ความคิดเห็นของคุณ", h="คุณมีแนวโน้มจะแนะนำ Solar ESS ให้เพื่อนหรือเพื่อนร่วมงานมากน้อยเพียงใด?",
        lo="1 = ไม่แนะนำเลย", hi="10 = แนะนำอย่างยิ่ง", why="เหตุผลหลักที่ให้คะแนนนี้ (ไม่บังคับ)",
        send="ส่งคะแนน", note="ให้คะแนนได้เดือนละ 1 ครั้งต่อการเชื่อมต่ออินเทอร์เน็ต เราไม่เก็บที่อยู่ IP ของคุณ",
        sc=dict(lbl="คะแนนความพึงพอใจจากผู้อ่าน (NPS)", of="เฉลี่ย {avg}/10 · จาก {n} คะแนน ใน 12 เดือนล่าสุด", none="ยังไม่มีคะแนน ร่วมให้คะแนนเป็นคนแรก", rate="ให้คะแนนเรา"),
        njs=dict(thanks="ขอบคุณครับ บันทึกคะแนนของคุณเรียบร้อยแล้ว", done="คุณให้คะแนนเราแล้วในเดือนนี้ ขอบคุณครับ แล้วพบกันใหม่เดือนหน้า",
                 err="ขออภัย ส่งไม่สำเร็จ กรุณาลองอีกครั้ง", sending="กำลังส่ง…")),
    "zh": dict(
        label="站内搜索 solaress.org", ph="搜索任何内容：工作、电池、合艾、补贴…", go="搜索",
        js=dict(none="没有找到结果。请换一个词，或通过 LINE 联系我们：solaress1。", other="中文页面没有结果；其他语言的结果：",
                loading="加载中…", err="搜索暂时不可用。"),
        eyebrow="您的意见", h="您有多大可能向朋友或同事推荐 Solar ESS？",
        lo="1 = 完全不可能", hi="10 = 非常可能", why="您给出这个分数的主要原因是什么？（选填）",
        send="提交评分", note="每个网络连接每月只能评分一次。我们不会保存您的 IP 地址。",
        sc=dict(lbl="读者推荐指数 (NPS)", of="平均 {avg}/10 · 最近 12 个月 {n} 个评分", none="暂无评分，欢迎成为第一位评分者", rate="为我们评分"),
        njs=dict(thanks="谢谢！您的评分已记录。", done="您本月已经评过分了。谢谢，下个月再见。",
                 err="抱歉，提交失败，请重试。", sending="提交中…")),
}

CSS = """<style id="ss-css">
#sitesearch{margin-top:30px;max-width:720px}
#sitesearch label{display:block;font-family:var(--mono);font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:#C7D2FE;margin-bottom:8px}
#sitesearch .ss-f{display:flex;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 10px 30px rgba(0,0,0,.28)}
#sitesearch input{flex:1;min-width:0;border:0;padding:15px 16px;font:inherit;font-size:16px;color:#0A0E2E!important;-webkit-text-fill-color:#0A0E2E!important;background:#fff!important;outline:0}
#sitesearch input::placeholder{color:#6B7280!important;-webkit-text-fill-color:#6B7280!important}
#sitesearch .ss-f:focus-within{outline:3px solid #818CF8;outline-offset:2px}
#sitesearch .ss-go{border:0;background:#4338CA;color:#fff;padding:0 20px;font-family:var(--mono);font-size:13px;letter-spacing:.08em;text-transform:uppercase;cursor:pointer;display:flex;align-items:center;gap:8px}
#sitesearch .ss-go:hover{background:#2563EB}
#sitesearch .ss-res{margin-top:10px;background:#fff;color:#0A0E2E;border-radius:12px;max-height:440px;overflow:auto;box-shadow:0 10px 30px rgba(0,0,0,.28)}
#sitesearch .ss-it{display:grid;gap:3px;padding:12px 16px;border-bottom:1px solid #DEE3ED;text-decoration:none;color:#0A0E2E}
#sitesearch .ss-it:hover,#sitesearch .ss-it:focus{background:#EEF2FF;outline:0}
#sitesearch .ss-it b{font-size:15px;color:#0A1230;line-height:1.35}
#sitesearch .ss-it span{font-size:13.5px;color:#3E548E;line-height:1.45}
#sitesearch .ss-it em{font-style:normal;font-family:var(--mono);font-size:11px;color:#4338CA;word-break:break-all}
#sitesearch mark{background:#E0E7FF;color:#1E1B4B;padding:0 1px;border-radius:2px}
#sitesearch .ss-k{display:inline-block;font-family:var(--mono);font-size:10px;letter-spacing:.08em;background:#0A1230;color:#fff;border-radius:4px;padding:1px 5px;margin-right:7px;vertical-align:2px}
#sitesearch .ss-none,#sitesearch .ss-note{margin:0;padding:12px 16px;font-size:14px;color:#3E548E}
#sitesearch .ss-note{border-bottom:1px solid #DEE3ED;font-size:12.5px}
</style>"""

NCSS = """<style id="nps-css">
#npsscore{display:inline-flex;align-items:center;gap:12px;margin-top:22px;padding:10px 18px 10px 14px;border-radius:999px;background:rgba(255,255,255,.08);border:1.5px solid rgba(255,255,255,.28);color:#fff;text-decoration:none;max-width:100%}
#npsscore:hover{background:rgba(255,255,255,.16)}
#npsscore .ns-num{font:800 30px/1 var(--display);letter-spacing:-.02em;min-width:2.2ch;text-align:center;animation:nsblink 1.2s ease-in-out infinite}
#npsscore.good .ns-num{color:#4ADE80}#npsscore.mid .ns-num{color:#FACC15}#npsscore.low .ns-num{color:#F87171}
#npsscore .ns-dot{width:10px;height:10px;border-radius:50%;background:#4ADE80;box-shadow:0 0 0 0 rgba(74,222,128,.7);animation:nspulse 1.6s infinite}
#npsscore .ns-t{display:grid;gap:2px;line-height:1.25}#npsscore .ns-t b{font-size:14px}#npsscore .ns-t small{font-size:12.5px;color:#C7D2FE}
@keyframes nsblink{0%,100%{opacity:1}50%{opacity:.25}}@keyframes nspulse{70%{box-shadow:0 0 0 10px rgba(74,222,128,0)}100%{box-shadow:0 0 0 0 rgba(74,222,128,0)}}
#nps{background:linear-gradient(135deg,#0A1230 0%,#1E1B4B 60%,#312E81 100%);color:#fff}
#nps .wrap{max-width:900px}
#nps h2{font-size:clamp(24px,3.4vw,38px);color:#fff}
#nps .eyebrow{color:#A5B4FC}
#npsbox{margin-top:26px}
.nps-s{display:grid;grid-template-columns:repeat(10,minmax(0,1fr));gap:8px}
.nps-s button{font:700 18px var(--display);height:52px;border-radius:10px;border:1.5px solid rgba(255,255,255,.35);background:rgba(255,255,255,.06);color:#fff;cursor:pointer;transition:background .15s,transform .15s}
.nps-s button:hover{background:rgba(255,255,255,.16);transform:translateY(-2px)}
.nps-s button[aria-pressed=true]{background:#fff;color:#1E1B4B;border-color:#fff}
.nps-ends{display:flex;justify-content:space-between;gap:12px;margin-top:8px;font-family:var(--mono);font-size:11.5px;letter-spacing:.06em;color:#C7D2FE}
.nps-more{margin-top:18px;display:grid;gap:8px}
.nps-more label{font-size:14px;color:#E0E7FF}
.nps-more textarea{font:inherit;font-size:15px;border:0;border-radius:10px;padding:12px 14px;min-height:84px;resize:vertical}
.nps-act{display:flex;gap:16px;align-items:center;flex-wrap:wrap;margin-top:16px}
.nps-send{font-family:var(--mono);font-size:13px;letter-spacing:.1em;text-transform:uppercase;padding:14px 22px;border:1.5px solid #fff;background:#fff;color:#1E1B4B;border-radius:0;cursor:pointer}
.nps-send:disabled{opacity:.45;cursor:not-allowed}
.nps-note{font-size:13px;color:#C7D2FE;margin:0}
.nps-msg{margin-top:6px;font-size:18px;font-weight:600;color:#fff}
@media(max-width:620px){.nps-s{grid-template-columns:repeat(5,minmax(0,1fr))}}
</style>"""


def search_html(lg, t):
    js = json.dumps(t["js"], ensure_ascii=False).replace('"', "&quot;")
    icon = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>'
    return (f'<!--sitesearch--><div id="sitesearch" role="search" data-lang="{lg}" data-t="{js}"><form action="/" method="get">'
            f'<label for="ss-q">{t["label"]}</label><div class="ss-f"><input id="ss-q" name="q" type="search" autocomplete="off" '
            f'placeholder="{t["ph"]}" aria-controls="ss-res"><button class="ss-go" type="submit">{icon}<span>{t["go"]}</span></button></div></form>'
            f'<div class="ss-res" id="ss-res" aria-live="polite" hidden></div></div>'
            f'<script src="/js/site-search.js?v=1" defer></script><!--/sitesearch-->')


def score_html(lg, t):
    js = json.dumps(t["sc"], ensure_ascii=False).replace('"', "&quot;")
    return (f'<!--npsscore--><a id="npsscore" href="#nps" data-lang="{lg}" data-t="{js}" aria-live="polite">'
            f'<span class="ns-dot" aria-hidden="true"></span><span class="ns-num">…</span>'
            f'<span class="ns-t"><b>{t["sc"]["lbl"]}</b><small>{t["sc"]["rate"]} →</small></span></a>'
            f'<script src="/js/nps-score.js?v=1" defer></script><!--/npsscore-->')


def nps_html(lg, t):
    js = json.dumps(dict(t["njs"], send=t["send"]), ensure_ascii=False).replace('"', "&quot;")
    btns = "".join(f'<button type="button" value="{i}" aria-pressed="false" aria-label="{i} / 10">{i}</button>' for i in range(1, 11))
    return (f'<!--nps--><section class="band dark" id="nps"><div class="wrap"><p class="eyebrow">{t["eyebrow"]}</p><h2>{t["h"]}</h2>'
            f'<div id="npsbox" data-lang="{lg}" data-t="{js}"><form novalidate>'
            f'<div class="nps-s" role="group" aria-label="{t["h"]}">{btns}</div>'
            f'<div class="nps-ends"><span>{t["lo"]}</span><span>{t["hi"]}</span></div>'
            f'<div class="nps-more" hidden><label for="nps-c">{t["why"]}</label><textarea id="nps-c" name="comment" maxlength="600"></textarea></div>'
            f'<input type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px">'
            f'<div class="nps-act"><button class="nps-send" type="submit" disabled>{t["send"]}</button><p class="nps-note">{t["note"]}</p></div></form>'
            f'<p class="nps-msg" role="status" hidden></p></div></div></section>'
            f'<script src="/js/nps-widget.js?v=1" defer></script><!--/nps-->')


def main():
  for lg, path in (("en", "index.html"), ("th", "th/index.html"), ("zh", "zh/index.html")):
      p = ROOT / path
      s = p.read_text(encoding="utf-8")
      s = re.sub(r"<!--sitesearch-->.*?<!--/sitesearch-->", "", s, flags=re.S)
      s = re.sub(r"<!--nps-->.*?<!--/nps-->", "", s, flags=re.S)
      s = re.sub(r"<!--npsscore-->.*?<!--/npsscore-->", "", s, flags=re.S)
      s = re.sub(r'<style id="ss-css">.*?</style>', "", s, flags=re.S)
      s = re.sub(r'<style id="nps-css">.*?</style>', "", s, flags=re.S)
      s = s.replace("</head>", CSS + NCSS + "</head>", 1)
      m = re.search(r'<div class="cta">.*?</div>', s, re.S)  # hero buttons (the only cta without a style attribute)
      s = s[: m.end()] + search_html(lg, T[lg]) + score_html(lg, T[lg]) + s[m.end():]
      s = s.replace("<footer>", nps_html(lg, T[lg]) + "\n<footer>", 1)
      p.write_text(s, encoding="utf-8")
      print("updated", path)


if __name__ == "__main__":
    main()
