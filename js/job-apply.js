/* Jobs page apply form (/job.html, /th/job.html): job picker + job proposal box. Added by tools/job_apply_box.py.
   - The "Position or project job" list is built live from the job posts on the page: every open job, newest first,
     grouped (project jobs / permanent roles / open application). Closed jobs are left out; jobs on hold are shown
     but cannot be picked. A filter box narrows the list by place or type of work.
   - Picking a job shows its location and a link back to the post, and fills the hidden job-id.
   - For project jobs the proposal box (2 prices, proposal, start date, days) is shown and required;
     for permanent roles and open applications it is hidden. */
(function () {
  var sel = document.getElementById('j-role'), find = document.getElementById('j-find'), info = document.getElementById('j-info'),
    jid = document.getElementById('j-id'), prop = document.getElementById('j-prop'), form = sel && sel.form;
  if (!sel || !form) return;
  var TH = (document.documentElement.lang || '').indexOf('th') === 0;
  var L = TH ? { proj: 'งานรายโครงการที่เปิดรับ', perm: 'ตำแหน่งงานประจำ', other: 'อื่น ๆ', open: 'สมัครงานทั่วไป (Open application)', pick: 'เลือกงานที่ต้องการสมัคร / เสนอราคา', hold: ' (ระงับชั่วคราว)', none: 'ไม่พบงานที่ตรงกับคำค้น', view: 'ดูรายละเอียดงาน', n: '{n} งานที่เปิดรับ' }
    : { proj: 'Project based jobs (open)', perm: 'Permanent roles', other: 'Other', open: 'Open application', pick: 'Choose the job you are applying or quoting for', hold: ' (on hold)', none: 'No job matches your filter', view: 'View the job details', n: '{n} open jobs' };
  var JOBS = [];
  function txt(el) { return el ? el.textContent.replace(/\s+/g, ' ').trim() : ''; }
  function collect() {
    JOBS = [];
    [].forEach.call(document.querySelectorAll('article.card'), function (a) {
      var link = a.querySelector('a[href="#apply"][data-job]'); if (!link) return;
      var closed = a.classList.contains('is-closed') || !!a.querySelector('.go .closed');
      if (closed) return;
      var hold = a.classList.contains('is-hold');
      JOBS.push({ name: link.getAttribute('data-job'), id: a.id || '', proj: !!a.closest('.cards.fl'), hold: hold,
        where: txt(a.querySelector('.where')), kind: txt(a.querySelector('.kind')), title: txt(a.querySelector('h3')),
        q: (link.getAttribute('data-job') + ' ' + (a.getAttribute('data-q') || '') + ' ' + txt(a.querySelector('.where')) + ' ' + (a.getAttribute('data-work') || '')).toLowerCase() });
    });
  }
  function build() {
    var cur = sel.value, f = (find && find.value || '').toLowerCase().trim(), words = f.split(/\s+/).filter(Boolean), shown = 0;
    function ok(j) { return words.every(function (w) { return j.q.indexOf(w) > -1; }); }
    var h = '<option value="">' + L.pick + '</option>', proj = JOBS.filter(function (j) { return j.proj && ok(j); }), perm = JOBS.filter(function (j) { return !j.proj && ok(j); });
    function opt(j) { shown++; return '<option value="' + j.name.replace(/"/g, '&quot;') + '"' + (j.hold ? ' disabled' : '') + '>' + j.name.replace(/</g, '&lt;') + (j.hold ? L.hold : '') + '</option>'; }
    if (proj.length) h += '<optgroup label="' + L.proj + ' · ' + proj.length + '">' + proj.map(opt).join('') + '</optgroup>';
    if (perm.length) h += '<optgroup label="' + L.perm + '">' + perm.map(opt).join('') + '</optgroup>';
    h += '<optgroup label="' + L.other + '"><option value="Open application">' + L.open + '</option></optgroup>';
    if (words.length && !shown) h = h.replace('<option value="">' + L.pick + '</option>', '<option value="">' + L.none + '</option>');
    sel.innerHTML = h;
    if (cur && [].some.call(sel.options, function (o) { return o.value === cur && !o.disabled; })) sel.value = cur;
    else if (words.length && shown === 1) { var first = [].filter.call(sel.options, function (o) { return o.value && o.value !== 'Open application' && !o.disabled; })[0]; if (first) sel.value = first.value; }
    var cnt = document.getElementById('j-count'); if (cnt) cnt.textContent = L.n.replace('{n}', JOBS.filter(function (j) { return !j.hold; }).length);
    update();
  }
  function update() {
    var j = JOBS.filter(function (x) { return x.name === sel.value; })[0], isProj = !!(j && j.proj);
    if (jid) jid.value = j ? j.id : '';
    if (info) {
      if (j) {
        info.innerHTML = '<b>' + (j.title || j.name).replace(/</g, '&lt;') + '</b>' + (j.where ? '<span>📍 ' + j.where.replace(/</g, '&lt;') + '</span>' : '') +
          (j.id ? '<a href="#' + j.id + '">' + L.view + ' ↑</a>' : '');
        info.hidden = false;
      } else info.hidden = true;
    }
    if (prop) {
      prop.hidden = !isProj && !!sel.value;
      [].forEach.call(prop.querySelectorAll('input,textarea,select'), function (el) {
        if (el.type === 'hidden') return;
        el.disabled = prop.hidden;
        if (el.hasAttribute('data-req')) el.required = !prop.hidden;
      });
    }
  }
  sel.addEventListener('change', update);
  if (find) find.addEventListener('input', build);
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href="#apply"][data-job]'); if (!a) return;
    if (find) find.value = '';
    setTimeout(function () { build(); sel.value = a.getAttribute('data-job'); update(); }, 0);
  });
  form.addEventListener('submit', function () {
    var p1 = form.querySelector('[name="price-labour-only"]'), p2 = form.querySelector('[name="price-labour-materials"]'), q = document.getElementById('j-price');
    if (q) q.value = (p1 && p1.value ? 'Labour only: ' + p1.value : '') + (p2 && p2.value ? (p1 && p1.value ? ' / ' : '') + 'Labour + materials: ' + p2.value : '');
  });
  function go() { collect(); build(); }
  go();
  window.addEventListener('load', function () { setTimeout(go, 300); setTimeout(go, 2500); }); // after closed / on-hold marks are applied
})();
