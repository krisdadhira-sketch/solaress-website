/* Solar ESS share buttons: one bar per page + a small share row on every topic
   (technical notes, news articles, FAQ sections, job cards, Our picks sections). */
(function () {
  var lang = (document.documentElement.lang || 'en').slice(0, 2);
  var T = {
    en: { page: 'Share this page', topic: 'Share', copy: 'Copy link', copied: 'Link copied', more: 'More…' },
    th: { page: 'แชร์หน้านี้', topic: 'แชร์', copy: 'คัดลอกลิงก์', copied: 'คัดลอกแล้ว', more: 'อื่นๆ…' },
    zh: { page: '分享此页', topic: '分享', copy: '复制链接', copied: '已复制', more: '更多…' }
  }[lang] || null;
  if (!T) T = { page: 'Share this page', topic: 'Share', copy: 'Copy link', copied: 'Link copied', more: 'More…' };

  var NETS = [
    { k: 'fb', n: 'Facebook', c: '#1877F2', u: function (url) { return 'https://www.facebook.com/sharer/sharer.php?u=' + url; } },
    { k: 'line', n: 'LINE', c: '#06C755', u: function (url) { return 'https://social-plugins.line.me/lineit/share?url=' + url; } },
    { k: 'wa', n: 'WhatsApp', c: '#25D366', u: function (url, t) { return 'https://wa.me/?text=' + t + '%20' + url; } },
    { k: 'x', n: 'X', c: '#0F1419', u: function (url, t) { return 'https://twitter.com/intent/tweet?url=' + url + '&text=' + t; } },
    { k: 'in', n: 'LinkedIn', c: '#0A66C2', u: function (url) { return 'https://www.linkedin.com/sharing/share-offsite/?url=' + url; } }
  ];

  var css = '' +
    '.ssh{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:18px 0 6px}' +
    '.ssh .lbl{font-family:var(--mono,monospace);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--mute,#3E548E);margin-right:4px}' +
    '.ssh a,.ssh button{display:inline-flex;align-items:center;gap:6px;height:32px;padding:0 12px;border-radius:16px;border:0;cursor:pointer;' +
    'font:600 12.5px/1 var(--sans,inherit);color:#fff;text-decoration:none;white-space:nowrap}' +
    '.ssh a:hover,.ssh button:hover{filter:brightness(1.08)}' +
    '.ssh .cp{background:#fff;color:var(--navy,#0A1230);border:1.5px solid var(--navy,#0A1230)}' +
    '.ssh .nv{background:var(--hot,#FF2D55)}' +
    '.ssh-page{border-top:1px solid var(--line,#DEE3ED);padding-top:18px;margin-top:40px}' +
    '.ssh-wrap{max-width:1080px;margin:0 auto;padding:0 24px}' +
    '.ssh-topic{margin-top:14px}.ssh-topic a,.ssh-topic button{height:28px;padding:0 10px;font-size:12px}' +
    '@media(max-width:600px){.ssh a,.ssh button{height:30px;padding:0 10px}}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  function bar(url, title, label, cls) {
    var d = document.createElement('div'); d.className = 'ssh ' + cls;
    var l = document.createElement('span'); l.className = 'lbl'; l.textContent = label; d.appendChild(l);
    var eu = encodeURIComponent(url), et = encodeURIComponent(title);
    if (navigator.share) {
      var b = document.createElement('button'); b.type = 'button'; b.className = 'nv'; b.textContent = T.more;
      b.addEventListener('click', function () { navigator.share({ title: title, url: url }).catch(function () {}); });
      d.appendChild(b);
    }
    NETS.forEach(function (n) {
      var a = document.createElement('a'); a.href = n.u(eu, et); a.target = '_blank'; a.rel = 'noopener';
      a.style.background = n.c; a.textContent = n.n; a.setAttribute('aria-label', label + ': ' + n.n); d.appendChild(a);
    });
    var c = document.createElement('button'); c.type = 'button'; c.className = 'cp'; c.textContent = T.copy;
    c.addEventListener('click', function () {
      var done = function () { c.textContent = T.copied; setTimeout(function () { c.textContent = T.copy; }, 1800); };
      if (navigator.clipboard) navigator.clipboard.writeText(url).then(done, done);
      else { var i = document.createElement('input'); i.value = url; document.body.appendChild(i); i.select(); try { document.execCommand('copy'); } catch (e) {} i.remove(); done(); }
    });
    d.appendChild(c);
    return d;
  }

  var base = location.origin + location.pathname;
  var pageTitle = document.title;

  // Topic share rows
  var sel = '.tnote[id], article[id], section.fsec[id], .cards.fl .card[id], section.pick[id], section.wide[id]';
  document.querySelectorAll(sel).forEach(function (el) {
    var h = el.querySelector('h2, h3');
    var t = (h ? h.textContent.trim() : '') || pageTitle;
    var row = bar(base + '#' + el.id, t + ' | Solar ESS', T.topic, 'ssh-topic');
    var host = el.querySelector(':scope > .body') || el.querySelector(':scope > .pbody') || el;
    host.appendChild(row);
  });

  // Page share bar, just above the footer
  var f = document.querySelector('footer');
  if (f) {
    var w = document.createElement('div'); w.className = 'ssh-wrap';
    w.appendChild(bar(base, pageTitle, T.page, 'ssh-page'));
    f.parentNode.insertBefore(w, f);
  }
})();
