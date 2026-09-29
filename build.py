#!/usr/bin/env python3
"""Erzeugt die Genusswerk-Website aus daten/inhalte.json und src/template.html.

Aufruf aus dem Repo-Root: python3 build.py

Ausgabe:
  index.html              Startseite
  karte/index.html        Speise- und Getränkekarte
  impressum/index.html    Impressum
  datenschutz/index.html  Datenschutz (Platzhalter bis zur Freigabe)
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATEN = json.loads((ROOT / "daten" / "inhalte.json").read_text(encoding="utf-8"))
TEMPLATE = (ROOT / "src" / "template.html").read_text(encoding="utf-8")

NAV = [("#genuss", "Über uns"), ("karte/", "Karte"), ("#events", "Musik"),
       ("#eindruecke", "Impressionen"), ("#besuch", "Besuch")]

FILTER = [("vegetarisch", "Vegetarisch"), ("vegan", "Vegan"), ("alkoholfrei", "Alkoholfrei")]

# Lichtlinien an der Decke wie im Gastraum: links, oben, Länge (in %), Winkel, Einschaltverzögerung (s)
LEDS = [(-6, 48, 52, -7, 0.30), (44, 50, 60, -7, 0.55), (26, 40, 22, 14, 0.80),
        (60, 68, 44, -7, 1.05), (78, 82, 30, -7, 1.25)]


def e(s) -> str:
    return html.escape(str(s))


def slug(s: str) -> str:
    s = s.lower().translate(str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"}))
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def tags(gericht: dict, kategorie: dict) -> list:
    """Normalisiert Tags für den Filter. vegan zählt auch als vegetarisch."""
    raw = set(gericht.get("tags", [])) | set(kategorie.get("tags", []))
    out = {slug(t) for t in raw}
    if "alkoholfrei-moeglich" in out:
        out.add("alkoholfrei")
    if "vegan" in out:
        out.add("vegetarisch")
    return sorted(out)


def preis(gericht: dict) -> str:
    if "preise" in gericht:
        return " ".join(f'<span class="preis-paar"><span class="preis-label">{e(p["label"])}</span> {e(p["preis"])} €</span>'
                        for p in gericht["preise"])
    return f'{e(gericht["preis"])} €'


def finde(karte: str, name: str) -> dict:
    for k in DATEN[karte]["kategorien"]:
        for g in k["gerichte"]:
            if g["name"] == name:
                return g
    raise KeyError(f"Highlight nicht gefunden: {karte} › {name}")


def bild_da(datei: str) -> bool:
    return (ROOT / datei).is_file()


# ---------- Bausteine ----------

def navigation(wurzel: str) -> str:
    links = []
    for href, label in NAV:
        ziel = href if (href.startswith("#") and wurzel == "") else wurzel + href
        links.append(f'<a class="menue-link" href="{e(ziel)}">{e(label)}</a>')
    return "\n      ".join(links)


def decke(leds=LEDS, glaeser=True) -> str:
    """Schwarze Decke mit Lichtlinien, Lüftungsrohr und Gläserregal."""
    striche = "".join(
        f'<span class="led" style="--x:{x}%;--y:{y}%;--l:{l}%;--w:{w}deg;--d:{d}s"></span>'
        for x, y, l, w, d in leds)
    regal = ""
    if glaeser:
        glas = "".join(
            f'<path d="M{x - 7} 14h14M{x} 14v26c-15 4-16 22-14 40h28c2-18 1-36-14-40"/>'
            for x in range(30, 400, 34))
        regal = f"""
    <svg class="glaeser" viewBox="0 0 420 96" aria-hidden="true" focusable="false">
      <defs>
        <linearGradient id="glanz" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="120" y2="0" gradientTransform="translate(-160 0)">
          <stop offset="0" stop-color="#c5cacd" stop-opacity=".22"/>
          <stop offset=".5" stop-color="#ffffff" stop-opacity=".95"/>
          <stop offset="1" stop-color="#c5cacd" stop-opacity=".22"/>
          <animateTransform id="funkeln" attributeName="gradientTransform" type="translate"
            from="-160 0" to="560 0" dur="2.8s" begin="2.2s; funkeln.end+11s" fill="freeze"/>
        </linearGradient>
      </defs>
      <rect x="4" y="8" width="412" height="6" rx="1" fill="#2f3337"/>
      <g class="glaeser-basis" fill="none" stroke="#c5cacd" stroke-opacity=".22" stroke-width="1.4">{glas}</g>
      <g fill="none" stroke="url(#glanz)" stroke-width="1.4">{glas}</g>
    </svg>"""
    return f"""
  <div class="decke" aria-hidden="true">
    <div class="rohr"></div>
    {striche}{regal}
  </div>"""


def theke(inhalt: str) -> str:
    return f"""
  <div class="theke">
    <div class="theke-platte" aria-hidden="true"></div>
    <div class="theke-front">
      <div class="theke-innen">{inhalt}</div>
    </div>
  </div>"""


def lichtlinie() -> str:
    return '<div class="lichtlinie" aria-hidden="true"><span></span></div>'


def zeiten_tabelle() -> str:
    zeilen = []
    for t in DATEN["oeffnungszeiten"]["tage"]:
        wert = t.get("label", "Ruhetag") if t.get("geschlossen") else f'{e(t["von"])} bis {e(t["bis"])} Uhr'
        zeilen.append(f'<tr data-tag="{e(t["kurz"])}"><th scope="row">{e(t["tag"])}</th><td>{wert}</td></tr>')
    return '<table class="zeiten">' + "".join(zeilen) + "</table>"


def zeiten_kurz() -> str:
    """Fasst gleiche Zeiten an Folgetagen zusammen: 'Dienstag bis Freitag: 16 bis 22 Uhr'."""
    def uhr(t):
        return t.removesuffix(":00")
    gruppen = []
    for t in DATEN["oeffnungszeiten"]["tage"]:
        wert = "Ruhetag" if t.get("geschlossen") else f'{uhr(t["von"])} bis {uhr(t["bis"])} Uhr'
        if gruppen and gruppen[-1][2] == wert:
            gruppen[-1][1] = t["tag"]
        else:
            gruppen.append([t["tag"], t["tag"], wert])
    zeilen = "".join(f'<li><span>{e(a) if a == z else e(a) + " bis " + e(z)}</span><span>{e(w)}</span></li>'
                     for a, z, w in gruppen)
    return f'<ul class="zeiten-kurz">{zeilen}</ul>'


def gericht_html(g: dict, k: dict) -> str:
    beschr = f'<p class="gericht-text">{e(g["beschreibung"])}</p>' if g.get("beschreibung") else ""
    t = tags(g, k)
    zeichen = [x for x in t if x in ("vegan", "vegetarisch", "hausmarke", "regional")]
    if "vegan" in zeichen:
        zeichen.remove("vegetarisch")
    namen = {"vegan": "vegan", "vegetarisch": "vegetarisch", "hausmarke": "Hausmarke", "regional": "aus der Region"}
    marker = ('<p class="gericht-tags">' + "".join(f'<span class="tag tag-{x}">{namen[x]}</span>' for x in zeichen) + "</p>"
              if zeichen else "")
    return (f'<li class="gericht" data-tags="{e(" ".join(t))}">'
            f'<div class="gericht-kopf"><h4>{e(g["name"])}</h4><span class="punkte" aria-hidden="true"></span>'
            f'<span class="preis">{preis(g)}</span></div>{beschr}{marker}</li>')


def karte_html(schluessel: str, titel: str) -> str:
    karte = DATEN[schluessel]
    teile = [f'<section class="karte-block" id="{slug(titel)}" aria-labelledby="t-{slug(titel)}">'
             f'<h2 class="etikett" id="t-{slug(titel)}">{e(titel)}</h2><div class="karte-spalten">']
    for k in karte["kategorien"]:
        teile.append(f'<section class="kategorie" id="{slug(titel)}-{slug(k["name"])}"><h3>{e(k["name"])}</h3>')
        if k.get("hinweis"):
            teile.append(f'<p class="kategorie-hinweis">{e(k["hinweis"])}</p>')
        teile.append('<ul class="gerichte">' + "".join(gericht_html(g, k) for g in k["gerichte"]) + "</ul>")
        if k.get("extras"):
            extras = "".join(f'<li>{e(x["name"])} <span>{e(x["preis"])} €</span></li>' for x in k["extras"])
            teile.append(f'<div class="extras" data-tags=""><h4>Extras</h4><ul>{extras}</ul></div>')
        teile.append("</section>")
    teile.append("</div>")
    teile.append(f'<p class="karte-pdf"><a href="{e(karte["pdf"])}" rel="noopener">{e(titel)}karte als PDF laden</a> (Stand {e(karte["stand"])})</p>')
    teile.append("</section>")
    return "\n".join(teile)


def vinyl() -> str:
    rillen = "".join(f'<circle r="{r}"/>' for r in range(40, 98, 5))
    return f"""
    <div class="platte" aria-hidden="true">
      <svg viewBox="-100 -100 200 200" focusable="false">
        <circle r="99" fill="#111315"/>
        <g fill="none" stroke="#ffffff" stroke-opacity=".06" stroke-width=".6">{rillen}</g>
        <circle r="34" fill="#d04d15"/>
        <text y="-4" text-anchor="middle" font-family="Barlow Semi Condensed, sans-serif" font-weight="900" font-size="13" fill="#fff" letter-spacing=".5">GENUSS</text>
        <text y="10" text-anchor="middle" font-family="Barlow Semi Condensed, sans-serif" font-weight="900" font-size="13" fill="#fff" letter-spacing=".5">WERK</text>
        <text y="23" text-anchor="middle" font-family="Barlow, sans-serif" font-size="5.5" fill="#fff" fill-opacity=".8">Bad Rothenfelde</text>
        <circle r="2.6" fill="#1a1c1f"/>
      </svg>
    </div>"""


def galerie() -> str:
    teile = []
    for b in DATEN["bilder_site"]["galerie"]:
        if bild_da(b["datei"]):
            teile.append(f'<figure class="rahmen"><img src="{e(b["datei"])}" alt="{e(b["alt"])}" loading="lazy" decoding="async">'
                         f'<figcaption>{e(b["motiv"])}</figcaption></figure>')
        else:
            teile.append(f'<figure class="rahmen rahmen-leer"><div class="rahmen-flaeche"><span>Foto folgt</span></div>'
                         f'<figcaption>{e(b["motiv"])}</figcaption></figure>')
    return '<div class="galerie">' + "".join(teile) + "</div>"


def jsonld() -> str:
    k = DATEN["kontakt"]
    tage_en = {"Mo": "Monday", "Di": "Tuesday", "Mi": "Wednesday", "Do": "Thursday",
               "Fr": "Friday", "Sa": "Saturday", "So": "Sunday"}
    oeffnung = [{"@type": "OpeningHoursSpecification", "dayOfWeek": tage_en[t["kurz"]],
                 "opens": t["von"], "closes": t["bis"]}
                for t in DATEN["oeffnungszeiten"]["tage"] if not t.get("geschlossen")]
    daten = {
        "@context": "https://schema.org", "@type": "Restaurant",
        "name": DATEN["betrieb"]["name"].title(), "slogan": DATEN["betrieb"]["slogan"],
        "url": DATEN["site"]["url"], "telephone": k["telefon_link"], "email": k["email"],
        "address": {"@type": "PostalAddress", "streetAddress": k["strasse"], "postalCode": k["plz"],
                    "addressLocality": k["ort"], "addressCountry": "DE"},
        "servesCuisine": ["Burger", "Flammkuchen", "Bar", "Café"], "priceRange": "€€",
        "hasMenu": DATEN["site"]["url"] + "/karte/", "acceptsReservations": True,
        "openingHoursSpecification": oeffnung, "sameAs": [k["instagram"], k["facebook"]],
        "foundingDate": str(DATEN["betrieb"]["gegruendet"]),
    }
    return '<script type="application/ld+json">' + json.dumps(daten, ensure_ascii=False) + "</script>"


# ---------- Seiten ----------

def startseite() -> str:
    b, u, m, k = DATEN["betrieb"], DATEN["ueber_uns"], DATEN["musik_events"], DATEN["kontakt"]
    hero_bild = DATEN["bilder_site"]["hero"]
    hero_stil = (f' style="--hero-bild:url(\'{e(hero_bild["datei"])}\')" data-bild'
                 if bild_da(hero_bild["datei"]) else "")

    highlights = "".join(
        f'<li><div class="gericht-kopf"><h3>{e(h.get("titel", h["name"]))}</h3><span class="punkte" aria-hidden="true"></span>'
        f'<span class="preis">{preis(finde(h["karte"], h["name"]))}</span></div>'
        f'<p class="gericht-text">{e(finde(h["karte"], h["name"]).get("beschreibung", ""))}</p></li>'
        for h in DATEN["highlights"])

    if m["termine"]:
        termine = '<ul class="termine">' + "".join(
            f'<li><time datetime="{e(t["datum"])}">{e(t.get("anzeige", t["datum"]))}</time>'
            f'<strong>{e(t["titel"])}</strong><span>{e(t.get("genre", ""))}</span></li>' for t in m["termine"]) + "</ul>"
    else:
        termine = (f'<p class="termine-leer">Die nächsten DJ-Abende und Specials stehen auf Instagram.</p>'
                   f'<a class="knopf knopf-hell" href="{e(k["instagram"])}" rel="noopener">Termine auf Instagram ansehen</a>')

    partner = DATEN["partner"]
    partner_liste = "".join(f"<li>{e(p)}</li>" for p in [partner["sponsor"]["name"]] + partner["lieferanten"])
    mail_text = "Datum:%0APersonen:%0AUhrzeit:%0AAnlass:%0ATelefon:"
    route = "https://www.openstreetmap.org/search?query=" + (k["strasse"] + " " + k["plz"] + " " + k["ort"]).replace(" ", "+")

    geschichte = [
        ("Früher", "Café Koch", "Traditionsreiches Kurcafé in Bad Rothenfelde, geführt als Familienbetrieb."),
        (str(b["gegruendet"]), "Umbau", "Nach umfassender Renovierung öffnet an gleicher Stelle das Genusswerk."),
        ("Heute", "Genusswerk", "Bar, Restaurant und Treffpunkt, in dritter Generation geführt."),
    ]
    zeitstrahl = "".join(f'<li><span class="zeit">{e(z)}</span><strong>{e(t)}</strong><p>{e(p)}</p></li>'
                         for z, t, p in geschichte)

    return f"""
