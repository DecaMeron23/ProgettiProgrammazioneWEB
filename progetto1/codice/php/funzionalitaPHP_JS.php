<?

header('Content-Type: application/json');

include "funzioniDB.php";

$aResult = array();
switch ($_GET["functionname"]) {
    case 'getQUIZ':
        $aResult = query_quiz($_GET["id_quiz"], "", "", "", "", true,  "", "");
        break;
}

echo $aResult;
return $aResult;
