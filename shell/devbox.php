<?php
define("DEVBOX_PROJECTS_DIR"    , "/projects");
define("DEVBOX_HOSTNAME"        , "devbox.localhost");

define("PROJECT_TYPE_UNKNOWN"   , "unknown");
define("PROJECT_TYPE_CONTAO3"   , "contao3");
define("PROJECT_TYPE_CONTAO4"   , "contao4");
define("PROJECT_TYPE_CRAFTCMS3" , "craftcms3");

class Project {
  public $serverName;
  public $documentRoot;
  public $type;

  public function __construct($documentRoot, $type, $serverName) {
    $this->documentRoot = $documentRoot;
    $this->type         = $type;
    $this->serverName   = $serverName;
  }

  public function links(): string {
    $html = "";

    switch ($this->type) {
      case PROJECT_TYPE_CONTAO3:
        $html .= html_link("/contao",             "http://" . $this->serverName . "/contao");
        $html .= html_link("/contao/install.php", "http://" . $this->serverName . "/contao/install.php");
	break;

      case PROJECT_TYPE_CONTAO4:
        $html .= html_link("/contao",         "http://" . $this->serverName . "/contao");
        $html .= html_link("/contao/install", "http://" . $this->serverName . "/contao/install");
        break;

      case PROJECT_TYPE_CRAFTCMS3:
        $html .= html_link("/admin", "http://" . $this->serverName . "/admin");
        break;
    }

    return $html;
  }
}

function find_projects(): array {
  $projects = [];

  foreach (glob(DEVBOX_PROJECTS_DIR . "/*/.devbox.yml") as $schema_file) {
    $raw_yaml = file_get_contents($schema_file);
    $schema = yaml_parse($raw_yaml);

    $webroot = $schema["project"]["webroot"];
    if (!isset($webroot)) {
      continue;
    }

    $dir           = dirname($schema_file);
    $name          = basename($dir);
    $document_root = realpath("$dir/$webroot");
    $host          = "$name." . DEVBOX_HOSTNAME;
    $type          = $schema["project"]["type"];

    $projects[] = new Project($document_root, $type, $host);
  }

  usort($projects, function($a, $b) {
    return $a->type >= $b->type;
  });

  return $projects;
}

function html_link(string $text, string $href): string {
  return '<a href="' . $href . '">' . $text . '</a> ';
}