<section class="hero" id="start"{hero_stil}>
  {decke()}
  <div class="hero-text">
    <p class="hand hero-hand">{e(b["claim"])}</p>
    <h1><span>Dein Mittelpunkt</span> <span>in Bad Rothenfelde!</span></h1>
    <p class="hero-lead">{e(b["unterzeile"])}</p>
  </div>
  {theke(f'''
        <p class="status" data-status>Öffnungszeiten weiter unten</p>
        <div class="knoepfe">
          <a class="knopf knopf-orange" href="#reservieren">Tisch reservieren</a>
          <a class="knopf knopf-linie" href="karte/">Karte ansehen</a>
        </div>''')}
</section>

<section class="abschnitt genuss" id="genuss" aria-labelledby="t-genuss">
  <div class="genuss-text">
    <h2 class="hand" id="t-genuss">{e(u["headline"])}</h2>
    <p class="lead">{e(u["absaetze"][0])}</p>
    {"".join(f"<p>{e(p)}</p>" for p in u["absaetze"][1:])}
  </div>
  <aside class="klinker" aria-labelledby="t-geschichte">
    <h3 id="t-geschichte">Vom Café Koch zum Genusswerk</h3>
    <ol class="zeitstrahl">{zeitstrahl}</ol>
  </aside>
