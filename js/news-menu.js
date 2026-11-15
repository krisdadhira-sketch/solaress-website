/* Blinking "NEW" badge on the top-menu News link while the newest news article is at most N days old.
   Dates come from /data/news-latest.json (written by tools/news_menu.py). */
(function () {
  var lang = (document.documentElement.lang || 'en').slice(0, 2);
  var href = lang === 'th' ? '/th/news.html' : lang === 'zh' ? '/zh/news.html' : '/news.html';
  var LABEL = { en: 'NEW', th: 'ใหม่', zh: '新' }[lang] || 'NEW';
  fetch('/data/news-latest.json', { cache: 'no-cache' }).then(function (r) { return r.json(); }).then(function (j) {
    var d = j[lang] || j.en; if (!d) return;
    var p = d.split('-'), pub = new Date(+p[0], p[1] - 1, +p[2]), now = new Date(); now.setHours(0, 0, 0, 0);
    var age = (now - pub) / 864e5; if (age < 0 || age > (j.days || 7)) return;
    var css = document.createElement('style');
    css.textContent = '.nav-new{display:inline-block;margin-left:6px;padding:1px 7px;border-radius:999px;background:#E8590C;color:#fff;' +
      'font:700 10px/1.5 system-ui,sans-serif;letter-spacing:.05em;vertical-align:middle;animation:navnewblink 1.1s ease-in-out infinite}' +
      '@keyframes navnewblink{0%,100%{opacity:1}50%{opacity:.3}}@media (prefers-reduced-motion:reduce){.nav-new{animation:none}}';
    document.head.appendChild(css);
    document.querySelectorAll('nav .dd > a, nav > a').forEach(function (a) {
      var h = (a.getAttribute('href') || '').split('#')[0];
      if (h !== href || a.querySelector('.nav-new')) return;
      var b = document.createElement('span'); b.className = 'nav-new'; b.textContent = LABEL;
      b.setAttribute('aria-label', LABEL); a.appendChild(b);
    });
  }).catch(function () {});
})();
