# Schemadatei (`.devbox.yml`)

Interne Projekte müssen zur Integration im Devbox-System mit einer
Projektschemadatei namens `.devbox.yml` ausgestattet sein. In dieser Schemadatei
werden Eigenschaften des Projektes definiert, die zur Automatisierung
verschiedener Prozesse erforderlich sind.

\[\[_TOC_\]\]

## Beispiel

```yaml
version: '1'

project:
  type: craftcms3
  webroot: backend/web
  php: '7.3'
  resources:
    - web/assets

instances:
  production:
    ssh:
      host: vsa-wiboxu.cyon.net
      user: riposach
    deployment:
      method: deployer
      dir: ~/public_html/production.riposa.ch

  staging:
    ssh:
      host: vsa-wiboxu.cyon.net
      user: riposach
    deployment:
      method: deployer
      dir: ~/public_html/staging.riposa.ch

  develop:
    ssh:
      host: vsa-wiboxu.cyon.net
      user: riposach
    deployment:
      method: deployer
      dir: ~/public_html/develop.riposa.ch
```

## Felder

Mit einem `*` markierte Felder sind erforderlich.

### `version` `*`

* mögliche Werte: `'1'`

Version des Schemas zum Erhalt der Abwärtskompatibilität, sollten später größere
Änderungen am Schemaformat erforderlich werden.

### `project` `*`

Eigenschaften des Projektes selbst.

#### `project.type`

* mögliche Werte: `craftcms3`, `contao3`, `contao4`

Typ des Projektes; meist das verwendete Framework oder CMS.

Dieses Feld ist für Datenbankoperationen sowie Schnellzugriffslinks auf der
Devbox-Übersichtsseite erforderlich.

#### `project.webroot`

Verzeichnis, das vom Entwicklungsserver als DocumentRoot für das Projekt benutzt
werden soll.

Dieser Wert wird relativ zum Wurzelverzeichnis des Projekt-Repositorys
angegeben. Wenn das Web-Verzeichnis wie beispielsweise bei Contao 3 gleich dem
Wurzelverzeichnis des Repositorys ist, muss `.` angegeben werden.

#### `project.php`

* mögliche Werte: `5.6`, `7.3`, `7.4`, `8.0`

PHP-Version, die vom Entwicklungsserver benutzt werden soll.

#### `project.resources`

Eine Liste von Pfaden, unter denen dynamische Seitenressourcen liegen. Dateien
unter diesen Pfaden werden generell nicht ins Repository aufgenommen und sollten
in der `.gitignore` des Projektes aufgeführt sein.

Diese Option wird z.B. von `devbox sync` verwendet, um Inhaltsdaten von einer
Seiteninstanz zu beziehen.

### `instances.<name>`

Instanzen dieses Projektes auf Remote-Servern.

#### `instances.<name>.ssh.host` `*`

Hostname, unter dem die Instanz per SSH erreichbar ist.

#### `instances.<name>.ssh.user` `*`

Benutzername für das SSH-Login.

#### `instances.<name>.deployment.type` `*`

Verwendete Deployment-Methode dieser Instanz. Dieser Wert ist für die
Synchronisation von Seitenressourcen erforderlich.

Mögliche Werte:

* `manual` – manuelles Deployment
* `deployer` – [Deployer](https://deployer.org/)

#### `instances.<name>.deployment.dir` `*`

Pfad, unter dem diese Instanz auf dem Server liegt. Relativ zum Home-Verzeichnis
des Server-Benutzers.

**Hinweis:** Dieser Pfad ist nicht immer dem DocumentRoot oder dem
Repository-Verzeichnis gleich. Wird z.B. Deployer verwendet, bezieht `dir` sich
auf das Deployer-Verzeichnis, in dem `current/`, `releases/` und `shared/`
liegen.
