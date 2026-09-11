(() => {
  'use strict';
  const config = window.LAUNCH_CONFIG || {};
  const syncLanguage = () => { document.documentElement.lang = document.body.dataset.locale || config.locale || 'uz'; };
  syncLanguage();
  new MutationObserver(syncLanguage).observe(document.body, { attributes: true, attributeFilter: ['data-locale'] });
  const dialog = document.querySelector('#notice');
  const message = document.querySelector('#notice-message');
  const close = () => dialog.close();
  document.querySelector('#notice-close').addEventListener('click', close);
  dialog.addEventListener('click', event => { if (event.target === dialog) close(); });
  function validUrl(value) {
    try { const url = new URL(value); return ['https:', 'http:'].includes(url.protocol) ? url.href : null; }
    catch { return null; }
  }
  function notice(text) { message.textContent = text; dialog.showModal(); }
  document.querySelectorAll('[data-video]').forEach(button => {
    button.addEventListener('click', () => {
      const url = validUrl(config.videos?.[Number(button.dataset.video)]);
      if (url) window.location.assign(url);
      else notice('Video hozircha mavjud emas. Iltimos, keyinroq qayta urinib ko‘ring.');
    });
  });
  const slides = [...document.querySelectorAll('.carousel .review')];
  let current = 0;
  function show(index) {
    current = (index + slides.length) % slides.length;
    slides.forEach((slide, i) => { slide.hidden = i !== current; });
    document.querySelector('#slide-status').textContent = `${current + 1} / ${slides.length}`;
  }
  if (slides.length) {
    document.querySelector('[data-prev]').addEventListener('click', () => show(current - 1));
    document.querySelector('[data-next]').addEventListener('click', () => show(current + 1));
    document.querySelector('.carousel').addEventListener('keydown', e => {
      if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') { e.preventDefault(); show(current + (e.key === 'ArrowLeft' ? -1 : 1)); }
    });
  }
  const timer = document.querySelector('[data-countdown]');
  const deadline = Date.parse(config.registrationDeadline);
  if (timer && Number.isFinite(deadline)) {
    const update = () => {
      const seconds = Math.max(0, Math.ceil((deadline - Date.now()) / 1000));
      timer.textContent = `${String(Math.floor(seconds / 60)).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}`;
      if (!seconds) document.querySelector('#countdown-label').textContent = 'Ro‘yxatdan o‘tish muddati tugadi';
      return seconds;
    };
    if (update()) { const id = setInterval(() => { if (!update()) clearInterval(id); }, 1000); }
  }
})();
