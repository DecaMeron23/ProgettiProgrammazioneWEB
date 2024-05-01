<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">


    <?php include '../elementiPrincipali/impostazioni.html' ?>

    <title>QMAP</title>
</head>

<body>
    <?php include '../elementiPrincipali/header.html' ?>
    <div class="maschera"></div>


    <?php include_once "../php/funzioniDB.php" ?>
    <div class="contenuto">
        <div class="filtroRicerca">
            <form action="#" method="post">
                <input type="text" name="creatore" id="creatore" placeholder="Nick Creatore">
                <input type="text" name="titolo" id="titolo" placeholder="Titolo Quiz"><br>
                <label for="data_inizio">Data Inizio:</label>
                <input type="date" name="data_inizio" id="data_inizio"><br>
                <label for="data_fine">Data Fine:</label>
                <input type="date" name="data_fine" id="data_fine" placeholder="">
                <input type="submit" value="Cerca">
            </form>
        </div>
        <img class="iconaRicerca" width="50" height="50" src="https://img.icons8.com/ios/50/search--v5.png" />


        <div class="risultati">
            <?php
            include_once '../php/connessioneDB.php';
            $codice = "";
            // Prelievo i dati dai campi
            if ($_SERVER["REQUEST_METHOD"] == "POST") {
                $creatore = $_POST["creatore"];
                $titolo = $_POST["titolo"];
                $data_inizio = $_POST["data_inizio"];
                $data_fine = $_POST["data_fine"];
                if (isset($_POST["codice"])) {
                    $codice  = $_POST["codice"];
                }
            }

            $sql = query_quiz($codice, $creatore, $titolo, $data_inizio, $data_fine, true, 3, 3);
            $risultato = $connessione->query($sql);
            if ($risultato  == "") {
                echo ("Non è stata trovata nessuna corrispondeza");
            } else {

                $n_righe = $risultato->rowCount();
                echo ("<h1>Sono state trovate $n_righe</h1>");
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

                $pari = "class = 'RigaPari'";
                $dispari = "class = 'RigaDispari'";
                $centra_testo = "class = 'TD_centra'";
                $classe_titolo = "class = TD_titolo";
                $i = 0;
                foreach ($risultato as $riga) {
                    $i++;
                    $classe = "";
                    if ($i % 2 == 0) {
                        $classe = $pari;
                    } else {
                        $classe = $dispari;
                    }
                    echo ("<tr $clsse><td $classe_titolo>" . $riga['titolo'] . "</td><td>" . $riga['creatore'] . "</td><td $centra_testo>" . $riga['data_inizio'] . "</td><td $centra_testo>" . $riga['data_fine'] . "</td><td $centra_testo>" . $riga['domande'] . "</td><td $centra_testo>" . $riga['partecipazioni'] . "</td></tr>");
                }
            }
                ?>
                </table>


        </div>
    </div>

    <?php include '../elementiPrincipali/navigazione.html' ?>

    <?php include '../elementiPrincipali/footer.html' ?>

</body>

</html>