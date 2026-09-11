(() => {
  const id = window.LAUNCH_CONFIG?.pixelId;
  if (!id || !/^\d+$/.test(id)) return;
  const fbq = window.fbq = window.fbq || function () {
    fbq.callMethod ? fbq.callMethod.apply(fbq, arguments) : fbq.queue.push(arguments);
  };
  if (!window._fbq) window._fbq = fbq;
  fbq.push = fbq; fbq.loaded = true; fbq.version = '2.0'; fbq.queue = fbq.queue || [];
  const script = document.createElement('script');
  script.defer = true;
  script.src = 'https://connect.facebook.net/en_US/fbevents.js';
  document.body.appendChild(script);
  fbq('init', id); fbq('track', 'PageView');
})();
