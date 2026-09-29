# Genusswerk Bad Rothenfelde – Website-Konzept (erste Gedanken)

Stand: 29.09.2026 · Status: Konzept, bereit zum Bauen

Dateien im Repository:

| Datei | Inhalt |
|---|---|
| `docs/KONZEPT.md` | Dieses Dokument: Recherche, Raumanalyse, Designrichtung, Seitenstruktur, Bauplan |
| `FEHLT.md` | Fehlende Dokumente, Freigaben und offene Fragen |
| `daten/inhalte.json` | Alle Inhalte aus dem Netz als strukturierte Daten: Texte, Kontakt, Öffnungszeiten, Impressum, komplette Speise- und Getränkekarte mit Preisen, Bildbestand |
| `src/design-tokens.css` | Farben, Schriften und Raster als CSS-Variablen, abgeleitet aus Raum und Marke |

---

## 1. Was im Netz steht (Recherche)

### Stammdaten

- **Name:** GENUSSWERK – Schlemmen & Verweilen
- **Slogan:** „Dein Mittelpunkt in Bad Rothenfelde!“ · „Bar, Restaurant, Events und vieles mehr!“
- **Betreiber:** Genusswerk Rothenfelde GmbH, Geschäftsführer Jonas Janböke, HRB 216057 (AG Osnabrück), USt-ID DE344012785
- **Adresse:** Salinenstraße 2-6, 49214 Bad Rothenfelde, nahe Kurpark und Gradierwerk
- **Kontakt:** +49 (0) 5424 – 294 97 46 · cafe@genusswerk.info
- **Social:** Instagram [@genusswerk.br](https://www.instagram.com/genusswerk.br/) (ca. 1.800 Follower), Facebook [genusswerk.br](https://www.facebook.com/genusswerk.br/)
- **Geschichte:** Eröffnet 2021 im ehemaligen **Café Koch**. Familienbetrieb, jetzt in dritter Generation. Nach umfassender Renovierung kaum wiederzuerkennen (Quelle: osnabruecker-land.de). Diese Geschichte fehlt auf der jetzigen Website komplett und ist ein starkes Thema.
- **Öffnungszeiten (offiziell):** Mo Ruhetag · Di–Fr 16–22 Uhr · Sa 12–22 Uhr · So 11–21 Uhr
- **Bewertung:** Google ca. 4,2 Sterne (laut Drittportal), Preisniveau 10–20 € pro Hauptgericht
- **Angebot:** Burger, Wraps, Flammkuchen, Currywurst, Poutine, Salat, Kinderkarte; Spritz-Varianten (drei Hausmarken), Fassbier (Krombacher, Starnberger, Erdinger, Sion Kölsch), Cocktails, Weine, Kaffee von Ferdinands Kaffeerösterei, Tee mit hausgebackenem Gebäck
- **Musik & Events:** Regelmäßig am Wochenende DJs mit Charts, Classic, Schlager, House/Techno. Specials (Angebote, Begrüßungsshot) und Termine nur über Social Media.
- **Partner:** Sponsor JOPA (jopa.de); regionale Lieferanten (Bad Rothenfelder Tafelwasser, Feinbrennerei Sasse aus dem Münsterland). Karte bietet Werbeplatz an: „Hier soll Ihr Unternehmen stehen?“

Alle Details mit Preisen: siehe `daten/inhalte.json`.

### Schwächen der jetzigen Seite (genusswerk.info, WordPress mit Theme „Betheme“)

1. **Speisekarte nur als PDF** (je ca. 4,4 MB, 12 und 18 Seiten). Auf dem Handy langsam, für Google nicht lesbar, kein Filter.
2. **Menüpunkt „Musik & Events“ führt ins Leere** (Anker `#kuchen_torte` existiert nicht). Der Event-Text steht nur als Bild, also unlesbar für Screenreader und Suchmaschinen.
3. **„Reservieren“-Button** ohne echte Reservierung, nur Sprung zum Kontakt.
4. **Versteckter Link „testy“ auf test.com** im Quelltext der Startseite. Das ist ein Theme- oder Testrest und schadet der Suchmaschinen-Bewertung. Unabhängig vom Relaunch sofort entfernen.
5. **Demo-Unterseiten online** (`/about-us/`, `/menu/`) mit Lorem-Ipsum-Text und falschen Öffnungszeiten („8 AM – 9 PM“).
6. **Keine Geschichte, kein Team, keine Gruppen- oder Feier-Infos**, obwohl die Texte Stammtisch und größere Gesellschaften ansprechen.
7. **Keine strukturierten Daten** (schema.org Restaurant), deshalb verbreiten Drittportale falsche Öffnungszeiten.

### Widersprüche, vor dem Bau mit dem Betrieb klären

| Thema | Offizielle Seite | Drittportale |
|---|---|---|
| Öffnungszeiten Di–Do | 16–22 Uhr | 12–22 Uhr (speisen.com u. a.) |
| Öffnungszeiten Fr/Sa | Fr 16–22, Sa 12–22 Uhr | Fr/Sa 12–24 Uhr |
| Café-Angebot | Kuchen erscheint nur auf Fotos (Torte mit Schoko-Logo) | Portale nennen „Café“, Café Koch war Konditorei |
| Preis Cheeseburger | 19,90 € (Smashed Burger 11,90 €) | – | 
| Außenplätze | nicht erwähnt | „Außensitzplätze vorhanden“ |

Weitere offene Fragen: Gibt es Kuchen und Torte noch täglich? Wie viele Plätze innen und außen? Gibt es einen separaten Raum für Feiern? Barrierefreier Zugang? Kartenzahlung? Parken?

---

## 2. Der Raum (Grundlage für das Design)

Analyse der vorhandenen Fotos vom Gastraum:

| Element im Raum | Wirkung | Übersetzung ins Web |
|---|---|---|
| **Klinker-Ziegelwand**, rotbraun, unverputzt | warm, handfest, „Werk“ | dezente Ziegel-Textur als Hintergrund einzelner Bänder, Farbe `--raum-ziegel` |
| **Schwarze Decke, schwarze Regale und Stühle** | Bar-Abend, Tiefe | dunkles Grundthema, Anthrazit statt reinem Schwarz |
| **Offene Lüftungsrohre aus Stahl** | Industrie, Loft | feine silbergraue Linien und Trenner, Icons im Strich-Stil |
| **Diagonale LED-Lichtlinien** an der Decke | modern, Bewegung | Signatur-Element: schräge Lichtlinie, die Abschnitte trennt und beim Scrollen leicht aufleuchtet |
| **Nussholz-Thekenplatte** mit indirektem Licht darunter | Genuss, Qualität | horizontales Holzband als „Theke“ unter dem Hero, Tabellenkopf der Karte |
| **Barhocker mit Petrol-Samtbezug** | weich, Farbtupfer | nach Rückmeldung nicht übernommen: die Seite bleibt ohne Blau, warm in Holz, Klinker und Orange |
| **Gläserregal über der Theke** | Bar-Handwerk | Fotomotiv für Hero, Glanzlichter |
| **Logo:** Turm-Signet über „GENUSS WERK“, Kupferrahmen | Marke, Bad Rothenfelde | Logo im Kupferrahmen, Signet als Favicon |
| **Marke:** Orange-Etiketten mit Pinselschrift („Speisen“, „Getränke“, „Musikgenuss!“), Navy-Textflächen | laut, freundlich, per Du | Pinselschrift nur für kurze emotionale Wörter, Orange für Handlungen, Navy für Info-Flächen |

**Leitidee: „Abend an der Theke“.** Die Website fühlt sich an wie ein Platz an der Nussholz-Theke: dunkler Raum, warmes Licht, Ziegel im Rücken, orange Etiketten als Wegweiser. Keine glatte Restaurant-Vorlage, sondern Loft-Charakter mit Handschrift.

### Designsystem (Kurzfassung, Werte in `design-tokens.css`)

- **Farben:** Anthrazit `#1f2124` (Grund), LED-Weiß `#e6e9e7` (Text), Orange `#d04d15` (Marke, Handlung), Navy `#1e425a` (Info-Flächen), Kupfer `#ab5634` (Logo, Linien), Nussholz `#9a6440`, Ziegel `#7b4a3c`, Petrol-Samt `#3d7d92`, Stahl `#b9bdc1`.
- **Kontrast:** Orange auf Anthrazit erreicht ca. 3,7:1, also nur für große Schrift und Flächen. Weiße Schrift auf Buttons braucht das dunklere Orange `#b8420f` (ca. 5:1).
- **Schriften:** *Barlow Semi Condensed* (identisch mit der Speisekarte) für Titel in 800/900 VERSAL, *Barlow* für Fließtext, beide selbst gehostet. Pinselschrift der Karte ist *Ernest and Emily* (kommerziell). Webfont-Lizenz anfragen, sonst Ersatz *Caveat Brush*.
- **Formen:** kantig, Radius 2 px, dünne Stahllinien, keine Schatten-Kacheln.
- **Fotos:** echte Fotos aus dem Raum, eher dunkel und warm. Schwarz-Weiß-Fotos (Espresso Martini, DJ) für den Event-Bereich.
- **Themen:** dunkles Standardthema „Abend“. Optional helles Thema „Tag“ für Kaffee am Sonntag.

---

## 3. Zielgruppen und Ziele

| Zielgruppe | Will wissen | Wichtigste Handlung |
|---|---|---|
| Einheimische, Freundesgruppen, Stammtische | Hat heute offen? Was läuft am Wochenende? | Tisch reservieren, Instagram folgen |
| Kurgäste und Tagesbesucher (Gradierwerk, Kurpark) | Wo ist das? Was kostet es? Gibt es Kaffee und Kuchen? | Route öffnen, Karte ansehen |
| Gruppen und Feiern (Geburtstag, Firmenabend) | Platz für wie viele? Paket? | Anfrage senden |
| Partner und Sponsoren | Werbeplatz auf Karte und Website | Kontakt |

**Ziele:** 1. Reservierungen und Anfragen erhöhen. 2. Speisekarte mobil in Sekunden lesbar. 3. Events sichtbar machen, auch ohne Instagram-Konto. 4. Richtige Öffnungszeiten überall (Google, Portale).

---

## 4. Seitenstruktur

Einseitige Startseite mit Ankern (wie heute, aber vollständig) plus wenige eigene Unterseiten:

```
/                    Startseite (One-Pager)
  #start             Hero: Raumfoto, Logo, "Dein Mittelpunkt in Bad Rothenfelde!",
                     Live-Status "Jetzt geöffnet bis 22 Uhr", Buttons Reservieren + Karte
  #genuss            Über uns: "Genuss mit allen Sinnen!" + Geschichte Café Koch → Genusswerk
  #karte             Speisen & Getränke: Vorschau (Highlights), Link zur vollen Karte
  #events            Musikgenuss!: nächste Termine, Genres, Instagram-Hinweis
  #feiern            Gruppen, Stammtisch, Gesellschaften: Anfrageformular
  #eindruecke        Impressionen: Galerie Raum, Drinks, Speisen
  #besuch            Kontakt: Öffnungszeiten, Adresse, Karte (OSM), Anfahrt Kurpark
/karte/              Volle Speise- und Getränkekarte als HTML, Filter, PDF-Download
/impressum/          Impressum
/datenschutz/        Datenschutz
```

### Inhalte und Ideen je Abschnitt

**Hero (#start)**
- Foto Theke mit Petrol-Hockern und Gläserregal (vorhanden), abgedunkelt.
- Diagonale Lichtlinie läuft einmal über das Bild (CSS-Animation, abschaltbar).
- Status-Chip aus `inhalte.json › oeffnungszeiten`: „Jetzt geöffnet · bis 22:00“ / „Heute Ruhetag · ab Di 16:00“.
- Zwei Buttons: **Tisch reservieren** (orange) · **Zur Karte** (Umriss).

**Über uns (#genuss)**
- Headline in Pinselschrift: „Genuss mit allen Sinnen!“
- Originaltext aus `ueber_uns`.
- Neuer Block „Vom Café Koch zum Genusswerk“: Zeitstrahl 3 Generationen → 2021 Umbau → heute. Altes Foto vom Café Koch anfragen.

**Speisen & Getränke (#karte und /karte/)**
- Startseite: zwei orange Etiketten „Speisen“ und „Getränke“ (Wiedererkennung von Karte und alter Seite), darunter 4–6 Highlights (Genusswerk Spritz, Smashed Burger, Poutine Kanada, Espresso Martini).
- `/karte/`: vollständige Karte aus `inhalte.json`. Sprungleiste der Kategorien (sticky), Filter-Chips „vegetarisch“, „vegan“, „alkoholfrei“, Preise rechtsbündig mit Punktlinie. Kurzer Erklärtext zu Poutine übernehmen, weil er Charakter hat. PDF-Download bleibt als Option.
- Druckansicht der Karte per CSS.

**Musikgenuss! (#events)**
- Navy-Fläche mit Pinselschrift wie im vorhandenen Event-Bild, Text als echter HTML-Text.
- Terminliste aus `inhalte.json › musik_events.termine` (Datum, DJ, Genre). Leere Liste zeigt: „Nächste Termine auf Instagram“.
- Genre-Tags: Charts · Classic · Schlager · House/Techno.
- Später: Termine aus Google-Kalender oder aus einer einfachen Tabelle pflegen.

**Feiern & Gruppen (#feiern)**
- Text für Stammtisch, Geburtstag, Firmenfeier.
- Formular: Datum, Personen, Anlass, Kontakt. Versand per E-Mail an cafe@genusswerk.info (Form-Dienst oder mailto).

**Impressionen (#eindruecke)**
- Masonry-Galerie mit den vorhandenen Fotos, Lightbox. Neue Fotos vom Raum am Abend wünschenswert (Lichtlinien, Außenbereich).

**Besuch (#besuch)**
- Öffnungszeiten als Tabelle, heutiger Tag hervorgehoben.
- Adresse, Telefon (klickbar), E-Mail, Instagram.
- Karte: statisches Bild mit Link zu OpenStreetMap/Google Maps, keine eingebettete Google-Karte (Datenschutz, kein Cookie-Banner nötig).
- Hinweis „Nur wenige Schritte vom Gradierwerk und Kurpark“.
- Partner-Leiste: JOPA, Ferdinands, Sasse, Bad Rothenfelder Tafelwasser + „Hier soll Ihr Unternehmen stehen?“

---

## 5. Funktionen

| Funktion | Stufe 1 (Start) | Stufe 2 (später) |
|---|---|---|
| Reservieren | Telefon-Button + E-Mail-Formular | Reservierungstool (z. B. OpenTable, Quandoo, resmio) nach Wahl des Betriebs |
| Öffnungsstatus | aus JSON, im Browser berechnet (Zeitzone Europe/Berlin) | Feiertage und Sonderzeiten |
| Speisekarte | HTML aus JSON, Filter | Allergene-Kennzeichnung, Tagesgericht |
| Events | Liste aus JSON | Kalender-Feed, iCal-Export je Termin |
| Instagram | Link + 3 feste Fotos | Feed nur mit Einwilligung (Datenschutz) |
| SEO | schema.org `Restaurant` mit Öffnungszeiten, `Menu`, `Event` als JSON-LD, Open-Graph-Bild | Google-Unternehmensprofil abgleichen |
| Sprache | Deutsch, per Du (wie heute) | Englisch für Kurgäste optional |

**Nicht vorgesehen:** Online-Shop, Lieferservice, Newsletter-Tool. Nur auf Wunsch des Betriebs.

---

## 6. Technik und Bauplan

Statische Seite, Inhalte getrennt vom Layout. Hosting noch offen (GitHub Pages oder deutscher Anbieter, siehe `FEHLT.md`).

```
daten/inhalte.json      Single Source of Truth
src/design-tokens.css   Farben, Schriften
src/template.html       Seitengerüst mit Platzhaltern
src/site.css            Stylesheet (Rohbau, edle Gestaltung folgt)
src/site.js             Scroll-Regel, Menü, Öffnungsstatus, Kartenfilter
build.py                erzeugt alle Seiten aus inhalte.json
index.html              (erzeugt) Startseite
karte/index.html        (erzeugt) Speise- und Getränkekarte
impressum/, datenschutz/ (erzeugt)
bilder/                 (nach Freigabe) optimierte WebP-Bilder, max. 200 KB je Bild
```

- Kein Framework, kein Build-Tool außer `python3 build.py`.
- **Neuladen startet immer oben:** `history.scrollRestoration = "manual"` im Head, `#hash` wird beim Neuladen entfernt, Anker-Links scrollen ohne `#hash` in der Adresse.
- Nur Google Fonts als externe Quelle, besser lokal einbinden (Datenschutz).
- Mobile first, 16 px Seitenrand, Zielgröße Startseite unter 1 MB.
- Barrierefreiheit: Kontrast nach WCAG AA, Fokus sichtbar, Alt-Texte, Bewegung abschaltbar.

### Schritte

1. **Freigaben holen:** Fotos in Originalgröße, Logo als SVG, Öffnungszeiten bestätigen, Widersprüche aus Abschnitt 1 klären, Lizenz Pinselschrift.
2. **Template bauen:** Startseite mit allen Abschnitten, Daten aus `inhalte.json`. Rohbau erledigt, edle Gestaltung auf Startsignal.
3. **Karte bauen:** `/karte/` mit Filtern und Druckansicht.
4. **Events + Anfrageformular** anbinden.
5. **SEO:** JSON-LD, Meta-Daten, Sitemap. Danach Google-Unternehmensprofil und Portale mit den richtigen Zeiten aktualisieren.
6. **Test:** Handy (iOS, Android), Lighthouse ≥ 90, Kontrast-Prüfung.
7. **Übergabe:** Anleitung, wie Karte und Termine in `inhalte.json` gepflegt werden.

### Soforttipps für die alte Seite (unabhängig vom Relaunch)

- Versteckten Link „testy“ → test.com entfernen.
- Demo-Seiten `/about-us/` und `/menu/` löschen oder auf Startseite umleiten.
- Menüpunkt „Musik & Events“ auf einen existierenden Abschnitt zeigen lassen.

---

## Quellen

- [genusswerk.info](https://genusswerk.info/) (Startseite, Speisekarten-PDFs Juni 2026)
- [genusswerk.info/impressum](https://genusswerk.info/impressum/)
- [Instagram @genusswerk.br](https://www.instagram.com/genusswerk.br/)
- [Facebook genusswerk.br](https://www.facebook.com/genusswerk.br/)
- [osnabruecker-land.de – Kulinarisch genießen in Bad Rothenfelde](https://www.osnabruecker-land.de/erlebnisse/kulinarisch-geniessen-in-bad-rothenfelde)
- [speisekartenweb.de](https://speisekartenweb.de/restaurants/bad+rothenfelde/genusswerk-rothenfelde-219491), [speisen.com](https://speisen.com/eintrag/genusswerk-rothenfelde/), [Tripadvisor](https://www.tripadvisor.com/Restaurant_Review-g198417-d27261042-Reviews-Genusswerk-Bad_Rothenfelde_Lower_Saxony.html), [Restaurant Guru](https://de.restaurantguru.com/Genusswerk-Rothenfelde-Bad-Rothenfelde)
