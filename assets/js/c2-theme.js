/* Clock-based auto theme for jaime.win.
   Auto mode: light between sunrise (~07:00) and a seasonal sunset.
   Sunset ranges 17:00 (Dec solstice) to 21:00 (Jun solstice), interpolated by day-of-year.
   No geolocation. No prefers-color-scheme. No deps. */
(function () {
  var KEY = "theme";                    // "auto" | "light" | "dark"
  var stored = null;
  try { stored = localStorage.getItem(KEY); } catch (e) {}
  var mode = stored || "auto";

  function seasonalSunsetHour(now) {
    // Day-of-year, 0..365
    var start = new Date(now.getFullYear(), 0, 0);
    var diff = now - start;
    var doy = Math.floor(diff / 86400000);
    // Solar term: peak around Jun 21 (doy 172), trough around Dec 21 (doy 355)
    // cos(2pi*(doy - 172)/365) is 1 in June, -1 in December
    var season = Math.cos(2 * Math.PI * (doy - 172) / 365);
    // Map [-1, 1] to [17, 21] hours
    return 19 + 2 * season;
  }

  function computed() {
    var now = new Date();
    var h = now.getHours() + now.getMinutes() / 60;
    var sunrise = 7;
    var sunset = seasonalSunsetHour(now);
    return (h >= sunrise && h < sunset) ? "light" : "dark";
  }

  function apply(m) {
    var effective = (m === "auto") ? computed() : m;
    document.documentElement.setAttribute("data-theme", effective);
    var toggle = document.querySelector(".theme-toggle");
    if (toggle) {
      toggle.querySelectorAll("button").forEach(function (b) {
        b.setAttribute("aria-pressed", b.dataset.mode === m ? "true" : "false");
      });
    }
  }

  // Apply immediately (before DOM) to prevent flash
  apply(mode);

  // Re-check every 10 min when in auto mode, in case user leaves tab open past sunset
  setInterval(function () { if (mode === "auto") apply(mode); }, 600000);

  document.addEventListener("DOMContentLoaded", function () {
    apply(mode); // re-apply now that toggle buttons exist
    var toggle = document.querySelector(".theme-toggle");
    if (!toggle) return;
    toggle.addEventListener("click", function (e) {
      var btn = e.target.closest("button[data-mode]");
      if (!btn) return;
      mode = btn.dataset.mode;
      try { localStorage.setItem(KEY, mode); } catch (err) {}
      apply(mode);
    });
  });
})();
