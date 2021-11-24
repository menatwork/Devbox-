# Devbox

Autarkes Entwicklungssystem für PHP- und Node-Projekte

Devbox ist ein Entwicklungssystem auf Basis von [Docker][1]. Es fasst alles in
einem Paket zusammen, was zur Arbeit an PHP-Projekten notwendig ist: Apache,
PHP, ein MariaDB-Server und ein Tool namens [Mailcatcher][2], mit dem
Mailversand getestet werden kann.

## Dokumentation

* [Setup](doc/setup.md)
* [Changelog](doc/changelog.md)
* [.devbox.toml](doc/schema-file.md)

## Versionen

Im Devbox-Image 0.3.0 sind folgende Software-Versionen vorhanden:

* PHP: `5.6`, `7.3`, `7.4`, `8.0`

[1]: https://www.docker.com/
[2]: https://mailcatcher.me/
