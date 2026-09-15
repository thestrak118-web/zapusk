/* ============================================================
   Zapusk landing — umumiy skript (taymer, CTA, analitika)
   ============================================================ */
(function () {
  'use strict';

  var CFG = window.SITE_CONFIG || {};
  var VARIANT = document.body.dataset.variant || '1';

  /* ---------- 1. Shoshilinch taymer ------------------------------------ */
  var STORE_KEY = 'zapusk_deadline_v' + VARIANT;

  function deadline() {
    var minutes = Number(CFG.timerMinutes) || 120;
    var saved = Number(localStorage.getItem(STORE_KEY));
    var now = Date.now();
    if (!saved || saved <= now) {
      saved = now + minutes * 60000;
      try { localStorage.setItem(STORE_KEY, String(saved)); } catch (e) {}
    }
    return saved;
  }

  function pad(n) { return n < 10 ? '0' + n : String(n); }

  function tick(nodes, end) {
    var left = Math.max(0, end - Date.now());
    var total = Math.floor(left / 1000);
    var h = Math.floor(total / 3600);
    var m = Math.floor((total % 3600) / 60);
    var s = total % 60;

    nodes.forEach(function (el) {
      if (el.dataset.timer === 'hms') {
        var slots = el.querySelectorAll('[data-slot]');
        if (slots.length === 3) {
          slots[0].textContent = pad(h);
          slots[1].textContent = pad(m);
          slots[2].textContent = pad(s);
        } else {
          el.textContent = pad(h) + ':' + pad(m) + ':' + pad(s);
        }
      } else {
        /* mm:ss — Figma'dagi "01:59" ko'rinishi */
        el.textContent = pad(h * 60 + m) + ':' + pad(s);
      }
    });

    if (left <= 0) { localStorage.removeItem(STORE_KEY); startTimer(); }
  }

  var timerId = null;
  function startTimer() {
    var nodes = [].slice.call(document.querySelectorAll('[data-timer]'));
    if (!nodes.length) return;
    var end = deadline();
    clearInterval(timerId);
    tick(nodes, end);
    timerId = setInterval(function () { tick(nodes, end); }, 1000);
  }
  startTimer();

  document.addEventListener('visibilitychange', function () {
    if (!document.hidden) startTimer();
  });

  /* ---------- 2. CTA havolalari ---------------------------------------- */
  function ctaHref(place) {
    var url = CFG.ctaUrl || '#';
    if (url === '#') return url;
    var sep = url.indexOf('?') === -1 ? '?' : '&';
    return url + sep + 'start=v' + VARIANT + '_' + place;
  }

  [].forEach.call(document.querySelectorAll('[data-cta]'), function (el) {
    var place = el.dataset.cta || 'cta';
    if (el.tagName === 'A') {
      el.href = ctaHref(place);
      el.target = '_blank';
      el.rel = 'noopener';
    }
    el.addEventListener('click', function () { track('cta_click', place); });
  });

  /* ---------- 3. Analitika (ixtiyoriy) --------------------------------- */
  function track(name, label) {
    if (typeof window.gtag === 'function') window.gtag('event', name, { label: label });
    if (typeof window.fbq === 'function') window.fbq('trackCustom', name, { label: label });
    if (typeof window.ym === 'function' && CFG.metrikaId) window.ym(CFG.metrikaId, 'reachGoal', name);
  }
})();
