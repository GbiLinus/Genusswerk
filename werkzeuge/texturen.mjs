// Rendert die SVG-Texturen aus src/texturen/quelle/ zu Bildern.
// SVG-Filter in CSS-Hintergründen rendern Browser unzuverlässig und langsam,
// deshalb liefert die Seite fertige Bilder aus.
// Aufruf aus dem Repo-Root: node werkzeuge/texturen.mjs  (braucht Playwright + Chromium)
import { chromium } from "playwright";
import { readFileSync } from "node:fs";

const texturen = [
  { quelle: "nuss.svg", ziel: "nuss.jpg", w: 900, h: 120, typ: "jpeg" },
  { quelle: "klinker.svg", ziel: "klinker.jpg", w: 240, h: 72, typ: "jpeg" },
  { quelle: "rauschen.svg", ziel: "rauschen.png", w: 240, h: 240, typ: "png", dpr: 1 },
];

const browser = await chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
for (const t of texturen) {
  const seite = await browser.newPage({ viewport: { width: t.w, height: t.h }, deviceScaleFactor: t.dpr ?? 2 });
  const svg = readFileSync(new URL(`../src/texturen/quelle/${t.quelle}`, import.meta.url), "utf8");
  await seite.setContent(`<style>html,body{margin:0;background:transparent}</style>${svg}`);
  await seite.screenshot({
    path: new URL(`../src/texturen/${t.ziel}`, import.meta.url).pathname,
    type: t.typ, omitBackground: t.typ === "png", ...(t.typ === "jpeg" ? { quality: 82 } : {}),
  });
  await seite.close();
  console.log("gerendert:", t.ziel);
}
await browser.close();
