(() => {
  'use strict';
  const message = document.querySelector('#thanks-message');
  const status = document.querySelector('#status');
  const channelStatus = document.querySelector('#channel-status');
  const retry = document.querySelector('#retry-submit');
  const telegram = document.querySelector('#telegram');
  const back = document.querySelector('#back-to-webinar');
  if (!message || !status || !retry || !telegram || !back) return;

  const path = new URL('.', location.href).pathname;
  const pendingKey = 'webinar.pending:' + path;
  const confirmationKey = 'webinar.confirmed:' + path;
  const acknowledged = new Set();
  let busy = false;

  function read(key) {
    try { return JSON.parse(sessionStorage.getItem(key) || 'null'); }
    catch { return null; }
  }
  // Rahmat sahifasi yangi tabda ochiladi. sessionStorage har doim ham yangi tabga
  // o'tmaydi, shuning uchun landing arizani localStorage ga ham yozadi. Eski
  // (10 daqiqadan oshgan) yozuv qayta yuborilmaydi.
  const LOCAL_MAX_AGE = 10 * 60 * 1000;
  function readLocal(key) {
    try { return JSON.parse(localStorage.getItem(key) || 'null'); }
    catch { return null; }
  }
  function pending() {
    let lead = read(pendingKey);
    if (!lead) {
      const local = readLocal(pendingKey);
      if (local && Number.isFinite(local.createdAt) && Date.now() - local.createdAt < LOCAL_MAX_AGE) lead = local;
    }
    if (!lead || typeof lead.id !== 'string' || !lead.id || lead.id.length > 100 ||
        typeof lead.name !== 'string' || lead.name.length > 100 || !/\p{L}/u.test(lead.name) ||
        !/^[\p{L}\p{M}\s'‘’ʻʼ`.-]+$/u.test(lead.name) ||
        typeof lead.phone !== 'string' || !/^\+\d{7,18}$/.test(lead.phone) ||
        !Number.isFinite(lead.createdAt) || lead.createdAt <= 0 ||
        typeof lead.timestamp !== 'string' || !lead.timestamp || lead.timestamp.length > 100) return null;
    return lead;
  }
  function text(node, value) { node.textContent = value; node.hidden = !value; }
  function receipt() {
    const saved = read(confirmationKey) || readLocal(confirmationKey);
    return saved?.confirmed === true && Number.isFinite(saved.confirmedAt) ? saved : null;
  }
  function hasPending() {
    return pending() !== null;
  }
  function clearMatchingPending(id) {
    try {
      if (read(pendingKey)?.id === id) sessionStorage.removeItem(pendingKey);
    } catch { /* Acknowledgment remains honest even if browser storage becomes unavailable. */ }
    try {
      if (readLocal(pendingKey)?.id === id) localStorage.removeItem(pendingKey);
    } catch {}
  }
  function showConfirmed() {
    text(message, 'Arizangiz qabul qilindi!');
    text(status, '');
    retry.hidden = true;
    back.hidden = true;
  }
  function showFailure() {
    text(message, '');
    text(status, 'Ariza tasdiqlanmadi. Internet aloqasini tekshirib, qayta yuboring.');
    retry.hidden = false;
    back.hidden = false;
  }
  function endpoint() {
    const raw = window.LOGISTICS_CONFIG?.endpointUrl;
    try {
      if (typeof raw !== 'string' || !raw.trim()) return null;
      const url = new URL(raw.trim(), location.href);
      return ['https:', 'http:'].includes(url.protocol) ? url.href : null;
    } catch { return null; }
  }

  // This channel action is independent of the background request.
  let channel = null;
  try {
    const raw = window.LOGISTICS_CONFIG?.telegramUrl;
    if (typeof raw === 'string' && raw.trim()) {
      const url = new URL(raw.trim());
      if (url.protocol === 'https:' && ['t.me', 'telegram.me'].includes(url.hostname) && url.pathname !== '/') channel = url;
    }
  } catch {}
  if (channel) {
    telegram.href = channel.href;
    telegram.removeAttribute('aria-disabled');
    telegram.removeAttribute('tabindex');
  } else {
    telegram.removeAttribute('href');
    telegram.setAttribute('aria-disabled', 'true');
    telegram.setAttribute('tabindex', '-1');
    if (channelStatus) text(channelStatus, 'Telegram kanali havolasi hali qo‘shilmagan.');
  }

  async function send() {
    if (busy) return;
    const lead = pending();
    if (!lead) {
      retry.hidden = true;
      if (!hasPending() && receipt()) showConfirmed();
      else {
        text(message, 'Ariza qoldirish uchun asosiy sahifaga qayting.');
        back.hidden = false;
      }
      return;
    }
    const confirmed = receipt();
    if (acknowledged.has(lead.id) || confirmed?.id === lead.id) {
      clearMatchingPending(lead.id);
      showConfirmed();
      return;
    }
    const url = endpoint();
    if (!url) { showFailure(); return; }
    busy = true;
    retry.hidden = true;
    retry.disabled = true;
    back.hidden = true;
    text(message, '');
    text(status, '');
    const controller = new AbortController();
    const timeout = window.setTimeout(() => controller.abort(), 20000);
    try {
      const payload = new FormData();
      const sheetName = window.LOGISTICS_CONFIG?.sheetName;
      if (typeof sheetName === 'string' && sheetName.trim()) payload.set('sheetName', sheetName.trim());
      payload.set('Ism', lead.name);
      payload.set('Telefon raqam', lead.phone);
      payload.set("Royhatdan o'tgan vaqti", lead.timestamp);
      const response = await fetch(url, {
        method: 'POST', body: payload, credentials: 'omit', cache: 'no-store',
        signal: controller.signal, keepalive: true
      });
      if (!response.ok) throw new Error('HTTP response rejected');
      const result = await response.json();
      if (!result || !(result.ok === true || result.success === true || result.status === 'success' || result.result === 'success')) {
        throw new Error('Submission was not acknowledged');
      }
      acknowledged.add(lead.id);
      // A late response for an older lead must not erase a newer handoff.
      const latest = pending();
      if (!latest || latest.id === lead.id) {
        const stamp = JSON.stringify({ id: lead.id, confirmed: true, confirmedAt: Date.now() });
        try { sessionStorage.setItem(confirmationKey, stamp); }
        catch { /* Do not turn a successful POST into a retry because storage failed. */ }
        // Landing tabi ochiq qoladi — o'sha ariza qayta yuborilsa, yangi tab buni ko'rsin.
        try { localStorage.setItem(confirmationKey, stamp); } catch {}
        clearMatchingPending(lead.id);
        showConfirmed();
      }
    } catch {
      if (pending()?.id === lead.id) showFailure();
    } finally {
      window.clearTimeout(timeout);
      busy = false;
      retry.disabled = false;
      const latest = pending();
      if (latest && latest.id !== lead.id) send();
    }
  }
  // Meta CompleteRegistration bu yerda EMAS — landing (js/main.js) forma
  // yuborilganda o'zi yuboradi va bu sahifani yangi tabda ochadi.

  retry.addEventListener('click', send);
  window.addEventListener('pageshow', event => { if (event.persisted) send(); });
  send();
})();
