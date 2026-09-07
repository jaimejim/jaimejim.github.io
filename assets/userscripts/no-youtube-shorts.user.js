// ==UserScript==
// @name         No YouTube Shorts (redirect + hide bottom-bar Shorts tab)
// @description  Redirects every /shorts/ URL to the normal watch player AND removes the "Shorts" item from the bottom navigation bar. Works on youtube.com and m.youtube.com.
// @match        *://*.youtube.com/*
// @run-at       document-start
// @version      1.1
// ==/UserScript==
(function () {
  "use strict";

  // 1) Redirect any Short into the regular player (kills the swipe feed).
  const redirect = () => {
    const m = location.pathname.match(/^\/shorts\/([\w-]+)/);
    if (m) location.replace("/watch?v=" + m[1]);
  };

  // 2) Remove the "Shorts" tab from the bottom pivot bar (mobile) and any
  //    Shorts entry in the desktop sidebar. YouTube re-renders these, so we
  //    re-run on every DOM mutation.
  const hideShortsNav = () => {
    // Mobile bottom bar items + desktop guide/mini-guide entries.
    const items = document.querySelectorAll(
      "ytm-pivot-bar-item-renderer, a.pivot-bar-item-tab, " +
      "ytd-guide-entry-renderer, ytd-mini-guide-entry-renderer, a.pivot-shorts"
    );
    items.forEach((el) => {
      const label = (el.textContent || "").toLowerCase();
      const aria = (el.getAttribute("aria-label") || "").toLowerCase();
      const href = el.querySelector && el.querySelector("a")
        ? (el.querySelector("a").getAttribute("href") || "")
        : (el.getAttribute("href") || "");
      const isShorts =
        href.includes("/shorts") ||
        /(^|\s)shorts(\s|$)/.test(label) ||
        aria === "shorts";
      if (isShorts) {
        // Hide the tappable item and, on the pivot bar, its wrapper too.
        el.style.display = "none";
        const wrap = el.closest("ytm-pivot-bar-item-renderer, .pivot-bar-item-tab");
        if (wrap) wrap.style.display = "none";
      }
    });
  };

  const run = () => { redirect(); hideShortsNav(); };
  run();

  // YouTube is a single-page app: catch in-app navigation and re-renders.
  new MutationObserver(run).observe(document, { subtree: true, childList: true });
})();
