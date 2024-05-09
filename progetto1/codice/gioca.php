<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">


    <?php include 'elementiPrincipali/impostazioni.html' ?>
    <link rel="stylesheet" href="css/stile_info_quiz.css">
    <link rel="stylesheet" href="css/popup.css">
    <script src="javaScript/js_gioco.js"></script>

    <title>Gioca QUIZ</title>
</head>

<body>

    <?php include_once 'elementiPrincipali/header.html' ?>
    <div class="maschera"></div>

    <?php include_once "php/funzioniDB.php" ?>

    <div class="info_QUIZ">
        <div class="testata_info_QUIZ">
            <div id="autore_date">
                <div class="descrizione_quiz">
                    <div><i class="fa-regular fa-user"></i></div>
                    <div><? echo ($_GET["creatore"] != "") ? "$_GET[creatore]" : "NO UTENTE" ?></div>
                </div>
                <div class="descrizione_quiz">
                    <div><i class="fa-regular fa-calendar-check"></i></div>
                    <div class="descrizione_quiz_data"><? echo ($_GET["data_inizio"] != "") ? "$_GET[data_inizio]" : "NO DATA INIZIO" ?></div>
                </div>
                <div class="descrizione_quiz">
                    <div><i class="fa-regular fa-calendar-xmark"></i></div>
                    <div class="descrizione_quiz_data"><? echo ($_GET["data_fine"] != "") ? "$_GET[data_fine]" : "NO DATA" ?></div>
                </div>
            </div>
            <div id="info_quiz_titolo_quiz">
                <div><? echo ($_GET["titolo"] != "") ? "" . $_GET["titolo"] : "NO TITOLO" ?></div>
            </div>
            <div></div>
        </div>
        <div class="contenuto_info_QUIZ">
            <?
            $id_quiz = $_GET["codice"];
            $domande_quiz_string = query_domande_quiz($id_quiz);
            $domande_quiz = (array)(json_decode($domande_quiz_string));
            $n_righe = count($domande_quiz);
            if ($n_righe == 0) {
                echo "<div class ='tutte_domande'>";
                echo "<div class='domanda_risposte'><div class='domanda_punteggio'><div class='domanda'>Questo quiz attualmente non ha nessuna domanda</div>";
            } else {
                echo "<div class = 'tutte_domande'>";
                $pallino_risposta = '<i class="fa-regular fa-circle" onclick="seleziona_risposta(this)"></i>';
                $i =0;
                shuffle($domande_quiz);
                foreach ($domande_quiz as $riga) {
                    $i++;
                    $riga = (array)$riga;
                    echo "<div class='domanda_risposte' domanda_numero='$riga[numero]'><div class='domanda_punteggio'><div class='domanda'>$i. $riga[testo]</div>";
                    $risposte_quiz_string = query_risposte_quiz($id_quiz, $riga["numero"]);
                    $risposte_quiz = (array)(json_decode($risposte_quiz_string));
                    // Ricerco il punteggio della domanda, per come è definito il data base devo cercare dentro le risposte =(
                    $tutte_risposte = "";
                    $punteggio = 0;

                    //rimescolo l'ordine dell'array
                    shuffle($risposte_quiz);
                    foreach ($risposte_quiz as $risposta) {
                        $risposta = (array)$risposta;
                        if ($risposta["tipo"] == 1) {
                            $punteggio = $risposta["punteggio"];
                        }
                        $tutte_risposte .= "<div class='risposta_quiz' risposta_numero=$risposta[numero]><span class='opzione'>$pallino_risposta</span> $risposta[testo]</div>\n";
                    }

                    echo "<div class='punteggio'>[$punteggio pt.]</div></div>\n";
                    echo $tutte_risposte;
                    echo "</div>";
                }
            }
            ?>

            <div class="pulsanti_gioca">
                <div class="pulsante" onclick="restart_quiz()">Riprova</div>
                <div class="pulsante" onclick="reset_risposte()">Cancella</div>
                <div class="pulsante" onclick="verifica_quiz()">Invia</div>

            </div>
            <?
            echo "</div>"
            ?>
        </div>


    </div>

    <?php include 'elementiPrincipali/navigazione.html' ?>

    <div></div>
    <?php include 'elementiPrincipali/footer.html' ?>

</body>