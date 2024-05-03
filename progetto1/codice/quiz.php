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
                        <input type="text" id="titolo" name="titolo" placeholder=" "><!--IMPORTANTE NON TOGLIERE IL PLACEHOLDER CON LO SPAZIO -->
                        <div class="underline"></div>
                        <label for="">Titolo</label>
                    </div>
                </div>
                <!-- CREATORE -->
                <div class="form-row">
                    <div class="input-data">
                        <input type="text" id="creatore" name="creatore" placeholder=" "><!--IMPORTANTE NON TOGLIERE IL PLACEHOLDER CON LO SPAZIO -->
                        <div class="underline"></div>
                        <label for="">Autore</label>
                    </div>
                </div>
                <!-- DATA INIZIO -->
                <div class="form-row">
                    <div class="input-data">
                        <input type="text" id="data_inizio" name="data_inizio" placeholder=" "><!--IMPORTANTE NON TOGLIERE IL PLACEHOLDER CON LO SPAZIO -->
                        <div class="underline"></div>
                        <label for="">Data Inizio Quiz</label>
                    </div>
                </div>
                <!-- DATA FINE -->
                <div class="form-row">
                    <div class="input-data">
                        <input type="text" id="data_fine" name="data_fine" placeholder=" "><!--IMPORTANTE NON TOGLIERE IL PLACEHOLDER CON LO SPAZIO -->
                        <div class="underline"></div>
                        <label for="">Data Fine Quiz</label>
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
                        <input type="submit" value="Reset" onclick=""> <!-- Da implementare -->
                    </div>
                </div>
            </form>
        </div>
        <div class="iconaRicerca"><i class="fa-solid fa-magnifying-glass"></i></div>


        <!-- <img class="iconaRicerca" width="50" height="50" src="https://img.icons8.com/ios/50/search--v5.png" /> -->

        <div class="risultati">
            <?php
            $connessione = connessioneDB();
            $codice = "";
            // Prelievo i dati dai campi
            if ($_SERVER["REQUEST_METHOD"] == "POST") {
                $creatore = $_POST["creatore"];
                $titolo = $_POST["titolo"];
                $data_inizio = $_POST["data_inizio"];
                $data_fine = $_POST["data_fine"];
                $like =  $_POST["like"] == "false" ? FALSE : TRUE;
                if (isset($_POST["codice"])) {
                    $codice  = $_POST["codice"];
                }
            }
            $risultato_query = query_quiz($codice, $creatore, $titolo, $data_inizio, $data_fine, $like, 3, 3);
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