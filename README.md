# Devbox

**Hinweis**: Das Devbox-System ist zurzeit nicht für den produktiven Einsatz
vorgesehen. Wichtige Dokumentation kann fehlen, und es kann zu unvorhergesehene
Änderungen kommen. Die Benutzung erfolgt auf eigene Gefahr.

Autarkes Entwicklungssystem für PHP- und Node-Projekte

Devbox ist ein Entwicklungssystem auf Basis von [Docker][1]. Es fasst alles in
einem Paket zusammen, was zur Arbeit an PHP-Projekten notwendig ist:

* Apache
* PHP in mehreren Versionen
* MariaDB
* [MailCatcher][2]

## Dokumentation

* [Setup](docs/setup.md)
* [Changelog](docs/changelog.md)
* [.devbox.toml](docs/schema-file.md)

[1]: https://www.docker.com/
[2]: https://mailcatcher.me/

## Copyright & Lizensierung

Devbox ist geistiges Eigentum der [MEN AT WORK Werbeagentur GmbH][maw] und steht
under der GPL-3.0-Lizenz. Eine Kopie des Lizenztexts ist in der Datei `COPYING`
enthalten.

[maw]: https://www.men-at-work.de/
