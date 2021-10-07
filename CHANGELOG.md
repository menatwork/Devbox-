# Devbox Changelog

## 0.2.0 (11. Oktober 2021)

| Software | Upgrade |
| --- | --- |
| Ubuntu | 18.04.3 LTS ("bionic") → 20.04.3 LTS ("focal") |
| PHP 7 | 7.3.14 → 7.4.24 |
| Composer 1 | 1.6.3 → 1.10.22 |
| Node.js | 12.14.1 → 14.18.0 |
| Yarn | 1.21.1 → 1.22.15 |
| MariaDB | 10.1.43 → 10.3.31 |

### PHP

* Composer 1 muss nun per `composer1` aufgerufen werden
* Composer 2 wird unter dem Befehl `composer` bereitgestellt
* Das Speicherlimit wurde für alle PHP-Versionen aufgehoben

### Sonstiges

* Der Hilfetext von `devbox help` wurde umstrukturiert
* `htop` und `curl` werden jetzt mitgeliefert
* `devbox build` aktualisiert nicht mehr automatisch das base-image
* `devbox build` nimmt nun ein optionales Versionsargument an, mit dem
  Release-Images getaggt werden können

## 0.1.0 (4. Februar 2020)

* erstes Release
