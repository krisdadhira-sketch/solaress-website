/* Blinking "NEW" badge on news articles published in the last NEW_DAYS days.
   Reads the date at the start of each article's eyebrow (EN "15 November 2026", TH "15 พฤศจิกายน 2569",
   ZH "2026年11月15日"), so articles added later get the badge automatically and lose it after NEW_DAYS. */
(function () {
  var NEW_DAYS = 7;
  var EN = ['january','february','march','april','may','june','july','august','september','october','november','december'];
  var TH = ['มกราคม','กุมภาพันธ์','มีนาคม','เมษายน','พฤษภาคม','มิถุนายน','กรกฎาคม','สิงหาคม','กันยายน','ตุลาคม','พฤศจิกายน','ธันวาคม'];
  var lang = (document.documentElement.lang || 'en').slice(0, 2);
  var LABEL = { en: 'NEW', th: 'ใหม่', zh: '新' }[lang] || 'NEW';
  function parse(t) {
    var m;
    if ((m = t.match(/(\d{4})年(\d{1,2})月(\d{1,2})日/))) return new Date(+m[1], m[2] - 1, +m[3]);
    if ((m = t.match(/^(\d{1,2})\s+(\S+)\s+(\d{4})/))) {
      var mo = EN.indexOf(m[2].toLowerCase()); if (mo < 0) mo = TH.indexOf(m[2]);
      if (mo < 0) return null;
      var y = +m[3]; if (y > 2400) y -= 543;
      return new Date(y, mo, +m[1]);
    }
    return null;
  }
  var css = document.createElement('style');
  css.textContent = '.news-new{display:inline-flex;align-items:center;gap:6px;margin-right:10px;padding:2px 10px;border-radius:999px;' +
    'background:#E8590C;color:#fff;font-weight:700;font-size:12px;letter-spacing:.06em;vertical-align:middle;animation:newsblink 1.1s ease-in-out infinite}' +
    '.news-new:before{content:"";width:7px;height:7px;border-radius:50%;background:#fff}' +
    '@keyframes newsblink{0%,100%{opacity:1}50%{opacity:.35}}' +
    '@media (prefers-reduced-motion:reduce){.news-new{animation:none}}';
  document.head.appendChild(css);
  var now = new Date(); now.setHours(0, 0, 0, 0);
  document.querySelectorAll('article[id] > .eyebrow:first-child, article[id] > p.eyebrow').forEach(function (e) {
    if (e.querySelector('.news-new')) return;
    var d = parse(e.textContent.trim());
    if (!d) return;
    var age = (now - d) / 864e5;
    if (age < 0 || age > NEW_DAYS) return;
    var b = document.createElement('span');
    b.className = 'news-new'; b.textContent = LABEL; b.setAttribute('aria-label', LABEL);
    e.insertBefore(b, e.firstChild);
  });
})();