</section>

{lichtlinie()}

<section class="abschnitt karte-vorschau" id="karte" aria-labelledby="t-karte">
  <div class="karte-kopf">
    <h2 id="t-karte">Speisen &amp; Getränke</h2>
    <div class="etiketten">
      <a class="etikett etikett-link" href="karte/#speisen">Speisen</a>
      <a class="etikett etikett-link etikett-schief" href="karte/#getraenke">Getränke</a>
    </div>
  </div>
  <ul class="highlights">{highlights}</ul>
  <p class="karte-mehr"><a class="knopf knopf-linie" href="karte/">Ganze Karte ansehen</a></p>
</section>

<section class="events" id="events" aria-labelledby="t-events">
  <div class="events-innen">
    <div class="events-text">
      <h2 class="hand" id="t-events">{e(m["headline"])}</h2>
      {"".join(f"<p>{e(p)}</p>" for p in m["absaetze"])}
      <ul class="genres">{"".join(f"<li>{e(g)}</li>" for g in m["genres"])}</ul>
      {termine}
    </div>
    {vinyl()}
  </div>
</section>

<section class="abschnitt reservieren" id="reservieren" aria-labelledby="t-reservieren">
  <div class="polster">
    <h2 id="t-reservieren">Reservieren &amp; feiern</h2>
    <p class="lead">Zu zweit, mit dem Stammtisch oder mit der ganzen Gesellschaft: Ruf an oder schreib uns, wir halten deinen Tisch frei.</p>
    <div class="knoepfe">
      <a class="knopf knopf-orange" href="tel:{e(k["telefon_link"])}">{e(k["telefon_anzeige"])} anrufen</a>
      <a class="knopf knopf-hell" href="mailto:{e(k["email"])}?subject=Reservierung%20im%20Genusswerk&amp;body={mail_text}">E-Mail schreiben</a>
    </div>
    <p class="polster-hinweis">Für Feiern und größere Gruppen sprich uns gern frühzeitig an.</p>
    <div class="polster-zeiten">
      <p class="status" data-status></p>
      {zeiten_kurz()}
    </div>
  </div>
