# -*- coding: utf-8 -*-
"""Jobs page apply form (EN /job.html, TH /th/job.html): candidate information Kris requires on every job (Nov 2026).
1. Personal information: name and last name, contact address, phone, ID card (upload), company name
2. Quantification (used for the automatic candidate score): age, years of experience in this job, project values (THB)
3. Certificates: academic / institute, product certificate (name + optional PDF)
4. References: a person and a company
Plus a PDPA consent box (ID card and personal data are used only to screen candidates and never published).
The score itself is computed server-side in netlify/functions/submission-created.mjs (jobScore) and shown in the inbox admin.
Idempotent. Run:  python3 tools/job_candidate_form.py   (then tools/form_ink.py and tools/accessibility.py)"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

T = {
    "en": dict(
        name="Name and last name",
        lede=("To apply, fill in the 4 parts below: <b>1) personal information</b> (name, address, phone, ID card, company), "
              "<b>2) your numbers</b> (age, years of experience in this job, project values), <b>3) certificates</b> "
              "(academic/institute and product) and <b>4) references</b> (a person and a company). We score every application on "
              "these answers to shortlist the best candidate for each job, then send the qualified candidate our contract. "
              "We read every application and reply to shortlisted candidates. "
              '<a href="/contract.html" style="color:#fff;text-decoration:underline">Read the installer hiring contract</a> (read only).'),
        p1="1. Personal information",
        addr="Contact address (house no., road, sub-district, district, province)",
        company="Name of company (write “Individual” if you work on your own)",
        idcard="ID card (photo or PDF of your Thai ID card or passport)",
        idnote="Used only to confirm who you are. Kept in our private admin area and never published.",
        p2="2. Your numbers (used to select the best candidate)",
        age="Age (years)", exp="Experience in this kind of job (years)",
        pval="Largest project you have completed (value, THB)",
        ptot="Total value of your projects in the last 3 years (THB, approximate)",
        p3="3. Certificates",
        acad="Academic / institute: your qualification and where you got it (e.g. Electrical Power Vocational Certificate, Chiang Rai Technical College). Write “None” if none.",
        acadf="Academic / institute certificate (PDF or photo, optional)",
        prod="Product certificates: brands or products you are trained/certified on (e.g. Solis, Deye, Huawei installer training). Write “None” if none.",
        prodf="Product certificate (PDF or photo, optional)",
        p4="4. References",
        rp="Reference person: name, relation (e.g. past customer, employer) and phone",
        rc="Reference company: company name, contact person and phone",
        more="Other files (optional)",
        cv="CV (PDF or Word, optional)",
        quote="Quotation (PDF, optional): your price for this job, with or without materials",
        msg="Anything else about yourself and your work (optional)",
        pdpa=("<b>I agree</b> that Solar ESS keeps my personal information and ID card to screen me for this and future jobs, "
               "contacts my references, and sends me a contract if I am selected. Solar ESS does not publish or share them "
               "(Personal Data Protection Act B.E. 2562)."),
        size="Keep all files together under 8 MB."),
    "th": dict(
        name="ชื่อ-นามสกุล",
        lede=("การสมัครงานต้องกรอกข้อมูล 4 ส่วน: <b>1) ข้อมูลส่วนตัว</b> (ชื่อ ที่อยู่ เบอร์โทร บัตรประชาชน ชื่อบริษัท) "
              "<b>2) ข้อมูลตัวเลข</b> (อายุ ประสบการณ์ในงานนี้ มูลค่าโครงการ) <b>3) ใบรับรอง</b> (สถาบันการศึกษา และใบรับรองผลิตภัณฑ์) "
              "และ <b>4) บุคคล/บริษัทอ้างอิง</b> เราให้คะแนนใบสมัครทุกใบจากข้อมูลเหล่านี้เพื่อคัดเลือกผู้สมัครที่เหมาะสมที่สุดในแต่ละงาน "
              "แล้วส่งสัญญาให้ผู้ที่ผ่านการคัดเลือก เราอ่านทุกใบสมัครและติดต่อกลับผู้ที่ผ่านการคัดเลือกเบื้องต้น "
              '<a href="/th/contract.html" style="color:#fff;text-decoration:underline">อ่านสัญญาจ้างช่างติดตั้ง</a> (อ่านได้อย่างเดียว)'),
        p1="1. ข้อมูลส่วนตัว",
        addr="ที่อยู่ติดต่อ (บ้านเลขที่ ถนน ตำบล อำเภอ จังหวัด)",
        company="ชื่อบริษัท (หากทำงานอิสระ ให้เขียนว่า “บุคคลธรรมดา”)",
        idcard="บัตรประชาชน (รูปถ่ายหรือ PDF ของบัตรประชาชนหรือหนังสือเดินทาง)",
        idnote="ใช้เพื่อยืนยันตัวตนเท่านั้น เก็บไว้ในส่วนผู้ดูแลระบบ ไม่เปิดเผยต่อสาธารณะ",
        p2="2. ข้อมูลตัวเลข (ใช้คัดเลือกผู้สมัครที่เหมาะสมที่สุด)",
        age="อายุ (ปี)", exp="ประสบการณ์ในงานลักษณะนี้ (ปี)",
        pval="มูลค่าโครงการที่ใหญ่ที่สุดที่เคยทำเสร็จ (บาท)",
        ptot="มูลค่ารวมของโครงการในช่วง 3 ปีที่ผ่านมา (บาท โดยประมาณ)",
        p3="3. ใบรับรอง",
        acad="สถาบันการศึกษา: วุฒิการศึกษาและสถาบัน (เช่น ปวช. ไฟฟ้ากำลัง วิทยาลัยเทคนิคเชียงราย) หากไม่มีให้เขียนว่า “ไม่มี”",
        acadf="ใบรับรองวุฒิการศึกษา/สถาบัน (PDF หรือรูปถ่าย ไม่บังคับ)",
        prod="ใบรับรองผลิตภัณฑ์: ยี่ห้อหรือผลิตภัณฑ์ที่ผ่านการอบรม/รับรอง (เช่น อบรมช่างติดตั้ง Solis, Deye, Huawei) หากไม่มีให้เขียนว่า “ไม่มี”",
        prodf="ใบรับรองผลิตภัณฑ์ (PDF หรือรูปถ่าย ไม่บังคับ)",
        p4="4. บุคคลและบริษัทอ้างอิง",
        rp="บุคคลอ้างอิง: ชื่อ ความสัมพันธ์ (เช่น ลูกค้าเก่า นายจ้าง) และเบอร์โทร",
        rc="บริษัทอ้างอิง: ชื่อบริษัท ผู้ติดต่อ และเบอร์โทร",
        more="ไฟล์อื่น ๆ (ไม่บังคับ)",
        cv="ประวัติย่อ (PDF หรือ Word ไม่บังคับ)",
        quote="ใบเสนอราคา (PDF ไม่บังคับ): ค่าจ้างสำหรับงานนี้ แบบรวมหรือไม่รวมวัสดุ",
        msg="ข้อมูลเพิ่มเติมเกี่ยวกับตัวคุณและผลงาน (ไม่บังคับ)",
        pdpa=("<b>ข้าพเจ้ายินยอม</b>ให้ Solar ESS เก็บข้อมูลส่วนบุคคลและสำเนาบัตรประชาชนของข้าพเจ้า เพื่อใช้คัดเลือกผู้สมัครในงานนี้และงานต่อ ๆ ไป "
               "ติดต่อบุคคล/บริษัทอ้างอิง และส่งสัญญาให้หากได้รับการคัดเลือก โดย Solar ESS จะไม่เปิดเผยหรือส่งต่อข้อมูลดังกล่าว "
               "(พ.ร.บ. คุ้มครองข้อมูลส่วนบุคคล พ.ศ. 2562)"),
        size="ขนาดรวมทุกไฟล์ไม่เกิน 8 MB"),
}

CSS = """<style id="jcand-css">
.jcand{border:1.5px solid rgba(165,180,252,.55);border-radius:12px;padding:14px 14px 6px;margin:6px 0 4px;display:grid;gap:10px;background:rgba(91,91,214,.10);min-width:0}
.jcand legend{padding:0 8px;font-weight:700;color:#C7D2FE!important;font-size:16px}
.jcand .fine{margin:0;opacity:.85}
.jcand input,.jcand textarea{width:100%;min-width:0;box-sizing:border-box}
</style>"""


def block1(t):
    return (f'<!--jcand1--><fieldset class="jcand" id="j-personal"><legend>{t["p1"]}</legend>'
            f'<label for="j-addr">{t["addr"]}<textarea id="j-addr" name="contact-address" rows="2" required autocomplete="street-address"></textarea></label>'
            f'<label for="j-company">{t["company"]}<input id="j-company" name="company-name" required autocomplete="organization"></label>'
            f'<label for="j-idcard">{t["idcard"]}<input id="j-idcard" name="id-card" type="file" accept=".pdf,.jpg,.jpeg,.png,.webp" required></label>'
            f'<p class="fine">{t["idnote"]}</p></fieldset><!--/jcand1-->')


def block2(t):
    return (f'<!--jcand2--><fieldset class="jcand" id="j-numbers"><legend>{t["p2"]}</legend><div class="jp2">'
            f'<label for="j-age">{t["age"]}<input id="j-age" name="age" type="number" min="18" max="80" inputmode="numeric" required></label>'
            f'<label for="j-exp">{t["exp"]}<input id="j-exp" name="experience-years" type="number" min="0" max="60" step="0.5" inputmode="decimal" required></label></div>'
            f'<div class="jp2"><label for="j-pval">{t["pval"]}<input id="j-pval" name="largest-project-value" inputmode="numeric" required placeholder="e.g. 350000"></label>'
            f'<label for="j-ptot">{t["ptot"]}<input id="j-ptot" name="total-project-value-3y" inputmode="numeric" placeholder="e.g. 2000000"></label></div>'
            f'</fieldset><!--/jcand2-->'
            f'<!--jcand3--><fieldset class="jcand" id="j-certs"><legend>{t["p3"]}</legend>'
            f'<label for="j-acad">{t["acad"]}<input id="j-acad" name="academic-certificate" required></label>'
            f'<label for="j-acadf">{t["acadf"]}<input id="j-acadf" name="certificate" type="file" accept=".pdf,.jpg,.jpeg,.png,.webp"></label>'
            f'<label for="j-prod">{t["prod"]}<input id="j-prod" name="product-certificate" required></label>'
            f'<label for="j-prodf">{t["prodf"]}<input id="j-prodf" name="product-certificate-file" type="file" accept=".pdf,.jpg,.jpeg,.png,.webp"></label>'
            f'</fieldset><!--/jcand3-->'
            f'<!--jcand4--><fieldset class="jcand" id="j-refs"><legend>{t["p4"]}</legend>'
            f'<label for="j-refp">{t["rp"]}<input id="j-refp" name="reference-person" required></label>'
            f'<label for="j-refc">{t["rc"]}<input id="j-refc" name="reference-company" required></label>'
            f'</fieldset><!--/jcand4-->'
            f'<!--jcandx--><fieldset class="jcand" id="j-more"><legend>{t["more"]}</legend>'
            f'<label for="j-cv">{t["cv"]}<input id="j-cv" name="cv" type="file" accept=".pdf,.doc,.docx"></label>'
            f'<label for="j-quote">{t["quote"]}<input id="j-quote" name="quotation" type="file" accept=".pdf"></label>'
            f'<label for="j-msg">{t["msg"]}<textarea id="j-msg" name="message" rows="3"></textarea></label>'
            f'<p class="fine">{t["size"]}</p></fieldset><!--/jcandx-->'
            f'<label class="chk"><input type="checkbox" name="pdpa-consent" value="yes" required><span>{t["pdpa"]}</span></label>')


def run(path, lang):
    t = T[lang]
    s = path.read_text(encoding="utf-8")
    a = s.index('<form name="job-application"')
    b = s.index("</form>", a)
    f = s[a:b]
    # name label
    f = re.sub(r'<label for="j-name">[^<]*<input', f'<label for="j-name">{t["name"]}<input', f, count=1)
    # block 1 after the phone field
    f = re.sub(r"<!--jcand1-->.*?<!--/jcand1-->", "", f, flags=re.S)
    f = re.sub(r'(<label for="j-phone">.*?</label>)', lambda m: m.group(1) + block1(t), f, count=1, flags=re.S)
    # blocks 2–4: replace old optional-docs section (first run) or previous blocks (re-run)
    if "<!--jcand2-->" in f:
        f = re.sub(r"<!--jcand2-->.*?<label class=\"chk\"><input type=\"checkbox\" name=\"pdpa-consent\".*?</label>", block2(t), f, count=1, flags=re.S)
    else:
        f = re.sub(r'<label for="j-cv">.*?<label for="j-msg">.*?</label>', block2(t), f, count=1, flags=re.S)
    s = s[:a] + f + s[b:]
    # lede above the form
    s = re.sub(r'(<section class="band dark" id="apply".*?<p class="lede" style="margin-top:18px">).*?(</p>)',
               lambda m: m.group(1) + t["lede"] + m.group(2), s, count=1, flags=re.S)
    if 'id="jcand-css"' not in s:
        s = s.replace("</head>", CSS + "\n</head>", 1)
    path.write_text(s, encoding="utf-8")
    print("updated", path.relative_to(ROOT))


if __name__ == "__main__":
    run(ROOT / "job.html", "en")
    run(ROOT / "th" / "job.html", "th")
