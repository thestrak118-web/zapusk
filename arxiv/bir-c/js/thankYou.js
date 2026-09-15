(() => {
  'use strict';
  const config = window.LAUNCH_CONFIG || {};
  const syncLanguage = () => { document.documentElement.lang = document.body.dataset.locale || config.locale || 'uz'; };
  syncLanguage();
  new MutationObserver(syncLanguage).observe(document.body, {attributes:true, attributeFilter:['data-locale']});
  const key = 'bir.pendingLead:' + new URL('.', location.href).pathname;
  const panel = document.getElementById('lead-progress');
  const message = document.getElementById('lead-message');
  const retry = document.getElementById('lead-retry');
  let lead = null;
  let pending = false;
  let completed = false;
  try { lead = JSON.parse(sessionStorage.getItem(key)); } catch { /* No stored submission. */ }
  if (!lead || !lead.requestId || !lead.body || Date.now() - lead.createdAt > 3600000) {
    try { sessionStorage.removeItem(key); } catch { /* Storage can be disabled. */ }
    return;
  }
  function state(text, value) {
    panel.hidden = value !== 'error'; panel.dataset.state = value;
    panel.setAttribute('aria-busy', String(value === 'pending'));
    message.textContent = value === 'error' ? text : ''; retry.hidden = value !== 'error';
  }
  async function send() {
    if (pending || completed) return;
    pending = true;
    state('', 'pending');
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 25000);
    try {
      const url = new URL(config.sheetUrl);
      if (url.protocol !== 'https:' || url.hostname !== 'script.google.com' || !/^\/macros\/s\/[\w-]+\/exec$/.test(url.pathname)) throw Error('Invalid endpoint');
      let body = JSON.stringify(lead.body);
      let headers = {'Content-Type':'text/plain;charset=utf-8'};
      if (lead.transport === 'form-data') {
        body = new FormData(); headers = {};
        for (const [key, value] of Object.entries(lead.body)) body.append(key, value);
      }
      const response = await fetch(url.href, {method:'POST', mode:'cors', credentials:'omit', redirect:'follow', headers, body, signal:controller.signal, keepalive:true});
      if (!response.ok) throw Error('HTTP error');
      const result = await response.json();
      const accepted = result && !result.error && (result.ok === true || result.result === 'success' || result.status === 'success');
      if (!accepted || (result.requestId && result.requestId !== lead.requestId) || (lead.transport !== 'form-data' && result.requestId !== lead.requestId)) throw Error('Unconfirmed submission');
      completed = true;
      try { sessionStorage.removeItem(key); } catch { /* Do not report a successful write as failed. */ }
      state('', 'success');
      if (typeof window.fbq === 'function') window.fbq('track', 'Lead', {content_name:'BIR vebinar', variant:lead.variant}, {eventID:lead.requestId});
      lead = null;
    } catch (error) {
      state(error.name === 'AbortError'
        ? 'Serverdan javob kelmadi. Ariza saqlangani tasdiqlanmadi.'
        : 'Ariza saqlangani tasdiqlanmadi. Qayta yuborib ko‘ring.', 'error');
    } finally { clearTimeout(timeout); pending = false; }
  }
  retry.addEventListener('click', send);
  send();
})();