</section>

<section class="abschnitt eindruecke" id="eindruecke" aria-labelledby="t-eindruecke">
  <h2 id="t-eindruecke">Impressionen</h2>
  {galerie()}
</section>

{lichtlinie()}

<section class="abschnitt besuch" id="besuch" aria-labelledby="t-besuch">
  <h2 id="t-besuch">Besuch</h2>
  <div class="besuch-raster">
    <div>
      <h3>Öffnungszeiten</h3>
      <p class="status" data-status></p>
      {zeiten_tabelle()}
    </div>
    <div>
      <h3>Adresse</h3>
      <address>{e(k["firma"])}<br>{e(k["strasse"])}<br>{e(k["plz"])} {e(k["ort"])}</address>
      <p class="leise">Nahe Kurpark und Gradierwerk.</p>
      <a class="knopf knopf-linie knopf-klein" href="{e(route)}" rel="noopener">Route planen</a>
    </div>
    <div>
      <h3>Kontakt</h3>
      <p><a href="tel:{e(k["telefon_link"])}">{e(k["telefon_anzeige"])}</a><br>
      <a href="mailto:{e(k["email"])}">{e(k["email"])}</a></p>
      <p><a href="{e(k["instagram"])}" rel="noopener">Instagram</a> und <a href="{e(k["facebook"])}" rel="noopener">Facebook</a></p>
    </div>
  </div>
  <div class="partner">
    <h3>Partner und Lieferanten</h3>
    <ul>{partner_liste}</ul>
    <p class="leise">{e(partner["werbeplatz"])}</p>
  </div>
