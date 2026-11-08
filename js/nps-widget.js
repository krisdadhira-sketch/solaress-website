/* Reader NPS widget (home pages). Backend: /api/nps (netlify/functions/nps/nps.mjs). One score per IP per month. */
(function () {
  var w = document.getElementById('npsbox'); if (!w || !window.fetch) return;
  var T = JSON.parse(w.getAttribute('data-t') || '{}'), lang = w.getAttribute('data-lang') || 'en';
  var f = w.querySelector('form'), btns = [].slice.call(w.querySelectorAll('.nps-s button')), send = w.querySelector('.nps-send'),
    msg = w.querySelector('.nps-msg'), more = w.querySelector('.nps-more'), score = 0;
  function done(t) { f.hidden = true; f.style.display = 'none'; msg.textContent = t; msg.hidden = false; }
  fetch('/api/nps?a=status').then(function (r) { return r.json(); }).then(function (j) { if (j.done) done(T.done); }).catch(function () {});
  btns.forEach(function (b) {
    b.addEventListener('click', function () {
      score = +b.value;
      btns.forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      more.hidden = false; send.disabled = false;
    });
  });
  f.addEventListener('submit', function (e) {
    e.preventDefault(); if (!score) return;
    send.disabled = true; send.textContent = T.sending || '…';
    fetch('/api/nps', { method: 'POST', headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ score: score, comment: f.comment.value, website: f.website.value, lang: lang, page: location.pathname }) })
      .then(function (r) { return r.json().then(function (j) { return [r.status, j]; }); })
      .then(function (x) {
        if (x[0] === 409) return done(T.done);
        if (x[0] !== 200) throw new Error(x[1].error || x[0]);
        done(T.thanks);
        if (window.gtag) gtag('event', 'nps_score', { score: score });
      })
      .catch(function () { send.disabled = false; send.textContent = T.send; msg.textContent = T.err; msg.hidden = false; });
  });
})();
