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

NAV = [("#genuss", "Über uns"), ("karte/", "Karte"), ("#events", "Musik & Events"),
       ("#eindruecke", "Impressionen"), ("#besuch", "Besuch")]

FILTER = [("vegetarisch", "Vegetarisch"), ("vegan", "Vegan"), ("alkoholfrei", "Alkoholfrei")]


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


# ---------- Bausteine ----------

def navigation(wurzel: str) -> str:
    links = []
    for href, label in NAV:
        ziel = href if (href.startswith("#") and wurzel == "") else wurzel + href
        links.append(f'<a href="{e(ziel)}">{e(label)}</a>')
    return "\n      ".join(links)


def zeiten_tabelle() -> str:
    zeilen = []
    for t in DATEN["oeffnungszeiten"]["tage"]:
        wert = t.get("label", "Ruhetag") if t.get("geschlossen") else f'{e(t["von"])} – {e(t["bis"])} Uhr'
        zeilen.append(f'<tr data-tag="{e(t["kurz"])}"><th scope="row">{e(t["tag"])}</th><td>{wert}</td></tr>')
    return '<table class="zeiten">' + "".join(zeilen) + "</table>"


def gericht_html(g: dict, k: dict) -> str:
    beschr = f'<p class="gericht-text">{e(g["beschreibung"])}</p>' if g.get("beschreibung") else ""
    t = tags(g, k)
    marker = "".join(f'<span class="tag tag-{e(x)}">{e(x.replace("-", " "))}</span>'
                     for x in t if x in ("vegan", "vegetarisch", "hausmarke", "regional"))
    return (f'<li class="gericht" data-tags="{e(" ".join(t))}">'
            f'<div class="gericht-kopf"><h4>{e(g["name"])}</h4><span class="punkte" aria-hidden="true"></span>'
            f'<span class="preis">{preis(g)}</span></div>{beschr}{marker}</li>')


