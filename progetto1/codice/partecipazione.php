<!DOCTYPE html>
<html lang="en">

<head>


    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">


    <?php include 'elementiPrincipali/impostazioni.html' ?>

    <title>QMAP</title>
</head>

<body>
    <?php include_once 'elementiPrincipali/header.html' ?>
    <div class="maschera"></div>


    <?php include_once "php/funzioniDB.php" ?>
    <div class="contenuto">
        <div class="filtroRicerca">
            <form action="#" method="post">
                <!-- TITOLO -->
                <div class="form-row">
                    <div class="input-data">
                        <input type="text" id="nome_untente" name="nome_untente" placeholder=" " <? echo ((isset($_POST["nome_utente"]) && ($_POST["nome_utente"] != "")) ? "value = $_POST[nome_utente]" : "") ?>><!--IMPORTANTE NON TOGLIERE IL PLACEHOLDER CON LO SPAZIO -->
                        <div class="underline"></div>
                        <label for="">Nome Utente</label>
                    </div>
                </div>
                <!-- CREATORE -->
                <div class="form-row">
                    <div class="input-data">
                        <input type="text" id="titolo_quiz" name="titolo_quiz" placeholder=" " <? echo ((isset($_POST["titolo_quiz"]) && ($_POST["titolo_quiz"] != "")) ? "value = $_POST[titolo_quiz]" : "") ?>><!--IMPORTANTE NON TOGLIERE IL PLACEHOLDER CON LO SPAZIO -->
                        <div class="underline"></div>
                        <label for="">Titolo Quiz</label>
                    </div>
                </div>
                <!-- DATA -->
                <div class="form-row">
                    <div class="input-data">
                        <input type="text" id="data" name="data" placeholder=" " <? echo ((isset($_POST["data"]) && ($_POST["data"] != "")) ? "value = $_POST[data]" : "") ?>><!--IMPORTANTE NON TOGLIERE IL PLACEHOLDER CON LO SPAZIO -->
                        <div class="underline"></div>
                        <label for="">Data partecipazione</label>
                    </div>
                </div>
                <div class="form-row submit-btn">
                    <div class="input-data">
                        <div class="inner"></div>
                        <input type="submit" value="submit">
                    </div>
                </div>
                <div class="form-row submit-btn">
                    <div class="input-data">
                        <div class="inner"></div>
                        <input type="submit" value="Reset" onclick="resetRicerca()"> <!-- Da implementare -->
                    </div>
                </div>
            </form>
        </div>
        <div class="iconaRicerca"><i class="fa-solid fa-magnifying-glass"></i></div>

        <div class="risultati">
            <?php
            $codice = "";
            // Prelievo i dati dai campi
            if ($_SERVER["REQUEST_METHOD"] == "POST") {
                $codice_quiz = $_POST["id_quiz"];
                $nome_utente = $_POST["nome_utente"];
                $titolo_quiz = $_POST["titolo_quiz"];
                $data = $_POST["data"];
                $like =  $_POST["like"] == "false" ? FALSE : TRUE;
            }
            
            $risultato_query = query_partecipazione($id_quiz, $nome_utente, $titolo_quiz, $data, $like /* AL MOMENTO TRUE POI DA FARE */, 3 /* Al momento 3*/, $codice_quiz);
            $risultato = (array) json_decode($risultato_query);
            $n_righe = count($risultato);
            if ($n_righe == 0) {
                echo "<h1>Non è stata trovata nessuna partecipazione</h1>";
            } else {
                echo $n_righe == 1 ? ("<h1>Ho trovato solo una partecipazione</h1>") : ("<h1>Sono state trovate $n_righe partecipazioni</h1>");
            ?>
                <table class="tabellaRisultati">
                    <tr>
                        <th>Nickname</th>
                        <th>Quiz</th>
                        <th>Data</th>
                        <th>N° Risposte<br>
                            Date</th>
                    </tr>
                <?php

                $centra_testo = "class = 'TD_centra'";
                // creo un attributo per gli elementi che contengono onclik (per css)
                $onclick = " implementa='onclick'";
                // altre cose per css
                $niente = " implementa='niente'";
                foreach ($risultato as $riga) {
                    $riga = (array)$riga;
                    echo ("<tr>
                        <td $onclick onclick='clickNomeUtentePARTECIPAZIONI(this)'>" . $riga['nome_utente'] . "</td>
                        <td $onclick onclick='clickTitoloQuizPARTECIPAZIONI(this)' id-quiz ='" . $riga["codice_quiz"] . "'>" . $riga['titolo_quiz'] . "</td>
                        <td $niente $centra_testo>" . $riga['data'] . "</td>
                        <td $centra_testo>" . $riga['risposte_utente'] . "</td>
                    </tr>");
                }
            }
                ?>
                </table>
        </div>
    </div>

    <?php include 'elementiPrincipali/navigazione.html' ?>

    <?php include 'elementiPrincipali/footer.html' ?>
</body>

</html>