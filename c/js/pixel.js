(() => {
  'use strict';
  const id = window.LOGISTICS_CONFIG?.pixelId;
  if (typeof id !== 'string' || !/^\d+$/.test(id.trim())) return;
  if (window.fbq) return;
  const queue = window.fbq = function () {
    if (queue.callMethod) queue.callMethod.apply(queue, arguments);
    else queue.queue.push(arguments);
  };
  queue.queue = [];
  queue.loaded = true;
  queue.version = '2.0';
  const script = document.createElement('script');
  script.async = true;
  script.src = 'https://connect.facebook.net/en_US/fbevents.js';
  document.head.append(script);
  queue('init', id.trim());
  queue('track', 'PageView');
})();
