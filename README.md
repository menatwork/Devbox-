# devbox

devbox ist ein autarkes Entwicklungssystem auf Basis von
[Docker][1]. Es fasst alles in einem Container zusammen, was zur
Arbeit an PHP-Projekten notwendig ist: Apache, PHP, ein MariaDB-Server
und ein Tool namens [Mailcatcher][2], mit dem Mailversand getestet
werden kann.

## Installation

### Windows

1. [Docker Desktop][3] installieren
2. Den eigenen Benutzer zur lokalen `docker-users`-Gruppe hinzufügen
   (am besten einen Windows-Admin fragen)
3. [Git for Windows][4] installieren
4. → Allgemeine Schritte

### Ubuntu & Ubuntu-Derivate

1. `sudo apt install docker.io`
2. `sudo gpasswd -a $(whoami) docker`
3. Neu anmelden, um die Änderung der Benutzergruppen zu übernehmen
4. → Allgemeine Schritte

### Allgemeine Schritte

```
$ git clone https://gitlab.men-at-work.de/entwicklung/devbox.git
$ cd devbox
$ bin/devbox setup
```

[1]: https://www.docker.com/
[2]: https://mailcatcher.me/
[3]: https://www.docker.com/products/docker-desktop
[4]: https://gitforwindows.org/
