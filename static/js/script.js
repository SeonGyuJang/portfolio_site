// Detail view, scroll reveal and active-section highlight
(function () {
  // ── detail dialog ──
  const dialog = document.getElementById('detail');
  const body = document.getElementById('detailBody');
  let lastFocus = null;

  function openDetail(entry) {
    const tpl = document.getElementById(entry.dataset.detail);
    if (!tpl || !dialog) return;
    body.replaceChildren(tpl.content.cloneNode(true));
    lastFocus = entry;
    dialog.showModal();
    dialog.scrollTop = 0;
  }

  if (dialog) {
    document.addEventListener('click', function (e) {
      const entry = e.target.closest('.entry.clickable');
      if (!entry || e.target.closest('a')) return;   // inline links keep working
      openDetail(entry);
    });
    document.addEventListener('keydown', function (e) {
      const entry = e.target.closest && e.target.closest('.entry.clickable');
      if (entry && (e.key === 'Enter' || e.key === ' ') && e.target === entry) {
        e.preventDefault();
        openDetail(entry);
      }
    });
    dialog.querySelector('.detail-close').addEventListener('click', function () { dialog.close(); });
    dialog.addEventListener('click', function (e) { if (e.target === dialog) dialog.close(); });
    dialog.addEventListener('close', function () { if (lastFocus) lastFocus.focus({ preventScroll: true }); });
  }

  // ── reveal on scroll ──
  const reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }

  // ── active nav link ──
  const links = Array.from(document.querySelectorAll('.nav a[href^="#"]'));
  const sections = links.map(function (a) { return document.querySelector(a.getAttribute('href')); }).filter(Boolean);
  if (sections.length && 'IntersectionObserver' in window) {
    const spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        links.forEach(function (a) { a.classList.toggle('active', a.getAttribute('href') === '#' + en.target.id); });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    sections.forEach(function (s) { spy.observe(s); });
  }
})();
