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
                        <input type="text" id="titolo" name="titolo" placeholder=" " spellcheck="false" value="<? echo $_GET['titolo'] ?>"><!--IMPORTANTE NON TOGLIERE IL PLACEHOLDER CON LO SPAZIO -->
                        <div class="underline"></div>
                        <label for="">Titolo</label>
                    </div>
                </div>
                <!-- CREATORE -->
                <div class="form-row">
                    <div class="input-data">
                        <input type="text" id="creatore" name="creatore" placeholder=" " spellcheck="false" value="<? echo $_GET['creatore'] ?>"><!--IMPORTANTE NON TOGLIERE IL PLACEHOLDER CON LO SPAZIO -->
                        <div class="underline"></div>
                        <label for="">Autore</label>
                    </div>
                </div>
                <!-- DATA INIZIO -->
                <div class="form-row">
                    <div class="input-data">
                        <input type="text" id="data_inizio" name="data_inizio" placeholder=" " spellcheck="false" value="<? echo $_GET['data_inizio'] ?>"><!--IMPORTANTE NON TOGLIERE IL PLACEHOLDER CON LO SPAZIO -->
                        <div class="underline"></div>
                        <label for="">Data Inizio Quiz</label>
                    </div>
                </div>
                <div class="radio-button">
                    <input type="radio" name="quale_data_inizio" value="1" class="radio-form" id="quale_data_inizio_prima" <? echo $_GET["quale_data_inizio"] == 1 ? "checked" : "" ?>>
                    <input type="radio" name="quale_data_inizio" value="2" class="radio-form" id="quale_data_inizio_uguale" <? echo $_GET["quale_data_inizio"] == 2 ? "checked" : "" ?>>
                    <input type="radio" name="quale_data_inizio" value="3" class="radio-form" id="quale_data_dopo_dopo" <? echo $_GET["quale_data_inizio"] == 3 ? "checked" : "" ?>>
                    <div onclick="clickRadio(this)" value="1" name="quale_data_inizio" id="quale_data_inizio_prima_icona" <? echo $_GET["quale_data_inizio"] == 1 ? "class='selected-radio'" : "" ?>><i class="fa-solid fa-backward"></i></div>
                    <div onclick="clickRadio(this)" value="2" name="quale_data_inizio" id="quale_data_inizio_uguale_icona" <? echo $_GET["quale_data_inizio"] == 2 ? "class='selected-radio'" : "" ?>><i class="fa-solid fa-arrows-to-circle"></i></div>
                    <div onclick="clickRadio(this)" value="3" name="quale_data_inizio" id="quale_data_inizio_dopo_icona" <? echo $_GET["quale_data_inizio"] == 3 ? "class='selected-radio'" : "" ?>><i class="fa-solid fa-forward"></i></div>
                </div>
                <!-- DATA FINE -->
                <div class="form-row">
                    <div class="input-data">
                        <input type="text" id="data_fine" name="data_fine" placeholder=" " value="<? echo $_GET['data_fine'] ?>"><!--IMPORTANTE NON TOGLIERE IL PLACEHOLDER CON LO SPAZIO -->
                        <div class="underline"></div>
                        <label for="">Data Fine Quiz</label>
                    </div>
                </div>
                <div class="radio-button">
                    <input type="radio" name="quale_data_fine" value="1" class="radio-form" id="quale_data_fine_prima" <? echo $_GET["quale_data_fine"] == 1 ? "checked" : "" ?>>
                    <input type="radio" name="quale_data_fine" value="2" class="radio-form" id="quale_data_fine_uguale" <? echo $_GET["quale_data_fine"] == 2 ? "checked" : "" ?>>
                    <input type="radio" name="quale_data_fine" value="3" class="radio-form" id="quale_data_fine_dopo" <? echo $_GET["quale_data_fine"] == 3 ? "checked" : "" ?>>
                    <div onclick="clickRadio(this)" value="1" name="quale_data_fine" id="quale_data_fine_prima_icona" <? echo $_GET["quale_data_fine"] == 1 ? "class='selected-radio'" : "" ?>><i class="fa-solid fa-backward"></i></div>
                    <div onclick="clickRadio(this)" value="2" name="quale_data_fine" id="quale_data_fine_uguale_icona"  <? echo $_GET["quale_data_fine"] == 2 ? "class='selected-radio'" : "" ?>><i class="fa-solid fa-arrows-to-circle"></i></div>
                    <div onclick="clickRadio(this)" value="3" name="quale_data_fine" id="quale_data_fine_dopo_icona"  <? echo $_GET["quale_data_fine"] == 3 ? "class='selected-radio'" : "" ?>><i class="fa-solid fa-forward"></i></div>
                </div>
                <!-- QUIZ domande -->
                <div class="form-row">
                    <div class="input-data">
                        <input type="number" id="domande" name="domande" placeholder=" " <? echo ((isset($_GET["domande"]) && ($_GET["domande"] != "")) ? "value = $_GET[domande]" : "") ?>><!--IMPORTANTE NON TOGLIERE IL PLACEHOLDER CON LO SPAZIO -->
                        <div class="underline"></div>
                        <label for="">Domande Quiz</label>
                    </div>
                </div>
                <div class="radio-button">
                    <input type="radio" name="quali_domande" value="<" class="radio-form" id="quali_domande_prima" <? echo $_GET["quali_domande"] == 1 ? "checked" : "" ?>>
                    <input type="radio" name="quali_domande" value="=" class="radio-form" id="quali_domande_uguale" <? echo $_GET["quali_domande"] == 2 ? "checked" : "" ?>>
                    <input type="radio" name="quali_domande" value=">" class="radio-form" id="quali_domande_dopo" <? echo $_GET["quali_domande"] == 3 ? "checked" : "" ?>>
                    <div onclick="clickRadio(this)" value="<" name="quali_domande" id="quali_domande_prima_icona" <? echo $_GET["quali_domande"] == 1 ? "class='selected-radio'" : "" ?>><i class="fa-solid fa-backward"></i></div>
                    <div onclick="clickRadio(this)" value="=" name="quali_domande" id="quali_domande_uguale_icona" <? echo $_GET["quali_domande"] == 2 ? "class='selected-radio'" : "" ?>><i class="fa-solid fa-arrows-to-circle"></i></div>
                    <div onclick="clickRadio(this)" value=">" name="quali_domande" id="quali_domande_dopo_icona" <? echo $_GET["quale_data"] == 3 ? "class='selected-radio'" : "" ?>><i class="fa-solid fa-forward"></i></div>
                </div>
                <!-- QUIZ partecipazioni -->
                 <div class="form-row">
                    <div class="input-data">
                        <input type="number" id="partecipazioni" name="partecipazioni" placeholder=" " <? echo ((isset($_GET["partecipazioni"]) && ($_GET["partecipazioni"] != "")) ? "value = $_GET[partecipazioni]" : "") ?>><!--IMPORTANTE NON TOGLIERE IL PLACEHOLDER CON LO SPAZIO -->
                        <div class="underline"></div>
                        <label for="">N° di partecipanti</label>
                    </div>
                </div>
                <div class="radio-button">
                    <input type="radio" name="quali_partecipazioni" value="<" class="radio-form" id="quali_partecipazioni_prima" <? echo $_GET["quali_partecipazioni"] == 1 ? "checked" : "" ?>>
                    <input type="radio" name="quali_partecipazioni" value="=" class="radio-form" id="quali_partecipazioni_uguale" <? echo $_GET["quali_partecipazioni"] == 2 ? "checked" : "" ?>>
                    <input type="radio" name="quali_partecipazioni" value=">" class="radio-form" id="quali_partecipazioni_dopo" <? echo $_GET["quali_partecipazioni"] == 3 ? "checked" : "" ?>>
                    <div onclick="clickRadio(this)" value="<" name="quali_partecipazioni" id="quali_partecipazioni_prima_icona" <? echo $_GET["quali_partecipazioni"] == 1 ? "class='selected-radio'" : "" ?>><i class="fa-solid fa-backward"></i></div>
                    <div onclick="clickRadio(this)" value="=" name="quali_partecipazioni" id="quali_partecipazioni_uguale_icona" <? echo $_GET["quali_partecipazioni"] == 2 ? "class='selected-radio'" : "" ?>><i class="fa-solid fa-arrows-to-circle"></i></div>
                    <div onclick="clickRadio(this)" value=">" name="quali_partecipazioni" id="quali_partecipazioni_dopo_icona" <? echo $_GET["quale_data"] == 3 ? "class='selected-radio'" : "" ?>><i class="fa-solid fa-forward"></i></div>
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

        <div class="dove_siamo">Quiz</div>
        <div class="risultati">
            <?php
            $codice = "";
            // Prelievo i dati dai campi
            if ($_SERVER["REQUEST_METHOD"] == "GET") {
                $creatore = $_GET["creatore"];
                $titolo = $_GET["titolo"];
                $data_inizio = $_GET["data_inizio"];
                $data_fine = $_GET["data_fine"];
                $like =  $_GET["like"] == "false" ? FALSE : TRUE;
                if (isset($_GET["codice"])) {
                    $codice  = $_GET["codice"];
                }
                $quale_data_inizio = $_GET["quale_data_inizio"];
                $quale_data_fine = $_GET["quale_data_fine"];
                $domande = $_GET["domande"];
                $quali_domande = $_GET["quali_domande"];
                $partecipazioni = $_GET["partecipazioni"];
                $quali_partecipazioni = $_GET["quali_partecipazioni"];
            }
            // echo $quale_data_inizio . "   " . $quale_data_fine . " ";

            $risultato_query = query_quiz($codice, $creatore, $titolo, $data_inizio, $data_fine, $like, $quale_data_inizio, $quale_data_fine , $domande , $quali_domande , $partecipazioni , $quali_partecipazioni);
            $risultato = (array) json_decode($risultato_query);
            $n_righe = count($risultato);
            if ($n_righe == 0) {
                echo "<h1>Non è stato trovato nessun quiz</h1>";
            } else {
                echo $n_righe == 1 ? ("<h1>Ho trovato solo $n_righe quiz</h1>") : ("<h1>Sono stati trovati $n_righe quiz</h1>");

            ?>
                <table class="tabellaRisultati">
                    <tr>
                        <th>Titolo</th>
                        <th>Creatore</th>
                        <th>Data Inizio</th>
                        <th>Data Fine</th>
                        <th>N° di <br>
                            Domande</th>
                        <th>N° di<br>
                            Partecipanti</th>
                    </tr>
                <?php

                $centra_testo = "class = 'TD_centra'";
                // creo un attributo per gli elementi che contengono onclik (per css)
                $onclick = " implementa='onclick'";
                // altre cose per css
                $niente = " implementa='niente'";
                foreach ($risultato as $riga) {
                    $riga = (array)$riga;
                    echo ("<tr $clsse>
                    <td id-quiz = '$riga[codice]' onclick = 'clickTitoloQUIZ(this)' $onclick>" . $riga['titolo'] . "</td>
                    <td onclick = 'clickCreatoreQUIZ(this)' $onclick>" . $riga['creatore'] . "</td>
                    <td $centra_testo $niente>" . $riga['data_inizio'] . "</td>
                    <td $centra_testo $niente>" . $riga['data_fine'] . "</td>
                    <td $centra_testo $niente>" . $riga['domande'] . "</td>
                    <td $centra_testo onclick = 'clickPartecipantiQUIZ(this)' id-quiz = '" . $riga["codice"] . "' $onclick>" . $riga['partecipazioni'] . "</td>
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