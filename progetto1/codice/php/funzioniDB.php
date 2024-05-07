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
function query_quiz($codice, $creatore, $titolo, $data_inizio, $data_fine, $like, $quale_data_inizio, $quale_data_fine, $domande = "", $quali_domande = "", $partecipazioni = "", $quali_partecipazioni = ""): string
{
    $query = "SELECT QUIZ.CODICE AS codice, QUIZ.CREATORE AS creatore, QUIZ.TITOLO AS titolo, QUIZ.DATA_INIZIO AS data_inizio, QUIZ.DATA_FINE AS data_fine, COUNT(DISTINCT DOMANDA.NUMERO) AS domande, COUNT(DISTINCT PARTECIPAZIONE.CODICE) AS partecipazioni
    FROM  QUIZ LEFT JOIN DOMANDA ON QUIZ.CODICE = DOMANDA.QUIZ LEFT JOIN PARTECIPAZIONE ON QUIZ.CODICE = PARTECIPAZIONE.QUIZ ";

    $titolo = str_replace("'", "''", $titolo);

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
    if ($data_inizio != "" && $quale_data_inizio != "") {
        $lista .= (strlen($lista) == 0 ? " WHERE " : " AND ") . "QUIZ.DATA_INIZIO " . query_data($quale_data_inizio, $data_inizio);
    }
    if ($data_fine != "" && $quale_data_fine != "") {
        $lista .= (strlen($lista) == 0 ? " WHERE " : " AND ") . "QUIZ.DATA_FINE " . query_data($quale_data_fine, $data_fine);
    }
    $query .=  $lista . " GROUP BY QUIZ.CODICE, QUIZ.CREATORE, QUIZ.TITOLO, QUIZ.DATA_INIZIO, QUIZ.DATA_FINE ";


    $having = "";

    if ($domande != "" && $quali_domande != "") {
        $having .= " HAVING domande " . $quali_domande . " " . $domande;
    }

    if ($partecipazioni != "" && $quali_partecipazioni != "") {
        $having .= (($having == "") ? " HAVING" : " AND ") . " partecipazioni " . $quali_partecipazioni . " " . $partecipazioni;
    }

    $query .= $having;

    // echo $query;
    return eseguiQuery($query, true);
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
function query_utente($nomeUtente, $nome, $cognome, $email, $like, $quiz_creati = "", $quali_quiz_creati = "", $quiz_giocati = "", $quali_quiz_giocati = ""): string
{
    $query = "SELECT UTENTE.NOME_UTENTE AS nome_utente , UTENTE.NOME AS nome , UTENTE.COGNOME AS cognome , UTENTE.EMAIL AS email , COUNT(DISTINCT QUIZ.CODICE) as numero_quiz , COUNT(DISTINCT PARTECIPAZIONE.QUIZ) as numero_partecipazioni 
    FROM UTENTE LEFT JOIN QUIZ ON UTENTE.NOME_UTENTE = QUIZ.CREATORE , PARTECIPAZIONE
    WHERE UTENTE.NOME_UTENTE = PARTECIPAZIONE.UTENTE";


    $query .= ($nomeUtente == "") ? "" : ($like ? " AND UTENTE.NOME_UTENTE LIKE '%$nomeUtente%'" : " AND UTENTE.NOME_UTENTE = '$nomeUtente'");

    $query .= ($nome == "") ? "" : ($like ? " AND UTENTE.NOME LIKE '%$nome%'" : "AND UTENTE.NOME = '$nome'");

    $query .= ($cognome == "") ? "" : ($like ? " AND UTENTE.COGNOME LIKE '%$cognome%'" : " AND UTENTE.COGNOME = '$cognome'");

    $query .= ($email == "") ? "" : ($like ? " AND UTENTE.EMAIL LIKE '%$email%'" : " AND UTENTE.EMAIL = '$email'");

    $query .= " GROUP BY UTENTE.NOME_UTENTE ";


    $having = "";

    if ($quiz_creati != "" && $quali_quiz_creati != "") {
        $having .= " HAVING numero_quiz " . $quali_quiz_creati . " " . $quiz_creati;
    }

    if ($quiz_giocati != "" && $quali_quiz_giocati != "") {
        $having .= (($having == "") ? " HAVING " : " AND ") . "numero_partecipazioni " . $quali_quiz_giocati . " " . $quiz_giocati;
    }

    $query .= $having;

    // echo $query;

    return eseguiQuery($query, true);
}

/**
 * Funzione che crea la query per le ricerce sugli utenti
 *  
 * @param bool $like
 * @param string $codice
 * @param string $utente
 * @param string $titolo_quiz
 * @param string $data
 */
function query_partecipazione($codice, $utente, $titolo_quiz, $data, $like, $quale_data, $codice_quiz = "", $risposte = "", $quali_risposte = ""): string
{
    $query = "SELECT PARTECIPAZIONE.CODICE AS codice , PARTECIPAZIONE.UTENTE AS nome_utente , QUIZ.TITOLO AS titolo_quiz, QUIZ.CODICE AS codice_quiz, PARTECIPAZIONE.DATA AS data, COUNT(RISPOSTA_UTENTE_QUIZ.RISPOSTA) AS risposte_utente
    FROM (PARTECIPAZIONE JOIN RISPOSTA_UTENTE_QUIZ ON PARTECIPAZIONE.CODICE = RISPOSTA_UTENTE_QUIZ.PARTECIPAZIONE) JOIN QUIZ ON PARTECIPAZIONE.QUIZ = QUIZ.CODICE
    WHERE 1 = 1 ";

    $titolo_quiz = str_replace("'", "''", $titolo_quiz);

    $query .= ($codice == "") ? "" : ("AND PARTECIPAZIONE.CODICE = '$codice'");

    $query .= ($utente == "") ? "" : ("AND PARTECIPAZIONE.UTENTE " . ($like ? " LIKE '%$utente%'" : "= '$utente'"));

    $query .= ($titolo_quiz == "") ? "" : ("AND QUIZ.TITOLO LIKE '%$titolo_quiz%'");

    $query .= ($codice_quiz == "") ? "" : ("AND QUIZ.CODICE = '$codice_quiz'");

    $query .= ($data == "" || $quale_data == "") ? "" : ("AND PARTECIPAZIONE.DATA " . query_data($quale_data, $data));

    $query .= " GROUP BY PARTECIPAZIONE.CODICE ";

    $having = "";

    if ($risposte != "" && $quali_risposte != "") {
        $having .= " HAVING risposte_utente " . $quali_risposte . " " . $risposte;
    }

    $query .= $having;

    $query .= " ORDER BY PARTECIPAZIONE.UTENTE ";

    // echo $query;

    return eseguiQuery($query, true);
}

/**
 * Funzione che crea la query per le ricerce sulle domande
 * 
 * @param string $codice
 */
function query_domande_quiz($codice): string
{
    $query =
        "SELECT NUMERO as numero ,  TESTO as testo
        FROM DOMANDA
        WHERE QUIZ = $codice
        ORDER BY NUMERO ASC";

    return eseguiQuery($query, true);
}
/**
 * Funzione che crea la query per le ricerce sulle domande
 * 
 * @param string $id_quiz il codice del quiz
 * @param string $n_domanda il numero di domanda
 */
function query_risposte_quiz($id_quiz, $n_domanda): string
{
    $query =
        "SELECT NUMERO AS numero ,TESTO AS testo, TIPO AS tipo , PUNTEGGIO AS punteggio
        FROM RISPOSTA
        WHERE QUIZ = $id_quiz AND DOMANDA = $n_domanda
        ORDER BY NUMERO ASC";

    return eseguiQuery($query, true);
}


/**
 * 
 * @param int $indice valore compreso tra 1 e 3
 * @param string $data la data
 */
function query_data($indice, $data): string
{
    $sql = "";
    switch ($indice) {
        case 1:
            $sql .= "<";
            break;
        case 2:
            $sql .= "=";
            break;
        case 3:
            $sql .= ">";
            break;
    }
    $return = $sql . "'" . $data . "'";
    // echo $return +"\n";
    return $return;
}

// Aggiunta QUIZ

/**
 *  Questa funzione prevede l'aggiunta di un quiz 
 * 
 * @param string $autore
 * @param string $titolo
 * @param string $data_inizio
 * @param string $data_fine
 */
function aggiungi_quiz($autore, $titolo, $data_inizio, $data_fine)
{
    $titolo = str_replace("'", "''", $titolo);
    $query = "INSERT INTO QUIZ(CREATORE, TITOLO, DATA_INIZIO, DATA_FINE) VALUES ('$autore','$titolo','$data_inizio','$data_fine')";

    try {
        eseguiQuery($query, false);
    } catch (\Throwable $th) {
        return $th->getMessage();
    }
    return "ok";
}

function elimina_quiz($id_quiz)
{
    $query = "DELETE FROM QUIZ WHERE QUIZ.CODICE = $id_quiz";
    try {
        eseguiQuery($query, false);
    } catch (\Throwable $th) {
        return $th->getMessage();
    }
    return "ok";
}

/**
 * Le date vengono verificate prima
 * 
 * @param string $codice
 * @param string $nome_utente
 * @param string $titolo
 * @param string $data_inizio
 * @param string $data_fine
 */
function update_quiz($codice, $nome_utente, $titolo, $data_inizio, $data_fine): string
{
    // Verifichiamo se l'utente esiste
    $query_utente = "SELECT COUNT(*) AS utenti FROM UTENTE WHERE NOME_UTENTE = '$nome_utente' GROUP BY(NOME_UTENTE)";
    $risultati = eseguiQuery($query_utente, true);
    // Verificare se esiste l'utente
    $risultati = (array)json_decode($risultati);
    $risultati = (array)$risultati[0];
    if ($risultati["utenti"] == 0) {
        return "L'utente non esiste: $risultati[utenti]";
    }

    $titolo = str_replace("'", "''", $titolo);

    // Eliminiamo il vecchio
    $query = "UPDATE QUIZ
    SET CREATORE ='$nome_utente', TITOLO ='$titolo', DATA_INIZIO ='$data_inizio', DATA_FINE ='$data_fine'
    WHERE CODICE = $codice";

    eseguiQuery($query, false);

    return "ok";
}

//connessione DB

function connessioneDB()
{
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

    return $connessione;
}

// Funzione che prende il singolo QUIZ e lo restituisce in formato json
function getQUIZ($codie_QUIZ)
{
    $query = query_quiz($codie_QUIZ, "", "", "", "", FALSE, "", "");
    return eseguiQuery($query, true);
}

/**
 * 
 * @param string $query la query da eseguire
 * @param bool $isSelect se la query è un SELECT
 */
function eseguiQuery($query, $isSelect)
{
    $connessione = connessioneDB();
    $risultati = $connessione->query($query);
    $json = "";
    if ($isSelect) {
        $valori = $risultati->fetchAll(PDO::FETCH_ASSOC);
        $json = json_encode($valori, JSON_PRETTY_PRINT);
    }
    return $json;
}
