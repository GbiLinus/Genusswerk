# Genusswerk – Projektregeln

- Sprache der Seite und der Doku: Deutsch, Gäste per Du ansprechen (wie Betrieb).
- Inhalte nur in `daten/inhalte.json` pflegen. `index.html`, `karte/`, `impressum/`, `datenschutz/` erzeugt `python3 build.py`, nie von Hand ändern.
- Pflicht: Nach Neuladen startet jede Seite oben. Nie `scroll-behavior: smooth` auf `html` setzen. Anker-Links ohne `#hash` in der URL (siehe `src/site.js`). Nach Änderungen an Layout oder JS die Regel in Chromium testen (Seite scrollen, neu laden, `scrollY` muss 0 sein; auch mit `#hash` in der URL).
- Design-Richtung und Farben: `docs/KONZEPT.md` und `src/design-tokens.css`. Weißer Text auf Orange nur mit `--orange-tief` (Kontrast 5,7:1). Kein Blau: Farben kommen aus Decke, Nussholz, Klinker, Stahl, LED und Orange.
- `site.vorschau` bleibt `true`, bis der Betreiber freigibt.
- Offene Punkte stehen in `FEHLT.md`. Erledigtes dort abhaken.
- Keine Fotos oder Logos ohne Freigabe ins Repo.
- Bewegung sparsam: ein Lade-Moment im Hero, sonst nur Reaktionen auf Scrollen oder Klicks. Jede Animation muss bei `prefers-reduced-motion: reduce` aus sein.
- Texturen nicht als SVG-Filter im CSS verwenden (rendert in Chromium lückenhaft). Quelle in `src/texturen/quelle/` ändern, dann `node werkzeuge/texturen.mjs`.
