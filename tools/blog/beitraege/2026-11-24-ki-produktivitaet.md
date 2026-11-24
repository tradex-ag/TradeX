---
slug: ki-produktivitaet-schneller-code
title: KI-Produktivität: Schneller Code ist nicht schneller live
h1: Schneller programmieren heisst nicht schneller live
description: KI schreibt Code in Minuten, live geht trotzdem nichts schneller. Wie wir bei TradeX mit KI entwickeln und wo die Zeit wirklich hängen bleibt.
excerpt: KI schreibt Code in Minuten. Trotzdem ist eine Änderung nicht schneller live. So bauen wir bei TradeX Software mit KI, und hier hängt bei uns die Zeit.
keyword: KI-Produktivität
category: So arbeiten wir
publishedAt: 2026-11-24
updatedAt: 2026-11-24
author: Lars Orlamünde
quelle: Kai Spichale, „Die KI-Produktivitätslüge“, iX 1/2027 | https://www.heise.de/hintergrund/Die-KI-Produktivitaetsluege-Warum-schnellerer-Code-nichts-bringt-11511612.html
---

**Kurz gesagt:** KI-Produktivität beim Programmieren ist echt. Bei uns schreibt KI einen grossen Teil des Codes. Trotzdem ist eine Änderung dadurch nicht automatisch schneller live. Die Zeit hängt woanders: in der Prüfung, beim Zusammenführen und bei der Freigabe. Hier zeigen wir, wie wir bei TradeX arbeiten und was wir gegen die Wartezeit tun.

## KI-Produktivität: die Beobachtung dahinter

In der iX beschreibt Kai Spichale von SAP etwas, das viele Teams kennen: Einzelne Entwickler sind mit KI deutlich schneller. Bis eine Änderung beim Nutzer ankommt, dauert es aber nicht im gleichen Mass kürzer. KI verkürzt die Arbeit an einer Aufgabe. Die Zeit, in der eine Aufgabe nur liegt und wartet, bleibt.

Wir haben genau das in unserem eigenen Alltag gesehen. Deshalb schreiben wir hier auf, wie wir das lösen.

## Wie wir bei TradeX Software mit KI bauen

Wir entwickeln unsere eigene Software mit KI, unter anderem die Marktplatz-Software ASEIO. Dabei arbeiten mehrere KI-Modelle mit festen Rollen zusammen. Der Grundsatz: Kein Modell prüft seine eigene Arbeit.

| Rolle | Wer | Ergebnis |
|---|---|---|
| Planen | ein KI-Modell | Ziel, Umfang, Abnahmekriterien, Auftrag |
| Umsetzen | ein zweites KI-Modell | Code und Tests, noch nicht übernommen |
| Prüfen | ein drittes KI-Modell | Bestanden und übernommen, oder eine Fix-Liste zurück |
| Freigeben | ein Mensch | Entscheidung, was live geht |

Der Mensch steht am Ende. Was live geht, entscheidet bei uns Lars. Das ist bewusst so.

Dazu kommen ein paar feste Regeln:

- **Jede Arbeit hat eine Nummer.** Kein Umbau und kein Feature startet ohne Eintrag auf unserem Board. Die Nummer zieht sich durch Plan, Auftrag, Prüfbericht und Commit.
- **Eine Stelle für den Stand.** Das Board ist die einzige Quelle dafür, wo eine Aufgabe steht. Ob etwas umgesetzt, getestet oder live ist, tippt niemand von Hand. Das leitet ein Werkzeug aus Belegen ab: Commit, Prüfbericht, Testlauf, Live-Version.
- **Die Regeln stehen im Code.** Wie gearbeitet wird, steht als Datei im Repository. Jedes Modell liest sie vor der Arbeit. Eine Regel nur im Kopf oder nur in einem Chat reicht nicht.
- **Das passende Modell für die Aufgabe.** Einfache Aufgaben bekommen ein günstiges Modell, schwere ein starkes. Das spart Budget und Zeit.

## Wo bei uns die Zeit wirklich hängt

Seit die KI den Code schreibt, ist das Schreiben selten der Engpass. Die Zeit hängt an vier anderen Stellen.

### 1. Prüfen

Mehr Code heisst mehr zu prüfen. Wenn jede Änderung erst nach Stunden geprüft wird, ist die gewonnene Zeit weg.

### 2. Tests

Eine volle Testsuite über das ganze Projekt dauert. Läuft sie vor jedem kleinen Schritt, wartet jeder Schritt auf sie.

### 3. Zusammenführen

Oft arbeiten mehrere Sitzungen parallel am selben Projekt. Jede ist schnell. Aber ihre Ergebnisse müssen sauber zusammenkommen, ohne sich gegenseitig zu überschreiben.

### 4. Freigabe

