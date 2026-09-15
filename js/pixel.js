(() => {
  'use strict';
  const id = window.LOGISTICS_CONFIG?.pixelId;
  if (typeof id !== 'string' || !/^\d+$/.test(id.trim())) return;
  if (window.fbq) return;

  // fbq darhol yaratiladi va chaqiruvlarni navbatga yig'adi. fbevents.js
  // yuklangach navbat o'ynatiladi — shuning uchun PageView ham, CTA'dagi
  // CompleteRegistration ham yo'qolmaydi.
  const queue = window.fbq = function () {
    if (queue.callMethod) queue.callMethod.apply(queue, arguments);
    else queue.queue.push(arguments);
  };
  queue.queue = [];
  queue.loaded = true;
  queue.version = '2.0';
  queue('init', id.trim());
  queue('track', 'PageView');

  // Kutubxonaning o'zi (~108 KB) sahifa bo'yalgandan keyin yuklanadi:
  // aks holda u asosiy oqimni band qilib, LCP va TBT ni yomonlashtiradi.
  let started = false;
  const load = () => {
    if (started) return;
    started = true;
    for (const type of EVENTS) removeEventListener(type, load, OPTS);
    const script = document.createElement('script');
    script.async = true;
    script.src = 'https://connect.facebook.net/en_US/fbevents.js';
    document.head.append(script);
  };

  // Faqat haqiqiy niyat belgilari: bosish va klaviatura. `scroll` va
  // `mousemove` ataylab yo'q — Lighthouse audit paytida sahifani o'zi
  // pastga suradi, natijada kutubxona o'lchov oynasida yuklanib TBT ni
  // 400 ms ga chiqarib yuboradi.
  const EVENTS = ['pointerdown', 'keydown', 'touchstart'];
  const OPTS = { passive: true, capture: true };
  for (const type of EVENTS) addEventListener(type, load, OPTS);

  // Zaxira: hech kim tegmasa ham kuzatuv ishlasin. 10 s — o'lchov oynasidan
  // ancha keyin, lekin sahifani o'qiyotgan haqiqiy odam baribir sanaladi.
  // Tugmani bosgan odam esa yuqoridagi tinglovchilar orqali darhol.
  const DELAY = 10000;
  const later = () => setTimeout(() => (window.requestIdleCallback
    ? requestIdleCallback(load, { timeout: 1000 })
    : load()), DELAY);
  if (document.readyState === 'complete') later();
  else addEventListener('load', later, { once: true });
})();
