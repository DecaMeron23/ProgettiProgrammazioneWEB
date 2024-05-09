<?

header('Content-Type: application/json');

include "funzioniDB.php";

$aResult = array();
switch ($_GET["functionname"]) {
    case 'getQUIZ':
        $aResult = query_quiz($_GET["id_quiz"], "", "", "", "", true,  "", "");
        break;
    case 'addQUIZ':
        $aResult = aggiungi_quiz($_GET["nome_utente"], $_GET["titolo"], $_GET["data_inizio"], $_GET["data_fine"]);
        break;
    case 'deleteQUIZ':
        $aResult = elimina_quiz($_GET["id_quiz"]);
        break;
    case 'updateQUIZ':
        $aResult = update_quiz($_GET["id_quiz"], $_GET["nome_utente"], $_GET["titolo"], $_GET["data_inizio"], $_GET["data_fine"]);
        break;
    case 'get_risposte_corrette':
        $aResult = get_risposte_corrette($_GET["codice"]);
}
echo $aResult;
return $aResult;
