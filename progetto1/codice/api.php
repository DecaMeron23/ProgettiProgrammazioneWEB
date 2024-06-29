<?php

header('Content-Type: application/json');

include_once "php/funzioniDB.php";


if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $query = $_GET["query"];
    $isSelect = $_GET["isSelect"] == 1;

    $risultato = eseguiQuery($query , $isSelect);

    echo json_encode($risultato);
}

?>