/* Approved TSIA members on the team page (/team.html#network): company members and Installer Partners. Data: /api/members?a=public&type=tsia.
   Only public fields are returned by the API; contact details are never sent to the browser. */
(function () {
  var me = document.currentScript, lang = (me && me.getAttribute('data-lang')) || 'en';
  var T = {
    en: { since: 'Founded', team: 'Installers', elec: 'Certified electricians', proj: 'Projects', kwp: 'kWp installed', ver: 'Approved TSIA member', cat_company: 'TSIA company member', cat_partner: 'TSIA Installer Partner', more: 'Partner profile' },
    th: { since: 'ก่อตั้ง', team: 'ช่างในทีม', elec: 'ช่างไฟฟ้ามีใบรับรอง', proj: 'โครงการ', kwp: 'kWp ที่ติดตั้ง', ver: 'สมาชิก TSIA ที่ได้รับการอนุมัติ', cat_company: 'สมาชิก TSIA ประเภทบริษัท', cat_partner: 'ช่างพันธมิตร TSIA', more: 'ดูโปรไฟล์ช่างพันธมิตร' },
    zh: { since: '成立', team: '安装人员', elec: '持证电工', proj: '项目', kwp: '已装 kWp', ver: '已批准的 TSIA 会员', cat_company: 'TSIA 企业会员', cat_partner: 'TSIA 安装合作伙伴', more: '合作伙伴资料' }
  }[lang] || {};
  var box = document.getElementById('tsia-members'), grid = document.getElementById('tsia-grid');
  if (!box || !grid) return;
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function stat(v, l) { return (v === null || v === undefined || v === '') ? '' : '<div><b>' + esc(typeof v === 'number' ? v.toLocaleString() : v) + '</b>' + esc(l) + '</div>'; }
  fetch('/api/members?a=public&type=tsia').then(function (r) { return r.ok ? r.json() : { items: [] }; }).catch(function () { return { items: [] }; }).then(function (d) {
    var items = (d && d.items) || [];
    if (!items.length) return;
    grid.innerHTML = items.map(function (m) {
      var reg = [m.province].concat(m.regions || []).filter(Boolean).join(' · ');
      return '<article class="ncard" id="tsia-' + esc(m.id) + '"><div class="nwrap">' +
        (m.photo ? '<img class="nlogo wide" src="' + esc(m.photo) + '" alt="" loading="lazy">' : '') +
        '<div class="reg">' + esc(m.category === 'partner' ? T.cat_partner : T.cat_company) + ' · ' + esc(reg) + '</div><h3>' + esc(m.name) + '</h3>' +
        (m.intro ? '<p>' + esc(m.intro) + '</p>' : '') +
        ((m.services || []).length ? '<p style="font-size:14px;color:var(--mute)">' + esc(m.services.join(' · ')) + '</p>' : '') +
        '</div><div class="st">' + stat(m.year, T.since) + stat(m.team, T.team) + stat(m.electricians, T.elec) + stat(m.projects, T.proj) + stat(m.kwp, T.kwp) + '</div>' +
        '<div class="reg">✓ ' + esc(T.ver) + (m.verified ? ' · ' + esc(m.verified) : '') + (m.category === 'partner' ? ' · <a href="' + (lang === 'th' ? '/th' : '') + '/partners.html#partner-' + esc(m.id) + '">' + esc(T.more) + '</a>' : '') + '</div></article>';
    }).join('');
    box.hidden = false;
  });
})();
