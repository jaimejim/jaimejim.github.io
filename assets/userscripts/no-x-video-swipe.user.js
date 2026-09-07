// ==UserScript==
// @name         No X video swipe feed (viewer stays, swipe is dead)
// @description  Keeps X's full-screen video viewer (/mediaViewer) so you can tap a video in the feed and watch it big with sound, but kills the vertical swipe that feeds you the next video, and the next, and the next. Taps, horizontal swipes (multi-image tweets) and the close button still work. Works on x.com and twitter.com.
// @match        *://*.x.com/*
// @match        *://*.twitter.com/*
// @run-at       document-start
// @version      2.0
// ==/UserScript==
(function () {
  "use strict";

  // The swipe feed lives at:  /<user>/status/<id>/mediaViewer?currentTweet=...
  // Swiping up/down changes currentTweet. We block the gesture itself and, as a
  // backstop, snap back if currentTweet changes anyway.
  const VIEWER = /^\/[^/]+\/status\/\d+\/mediaViewer/;
  const inViewer = () => VIEWER.test(location.pathname);

  // ---- 1) Gesture blocking (only while the viewer is open) ----
  // Listeners are on window in the capture phase, so they run before React's
  // root listener; stopImmediatePropagation means X never sees the event.
  const THRESH = 8; // px before we decide a touch is a vertical swipe
  let sx = 0, sy = 0, vertical = false;

  const onTouchStart = (e) => {
    if (!inViewer()) return;
    const t = e.touches[0];
    sx = t.clientX; sy = t.clientY; vertical = false;
  };
  const onTouchMove = (e) => {
    if (!inViewer()) return;
    const t = e.touches[0];
    const dx = Math.abs(t.clientX - sx), dy = Math.abs(t.clientY - sy);
    if (!vertical && dy > THRESH && dy > dx) vertical = true;
    if (vertical) { e.stopImmediatePropagation(); e.preventDefault(); }
  };
  const onTouchEnd = (e) => {
    if (!inViewer()) return;
    // Swallow the end of a vertical swipe too, so X can't act on the release.
    if (vertical) { e.stopImmediatePropagation(); e.preventDefault(); }
    vertical = false;
  };
  const onWheel = (e) => {
    if (!inViewer()) return;
    if (Math.abs(e.deltaY) > Math.abs(e.deltaX)) { e.stopImmediatePropagation(); e.preventDefault(); }
  };
  const onKey = (e) => {
    if (!inViewer()) return;
    if (e.key === "ArrowUp" || e.key === "ArrowDown" || e.key === "PageUp" || e.key === "PageDown") {
      e.stopImmediatePropagation(); e.preventDefault();
    }
  };

  const opts = { capture: true, passive: false };
  window.addEventListener("touchstart", onTouchStart, opts);
  window.addEventListener("touchmove", onTouchMove, opts);
  window.addEventListener("touchend", onTouchEnd, opts);
  window.addEventListener("touchcancel", onTouchEnd, opts);
  window.addEventListener("wheel", onWheel, opts);
  window.addEventListener("keydown", onKey, opts);

  // ---- 2) URL backstop ----
  // Remember the tweet the viewer opened on. X sets currentTweet itself after
  // load, so the anchor is the first non-empty value we see, not the entry URL.
  let anchorPath = "", anchorTweet = "", last = "";
  const check = () => {
    if (location.href === last) return;
    last = location.href;
    if (!inViewer()) { anchorPath = ""; anchorTweet = ""; return; }
    const path = location.pathname.match(VIEWER)[0];
    const tweet = new URLSearchParams(location.search).get("currentTweet") || "";
    if (!anchorPath) { anchorPath = path; anchorTweet = tweet; return; }
    if (!anchorTweet && tweet) { anchorTweet = tweet; return; }
    if (path !== anchorPath || (tweet && tweet !== anchorTweet)) {
      // X advanced to another video despite the gesture block: snap back.
      history.back();
    }
  };
  check();
  new MutationObserver(check).observe(document, { subtree: true, childList: true });
  setInterval(check, 400); // cheap backstop for pure URL-only changes
})();