</section>
"""


def kartenseite() -> str:
    filter_btn = "".join(f'<button type="button" data-filter="{f}" aria-pressed="false">{label}</button>'
                         for f, label in FILTER)
    sprung = "".join(f'<a href="#{slug(t)}-{slug(k["name"])}">{e(k["name"])}</a>'
                     for s, t in (("speisekarte", "Speisen"), ("getraenkekarte", "Getränke"))
                     for k in DATEN[s]["kategorien"])
    kopf_leds = [(-4, 44, 58, -8, 0.2), (42, 34, 70, -8, 0.45), (22, 70, 26, 14, 0.7)]
    return f"""
<section class="hero hero-klein">
  {decke(kopf_leds, glaeser=False)}
  <div class="hero-text">
    <h1>Speisen &amp; Getränke</h1>
    <p class="hero-lead">Unsere Karte, Stand {e(DATEN["speisekarte"]["stand"])}.</p>
  </div>
  {theke('')}
</section>
<div class="karte-leiste" id="karte-leiste">
  <div class="karte-leiste-innen">
    <div class="filter" role="group" aria-label="Karte filtern">{filter_btn}</div>
    <nav class="sprung" aria-label="Kategorien">{sprung}</nav>
  </div>
</div>
<div class="abschnitt karte-seite">
  {karte_html("speisekarte", "Speisen")}
  {karte_html("getraenkekarte", "Getränke")}
  <p class="leise karte-allergene">{e(DATEN["speisekarte"]["hinweis"])}</p>
