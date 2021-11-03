# Installation

Hier wird die Installation der Devbox auf unterstützten Systemen beschrieben.

## Windows

1. [Docker Desktop][1] installieren
2. Den eigenen Benutzer zur lokalen `docker-users`-Gruppe hinzufügen
   (hierzu am besten einen Windows-Admin fragen)
3. [Git for Windows][2] installieren
4. → Allgemeine Schritte

## Ubuntu & Ubuntu-Derivate

1. `sudo apt install docker.io`
2. `sudo gpasswd -a $(whoami) docker`
3. Neu anmelden, um die Änderung der Benutzergruppen zu übernehmen
4. → Allgemeine Schritte

## Allgemeine Schritte

```
$ git clone https://gitlab.men-at-work.de/entwicklung/devbox.git
$ cd devbox
$ cp .env.sample .env
```

1. `.env`-Datei anpassen
2. `docker login gitlab.men-at-work.de:4774` ausführen und mit GitLab-Zugang anmelden
3. In `~/.bashrc` (oder der RC-Datei deiner Lieblingsshell) folgendes eintragen:
   ```
   eval $(<pfad_zum_devbox_repository>/bin/devbox shell-init)
   ```
4. Pfadänderung für den `devbox`-Befehl aktivieren:
  - entweder einen neuen Terminal öffnen...
  - ... oder den Code aus dem vorherigen Schritt im aktuellen Terminal ausführen
5. Aktuelles Devbox-Image mit `devbox pull` beziehen

Die Devbox sollte nun per `devbox run` gestartet werden können.

[1]: https://www.docker.com/products/docker-desktop
[2]: https://gitforwindows.org/
