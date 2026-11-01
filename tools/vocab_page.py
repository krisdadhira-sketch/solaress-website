"""Build vocabulary.html (students) and vocab-admin.html (teacher) from the site shell in members.html.
Content lives in tools/vocab/student.html and tools/vocab/admin.html. Run: python3 tools/vocab_page.py"""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
shell = (root / "members.html").read_text(encoding="utf-8")
head_end = shell.index("</head>")
nav_end = shell.index("<!--/mnav-->") + len("<!--/mnav-->")
foot = shell.index("<footer")
foot_html = shell[foot:]
# drop the members-page script (price-list download) but keep share.js and the LINE/Facebook buttons
foot_html = re.sub(r"</footer>\s*<script>.*?</script>", "</footer>", foot_html, count=1, flags=re.S)
body_open = shell[head_end:nav_end]

def page(fname, title, desc, frag, index):
    head = shell[:head_end]
    head = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", head, flags=re.S)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', r"\g<1>" + title, head)
    head = re.sub(r'(<meta (?:property="og:description"|name="description") content=")[^"]*', r"\g<1>" + desc, head)
    head = head.replace("https://solaress.org/members.html", "https://solaress.org/" + fname)
    if index:
        head = head.replace('<meta name="robots" content="noindex">\n', "")
    head = re.sub(r'<link rel="alternate" hreflang[^>]*>\n?', "", head)
    head = re.sub(r'(<link rel="canonical" href=")[^"]*', r"\g<1>https://solaress.org/" + fname.replace(".html", ""), head)
    nav = re.sub(r'<span class="langsw">.*?</span>', "", body_open, flags=re.S)
    html = head + nav + "\n" + (root / "tools/vocab" / frag).read_text(encoding="utf-8") + "\n" + foot_html
    (root / fname).write_text(html, encoding="utf-8")
    print("wrote", fname, len(html))

page("vocabulary.html", "Vocabulary Tests | Solar ESS",
     "100 English synonym tests, 20 questions each, from everyday words to advanced vocabulary. Log in, take a test and track your scores.",
     "student.html", True)
page("vocab-admin.html", "Vocabulary Results | Solar ESS", "Teacher dashboard for the Solar ESS vocabulary tests.", "admin.html", False)
