# pyKasso

(c) Jan-Peer Grunwald,  pekh@eufrutki.net

Werkzeuge zur Erleichterung der Kassenverwaltung.

## Idee

In unserem Verein wird [GnuCash]:https://www.gnucash.org zur Verwaltung unserer Kasse verwendet. Grundsätzlich verfügt jedes Mitglied über ein eigenes Konto und soll mehrmals im Jahr eine Abrechnung / einen Kontoauszug erhalten. Die Anforderungen sind wie folgt:

- Jedes Mitglied soll eine separate PDF-Datei mit allen im Zeitraum angefallenen Transaktionen erhalten.
- Diese PDF-Datei soll (halb-)automatisch per E-Mail verschickt werden können.

Ziel ist es, den Arbeitsaufwand für die Kassierer so weit wie möglich auf die reine Buchhaltung zu beschränken.

**pyKasso** soll in der ersten Ausbaustufe folgendes leisten:

- eine in GnuCash erzeugte CSV-Datei (Export aller auf den Mitgliederkonten gelaufenen Transaktionen in einem definierten Zeitraum, eine Zeile pro Transaktion) einlesen,
- daraus die entsprechenden Abrechnungen (PDF) generieren und in einem zu definierenden Ausgabeverzeichnis ablegen,
- und auf Wunsch sofort oder später an die hinterlegte E-Mail-Adresse des Empfängers versenden.

Grundsätzlich reden wir hier immer von Stapel-Operationen, d.h. ich möchte nicht anfangen, jede E-Mail einzeln freizugeben.