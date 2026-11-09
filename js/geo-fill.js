/* GPS → address: after the GPS button gets lat/lng, look up province, district (amphoe/khet)
   and sub-district (tambon/khwaeng) with OpenStreetMap Nominatim and fill the form fields.
   Used by location.html and th/location.html. Needs js/th-provinces.js (TH_PROV) first. */
(function () {
  function strip(s, words) {
    s = (s || '').trim();
    words.forEach(function (w) {
      if (s.indexOf(w) === 0) s = s.slice(w.length).trim();
      if (s.length > w.length && s.slice(-w.length) === w) s = s.slice(0, -w.length).trim();
    });
    return s;
  }
  var PROV_W = ['จังหวัด', ' Province', 'Province'];
  var DIST_W = ['อำเภอ', 'เขต', 'กิ่งอำเภอ', ' District', 'Amphoe ', 'Khet '];
  var SUB_W = ['ตำบล', 'แขวง', ' Subdistrict', ' Sub-district', 'Tambon ', 'Khwaeng '];
  function norm(s) { return (s || '').toLowerCase().replace(/[\s\-.]/g, ''); }
  function findProv(name) {
    var n = norm(name);
    if (!n || !window.TH_PROV) return null;
    if (n === 'bangkok' || n === 'กรุงเทพฯ' || n === 'กรุงเทพมหานคร') n = norm('Bangkok');
    for (var i = 0; i < TH_PROV.length; i++) {
      var p = TH_PROV[i];
      if (norm(p[0]) === n || norm(p[1]) === n) return p;
    }
    return null;
  }
  window.solGeoFill = function (f, lat, lng, lang, done) {
    var url = 'https://nominatim.openstreetmap.org/reverse?format=jsonv2&zoom=16&addressdetails=1&lat=' +
      lat + '&lon=' + lng + '&accept-language=' + (lang === 'th' ? 'th' : 'en');
    fetch(url, { headers: { 'Accept': 'application/json' } })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (j) {
        var a = (j && j.address) || {};
        if (a.country_code && a.country_code !== 'th') { done && done(false); return; }
        var bkk = !a.province && /กรุงเทพ|bangkok/i.test(a.city || a.state || '');
        var prov = bkk ? 'Bangkok' : strip(a.province || a.state, PROV_W);
        var dist = strip(bkk ? (a.suburb || a.city_district) : (a.county || a.district || a.city_district), DIST_W);
        var sub = strip(bkk ? (a.quarter || a.neighbourhood) : (a.municipality || a.subdistrict || a.quarter || a.suburb || a.village), SUB_W);
        var p = findProv(prov);
        var got = false;
        if (p && f.province) { f.province.value = p[0]; got = true; }
        if (dist && f.district) { f.district.value = dist; got = true; }
        if (f.subdistrict) f.subdistrict.value = sub || '';
        ['province', 'district', 'subdistrict'].forEach(function (k) {
          if (f[k]) { try { f[k].dispatchEvent(new Event('change', { bubbles: true })); } catch (e) {} }
        });
        done && done(got, { province: p ? (lang === 'th' ? p[1] : p[0]) : prov, district: dist, subdistrict: sub });
      })
      .catch(function () { done && done(false); });
  };
})();
