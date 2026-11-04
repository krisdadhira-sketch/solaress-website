/* Solar ESS installer-partner directory: renders /data/installer-partners.json by region,
   fills the request form's partner list, and adds small form helpers. No contact data is shown. */
(function () {
  var I = window.PARTNER_I18N || {}, T = I.t || {}, th = I.lang === 'th';
  var dir = document.getElementById('pdir');
  var fReg = document.getElementById('pf-region'), fSvc = document.getElementById('pf-svc');
  var sel = document.getElementById('q-partner');
  var partners = [];

  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]; }); }
  function L(p, k) { return (th && p[k + '_th']) ? p[k + '_th'] : p[k]; }
  function num(n) { return (n == null || n === '') ? '–' : Number(n).toLocaleString(th ? 'th-TH' : 'en-US'); }
  var regPath = th ? '/th/partners.html' : '/partners.html';

  function card(p) {
    var svc = (p.services || []).map(function (s) { return '<span>' + esc((I.services || {})[s] || s) + '</span>'; }).join('');
    var tools = (p.tools || []).map(function (s) { return (I.tools || {})[s] || s; }).join(', ');
    var langs = (L(p, 'languages') || []).join(', ');
    var loc = [L(p, 'district'), L(p, 'province')].filter(Boolean).join(', ');
    var flags = [];
    if (p.tax_invoice) flags.push(T.vat);
    if (p.insured) flags.push(T.ins);
    var dl = '';
    if (L(p, 'serves')) dl += '<dt>' + esc(T.serves) + '</dt><dd>' + esc(L(p, 'serves')) + '</dd>';
    if (p.max_size) dl += '<dt>' + esc(T.max) + '</dt><dd>' + esc((I.sizes || {})[p.max_size] || p.max_size) + '</dd>';
    if (p.brands && p.brands.length) dl += '<dt>' + esc(T.brands_l) + '</dt><dd>' + esc(p.brands.join(', ')) + '</dd>';
    if (tools) dl += '<dt>' + esc(T.tools_l) + '</dt><dd>' + esc(tools) + '</dd>';
    if (langs) dl += '<dt>' + esc(T.langs_l) + '</dt><dd>' + esc(langs) + '</dd>';
    return '<article class="pcard" id="partner-' + esc(p.id) + '">' +
      (p.photo ? '<div class="ph" style="background-image:url(\'' + esc(p.photo) + '\')" role="img" aria-label="' + esc(L(p, 'name')) + '"></div>' : '') +
      '<div class="bd"><div class="hd">' + (p.logo ? '<img src="' + esc(p.logo) + '" alt="" loading="lazy">' : '') +
      '<div><h4>' + esc(L(p, 'name')) + '</h4><div class="loc">' + esc(L(p, 'type') || '') + (loc ? ' · ' + esc(T.base) + ' ' + esc(loc) : '') + '</div></div></div>' +
      (p.verified ? '<span class="ver">✓ ' + esc(T.verified) + '</span>' : '') +
      (L(p, 'intro') ? '<p style="margin:0">' + esc(L(p, 'intro')) + '</p>' : '') +
      '<div class="pstats"><div><b>' + num(p.years) + '</b>' + esc(T.yrs) + '</div><div><b>' + num(p.team) + '</b>' + esc(T.team) + ' · ' + num(p.electricians) + ' ' + esc(T.elec) + '</div><div><b>' + num(p.projects) + '</b>' + esc(T.proj) + (p.kwp ? ' · ' + num(p.kwp) + ' ' + esc(T.kwp) : '') + '</div></div>' +
      (svc ? '<div class="ptags">' + svc + '</div>' : '') +
      (flags.length ? '<div class="ptags">' + flags.map(function (f) { return '<span>✓ ' + esc(f) + '</span>'; }).join('') + '</div>' : '') +
      (dl ? '<dl>' + dl + '</dl>' : '') +
      '<a class="btn" href="#request" data-partner="' + esc(p.id) + '">' + esc(T.req_btn) + '</a></div></article>';
  }

  function render() {
    if (!dir) return;
    var r = fReg ? fReg.value : '', s = fSvc ? fSvc.value : '';
    var html = '';
    Object.keys(I.regions || {}).forEach(function (key) {
      if (r && r !== key) return;
      var list = partners.filter(function (p) { return p.region === key && (!s || (p.services || []).indexOf(s) > -1); });
      html += '<div class="preg" id="region-' + key + '"><h3>' + esc(I.regions[key]) + '<small>' + list.length + '</small></h3>';
      html += list.length ? '<div class="pgrid">' + list.map(card).join('') + '</div>'
        : '<div class="pempty">' + esc(T.empty) + ' <a href="#register">' + esc(T.empty_cta) + ' →</a></div>';
      html += '</div>';
    });
    dir.innerHTML = html;
  }

  function fillSelect() {
    if (!sel) return;
    partners.forEach(function (p) {
      var o = document.createElement('option');
      o.value = p.id + ' · ' + p.name;
      o.textContent = L(p, 'name') + ' (' + ((I.regions || {})[p.region] || '') + ')';
      o.setAttribute('data-id', p.id);
      sel.appendChild(o);
    });
  }

  function pick(id) {
    if (!sel) return;
    for (var i = 0; i < sel.options.length; i++) if (sel.options[i].getAttribute('data-id') === id) { sel.selectedIndex = i; break; }
  }

  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[data-partner]');
    if (a) pick(a.getAttribute('data-partner'));
  });
  if (fReg) fReg.addEventListener('change', render);
  if (fSvc) fSvc.addEventListener('change', render);

  fetch('/data/installer-partners.json', { cache: 'no-cache' })
    .then(function (r) { return r.ok ? r.json() : { partners: [] }; })
    .catch(function () { return { partners: [] }; })
    .then(function (d) {
      partners = (d && d.partners) || [];
      partners.sort(function (a, b) { return (b.projects || 0) - (a.projects || 0); });
      render(); fillSelect();
      var m = location.hash.match(/^#partner-(.+)$/);
      if (m) { pick(m[1]); var el = document.getElementById('partner-' + m[1]); if (el) el.scrollIntoView(); }
    });

  // character counter for the introduction
  document.querySelectorAll('[data-count]').forEach(function (c) {
    var f = document.getElementById(c.getAttribute('data-count'));
    if (!f) return;
    var u = function () { c.textContent = f.value.length + ' / ' + (f.maxLength > 0 ? f.maxLength : ''); };
    f.addEventListener('input', u); u();
  });

  // checkbox groups that need at least one tick
  document.querySelectorAll('form').forEach(function (form) {
    var groups = form.querySelectorAll('[data-need-one]');
    if (!groups.length) return;
    form.addEventListener('submit', function (e) {
      for (var i = 0; i < groups.length; i++) {
        var boxes = groups[i].querySelectorAll('input[type=checkbox]');
        var ok = Array.prototype.some.call(boxes, function (b) { return b.checked; });
        boxes[0].setCustomValidity(ok ? '' : (th ? 'กรุณาเลือกอย่างน้อย 1 ข้อ' : 'Please tick at least one.'));
        if (!ok) { e.preventDefault(); boxes[0].reportValidity(); return; }
      }
    });
    groups.forEach(function (g) { g.addEventListener('change', function () { g.querySelector('input').setCustomValidity(''); }); });
  });
})();
