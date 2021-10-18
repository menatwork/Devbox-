<?php
require_once "devbox.php";

$start = microtime(true);
$page = 'pages/projects.php';

if (isset($_GET['page'])) {
  $page = 'pages/' . $_GET['page'] . '.php';
}

if (!file_exists($page)) {
  $page = 'pages/not-found.php';
}

ob_start();
require_once $page;
$page_body = ob_get_clean();
?>
<!DOCTYPE html>
<link rel="stylesheet" href="//<?= DEVBOX_HOSTNAME ?>/style.css">
<link rel="icon" type="image/png" href="//<?= DEVBOX_HOSTNAME ?>/img/favicon.png" sizes="32x32">
<title><?= $page_title ?> • <?= DEVBOX_HOSTNAME ?></title>

<header class="page-header">
  <h1 class="page-title"><?= DEVBOX_HOSTNAME ?></h1>
</header>

<main class="page-main">
  <?= $page_body ?>
</main>

<footer class="page-footer">
  <?php
  $end = microtime(true);
  $elapsed = $end - $start;
  ?>
  Rendered in <?= round($elapsed, 4) ?> ms
</footer>