Die Freigabe durch einen Menschen ist der langsamste Schritt. Wenn die KI mehr liefert, liegt dort mehr.

## Was wir gegen die Wartezeit tun

1. **Prüfung als eigene Rolle mit klarem Ergebnis.** Die Prüfung endet immer mit „bestanden“ oder mit einer konkreten Fix-Liste. Kein „sieht gut aus, aber“. Die Fix-Liste geht direkt zurück an die Umsetzung.
2. **Tests nach Wirkung statt immer alles.** Vor jedem Schritt laufen Typprüfung und Lint über das ganze Projekt, dazu nur die Tests der Dateien, die sich geändert haben. Die volle Testsuite läuft einmal täglich und immer vor einer Auslieferung.
3. **Kleine Schnitte.** Eine grosse Aufgabe zerlegen wir in Schritte, die einzeln geprüft und übernommen werden. Kleine Schritte sind schneller geprüft, und ein Fehler trifft weniger.
4. **Nur eigene Dateien übernehmen.** Jede Sitzung übernimmt gezielt ihre eigenen Änderungen und lässt fremde unangetastet. So kommen parallele Ergebnisse sauber zusammen.
5. **Freigaben vorbereiten.** Was zu Lars geht, ist geprüft, getestet und kommt mit einer klaren Empfehlung. Die Entscheidung dauert dann Minuten statt Tage.
6. **Wartezeit sichtbar machen.** Auf dem Board steht, worauf eine Aufgabe wartet und auf wen. Was liegt, fällt auf.

## Was das für Online-Händler heisst

Im E-Commerce ist es dasselbe Muster. KI schreibt Produkttexte und Auswertungen in Minuten. Das Listing ist trotzdem erst nach einer Woche online. Ein ausgedachtes Beispiel, keine Messung:

| Schritt | Arbeit | Warten |
|---|---|---|
| Stammdaten aus der Warenwirtschaft holen | 15 Min. | 2 Tage |
| Titel, Bullet Points und Attribute schreiben | mit KI 10 Min. | – |
| Freigabe durch Marke oder Geschäftsführung | 10 Min. | 4 Tage |
| Preis festlegen, Gebühren einrechnen | 20 Min. | 1 Tag |
| Hochladen, Fehler des Marktplatzes beheben | 30 Min. | 1 Tag |

Die Hebel sind dieselben wie bei uns: eine Datenquelle, Regeln als Einstellung statt als Rückfrage, automatische Prüfungen, kleine Schritte und vorbereitete Freigaben. Gemessen wird am Ende nicht, wie viel die KI erzeugt, sondern was im Deckungsbeitrag 3 ankommt.

Wie wir dabei Daten und Zugänge absichern, steht in unserer Wissensdatenbank [Sicherheit für Web-Apps](/wissen/sicherheit/), zum Beispiel im Kapitel [Mandantentrennung](/wissen/sicherheit/04-mandantentrennung/).

## Checkliste

- [ ] Für zwei, drei typische Aufgaben ist die Zeit vom Auftrag bis „live“ gemessen.
- [ ] Es ist bekannt, wo die Arbeit am längsten liegt.
- [ ] Wer etwas erzeugt, prüft es nicht selbst.
- [ ] Jede Prüfung endet mit „bestanden“ oder einer konkreten Fix-Liste.
- [ ] Vor jedem Schritt laufen die schnellen Prüfungen, die volle Prüfung regelmässig.
- [ ] Aufgaben gehen in kleinen Schritten live.
- [ ] Freigaben kommen vorbereitet und mit Empfehlung.
- [ ] Der Stand jeder Aufgabe steht an genau einer Stelle.

## Häufige Fragen

### Bringt KI beim Programmieren dann gar nichts?

Doch, viel. Bei uns schreibt KI einen grossen Teil des Codes. Der Gewinn kommt aber erst beim Nutzer an, wenn Prüfung, Tests und Freigabe mithalten.

### Warum prüft bei euch ein anderes Modell als das, das programmiert hat?

Weil ein Modell, das seine eigene Arbeit prüft, dieselben Annahmen noch einmal trifft. Ein zweites Modell mit eigenem Auftrag findet mehr. Das ist wie das Vier-Augen-Prinzip unter Menschen.

### Kann man die menschliche Freigabe nicht weglassen?

Nicht bei allem, was live geht. Wir lassen sie bewusst stehen und machen sie schnell: Was zur Freigabe kommt, ist geprüft, getestet und kommt mit einer Empfehlung.

### Womit fange ich an, wenn ich das im eigenen Team einführen will?

Mit einer Messung. Nimm eine Aufgabe, die oft vorkommt, und schreib zwei Wochen lang auf, wann sie wo liegt. Die längste Wartezeit ist dein erster Hebel.
