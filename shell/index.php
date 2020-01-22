<?php
require_once "devbox.php";
$start = microtime(true);
?>
<!DOCTYPE html>
<link rel="stylesheet" href="style.css">
<link rel="icon" type="image/png" href="/img/favicon.png" sizes="32x32">
<title>devbox.localhost</title>

<header class="page-header">

  <h1 class="page-title">devbox.localhost</h1>

</header>

<main class="page-main">

  <table class="vhosts">
    <tr>
      <th></th>
      <th><code>DocumentRoot</code></th>
      <th><code>ServerName</code></th>
      <th>Links</th>
    </tr>
    <?php foreach (find_projects() as $p): ?>
      <tr>
	<td>
	  <img class="project-icon" src="/img/icon-<?= $p->type ?>.png" alt="<?= $p->type ?>">
	</td>

	<td>
	  <code><?= $p->documentRoot ?></code>
	</td>

	<td>
	  <a href="http://<?= $p->serverName ?>"><?= $p->serverName ?></a>
	</td>

	<td class="project-links">
	  <?= $p->links() ?>
	</td>
      </tr>
    <?php endforeach; ?>
  </table>

</main>

<footer class="page-footer">
  <?php
  $end = microtime(true);
  $elapsed = $end - $start;
  ?>
  Rendered in <?= round($elapsed, 4) ?> ms
</footer>
