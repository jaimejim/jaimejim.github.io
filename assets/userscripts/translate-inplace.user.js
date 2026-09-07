// ==UserScript==
// @name         In-place translate to English (skips en/es/it)
// @description  Translates the visible text of any page whose language is NOT English/Spanish/Italian into English, in place, leaving HTML/links/CSS intact. Batches requests (translate_a/t) to stay under the free endpoint's rate limit. Shows a small status pill.
// @match        *://*/*
// @run-at       document-idle
// @version      3.0
// @connect      translate.googleapis.com
// @grant        GM.xmlHttpRequest
// @grant        GM_xmlhttpRequest
// ==/UserScript==
(function () {
  "use strict";

  const TL = "en";
  const SKIP = new Set(["en", "es", "it"]);
  const primary = (c) => (c || "").split(/[-_]/)[0].toLowerCase();

  // batching limits per request
  const MAX_NODES = 30;
  const MAX_ENC = 1500;   // approx encoded query budget
  const CONC = 3;         // concurrent requests

  // ---- status pill (phone feedback, no console) ----
  let pill;
  const setPill = (t, c) => {
    if (!pill) {
      pill = document.createElement("div");
      Object.assign(pill.style, {
        position: "fixed", top: "8px", right: "8px", zIndex: "2147483647",
        padding: "4px 8px", fontSize: "12px", fontWeight: "600", color: "#fff",
        borderRadius: "12px", boxShadow: "0 1px 4px rgba(0,0,0,.3)",
        pointerEvents: "none", opacity: "0.9", transition: "opacity .5s",
      });
      (document.body || document.documentElement).appendChild(pill);
    }
    pill.textContent = t; pill.style.background = c;
  };
  const hidePill = () => { if (pill) { pill.style.opacity = "0"; setTimeout(() => pill && pill.remove(), 600); } };

  // ---- cross-origin GET (GM bypasses CORS, else fetch) ----
  const gmGet = (url) =>
    new Promise((resolve, reject) => {
      const gm =
        (typeof GM_xmlhttpRequest !== "undefined" && GM_xmlhttpRequest) ||
        (typeof GM !== "undefined" && GM && GM.xmlHttpRequest);
      if (gm) {
        gm({ method: "GET", url,
          onload: (r) => (r.status >= 200 && r.status < 300 ? resolve(r.responseText) : reject(new Error("http " + r.status))),
          onerror: () => reject(new Error("gm error")),
          ontimeout: () => reject(new Error("gm timeout")) });
      } else {
        fetch(url).then((r) => (r.ok ? r.text() : Promise.reject(new Error("http " + r.status)))).then(resolve).catch(reject);
      }
    });

  const BASE = "https://translate.googleapis.com/translate_a/t?client=dict-chrome-ex&sl=auto&tl=" + TL;
  const cache = new Map();

  // Translate an array of strings -> array of {text, src} aligned by index.
  async function translateBatch(texts) {
    const url = BASE + texts.map((t) => "&q=" + encodeURIComponent(t)).join("");
    const arr = JSON.parse(await gmGet(url));
    // shape: [[translation, srcLang], ...]  (or a bare string for edge cases)
    return texts.map((_, i) => {
      const e = arr[i];
      if (Array.isArray(e)) return { text: e[0], src: primary(e[1]) };
      return { text: typeof e === "string" ? e : null, src: "" };
    });
  }

  // ---- node collection ----
  const SKIP_TAGS = new Set(["SCRIPT", "STYLE", "NOSCRIPT", "CODE", "PRE", "TEXTAREA", "KBD", "SAMP"]);
  const done = new WeakSet();
  const hasLetters = (s) => /[A-Za-zÀ-ÿ]/.test(s);
  function collect(root) {
    const nodes = [];
    const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode(n) {
        if (done.has(n)) return NodeFilter.FILTER_REJECT;
        const p = n.parentElement;
        if (!p || SKIP_TAGS.has(p.tagName) || p.isContentEditable) return NodeFilter.FILTER_REJECT;
        const t = n.nodeValue.trim();
        if (t.length < 2 || !hasLetters(t)) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      },
    });
    let n; while ((n = w.nextNode())) nodes.push(n);
    return nodes;
  }

  // ---- batch queue ----
  let active = 0, ok = 0, fail = 0;
  const batches = [];
  function enqueue(nodes) {
    let cur = [], len = 0;
    for (const n of nodes) {
      const t = n.nodeValue.trim().replace(/\s+/g, " ");
      const l = encodeURIComponent(t).length + 4;
      if (cur.length >= MAX_NODES || len + l > MAX_ENC) { if (cur.length) batches.push(cur); cur = []; len = 0; }
      cur.push(n); len += l;
    }
    if (cur.length) batches.push(cur);
  }
  function refresh() {
    if (active === 0 && batches.length === 0) { ok > 0 ? hidePill() : setPill("translate blocked", "#c0392b"); }
    else if (fail >= 2 && ok === 0) setPill("translate blocked", "#c0392b");
    else setPill("translating…", "#1a73e8");
  }
  function pump() {
    while (active < CONC && batches.length) {
      const batch = batches.shift();
      active++;
      const texts = batch.map((n) => n.nodeValue.trim().replace(/\s+/g, " "));
      translateBatch(texts)
        .then((res) => {
          batch.forEach((node, i) => {
            const r = res[i];
            if (r && r.text && !SKIP.has(r.src) && node.parentElement) {
              const orig = node.nodeValue;
              node.nodeValue = orig.replace(orig.trim(), r.text);
            }
          });
          ok++;
        })
        .catch(() => { fail++; })
        .finally(() => { active--; refresh(); pump(); });
    }
  }
  function process(root) {
    const nodes = collect(root);
    if (!nodes.length) return;
    nodes.forEach((n) => done.add(n));
    enqueue(nodes);
    setPill("translating…", "#1a73e8");
    pump();
  }

  // ---- gate: decide if the page needs translating ----
  async function shouldTranslate() {
    const declared = primary(document.documentElement.lang);
    if (declared) return !SKIP.has(declared);
    const sample = (document.body.innerText || "").replace(/\s+/g, " ").trim().slice(0, 400);
    if (sample.length < 200) return false;
    try {
      const [r] = await translateBatch([sample]);
      return r && r.src && !SKIP.has(r.src);
    } catch (e) { return false; }
  }

  shouldTranslate().then((go) => {
    if (!go) return;
    process(document.body);
    // debounce late-loading content into fewer batches
    let pending = [], timer = null;
    const flush = () => { const p = pending; pending = []; timer = null; p.forEach((n) => process(n)); };
    new MutationObserver((muts) => {
      for (const m of muts) m.addedNodes.forEach((n) => { if (n.nodeType === 1) pending.push(n); });
      if (pending.length && !timer) timer = setTimeout(flush, 400);
    }).observe(document.body, { childList: true, subtree: true });
  });
})();
