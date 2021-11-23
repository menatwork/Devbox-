# Setup-Anleitung

Die einzige aktuell unterstützte Setup-Methode ist das Setup per Repository.

## Setup per Repository

Klone dir zuerst das Devbox-Repo in einen Ordner deiner Wahl:

```
$ git clone git@gitlab.men-at-work.de:entwicklung/devbox.git
```

Als nächstes musst du dir einen Ordner aussuchen, in dem die Projekte liegen,
an denen du mit Devbox arbeitest. Falls du noch keinen Ordner dafür hast kannst
du per `mkdir` einen erstellen, z.B.: `mkdir ~/sites`

Kopiere dir jetzt im Devbox-Repository die `.env.sample`-Datei nach `.env`
und setz darin die Variable `DEVBOX_PROJECTS_DIR` auf das Verzeichnis, das du
für deine Projekte benutzen willst. Das könnte zum Beispiel so aussehen:

```
$ cd devbox
$ cp .env.sample .env
$ nano .env
```

Als letztes solltest du noch den `devbox`-Befehl in deiner `PATH`-Variable
installieren, damit du egal aus welchem Ordner heraus `devbox` aufrufen kannst.
Das machst du, indem du in der Datei `~/.bashrc` diese Zeile am Ende anfügst:

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
[1]: https://www.docker.com/products/docker-desktop
[2]: https://gitforwindows.org/
