/* Accessibility and reach helpers on every page (added by tools/accessibility.py):
   1) "More languages": a select in the language switcher that opens the same page machine-translated by Google
      (Lao, Burmese, Khmer, Vietnamese, Malay, Indonesian, Japanese, Korean, Hindi, French, German, Spanish, Russian, Arabic).
   2) A one-time, dismissible suggestion to switch to Thai / English / Chinese when the visitor's browser language
      differs from the page and that version exists (uses the page's own language-switcher links). */
(function () {
  // accent text sitting on a dark background: switch to the light accent so it stays readable
  function lum(c) { var m = c.match(/\d+(\.\d+)?/g); if (!m) return 1; var v = m.slice(0, 3).map(function (x) { x = x / 255; return x <= .03928 ? x / 12.92 : Math.pow((x + .055) / 1.055, 2.4); }); return .2126 * v[0] + .7152 * v[1] + .0722 * v[2]; }
  function bgOf(el) { while (el && el.nodeType === 1) { var c = getComputedStyle(el).backgroundColor; var m = c.match(/[\d.]+/g); if (m && (m.length < 4 || +m[3] > .5) && c !== 'transparent') return c; if (getComputedStyle(el).backgroundImage !== 'none') return 'rgb(10,18,48)'; el = el.parentElement; } return 'rgb(255,255,255)'; }
  function fixAccent() { [].forEach.call(document.querySelectorAll('.eyebrow, h1 em, h1 span, h2 em, h2 span, b, .k, .hint, legend'), function (el) {
    if (getComputedStyle(el).color.replace(/\s/g, '') !== 'rgb(91,91,214)') return;
    if (lum(bgOf(el)) < .2) el.style.setProperty('color', '#A5B4FC', 'important'); }); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fixAccent); else fixAccent();
})();
(function () {
  var page = (document.documentElement.lang || 'en').toLowerCase().slice(0, 2);
  var SRC = page === 'zh' ? 'zh-CN' : page;
  var T = {
    en: { more: 'More languages', note: 'Machine translation by Google', sug: 'This page is also in {L}.', go: 'Read in {L}', x: 'Close' },
    th: { more: 'ภาษาอื่น ๆ', note: 'แปลอัตโนมัติโดย Google', sug: 'หน้านี้มีภาษา{L}ด้วย', go: 'อ่านภาษา{L}', x: 'ปิด' },
    zh: { more: '更多语言', note: 'Google 机器翻译', sug: '本页也有{L}版本。', go: '阅读{L}版', x: '关闭' }
  }[page] || null;
  if (!T) return;
  var LANGS = [['lo', 'ພາສາລາວ (Lao)'], ['my', 'မြန်မာ (Burmese)'], ['km', 'ខ្មែរ (Khmer)'], ['vi', 'Tiếng Việt'], ['ms', 'Bahasa Melayu'],
    ['id', 'Bahasa Indonesia'], ['ja', '日本語'], ['ko', '한국어'], ['hi', 'हिन्दी'], ['fr', 'Français'], ['de', 'Deutsch'],
    ['es', 'Español'], ['ru', 'Русский'], ['ar', 'العربية']];
  function tr(tl) {
    var host = location.hostname.replace(/^www\./, '');
    if (!/solaress\.org$/.test(host)) host = 'solaress.org';
    return 'https://' + host.replace(/-/g, '--').replace(/\./g, '-') + '.translate.goog' + location.pathname +
      '?_x_tr_sl=' + SRC + '&_x_tr_tl=' + tl + '&_x_tr_hl=' + tl + location.hash;
  }
  var sw = document.querySelector('.langsw');
  if (sw && !sw.querySelector('.ml-sel') && !/translate\.goog$/.test(location.hostname)) {
    var s = document.createElement('select');
    s.className = 'ml-sel'; s.setAttribute('aria-label', T.more + ' (' + T.note + ')'); s.title = T.note;
    s.innerHTML = '<option value="">🌐 ' + T.more + '</option>' + LANGS.map(function (l) { return '<option value="' + l[0] + '" lang="' + l[0] + '">' + l[1] + '</option>'; }).join('');
    s.addEventListener('change', function () { if (s.value) { var u = tr(s.value); s.value = ''; location.href = u; } });
    sw.appendChild(s);
  }
  // language suggestion
  var NAMES = { en: { en: 'English', th: 'Thai', zh: 'Chinese' }, th: { en: 'อังกฤษ', th: 'ไทย', zh: 'จีน' }, zh: { en: '英文', th: '泰文', zh: '中文' } };
  var pref = ((navigator.languages && navigator.languages[0]) || navigator.language || '').toLowerCase().slice(0, 2);
  var seen = null; try { seen = localStorage.getItem('ss-lang-sug'); } catch (e) {}
  if (!sw || seen || !pref || pref === page || !NAMES.en[pref]) return;
  var a = sw.querySelector('a[lang^="' + pref + '"]'); if (!a || a.getAttribute('aria-current')) return;
  var bar = document.createElement('div'); bar.className = 'lang-sug'; bar.setAttribute('role', 'region'); bar.setAttribute('aria-label', 'Language');
  var lead = { en: 'This page is also in English.', th: 'หน้านี้มีภาษาไทยด้วย', zh: '本页也有中文版本。' }[pref];
  var btn = { en: 'Read in English', th: 'อ่านภาษาไทย', zh: '阅读中文版' }[pref];
  bar.innerHTML = '<span lang="' + pref + '">' + lead + '</span> <a lang="' + pref + '" href="' + a.getAttribute('href') + '">' + btn + ' →</a><button type="button" aria-label="' + T.x + '">×</button>';
  function done() { try { localStorage.setItem('ss-lang-sug', '1'); } catch (e) {} bar.remove(); }
  bar.querySelector('button').onclick = done; bar.querySelector('a').addEventListener('click', function () { try { localStorage.setItem('ss-lang-sug', '1'); } catch (e) {} });
  document.body.appendChild(bar);
})();
