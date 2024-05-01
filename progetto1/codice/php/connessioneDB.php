<?php
$nomeServer = "localhost";
$username = "quizmakeandplay";
$dbname = "my_quizmakeandplay";
$password = null;
$error = false;

try {
    $connessione = new PDO(
        "mysql:host=" . $nomeServer . ";" . "dbname=" . $dbname,
        $username,
        $password
    );

    $connessione->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

} catch (PDOException $e) {
    echo "<p>DB Error: " . $e->getMessage() . "</p>";
    $error = true;
}