def karte_html(schluessel: str, titel: str) -> str:
    karte = DATEN[schluessel]
    teile = [f'<section class="karte-block" id="{slug(titel)}"><h2 class="etikett">{e(titel)}</h2>']
    for k in karte["kategorien"]:
        teile.append(f'<section class="kategorie" id="{slug(titel)}-{slug(k["name"])}"><h3>{e(k["name"])}</h3>')
        if k.get("hinweis"):
            teile.append(f'<p class="kategorie-hinweis">{e(k["hinweis"])}</p>')
        teile.append('<ul class="gerichte">' + "".join(gericht_html(g, k) for g in k["gerichte"]) + "</ul>")
        if k.get("extras"):
            extras = ", ".join(f'{e(x["name"])} {e(x["preis"])} €' for x in k["extras"])
            teile.append(f'<p class="extras" data-tags=""><strong>Extras:</strong> {extras}</p>')
        teile.append("</section>")
    teile.append(f'<p class="karte-pdf"><a href="{e(karte["pdf"])}" rel="noopener">{e(titel)} als PDF (Stand {e(karte["stand"])})</a></p>')
    teile.append("</section>")
    return "\n".join(teile)


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
    highlights = "".join(
        f'<li><h3>{e(h.get("titel", h["name"]))}</h3><p>{e(finde(h["karte"], h["name"]).get("beschreibung", ""))}</p>'
        f'<span class="preis">{preis(finde(h["karte"], h["name"]))}</span></li>'
        for h in DATEN["highlights"])
    if m["termine"]:
        termine = '<ul class="termine">' + "".join(
            f'<li><time datetime="{e(t["datum"])}">{e(t.get("anzeige", t["datum"]))}</time> '
            f'<strong>{e(t["titel"])}</strong> {e(t.get("genre", ""))}</li>' for t in m["termine"]) + "</ul>"
    else:
        termine = (f'<p class="termine-leer">Die nächsten Termine und Getränkespecials findest du auf '
                   f'<a href="{e(k["instagram"])}" rel="noopener">Instagram @genusswerk.br</a>.</p>')
    partner = DATEN["partner"]
    betreff = "Tischreservierung Genusswerk"
    mail_text = "Datum:%0APersonen:%0AUhrzeit:%0AAnlass:%0ATelefon:"
    return f"""
<section class="hero" id="start">
  <div class="hero-innen">
    <p class="hand">{e(b["claim"])}</p>
    <h1>{e(b["slogan"])}</h1>
    <p class="hero-unterzeile">{e(b["unterzeile"])}</p>
    <p class="status" data-status>Öffnungszeiten siehe unten</p>
    <div class="knoepfe">
      <a class="knopf knopf-voll" href="#reservieren">Tisch reservieren</a>
      <a class="knopf" href="karte/">Zur Karte</a>
    </div>
  </div>
  <div class="lichtlinie" aria-hidden="true"></div>
</section>

<section class="abschnitt" id="genuss">
  <h2 class="hand">{e(u["headline"])}</h2>
  {"".join(f"<p>{e(p)}</p>" for p in u["absaetze"])}
  <aside class="geschichte">
    <h3>Vom Café Koch zum Genusswerk</h3>
    <p>{e(b["vorgaenger"])}. Eröffnet {e(b["gegruendet"])}.</p>
  </aside>
</section>

<section class="abschnitt abschnitt-theke" id="karte">
  <h2>Speisen &amp; Getränke</h2>
  <ul class="highlights">{highlights}</ul>
  <div class="knoepfe">
    <a class="knopf knopf-voll" href="karte/#speisen">Speisen</a>
    <a class="knopf knopf-voll" href="karte/#getraenke">Getränke</a>
  </div>
</section>

<section class="abschnitt abschnitt-navy" id="events">
  <h2 class="hand">{e(m["headline"])}</h2>
  {"".join(f"<p>{e(p)}</p>" for p in m["absaetze"])}
  <ul class="genres">{"".join(f"<li>{e(g)}</li>" for g in m["genres"])}</ul>
  {termine}
</section>

<section class="abschnitt" id="reservieren">
  <h2>Reservieren &amp; Feiern</h2>
  <p>Ob zu zweit, mit dem Stammtisch oder mit einer größeren Gesellschaft: Ruf uns an oder schreib uns, wir halten dir den Tisch frei.</p>
  <div class="knoepfe">
    <a class="knopf knopf-voll" href="tel:{e(k["telefon_link"])}">Anrufen: {e(k["telefon_anzeige"])}</a>
    <a class="knopf" href="mailto:{e(k["email"])}?subject={e(betreff)}&amp;body={mail_text}">E-Mail schreiben</a>
  </div>
</section>

<section class="abschnitt" id="eindruecke">
  <h2>Impressionen</h2>
  <div class="galerie" data-platzhalter>
    <p>Fotos folgen nach Freigabe durch das Genusswerk.</p>
  </div>
</section>

<section class="abschnitt" id="besuch">
  <h2>Besuch</h2>
  <div class="besuch-raster">
    <div>
      <h3>Öffnungszeiten</h3>
      <p class="status" data-status></p>
      {zeiten_tabelle()}
    </div>
    <div>
      <h3>Adresse</h3>
      <address>{e(k["firma"])}<br>{e(k["strasse"])}<br>{e(k["plz"])} {e(k["ort"])}</address>
      <p>{e(b["lage"])}.</p>
      <p><a href="https://www.openstreetmap.org/search?query={e((k["strasse"] + " " + k["plz"] + " " + k["ort"]).replace(" ", "+"))}" rel="noopener">Route planen</a></p>
      <p><a href="tel:{e(k["telefon_link"])}">{e(k["telefon_anzeige"])}</a><br><a href="mailto:{e(k["email"])}">{e(k["email"])}</a></p>
    </div>
  </div>
  <div class="partner">
    <h3>Partner &amp; Lieferanten</h3>
    <p>{e(" · ".join([partner["sponsor"]["name"]] + partner["lieferanten"]))}</p>
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
    return f"""
