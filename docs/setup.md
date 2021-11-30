# Setup-Anleitung

Die einzige aktuell unterstützte Setup-Methode ist das Setup per Repository auf
einem Ubuntu-System (18.04 oder neuer).

Devbox ist theoretisch auch unter Windows in [WSL2][wsl2] lauffähig. Hier sind
aber zusätzliche Schritte notwendig, die noch nicht dokumentiert sind.

## Abhängigkeiten

Damit das Devbox-Tooling funktioniert müssen bestimmte Systempakete installiert
sein. Folgender Befehl installiert diese Pakete:

```
$ sudo apt install python3-cerberus python3-docker python3-toml xdg-utils
```

## Setup per Repository

Klone dir zuerst das Devbox-Repo in einen Ordner deiner Wahl:

```
$ git clone git@gitlab.men-at-work.de:entwicklung/devbox.git
```

Als nächstes musst du dir einen Ordner aussuchen, in dem die Projekte liegen
werden, an denen du mit Devbox arbeitest. Falls du noch keinen Ordner dafür hast
kannst du per `mkdir` einen erstellen, z.B.: `mkdir ~/sites`

Lege jetzt im Devbox-Repository die Datei `config/local.toml` mit folgendem
Inhalt an (`~/sites` ersetzt du natürlich mit deinem Projektordner):

```toml
[general]
projects_root = ~/sites
```

Als letztes solltest du noch den `devbox`-Befehl in deiner `PATH`-Variable
installieren, damit du egal in welchem Ordner du bist `devbox` aufrufen kannst.
Dafür fügst du am Ende deiner `~/.bashrc` diese Zeile an:

```
eval $(<pfad_zum_devbox_repository>/bin/devbox shell-init)
```

Öffne jetzt einen neuen Terminal und führ darin `devbox` aus. Wenn alles
funktioniert sollte das in etwa so aussehen:

```
$ devbox
[devbox] CRITICAL: Kein Befehl angegeben!
[devbox] WARNING: Hilfetext fehlt.
```

Jetzt kannst du entweder per `devbox pull` das aktuelle Image aus unserem
GitLab-Registry beziehen, oder per `devbox build` dein eigenes Image bauen.

Danach ist der Entwicklungsserver startklar und kann per `devbox run` ausgeführt
werden.

Happy hacking!

[wsl2]: https://docs.microsoft.com/de-de/windows/wsl/