</div>
"""


def impressum() -> str:
    i = DATEN["impressum"]
    return f"""
<div class="abschnitt recht">
  <h1>Impressum</h1>
  <h2>Angaben gemäß § 5 DDG</h2>
  <p>{e(i["firma"])}<br>{e(i["anschrift"])}</p>
  <p>Vertreten durch den Geschäftsführer {e(i["geschaeftsfuehrer"])}</p>
  <h2>Kontakt</h2>
  <p>Telefon: {e(i["telefon"])}<br>E-Mail: <a href="mailto:{e(i["email"])}">{e(i["email"])}</a></p>
  <h2>Registereintrag</h2>
  <p>Registergericht: {e(i["registergericht"])}<br>Registernummer: {e(i["handelsregister"])}</p>
  <h2>Umsatzsteuer-ID</h2>
  <p>Umsatzsteuer-Identifikationsnummer gemäß § 27 a UStG: {e(i["ust_id"])}</p>
</div>
"""


def datenschutz() -> str:
    return """
<div class="abschnitt recht">
  <h1>Datenschutz</h1>
  <p>Die Datenschutzerklärung stellt der Betreiber vor dem Livegang bereit.</p>
</div>
"""


def seite(inhalt: str, titel: str, seite_id: str, wurzel: str, pfad: str) -> str:
    k = DATEN["kontakt"]
    vorschau = DATEN["site"]["vorschau"]
    werte = {
        "titel": titel, "beschreibung": DATEN["site"]["beschreibung"], "seite": seite_id,
        "canonical": DATEN["site"]["url"] + "/" + pfad, "wurzel": wurzel,
        "telefon_link": k["telefon_link"], "telefon_anzeige": k["telefon_anzeige"], "email": k["email"],
        "strasse": k["strasse"], "plz": k["plz"], "ort": k["ort"],
        "instagram": k["instagram"], "facebook": k["facebook"],
    }
    roh = {
        "inhalt": inhalt,
        "navigation": navigation(wurzel),
        "robots": '<meta name="robots" content="noindex, nofollow">' if vorschau else "",
        "vorschau_hinweis": '<p class="vorschau">Vorschau, noch nicht freigegeben</p>' if vorschau else "",
        "jsonld": jsonld() if seite_id == "start" else "",
        "zeiten_json": json.dumps(DATEN["oeffnungszeiten"]["tage"], ensure_ascii=False).replace("</", "<\\/"),
    }
    out = TEMPLATE
    for key, val in roh.items():
        out = out.replace("{{" + key + "}}", val)
    for key, val in werte.items():
        out = out.replace("{{" + key + "}}", e(val))
    rest = re.findall(r"\{\{\w+\}\}", out)
    if rest:
        raise SystemExit(f"Unersetzte Platzhalter: {rest}")
    return out


def schreibe(rel: str, text: str) -> None:
    ziel = ROOT / rel
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_text(text, encoding="utf-8")
    print(f"geschrieben: {rel}")


def main() -> None:
    name = "Genusswerk Bad Rothenfelde"
    schreibe("index.html", seite(startseite(), f"{name}: Bar & Restaurant", "start", "", ""))
    schreibe("karte/index.html", seite(kartenseite(), f"Speisen & Getränke | {name}", "karte", "../", "karte/"))
    schreibe("impressum/index.html", seite(impressum(), f"Impressum | {name}", "impressum", "../", "impressum/"))
    schreibe("datenschutz/index.html", seite(datenschutz(), f"Datenschutz | {name}", "datenschutz", "../", "datenschutz/"))


if __name__ == "__main__":
    main()
