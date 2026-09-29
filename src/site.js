/*
 * Genusswerk – Seitenlogik.
 *
 * Scroll-Regel (Vorgabe): Nach einem Neuladen startet die Seite immer oben.
 * Der erste Teil davon steht als Inline-Script im <head> (template.html),
 * damit der Browser die alte Scrollposition gar nicht erst wiederherstellt.
 * Hier: Anker-Links scrollen, ohne einen #hash in die Adresse zu schreiben.
 * So landet ein späteres Neuladen nicht wieder mitten auf der Seite.
 */
(function () {
  "use strict";

  var ruhig = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Sicherheitsnetz zur Head-Logik: nach dem vollständigen Laden noch einmal nach oben.
  window.addEventListener("load", function () {
    if (window.__gwNachOben) window.scrollTo(0, 0);
  });

  // Anker-Links auf derselben Seite: weich scrollen, URL unverändert lassen.
  document.addEventListener("click", function (e) {
    var a = e.target.closest('a[href^="#"]');
    if (!a) return;
    var id = a.getAttribute("href").slice(1);
    var ziel = id ? document.getElementById(id) : document.body;
    if (!ziel) return;
    e.preventDefault();
    ziel.scrollIntoView({ behavior: ruhig ? "auto" : "smooth", block: "start" });
    if (id) {
      ziel.setAttribute("tabindex", "-1");
      ziel.focus({ preventScroll: true });
    }
    var menue = document.getElementById("menue");
    if (menue) menue.removeAttribute("data-offen");
  });

  // Mobiles Menü.
  var knopf = document.getElementById("menue-knopf");
  if (knopf) {
    knopf.addEventListener("click", function () {
      var menue = document.getElementById("menue");
      var offen = menue.toggleAttribute("data-offen");
      knopf.setAttribute("aria-expanded", String(offen));
    });
  }

  // Öffnungsstatus ("Jetzt geöffnet bis 22:00") aus den Daten im Seiten-JSON.
  var datenEl = document.getElementById("gw-zeiten");
  var statusEl = document.querySelectorAll("[data-status]");
  if (datenEl && statusEl.length) {
    var tage = JSON.parse(datenEl.textContent);
    var jetzt = berlinJetzt();
    var text = status(tage, jetzt);
    statusEl.forEach(function (el) {
      el.textContent = text.label;
      el.setAttribute("data-status", text.offen ? "offen" : "zu");
    });
    var heute = document.querySelector('[data-tag="' + jetzt.tag + '"]');
    if (heute) heute.setAttribute("data-heute", "");
  }

  function berlinJetzt() {
    var teile = new Intl.DateTimeFormat("de-DE", {
      timeZone: "Europe/Berlin", weekday: "short", hour: "2-digit", minute: "2-digit", hour12: false
    }).formatToParts(new Date());
    var get = function (t) { return (teile.find(function (p) { return p.type === t; }) || {}).value; };
    var kurz = get("weekday").replace(".", "");
    return { tag: kurz, minuten: parseInt(get("hour"), 10) % 24 * 60 + parseInt(get("minute"), 10) };
  }

  function min(hhmm) { var p = hhmm.split(":"); return +p[0] * 60 + +p[1]; }

  function status(tage, jetzt) {
    var i = tage.findIndex(function (t) { return t.kurz === jetzt.tag; });
    var heute = tage[i];
    if (heute && !heute.geschlossen) {
      if (jetzt.minuten >= min(heute.von) && jetzt.minuten < min(heute.bis)) {
        return { offen: true, label: "Jetzt geöffnet · bis " + heute.bis + " Uhr" };
      }
      if (jetzt.minuten < min(heute.von)) {
        return { offen: false, label: "Heute ab " + heute.von + " Uhr geöffnet" };
      }
    }
    for (var n = 1; n <= 7; n++) {
      var t = tage[(i + n) % 7];
      if (!t.geschlossen) {
        return { offen: false, label: (heute && heute.geschlossen ? "Heute Ruhetag" : "Jetzt geschlossen") + " · " + t.kurz + " ab " + t.von + " Uhr" };
      }
    }
    return { offen: false, label: "Geschlossen" };
  }

  // Filter der Karte (vegetarisch, vegan, alkoholfrei).
  var filter = document.querySelectorAll("[data-filter]");
  filter.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var aktiv = btn.getAttribute("aria-pressed") !== "true";
      filter.forEach(function (b) { b.setAttribute("aria-pressed", "false"); });
      btn.setAttribute("aria-pressed", String(aktiv));
      var tag = aktiv ? btn.getAttribute("data-filter") : null;
      document.querySelectorAll("[data-tags]").forEach(function (el) {
        el.hidden = tag !== null && el.getAttribute("data-tags").split(" ").indexOf(tag) === -1;
      });
      document.querySelectorAll(".kategorie").forEach(function (k) {
        k.hidden = tag !== null && !k.querySelector("[data-tags]:not([hidden])");
      });
    });
  });
})();
