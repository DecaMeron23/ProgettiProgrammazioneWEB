<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">


    <?php include 'elementiPrincipali/impostazioni.html' ?>
    <link rel="stylesheet" href="css/popup.css">

    <title>Utente</title>
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
                        <input type="text" id="nome_utente" name="nome_utente" placeholder=" " spellcheck="false" value="<? echo $_GET['nome_utente'] ?>"><!--IMPORTANTE NON TOGLIERE IL PLACEHOLDER CON LO SPAZIO -->
                        <div class="underline"></div>
                        <label for="">Nome Utente</label>
                    </div>
                </div>
                <!-- CREATORE -->
                <div class="form-row">
                    <div class="input-data">
                        <input type="text" id="nome" name="nome" placeholder=" " spellcheck="false" value="<? echo $_GET['nome'] ?>"><!--IMPORTANTE NON TOGLIERE IL PLACEHOLDER CON LO SPAZIO -->
                        <div class="underline"></div>
                        <label for="">Nome</label>
                    </div>
                </div>
                <div class="form-row">
                    <div class="input-data">
                        <input type="text" id="cognome" name="cognome" placeholder=" " spellcheck="false" value="<? echo $_GET['cognome'] ?>"><!--IMPORTANTE NON TOGLIERE IL PLACEHOLDER CON LO SPAZIO -->
                        <div class="underline"></div>
                        <label for="">Cognome</label>
                    </div>
                </div>
                <div class="form-row">
                    <div class="input-data">
                        <input type="text" id="email" name="email" placeholder=" " spellcheck="false" value="<? echo $_GET['email'] ?>"><!--IMPORTANTE NON TOGLIERE IL PLACEHOLDER CON LO SPAZIO -->
                        <div class="underline"></div>
                        <label for="">Email</label>
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
                        <input type="button" value="Reset" onclick="resetRicerca()"> <!-- Da implementare -->
                    </div>
                </div>
            </form>
        </div>
        <div class="iconaRicerca"><i class="fa-solid fa-magnifying-glass"></i></div>
        <div class="dove_siamo">Utente</div>
        <div class="risultati">
            <?php
            $codice = "";
            // Prelievo i dati dai campi
            if ($_SERVER["REQUEST_METHOD"] == "GET") {
                $nome_utente = $_GET["nome_utente"];
                $nome = $_GET["nome"];
                $cognome = $_GET["cognome"];
                $email = $_GET["email"];
                $like =  $_GET["like"] == "false" ? FALSE : TRUE;
            }
            $risultato_query = query_utente($nome_utente, $nome, $cognome, $email, $like);
            $risultato = (array) json_decode($risultato_query);
            $n_righe = count($risultato);
            if ($n_righe == 0) {
                echo "<h1>Non è stato trovato nessun utente</h1>";
            } else {
                echo $n_righe == 1 ? ("<h1>Ho trovato solo $n_righe utente</h1>") : ("<h1>Sono stati trovati $n_righe utenti</h1>");

            ?>
                <table class="tabellaRisultati">
                    <tr>
                        <th>Nickname</th>
                        <th>Nome</th>
                        <th>Cognome</th>
                        <th>Email</th>
                        <th>N° Quiz<br>
                            Creati</th>
                        <th>N° Quiz<br>
                            Giocati</th>
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
                        <td $onclick onclick = 'clickNomeUtenteUTENTE(this)'>" . $riga['nome_utente'] . "</td>
                        <td $niente>" . $riga['nome'] . "</td>
                        <td $niente>" . $riga['cognome'] . "</td>
                        <td $niente>" . $riga['email'] . "</td>
                        <td $centra_testo onclick='clickNumeroQuizUTENTE(this)' $onclick nome_utente='" . $riga["nome_utente"] . "'>" . $riga['numero_quiz'] . "</td>
                        <td $centra_testo onclick = 'clickNumeroPartecipazioniUTENTE(this)' $onclick nome_utente='" . $riga["nome_utente"] . "'>" . $riga['numero_partecipazioni'] . "</td>
                    </tr>");
                }
            }
                ?>
                </table>
        </div>
    </div>

    <div class="popup_quiz" id="popup_cancella_quiz">
        <form action="#" method="get" onsubmit="aggiungiQUIZ(event)">
            <!-- TITOLO -->
            <div class="form-row">
                <div class="input-data">
                    <input type="text" id="creatore" name="creatore" placeholder=" " spellcheck="false" readonly required><!--IMPORTANTE NON TOGLIERE IL PLACEHOLDER CON LO SPAZIO -->
                    <div class="underline"></div>
                    <label for="">Autore</label>
                </div>
            </div>
            <!-- CREATORE -->
            <div class="form-row">
                <div class="input-data">
                    <input type="text" id="titolo" name="titolo" placeholder=" " spellcheck="false" required><!--IMPORTANTE NON TOGLIERE IL PLACEHOLDER CON LO SPAZIO -->
                    <div class="underline"></div>
                    <label for="">Titolo Quiz</label>
                </div>
            </div>
            <!-- DATA -->
            <div class="form-row">
                <div class="input-data">
                    <input type="text" id="data_inizio" name="data_inizio" placeholder=" " spellcheck="false" required><!--IMPORTANTE NON TOGLIERE IL PLACEHOLDER CON LO SPAZIO -->
                    <div class="underline"></div>
                    <label for="">Data Inizio</label>
                </div>
            </div>
            <div class="form-row">
                <div class="input-data">
                    <input type="text" id="data_fine" name="data_fine" placeholder=" " spellcheck="false" required><!--IMPORTANTE NON TOGLIERE IL PLACEHOLDER CON LO SPAZIO -->
                    <div class="underline"></div>
                    <label for="">Data Fine</label>
                </div>
            </div>
            <div class="form-row submit-btn">
                <div class="input-data">
                    <div class="inner"></div>
                    <input type="button" value="Cancella" onclick="openCancellaQUIZ()">
                </div>
                <div class="input-data">
                    <div class="inner"></div>
                    <input type="submit" value="Salva">
                </div>
            </div>
        </form>
    </div>


    <?php include 'elementiPrincipali/navigazione.html' ?>

    <?php include 'elementiPrincipali/footer.html' ?>
</body>

</html>