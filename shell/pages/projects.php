<?php
$page_title = "Projekte";
?>
<table class="vhosts">
  <tr>
    <th></th>
    <th><code>DocumentRoot</code></th>
    <th><code>ServerName</code></th>
    <th>Links</th>
  </tr>
  <?php foreach (devbox_find_projects() as $p): ?>
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
