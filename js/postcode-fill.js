/* Postcode from GPS: whenever a page's "Use my location" button gets a GPS fix, look up the postcode
   (OpenStreetMap Nominatim) and fill any empty postcode field in the same form. Load after the form. */
(function () {
  var g = navigator.geolocation; if (!g || g.__pcWrapped) return;
  var orig = g.getCurrentPosition.bind(g);
  g.getCurrentPosition = function (ok, err, opt) {
    var form = document.activeElement && document.activeElement.form;
    return orig(function (p) {
      try { ok && ok(p); } finally {
        var fields = form ? form.querySelectorAll('input[name="postcode"]') : document.querySelectorAll('input[name="postcode"]');
        var empty = [].filter.call(fields, function (f) { return !f.value; });
        if (!empty.length) return;
        fetch('https://nominatim.openstreetmap.org/reverse?format=jsonv2&zoom=18&addressdetails=1&lat=' + p.coords.latitude + '&lon=' + p.coords.longitude, { headers: { Accept: 'application/json' } })
          .then(function (r) { return r.json(); })
          .then(function (j) { var pc = j && j.address && j.address.postcode; if (pc && /^\d{5}$/.test(pc)) empty.forEach(function (f) { f.value = pc; f.dispatchEvent(new Event('input', { bubbles: true })); }); })
          .catch(function () {});
      }
    }, err, opt);
  };
  g.__pcWrapped = true;
})();
