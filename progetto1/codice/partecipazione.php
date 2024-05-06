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
            <form id="form_ricerca" action="#" method="get">
                <!-- TITOLO -->
                <div class="form-row">
                    <div class="input-data">
                        <input type="text" id="nome_utente" name="nome_utente" placeholder=" " spellcheck="false" <? echo ((isset($_GET["nome_utente"]) && ($_GET["nome_utente"] != "")) ? "value = $_GET[nome_utente]" : "") ?>><!--IMPORTANTE NON TOGLIERE IL PLACEHOLDER CON LO SPAZIO -->
                        <div class="underline"></div>
                        <label for="">Nome Utente</label>
                    </div>
                </div>
                <!-- CREATORE -->
                <div class="form-row">
                    <div class="input-data">
                        <input type="text" id="titolo_quiz" name="titolo_quiz" placeholder=" " spellcheck="false" <? echo ((isset($_GET["titolo_quiz"]) && ($_GET["titolo_quiz"] != "")) ? "value = $_GET[titolo_quiz]" : "") ?>><!--IMPORTANTE NON TOGLIERE IL PLACEHOLDER CON LO SPAZIO -->
                        <div class="underline"></div>
                        <label for="">Titolo Quiz</label>
                    </div>
                </div>
                <!-- DATA -->
                <div class="form-row">
                    <div class="input-data">
                        <input type="text" id="data" name="data" placeholder=" "  <? echo ((isset($_GET["data"]) && ($_GET["data"] != "")) ? "value = $_GET[data]" : "") ?>><!--IMPORTANTE NON TOGLIERE IL PLACEHOLDER CON LO SPAZIO -->
                        <div class="underline"></div>
                        <label for="">Data partecipazione</label>
                    </div>
                </div>
                <div class="radio-button">
                    <input type="radio" name="quale_data" value="1" class="radio-form" id="quale_data_prima" <? echo $_GET["quale_data"] == 1 ? "checked" : "" ?>>
                    <input type="radio" name="quale_data" value="2" class="radio-form" id="quale_data_uguale" <? echo $_GET["quale_data"] == 2 ? "checked" : "" ?>>
                    <input type="radio" name="quale_data" value="3" class="radio-form" id="quale_data_dopo" <? echo $_GET["quale_data"] == 3 ? "checked" : "" ?>>
                    <div onclick="clickRadio(this)" value="1" name="quale_data" id="quale_data_prima_icona" <? echo $_GET["quale_data"] == 1 ? "class='selected-radio'" : "" ?>><i class="fa-solid fa-backward"></i></div>
                    <div onclick="clickRadio(this)" value="2" name="quale_data" id="quale_data_uguale_icona" <? echo $_GET["quale_data"] == 2 ? "class='selected-radio'" : "" ?>><i class="fa-solid fa-arrows-to-circle"></i></div>
                    <div onclick="clickRadio(this)" value="3" name="quale_data" id="quale_data_dopo_icona" <? echo $_GET["quale_data"] == 3 ? "class='selected-radio'" : "" ?>><i class="fa-solid fa-forward"></i></div>
                </div>
                <!-- QUIZ partecipazioni -->
                <div class="form-row">
                    <div class="input-data">
                        <input type="number" id="risposte" name="risposte" placeholder=" " <? echo ((isset($_GET["risposte"]) && ($_GET["risposte"] != "")) ? "value = $_GET[risposte]" : "") ?>><!--IMPORTANTE NON TOGLIERE IL PLACEHOLDER CON LO SPAZIO -->
                        <div class="underline"></div>
                        <label for="">N° Risposte Date</label>
                    </div>
                </div>
                <div class="radio-button">
                    <input type="radio" name="quali_risposte" value="<" class="radio-form" id="quali_risposte_prima" <? echo $_GET["quali_risposte"] == 1 ? "checked" : "" ?>>
                    <input type="radio" name="quali_risposte" value="=" class="radio-form" id="quali_risposte_uguale" <? echo $_GET["quali_risposte"] == 2 ? "checked" : "" ?>>
                    <input type="radio" name="quali_risposte" value=">" class="radio-form" id="quali_risposte_dopo" <? echo $_GET["quali_risposte"] == 3 ? "checked" : "" ?>>
                    <div onclick="clickRadio(this)" value="<" name="quali_risposte" id="quali_risposte_prima_icona" <? echo $_GET["quali_risposte"] == 1 ? "class='selected-radio'" : "" ?>><i class="fa-solid fa-backward"></i></div>
                    <div onclick="clickRadio(this)" value="=" name="quali_risposte" id="quali_risposte_uguale_icona" <? echo $_GET["quali_risposte"] == 2 ? "class='selected-radio'" : "" ?>><i class="fa-solid fa-arrows-to-circle"></i></div>
                    <div onclick="clickRadio(this)" value=">" name="quali_risposte" id="quali_risposte_dopo_icona" <? echo $_GET["quale_data"] == 3 ? "class='selected-radio'" : "" ?>><i class="fa-solid fa-forward"></i></div>
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
                        <input type="button" value="Reset" onclick="resetRicerca()"> <!-- Da implementare -->
                    </div>
                </div>
            </form>
        </div>
        <div class="iconaRicerca"><i class="fa-solid fa-magnifying-glass"></i></div>

        <div class="dove_siamo">Partecipazioni</div>

        <div class="risultati">
            <?php
            $codice = "";
            // Prelievo i dati dai campi
            if ($_SERVER["REQUEST_METHOD"] == "GET") {
                $codice_quiz = $_GET["id_quiz"];
                $nome_utente = $_GET["nome_utente"];
                $titolo_quiz = $_GET["titolo_quiz"];
                $data = $_GET["data"];
                $like =  $_GET["like"] == "false" ? FALSE : TRUE;
                $quale_data = $_GET["quale_data"];
                $risposte = $_GET["risposte"];
                $quali_risposte = $_GET["quali_risposte"];
            }
            // echo $quale_data;
            $risultato_query = query_partecipazione($id_quiz, $nome_utente, $titolo_quiz, $data, $like, $quale_data, $codice_quiz , $risposte , $quali_risposte);
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