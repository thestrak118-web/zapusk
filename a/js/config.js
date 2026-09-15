/* ============================================================
   Sozlamalar — saytni ishga tushirishdan oldin shu faylni to'ldiring.
   Ikkita blok bor: ro'yxatdan o'tish oqimi va sahifa sozlamalari.
   ============================================================ */

/* 1. Ro'yxatdan o'tish (js/main.js + thankYou.html).
      Bo'sh qoldirilsa — forma halol ravishda o'chirilgan holatda qoladi,
      hech qanday so'rov yuborilmaydi. Eski loyihaning havolasi
      QO'YILMAYDI — yangi loyihaning o'z qiymatlari kerak. */
window.LOGISTICS_CONFIG = {
  endpointUrl: 'https://script.google.com/macros/s/AKfycbz7G8GKmjL0wIHd_gVgzv_AIqyBhXgGV9n1yjIDh173WqcDieJnX--xQgEJT4tropdM/exec',
  telegramUrl: 'https://t.me/+GzsmqPGpcew2MjZi',
  pixelId:     '2982763675408670',  /* Meta Pixel */
  sheetName:   ''    /* ⚠ TO'LDIRILISHI SHART — endpoint bo'lmasa
                        MISSING_SHEET xatosi qaytaradi */
};

/* 2. Sahifaning o'z sozlamalari (js/app.js — taymer, analitika). */
window.SITE_CONFIG = {
  /* Vebinar sanasi — sarlavhadagi matn va analitika uchun. */
  eventDate: '2026-09-19T20:00:00+05:00',

  /* Shoshilinch taymer necha daqiqadan boshlanadi (sahifada taymer bo'lsa). */
  timerMinutes: 2,

  /* Analitika (ixtiyoriy) — bo'sh qoldirilsa hech narsa yuklanmaydi. */
  metrikaId: '',
  pixelId: ''
};
