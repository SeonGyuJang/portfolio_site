// Image viewer for awards / papers / certificates
(function () {
  const dialog = document.getElementById('gallery');
  if (!dialog) return;
  const titleEl = document.getElementById('galleryTitle');
  const body = document.getElementById('galleryBody');

  document.addEventListener('click', function (e) {
    const btn = e.target.closest('.js-gallery');
    if (!btn) return;
    let images = [];
    try { images = JSON.parse(btn.dataset.images || '[]'); } catch (_) { images = []; }
    titleEl.textContent = btn.dataset.title || '';
    body.replaceChildren(...images.map(function (src) {
      const img = document.createElement('img');
      img.src = src;
      img.alt = btn.dataset.title || '';
      img.loading = 'lazy';
      return img;
    }));
    dialog.showModal();
  });

  dialog.querySelector('.gallery-close').addEventListener('click', function () { dialog.close(); });
  dialog.addEventListener('click', function (e) { if (e.target === dialog) dialog.close(); });
})();
