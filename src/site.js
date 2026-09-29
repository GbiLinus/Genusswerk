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
  var kopf = document.getElementById("kopf");

  // Sicherheitsnetz zur Head-Logik: nach dem vollständigen Laden noch einmal nach oben.
  window.addEventListener("load", function () {
    if (window.__gwNachOben) window.scrollTo(0, 0);
  });

  // Höhe des Kopfs für die klebende Leiste der Karte.
  function kopfHoehe() {
    if (kopf) document.documentElement.style.setProperty("--kopf-hoehe", kopf.getBoundingClientRect().bottom + "px");
  }
  kopfHoehe();
  window.addEventListener("resize", kopfHoehe);

  // Kopf bekommt Hintergrund, sobald die Seite gescrollt ist.
  function kopfZustand() {
    if (!kopf) return;
    kopf.toggleAttribute("data-fest", window.scrollY > 24);
    kopfHoehe();
  }
  kopfZustand();
  window.addEventListener("scroll", kopfZustand, { passive: true });

  // Anker-Links auf derselben Seite: weich scrollen, URL unverändert lassen.
  document.addEventListener("click", function (e) {
    var a = e.target.closest('a[href^="#"]');
    if (!a) return;
    var id = a.getAttribute("href").slice(1);
    var ziel = id ? document.getElementById(id) : document.body;
    if (!ziel) return;
    e.preventDefault();
    schliesseMenue();
    var y = ziel.getBoundingClientRect().top + window.scrollY - abstandOben(ziel);
    window.scrollTo({ top: Math.max(0, y), behavior: ruhig ? "auto" : "smooth" });
    if (id) {
      ziel.setAttribute("tabindex", "-1");
      ziel.focus({ preventScroll: true });
    }
  });

  function abstandOben(ziel) {
    var leiste = document.getElementById("karte-leiste");
    var h = kopf ? kopf.getBoundingClientRect().height : 0;
    if (leiste && ziel.closest(".karte-seite")) h += leiste.getBoundingClientRect().height;
    return h + 12;
  }

  // Mobiles Menü.
  var knopf = document.getElementById("menue-knopf");
  var menue = document.getElementById("menue");
  function schliesseMenue() {
    if (!menue) return;
    menue.removeAttribute("data-offen");
    if (knopf) knopf.setAttribute("aria-expanded", "false");
  }
  if (knopf && menue) {
    knopf.addEventListener("click", function () {
      var offen = menue.toggleAttribute("data-offen");
      knopf.setAttribute("aria-expanded", String(offen));
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && menue.hasAttribute("data-offen")) { schliesseMenue(); knopf.focus(); }
    });
  }

  // Lichtlinien gehen an, wenn sie ins Bild kommen. Die Schallplatte dreht nur, solange sie sichtbar ist.
  if ("IntersectionObserver" in window) {
    var licht = new IntersectionObserver(function (eintraege) {
      eintraege.forEach(function (x) {
        if (x.isIntersecting) { x.target.setAttribute("data-an", ""); licht.unobserve(x.target); }
      });
    }, { rootMargin: "0px 0px -15% 0px" });
    document.querySelectorAll(".lichtlinie").forEach(function (el) { licht.observe(el); });

    var platte = new IntersectionObserver(function (eintraege) {
      eintraege.forEach(function (x) { x.target.toggleAttribute("data-laeuft", x.isIntersecting); });
    });
    document.querySelectorAll(".platte").forEach(function (el) { platte.observe(el); });

    // Kartenseite: aktuelle Kategorie in der Sprungleiste markieren.
    var sprung = document.querySelector(".sprung");
    if (sprung) {
      var links = {};
      sprung.querySelectorAll("a").forEach(function (a) { links[a.getAttribute("href").slice(1)] = a; });
      var aktuell = new IntersectionObserver(function (eintraege) {
        eintraege.forEach(function (x) {
          if (!x.isIntersecting) return;
          Object.keys(links).forEach(function (k) { links[k].removeAttribute("aria-current"); });
          var a = links[x.target.id];
          if (a) {
            a.setAttribute("aria-current", "true");
            sprung.scrollTo({ left: a.offsetLeft - 16, behavior: ruhig ? "auto" : "smooth" });
          }
        });
      }, { rootMargin: "-30% 0px -60% 0px" });
      document.querySelectorAll(".kategorie").forEach(function (k) { aktuell.observe(k); });
    }
  } else {
    document.querySelectorAll(".lichtlinie").forEach(function (el) { el.setAttribute("data-an", ""); });
  }

  // Funkeln der Gläser anhalten, wenn Bewegung reduziert werden soll.
  if (ruhig) document.querySelectorAll("svg.glaeser").forEach(function (s) { if (s.pauseAnimations) s.pauseAnimations(); });

  // Öffnungsstatus ("Jetzt geöffnet bis 22:00 Uhr") aus den Daten im Seiten-JSON.
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
        return { offen: true, label: "Jetzt geöffnet bis " + heute.bis + " Uhr" };
      }
      if (jetzt.minuten < min(heute.von)) {
        return { offen: false, label: "Heute ab " + heute.von + " Uhr geöffnet" };
      }
    }
    for (var n = 1; n <= 7; n++) {
      var t = tage[(i + n) % 7];
      if (!t.geschlossen) {
        var tagName = n === 1 ? "morgen" : "am " + t.tag;
        return { offen: false, label: (heute && heute.geschlossen ? "Heute Ruhetag, " : "Jetzt geschlossen, ") + tagName + " ab " + t.von + " Uhr" };
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
        k.hidden = tag !== null && !k.querySelector(".gericht:not([hidden])");
      });
      document.querySelectorAll(".sprung a").forEach(function (a) {
        var k = document.getElementById(a.getAttribute("href").slice(1));
        a.hidden = !!(k && k.hidden);
      });
    });
  });
})();
