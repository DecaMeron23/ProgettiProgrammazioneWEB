<?php

/**
 * 
 * @param string $codice
 * @param string $creatore
 * @param string $titolo
 * @param string $data_inizio
 * @param string $data_fine
 * 
 * @return string
 */
function query_quiz($codice, $creatore, $titolo, $data_inizio, $data_fine, $like, $quale_data_inizio, $quale_data_fine): string
{
    $query = "SELECT 	QUIZ.CODICE AS codice , QUIZ.CREATORE AS creatore , QUIZ.TITOLO AS titolo , QUIZ.DATA_INIZIO AS data_inizio,  QUIZ.DATA_FINE AS data_fine, COUNT(DISTINCT DOMANDA.NUMERO) AS domande  , COUNT(DISTINCT PARTECIPAZIONE.CODICE) as partecipazioni 
        FROM QUIZ JOIN DOMANDA JOIN PARTECIPAZIONE ON QUIZ.CODICE = DOMANDA.QUIZ AND QUIZ.CODICE = PARTECIPAZIONE.QUIZ";

    // $ordine = ""; da fare
    $lista = "";
    if ($codice != "") {
        $lista .= (strlen($lista) == 0 ? " WHERE " : " AND ") . "QUIZ.CODICE = '$codice'";
    }
    if ($creatore != "") {
        $lista .= (strlen($lista) == 0 ? " WHERE " : " AND ") . "QUIZ.CREATORE" . ($like ? " LIKE '%$creatore%'" : "= '$creatore'");
    }
    if ($titolo != "") {
        $lista .= (strlen($lista) == 0 ? " WHERE " : " AND ") . "QUIZ.TITOLO" . ($like ? " LIKE '%$titolo%'" : "= '$titolo'");
    }
    if ($data_inizio != "") {
        $lista .= (strlen($lista) == 0 ? " WHERE " : " AND ") . "QUIZ.DATA_INIZIO " . query_data($quale_data_inizio, $data_inizio);
    }
    if ($data_fine != "") {
        $lista .= (strlen($lista) == 0 ? " WHERE " : " AND ") . "QUIZ.DATA_FINE " . query_data($quale_data_fine, $data_fine);
    }
    return $query . $lista . " GROUP BY QUIZ.CODICE";


}
/**
 * 
 * @param int $indice valore compreso tra 0 e 4
 * @param string $data la data
 */
function query_data($indice, $data): string
{
    $sql = "";
    switch ($indice) {
        case 0:
            $sql .= "<";
            break;
        case 1:
            $sql .= "<=";
            break;
        case 2:
            $sql .= "=";
            break;
        case 3:
            $sql .= ">=";
            break;
        case 4:
            $sql .= ">";
            break;
    }
    return $sql . $data;
}


/**
 * Funzione che crea la query per le ricerce sugli utenti
 * 
 * @param bool $like
 * @param string $nomeUtente
 * @param string $nome
 * @param string $cognome
 * @param string $email
 */
function query_utente($nomeUtente, $nome, $cognome, $email, $like): string
{
    $query = "SELECT 	UTENTE.NOME_UTENTE AS nome_utente , UTENTE.NOME AS nome , UTENTE.COGNOME AS cognome , UTENTE.EMAIL AS email  ,      COUNT(DISTINCT QUIZ.CODICE) as numero_quiz , 	COUNT(DISTINCT PARTECIPAZIONE.QUIZ) as numero_partecipazioni 
    FROM UTENTE LEFT JOIN QUIZ ON UTENTE.NOME_UTENTE = QUIZ.CREATORE , PARTECIPAZIONE
    WHERE UTENTE.NOME_UTENTE = PARTECIPAZIONE.UTENTE";


    if ($nomeUtente != "") {
        if ($like) {
            $query = $query . " AND QUIZ.NOME_UTENTE LIKE '%$nomeUtente%'";
        } else {
            $query = $query . " AND QUIZ.NOME_UTENTE = '$nomeUtente'";
        }
    }
    if ($nome != "") {
        if ($like) {
            $query = $query . " AND QUIZ.NOME LIKE '%$nome%'";
        } else {
            $query = $query . " AND QUIZ.NOME = '$nome'";
        }
    }
    if ($cognome != "") {
        if ($like) {
            $query = $query . " AND QUIZ.TITOLO LIKE '%$cognome%'";
        } else {
            $query = $query . " AND QUIZ.TITOLO = '$cognome'";
        }
    }
    if ($email != "") {
        if ($like) {
            $query = $query . " AND QUIZ.EMAIL LIKE '%$email%'";
        } else {
            $query = $query . " AND QUIZ.EMAIL = '$email'";
        }
    }

    $query = $query . "GROUP BY(nome_utente);";

    return $query;
}

/**
 * Funzione che crea la query per le ricerce sugli utenti
 * 
 * @param bool $like
 * @param string $codice
 * @param string $utente
 * @param string $quiz
 * @param string $data
 * @param int $quale_data solo tra 0 e 4 compresi (0 prima, 1 prima e uguale, 2 uguale, 3 dopo e uguale, 4 dopo)
 */
function query_partecipazione($codice, $utente, $quiz, $data, $like, $quale_data  /* inserire altre impostazioni, come bohhh */)
{
    $query = "SELECT PARTECIPAZIONE.CODICE AS codice , PARTECIPAZIONE.UTENTE AS utente , PARTECIPAZIONE.QUIZ AS quiz, PARTECIPAZIONE.DATA AS data, COUNT(DISTINCT *)  
    FROM PARTECIPAZIONE JOIN RISPOSTA_UTENTE_QUIZ ON quiz = RISPOSTA_UTENTE_QUIZ.QUIZ ";

    $lista = "";
    if ($codice != "") {
        $lista .= (strlen($lista) == 0 ? " WHERE " : " AND ") . "PARTECIPAZIONE.CODICE = '$codice'";
    }
    if ($utente != "") {
        $lista .= (strlen($lista) == 0 ? " WHERE " : " AND ") . "PARTECIPAZIONE.UTENTE" . ($like ? " LIKE '%$utente%'" : "= '$utente'");
    }
    if ($quiz != "") {
        $lista .= (strlen($lista) == 0 ? " WHERE " : " AND ") . "PARTECIPAZIONE.QUIZ" . ($like ? " LIKE '%$quiz%'" : "= '$quiz'");
    }
    if ($data != "") {
        $lista .= (strlen($lista) == 0 ? " WHERE " : " AND ") . "PARTECIPAZIONE.DATA ";
        switch ($quale_data) {
            case 0:
                $lista .= "<";
                break;
            case 1:
                $lista .= "<=";
                break;
            case 2:
                $lista .= "=";
                break;
            case 3:
                $lista .= ">=";
                break;
            case 4:
                $lista .= ">";
                break;
        }
        $lista .= " '$data'";
    }

    $query .= $lista . " GROUP BY(codice)";
}