<section class="abschnitt karte-seite">
  <h1>Speisen &amp; Getränke</h1>
  <div class="karte-leiste">
    <div class="filter" role="group" aria-label="Filter">{filter_btn}</div>
    <nav class="sprung" aria-label="Kategorien">{sprung}</nav>
  </div>
  {karte_html("speisekarte", "Speisen")}
  {karte_html("getraenkekarte", "Getränke")}
  <p class="leise">{e(DATEN["speisekarte"]["hinweis"])}</p>
</section>
"""


def impressum() -> str:
    i = DATEN["impressum"]
    return f"""
<section class="abschnitt recht">
  <h1>Impressum</h1>
  <h2>Angaben gemäß § 5 DDG</h2>
  <p>{e(i["firma"])}<br>{e(i["anschrift"])}</p>
  <p>Vertreten durch den Geschäftsführer: {e(i["geschaeftsfuehrer"])}</p>
  <h2>Kontakt</h2>
  <p>Telefon: {e(i["telefon"])}<br>E-Mail: <a href="mailto:{e(i["email"])}">{e(i["email"])}</a></p>
  <h2>Registereintrag</h2>
  <p>Registergericht: {e(i["registergericht"])}<br>Registernummer: {e(i["handelsregister"])}</p>
  <h2>Umsatzsteuer-ID</h2>
  <p>Umsatzsteuer-Identifikationsnummer gemäß § 27 a UStG: {e(i["ust_id"])}</p>
</section>
"""


def datenschutz() -> str:
    return """
<section class="abschnitt recht">
  <h1>Datenschutz</h1>
  <p>Die Datenschutzerklärung wird vor dem Livegang vom Betreiber bereitgestellt (siehe FEHLT.md).</p>
</section>
"""


def seite(inhalt: str, titel: str, seite_id: str, wurzel: str, pfad: str) -> str:
    k = DATEN["kontakt"]
    vorschau = DATEN["site"]["vorschau"]
    werte = {
        "titel": titel, "beschreibung": DATEN["site"]["beschreibung"], "seite": seite_id,
        "canonical": DATEN["site"]["url"] + "/" + pfad, "wurzel": wurzel,
        "navigation": navigation(wurzel), "inhalt": inhalt,
        "telefon_link": k["telefon_link"], "telefon_anzeige": k["telefon_anzeige"], "email": k["email"],
        "strasse": k["strasse"], "plz": k["plz"], "ort": k["ort"],
        "instagram": k["instagram"], "facebook": k["facebook"],
    }
    roh = {
        "robots": '<meta name="robots" content="noindex, nofollow">' if vorschau else "",
        "vorschau_hinweis": '<p class="vorschau">Vorschau · noch nicht freigegeben</p>' if vorschau else "",
        "jsonld": jsonld() if seite_id == "start" else "",
        "zeiten_json": json.dumps(DATEN["oeffnungszeiten"]["tage"], ensure_ascii=False).replace("</", "<\\/"),
    }
    out = TEMPLATE
    for key, val in roh.items():
        out = out.replace("{{" + key + "}}", val)
    for key in ("inhalt", "navigation"):
        out = out.replace("{{" + key + "}}", werte.pop(key))
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
    schreibe("index.html", seite(startseite(), f"{name} – Bar & Restaurant", "start", "", ""))
    schreibe("karte/index.html", seite(kartenseite(), f"Speisen & Getränke – {name}", "karte", "../", "karte/"))
    schreibe("impressum/index.html", seite(impressum(), f"Impressum – {name}", "impressum", "../", "impressum/"))
    schreibe("datenschutz/index.html", seite(datenschutz(), f"Datenschutz – {name}", "datenschutz", "../", "datenschutz/"))


if __name__ == "__main__":
    main()
