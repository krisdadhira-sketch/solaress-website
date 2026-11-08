/* Site search box (home pages). Index: /data/search-<lang>.json, built by tools/site_search.py.
   Loads the index on first focus. Searches the page's own language first; if nothing is found there, the other
   languages too. Every word typed must appear (title or text); Thai and Chinese are matched as substrings. */
(function () {
  var box = document.getElementById('sitesearch'); if (!box || !window.fetch) return;
  var inp = box.querySelector('input'), res = box.querySelector('.ss-res'), form = box.querySelector('form');
  var LANG = box.getAttribute('data-lang') || 'en', T = JSON.parse(box.getAttribute('data-t') || '{}');
  var IDX = {}, loading = {};
  function load(lg) {
    if (IDX[lg]) return Promise.resolve(IDX[lg]);
    if (!loading[lg]) loading[lg] = fetch('/data/search-' + lg + '.json?v=1').then(function (r) { return r.json(); }).then(function (j) {
      IDX[lg] = j.items.map(function (it) { it._t = norm(it.t); it._s = norm(it.s); it._u = norm(decodeURIComponent(it.u)); return it; });
      return IDX[lg];
    });
    return loading[lg];
  }
  function norm(s) { return String(s || '').toLowerCase().normalize('NFKC'); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function search(list, q) {
    var words = norm(q).split(/\s+/).filter(Boolean); if (!words.length) return [];
    var out = [];
    list.forEach(function (it) {
      var sc = 0;
      for (var i = 0; i < words.length; i++) {
        var w = words[i], inT = it._t.indexOf(w) > -1, inS = it._s.indexOf(w) > -1, inU = it._u.indexOf(w) > -1;
        if (!inT && !inS && !inU) return;
        sc += (inT ? 6 : 0) + (inS ? 2 : 0) + (inU ? 1 : 0);
      }
      if (it._t.indexOf(norm(q).trim()) > -1) sc += 8;
      sc += it.k === 'page' ? 3 : it.k === 'sec' ? 1 : 0;
      out.push([sc, it]);
    });
    out.sort(function (a, b) { return b[0] - a[0]; });
    return out.slice(0, 12).map(function (x) { return x[1]; });
  }
  function snip(it, q) {
    var s = it.s, w = norm(q).split(/\s+/).filter(Boolean)[0] || '', i = norm(s).indexOf(w);
    var a = Math.max(0, i - 60), part = (a > 0 ? '… ' : '') + s.slice(a, a + 180) + (s.length > a + 180 ? ' …' : '');
    var h = esc(part);
    norm(q).split(/\s+/).filter(function (x) { return x.length > 1; }).forEach(function (x) {
      h = h.replace(new RegExp('(' + x.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'ig'), '<mark>$1</mark>');
    });
    return h;
  }
  function render(list, q, other) {
    if (!list.length) { res.innerHTML = '<p class="ss-none">' + esc(T.none || 'No results') + '</p>'; res.hidden = false; return; }
    res.innerHTML = (other ? '<p class="ss-note">' + esc(T.other || 'Results in other languages') + '</p>' : '') + list.map(function (it) {
      var tag = it.k === 'pdf' ? '<span class="ss-k">PDF</span>' : '';
      return '<a class="ss-it" href="' + esc(it.u) + '"' + (it.k === 'pdf' ? ' target="_blank" rel="noopener"' : '') + '><b>' + tag + esc(it.t) + '</b><span>' + snip(it, q) + '</span><em>' + esc(decodeURIComponent(it.u)) + '</em></a>';
    }).join('');
    res.hidden = false;
  }
  var timer, seq = 0;
  function run() {
    var q = inp.value.trim(), my = ++seq;
    if (q.length < 2) { res.hidden = true; res.innerHTML = ''; return; }
    res.hidden = false; if (!IDX[LANG]) res.innerHTML = '<p class="ss-none">' + esc(T.loading || 'Loading…') + '</p>';
    load(LANG).then(function (l) {
      if (my !== seq) return;
      var r = search(l, q);
      if (r.length) { render(r, q, false); return; }
      var others = ['en', 'th', 'zh'].filter(function (x) { return x !== LANG; });
      Promise.all(others.map(load)).then(function (ls) {
        if (my !== seq) return;
        render(search([].concat.apply([], ls), q), q, true);
      });
    }).catch(function () { res.innerHTML = '<p class="ss-none">' + esc(T.err || 'Search is not available right now.') + '</p>'; });
    if (window.gtag) { clearTimeout(run.g); run.g = setTimeout(function () { gtag('event', 'search', { search_term: q }); }, 1500); }
  }
  inp.addEventListener('focus', function () { load(LANG); }, { once: true });
  inp.addEventListener('input', function () { clearTimeout(timer); timer = setTimeout(run, 160); });
  form.addEventListener('submit', function (e) { e.preventDefault(); run(); });
  inp.addEventListener('keydown', function (e) {
    var links = [].slice.call(res.querySelectorAll('.ss-it'));
    if (e.key === 'ArrowDown' && links.length) { e.preventDefault(); links[0].focus(); }
    if (e.key === 'Escape') { res.hidden = true; }
  });
  res.addEventListener('keydown', function (e) {
    var links = [].slice.call(res.querySelectorAll('.ss-it')), i = links.indexOf(document.activeElement);
    if (e.key === 'ArrowDown' && i < links.length - 1) { e.preventDefault(); links[i + 1].focus(); }
    if (e.key === 'ArrowUp') { e.preventDefault(); (i > 0 ? links[i - 1] : inp).focus(); }
    if (e.key === 'Escape') { res.hidden = true; inp.focus(); }
  });
  document.addEventListener('click', function (e) { if (!box.contains(e.target)) res.hidden = true; });
  inp.addEventListener('focus', function () { if (res.innerHTML) res.hidden = false; });
  var q0 = new URLSearchParams(location.search).get('q');
  if (q0) { inp.value = q0; run(); }
})();
