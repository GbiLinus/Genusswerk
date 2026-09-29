# Genusswerk Bad Rothenfelde – Website

Neue Website für das **GENUSSWERK – Schlemmen & Verweilen**, Bar & Restaurant in der Salinenstraße 2-6, 49214 Bad Rothenfelde.

**Status:** Vorbereitet, Rohbau steht. Die edle Gestaltung folgt auf Startsignal. Bis zur Freigabe durch den Betreiber trägt jede Seite `noindex` und einen Vorschau-Hinweis.

## Aufbau

| Pfad | Inhalt |
|---|---|
| [`docs/KONZEPT.md`](docs/KONZEPT.md) | Recherche, Raumanalyse, Designrichtung, Seitenstruktur, Bauplan |
| [`FEHLT.md`](FEHLT.md) | Liste aller Dokumente und Klärungen, die für eine perfekte Seite noch fehlen |
| [`daten/inhalte.json`](daten/inhalte.json) | Alle Inhalte: Texte, Kontakt, Öffnungszeiten, Impressum, Speise- und Getränkekarte |
| [`src/design-tokens.css`](src/design-tokens.css) | Farben, Schriften, Raster |
| [`src/template.html`](src/template.html) | Seitengerüst mit Platzhaltern |
| [`src/site.css`](src/site.css) | Rohbau-Stylesheet |
| [`src/site.js`](src/site.js) | Scroll-Regel, Menü, Öffnungsstatus, Kartenfilter |
| [`build.py`](build.py) | Erzeugt alle Seiten aus Daten und Vorlage |
| `bilder/` | Fotos nach Freigabe (WebP, max. 200 KB je Bild) |
| `index.html`, `karte/`, `impressum/`, `datenschutz/` | Erzeugte Seiten, nicht von Hand bearbeiten |

## Bauen und ansehen

```bash
python3 build.py
python3 -m http.server 8000   # dann http://localhost:8000
```

## Pflege

- Preise, Gerichte, Öffnungszeiten, Termine: nur in `daten/inhalte.json` ändern, danach `python3 build.py`.
- Event-Termine: in `musik_events.termine` eintragen, Format `{ "datum": "2026-10-10", "anzeige": "Sa, 10.10.", "titel": "DJ-Abend", "genre": "Charts & House" }`.
- Livegang: `site.vorschau` auf `false` setzen.

## Feste Regeln

- **Neuladen startet oben.** Kein `scroll-behavior: smooth` auf `html`, Anker-Links setzen keinen `#hash` in die Adresse. Logik: Inline-Script in `src/template.html` und `src/site.js`.
- Keine eingebettete Google-Karte und keine Tracker ohne Datenschutz-Klärung.
- Fotos und Logo nur mit Freigabe des Betriebs ins Repo.
