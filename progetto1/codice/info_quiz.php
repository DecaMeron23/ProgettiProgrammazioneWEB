<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">


    <?php include 'elementiPrincipali/impostazioni.html' ?>
    <link rel="stylesheet" href="css/stile_info_quiz.css">
    <link rel="stylesheet" href="css/popup.css">


    <title>info QUIZ</title>
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
                    <div><? echo ($_POST["creatore"] != "") ? "$_POST[creatore]" : "NO UTENTE" ?></div>
                </div>
                <div class="descrizione_quiz">
                    <div><i class="fa-regular fa-calendar-check"></i></div>
                    <div class="descrizione_quiz_data"><? echo ($_POST["data_inizio"] != "") ? "$_POST[data_inizio]" : "NO DATA INIZIO" ?></div>
                </div>
                <div class="descrizione_quiz">
                    <div><i class="fa-regular fa-calendar-xmark"></i></div>
                    <div class="descrizione_quiz_data"><? echo ($_POST["data_fine"] != "") ? "$_POST[data_fine]" : "NO DATA" ?></div>
                </div>
            </div>
            <div id="info_quiz_titolo_quiz">
                <!-- <div class="descrizione">Titolo:</div> -->
                <div><? echo ($_POST["titolo"] != "") ? "$_POST[titolo]" : "NO TITOLO" ?></div>
            </div>
            <div>
                <div id="bottone_modifica_quiz" onclick="openModificaQUIZ()"><i class="fa-regular fa-pen-to-square"></i>
                </div>
                <div id="bottone_elimina_quiz"><i class="fa-regular fa-trash-can"></i></div>
            </div>
        </div>
        <div class="contenuto_info_QUIZ">
            <?
            $id_quiz = $_POST["codice"];
            $domande_quiz_string = query_domande_quiz($id_quiz);
            $domande_quiz = (array)(json_decode($domande_quiz_string));
            $n_righe = count($domande_quiz);
            if ($n_righe == 0) {
                echo "Nessuna domanda per questo quiz";
            } else {
                echo "<div class = 'tutte_domande'>";
                $risposta_corretta = '<i class="fa-solid fa-circle-check"></i>';
                $risposta_sbagliata = '<i class="fa-regular fa-circle"></i>';
                foreach ($domande_quiz as $riga) {
                    $riga = (array)$riga;
                    echo "<div class='domanda_risposte'><div class='domanda_punteggio'><div class='domanda'>$riga[numero]. $riga[testo]</div>";
                    $risposte_quiz_string = query_risposte_quiz($id_quiz, $riga["numero"]);
                    $risposte_quiz = (array)(json_decode($risposte_quiz_string));
                    // Ricerco il punteggio della domanda, per come è definito il data base devo cercare dentro le risposte =(
                    $tutte_risposte = "";
                    $punteggio = 0;

                    //rimescolo l'ordine dell'array
                    shuffle($risposte_quiz);
                    foreach ($risposte_quiz as $risposta) {
                        $risposta = (array)$risposta;
                        $risposta_check = $risposta_sbagliata;
                        if ($risposta["tipo"] == 1) {
                            $punteggio = $risposta["punteggio"];
                            $risposta_check = $risposta_corretta;
                        }
                        // echo "<script>alert($risposta_check)<script>";
                        $tutte_risposte .= "<div class='risposta_quiz'>$risposta_check $risposta[testo]</div>\n";
                    }

                    echo "<div class='punteggio'>[$punteggio pt.]</div></div>\n";
                    echo $tutte_risposte;
                    echo "</div>";
                }
            }
            echo "</div>"
            ?>
        </div>
    </div>

    <div class="popup_quiz">
        <form action="#" method="post">
            <!-- TITOLO -->
            <div class="form-row">
                <div class="input-data">
                    <input type="text" id="creatore" name="creatore" placeholder=" " spellcheck="false" <? echo "value = '$_POST[creatore]'" ?> require><!--IMPORTANTE NON TOGLIERE IL PLACEHOLDER CON LO SPAZIO -->
                    <div class="underline"></div>
                    <label for="">Autore</label>
                </div>
            </div>
            <!-- CREATORE -->
            <div class="form-row">
                <div class="input-data">
                    <input type="text" id="titolo" name="titolo" placeholder=" " spellcheck="false" <? echo "value = '$_POST[titolo]'" ?> require><!--IMPORTANTE NON TOGLIERE IL PLACEHOLDER CON LO SPAZIO -->
                    <div class="underline"></div>
                    <label for="">Titolo Quiz</label>
                </div>
            </div>
            <!-- DATA -->
            <div class="form-row">
                <div class="input-data">
                    <input type="text" id="data_inizio" name="data_inizio" placeholder=" " spellcheck="false" <? echo "value = '$_POST[data_inizio]'" ?> require><!--IMPORTANTE NON TOGLIERE IL PLACEHOLDER CON LO SPAZIO -->
                    <div class="underline"></div>
                    <label for="">Data partecipazione</label>
                </div>
            </div>
            <div class="form-row">
                <div class="input-data">
                    <input type="text" id="data_fine" name="data_fine" placeholder=" " spellcheck="false" <? echo "value = '$_POST[data_fine]'" ?> require><!--IMPORTANTE NON TOGLIERE IL PLACEHOLDER CON LO SPAZIO -->
                    <div class="underline"></div>
                    <label for="">Data partecipazione</label>
                </div>
            </div>
            <div class="form-row submit-btn">
                <div class="input-data">
                    <div class="inner"></div>
                    <input type="button" value="Cancella" onclick="openModificaQUIZ()">
                </div>
                <div class="input-data">
                    <div class="inner"></div>
                    <input type="submit" value="Salva">
                </div>
            </div>
        </form>
    </div>


    <?php include 'elementiPrincipali/navigazione.html' ?>

    <div></div>
    <?php include 'elementiPrincipali/footer.html' ?>

</body>