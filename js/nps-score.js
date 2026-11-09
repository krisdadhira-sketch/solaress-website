/* Home-page headline reader score (blinking number in the hero). Data: GET /api/nps?a=score (last 12 months). */
(function () {
  var a = document.getElementById('npsscore'); if (!a || !window.fetch) return;
  var T = JSON.parse(a.getAttribute('data-t') || '{}');
  var num = a.querySelector('.ns-num'), sub = a.querySelector('.ns-t small');
  function f(s, o) { return String(s).replace(/\{(\w+)\}/g, function (m, k) { return o[k]; }); }
  fetch('/api/nps?a=score').then(function (r) { return r.json(); }).then(function (d) {
    if (!d || !d.n) { num.textContent = '–'; sub.textContent = T.none + ' →'; return; }
    num.textContent = (d.nps > 0 ? '+' : '') + d.nps;
    a.classList.add(d.nps >= 50 ? 'good' : d.nps >= 0 ? 'mid' : 'low');
    sub.textContent = f(T.of, { avg: d.avg, n: d.n }) + ' · ' + T.rate + ' →';
  }).catch(function () { num.textContent = '–'; });
})();
