# TradeX-Blog: Ablauf

Lars wirft eine Idee in den ReachX-Projektchat (Link, Stichwort, Foto, Gedanke).
Claude macht daraus einen Beitrag auf https://tradexag.ch/blog/ und öffnet einen PR.
Live geht er erst, wenn Lars den PR mergt (GitHub Pages veröffentlicht `main`).

## Grundsatz (Lars, 24.11.2026)

> „Wir schreiben alles für uns um und unser System, wie wir arbeiten.“

- Die Idee ist nur der Anlass. Jeder Beitrag erzählt, **wie wir bei TradeX
  arbeiten**: unser Vorgehen, unsere Werkzeuge, unsere Erfahrungen. Danach,
  was Händler und Marken daraus mitnehmen.
- Nie abschreiben. Fremde Quelle nur als Anregung nennen (Feld `quelle`).
- Nur behaupten, was belegbar ist. Aussagen über unsere Arbeitsweise und
  Software gegen den Code prüfen: `tradexag/aseio` (`AGENTS.md`,
  `docs/TICKETS.md`, `app/`), `tradexag/marketingmachine` (ReachX),
  diese Website. Tabelle „Aussage → Beleg“ in die PR-Beschreibung.
- Keine Kundennamen, keine Kundenzahlen ohne Zustimmung des Kunden, keine
  internen Preise, Margen oder Einkaufspreise, keine Zugangsdaten.

## Stil

Siehe `voice.md` im Projektordner (linkedin-voice). Kurz: Ergebnis zuerst
(„Kurz gesagt:“), kurze Sätze, Du, „wir“ für TradeX, keine Emoji, keine
Superlative, Zahlen statt Adjektive, Schweizer Schreibweise (ss statt ß).

## SEO (Lars, 24.11.2026: „für Google richtig SEO-optimiert“)

- **Ein Hauptkeyword** je Beitrag (Feld `keyword`), so wie Leute suchen.
  Es steht in `title`, im ersten Absatz, in mindestens einer H2 und in
  `description`.
- `title` höchstens 60 Zeichen (wird `<title>`), `description` 120 bis 160
  Zeichen. Das Skript bricht sonst ab. `h1` darf länger und griffiger sein.
- `slug` kurz, nur Kleinbuchstaben, Ziffern und Bindestriche, mit Keyword.
  Ein veröffentlichter Slug ändert sich nie mehr.
- Aufbau: „Kurz gesagt“, dann H2/H3, Tabellen und Listen, wo sinnvoll.
  800 bis 1.800 Wörter. Ende: Checkliste (optional) und `## Häufige Fragen`
  mit 3 bis 5 `### Frage` + einem Absatz (wird FAQ-Rich-Result).
- 2 bis 3 interne Links (andere Blogbeiträge `/blog/<slug>/`, Wissensdatenbank
  `/wissen/sicherheit/…`, `/termin/`), relativ.
- Das Skript erzeugt automatisch: Canonical, Open Graph, Twitter-Karte,
  JSON-LD (BlogPosting, BreadcrumbList, FAQPage, Blog), Vorschaubild
  1200×630 je Beitrag, RSS-Feed, Sitemap-Block mit `lastmod`,
  „Weitere Beiträge“.
- Inhalt ändern: `updatedAt` setzen, dann neu bauen.

## Schritte

1. Idee lesen. Links mit dem Browser öffnen (Flipboard/heise lassen sich nicht
   per WebFetch holen). Bezahlschranke: nur den freien Teil verwenden.
2. Belege sammeln (siehe Grundsatz).
3. Entwurf als `tools/blog/beitraege/JJJJ-MM-TT-<kurz>.md` nach dem Muster des
   ersten Beitrags. Kopf-Felder: `slug, title, h1, description, excerpt,
   keyword, category, publishedAt, updatedAt, author, quelle` (quelle:
   `Name | URL`, optional). `entwurf: ja` blendet einen Beitrag aus.
   Kategorien bisher: „So arbeiten wir“.
4. Bauen im Repo-Wurzelverzeichnis: `python3 tools/blog/bauen.py`
   (Vorschaubild braucht Node mit Playwright oder Puppeteer).
5. Seite und `og.png` ansehen (Desktop und 390 px breit, kein seitliches
   Scrollen).
6. Branch, Commit, PR gegen `main` in `tradex-ag/TradeX`, Titel
   `Blog: <h1>`. Lars als Assignee. Nicht mergen.
7. Lars eine kurze Nachricht: Titel, PR-Link, Keyword, eine Zeile Inhalt.
