# Portfoilioarbeit - Dashboard
Daniel Bonath, Tim Schacht, Quirin Barth

Video: https://youtu.be/i5NL70oW38g


---

## Ausgefallene Epics
Epic 3 (Datenexport und Reporting) ist durch Zeitbegrenzung ausgefallen, da wir uns eher auf die rollenbasierten Zugriffe konzentrieren wollten. Theoretisch implementierbar als ein Button mit einer Funktion die irgendeine Reporting API anspricht und die Meldung dort abgibt.

Epic 5 (Benutzerdefinierte Dashboards) ist ebenso durch Zeitbegrenzung entfallen, denn der aufwandt die Vorgefertigten Layouts zum laufen zu kriegen hat einen großteil der Zeit gefressen. Das dynamische ändern des dashboards, sowie das speichern der eigenen Layouts, und der implementierung von benutzerdefinierten analysen, hat damit einen zu großen Aufwandt und komplexifizierung des codes dargestellt.

## Implementierung

Dashboard wurde mit dem Python Packet Dash implementiert:
- Kostenfrei
- Einfach zu verwenden
- HTML basierte Layout-construktion
- Direkte Einbindung in gängige Python Web-Interface Packete (Flask, Plotly)

Die verschiedenen Layouts wurden als Klassen in `layout.py` definiert, um diese Modular anpassen zu können.

Dash Auth wird verwendet um einen sicheren Login für die verschiedenen Rollen zu gewährleisten.

