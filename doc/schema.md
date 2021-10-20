# Devbox-Projekteschema, aka `.devbox.yml`

Interne Projekte müssen zur Integration im Devbox-System mit einer sogenannten
Projektschemadatei namens `.devbox.yml` ausgestattet sein. In dieser Schemadatei
werden Eigenschaften des Projektes festgehalten, die zur Automatisierung
verschiedener Entwicklungsprozesse erforderlich sind.

\[\[_TOC_\]\]

# Beispiel
```yaml
version: 1

project:
  type: craftcms3
  webroot: backend/web
  php: '7.3'

servers:
  cyon:
    user: riposach
    host: vsa-wiboxu.cyon.net

instances:
  production:
    server: cyon
    path: public_html/production.riposa.ch
    deployment: php-deployer

  staging:
    server: cyon
    path: public_html/staging.riposa.ch
    deployment: php-deployer

  develop:
    server: cyon
    path: public_html/develop.riposa.ch
    deployment: php-deployer
```

# Felder

## `version`

* Mögliche Werte: `1`

Version des Schemas zum Erhalt der Abwärtskompatibilität, sollten später größere
Änderungen am Schemaformat erforderlich werden.

## `project`

Eigenschaften des Projektes.

### `project.type`

Typ des Projektes (normalerweise das verwendete Framework).

Mögliche Werte: `craftcms3`, `contao3`, `contao4`

Dieser Wert ist für Datenbankoperationen sowie Schnellzugriffslinks auf der
devbox-Übersichtsseite erforderlich.

### `project.webroot`

Verzeichnis, das als DocumentRoot für das Projekt gelten soll. Der Pfad wird
relativ zum Wurzelverzeichnis des Projekt-Repositorys angegeben.

Wenn das Web-Verzeichnis wie beispielsweise bei Contao 3 gleich dem
Wurzelverzeichnis des Repositorys ist, muss `.` angegeben werden.

### `project.php`

Zu verwendende PHP-Version. Die verfügbaren Versionen richten sich nach der
Devbox-Version.

## `servers`

Informationen über Server, auf denen Instanzen dieses Projektes laufen.

### `servers.*.user`

Der Linux/Unix-Benutzer, unter dem die Projektinstanz auf diesem Server läuft.

### `servers.*.host`

Der Hostname des Servers.

## `instances`

Laufende Instanzen dieses Projektes.

### `instances.*.server`

Name des Servers, auf dem dieses Projekt läuft. Der Name bezieht sich auf
Einträge unter dem Schlüssel `servers`.

### `instances.*.path`

Pfad, unter dem die Projektinstanz auf dem Server liegt. Relativ zum
Home-Verzeichnis des Server-Benutzers.

**Dieser Pfad muss nicht der DocumentRoot sein** – wird beispielsweise
 Deployer verwendet, bezieht dieser Pfad sich auf das Verzeichnis, in dem
 `current/`, `releases/` und `shared/` liegen.

### `instances.*.deployment`

Verwendete Deployment-Methode dieser Instanz.

Mögliche Werte:
* `manual` – händische Auslieferung per FTP/SFTP/`git pull` auf dem Remote-System
* `php-deployer` – [Deployer](https://deployer.org/)
