# Devbox Design

Das Devbox-System setzt sich im Wesentlichen aus zwei Komponenten zusammen:

1. Ein Docker-Image, in dem das Entwicklungssystem liegt (Apache, PHP, Datenbankserver, etc.)
2. Tooling zur Steuerung des laufenden Devbox-Containers

## Warum ein "Jumbo-Image" statt mehrerer Images?

Eine Lösung auf Basis von docker-compose mit mehreren Images und Containern ist
für den Einsatzzweck der Devbox aus verschiedenen Gründen unvorteilhaft:

- einige Teile der Devbox müssen interagieren
  - sowohl Webserver- als auch PHP-Container brauchen Zugriff auf den Code
  mitgelieferter Tools
  - `devbox-autoconfig.py` braucht Zugriff auf den Webserver-Container um
  VHost-Configs zu schreiben und den Server neu zu starten

Viele Vorteile von `docker-compose` sind außerdem für die Devbox von geringer
Bedeutung:

- die Verwaltung mehrerer Prozesse sowie automatische Neustarts bei abstürzen
werden im Devbox-Container bereits von runit übernommen
- Devbox ist nicht für skalierbarkeit konzipiert

