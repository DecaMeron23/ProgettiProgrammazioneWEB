<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">


    <?php include 'elementiPrincipali/impostazioni.html' ?>
    <link rel="stylesheet" href="css/stile-introduzione.css">

    <title>QMAP</title>
</head>

<body>
    <?php include 'elementiPrincipali/header.html' ?>

    <div class="maschera"></div>

    <div class="contenuto">
        <p class="intro">Programmazione WEB 2023/24: Progetto #1</p>
        <div class="norm-text">Il nostro gruppo è <span class="evidenzia">bevm24web</span> siamo <span class="evidenzia big">Vitale Benedetta</span> e <span class="evidenzia big">Emilio Meroni</span></div>
        <div class="norm-text stacca-sopra">Caratteristiche del nostro progetto:</div>
        <div class="caratteristiche norm-text">
            Progetto: <span class="evidenzia">75</span> <br>
            DB di riferimento: <span class="evidenzia">Quiz (TE 03-07-2020)</span> <br>
            Tabella per CRUD: <span class="evidenzia">Quiz </span><br>
            Interfaccia: <span class="evidenzia">Interfaccia 2 </span><br>
            Palette: <span class="evidenzia">Tortora </span>
        </div>
        <br>
        <br>
        <div class="intro small-intro stacca-sopra">
            Come Muoversi nel Nostro Sito
        </div>
        <div class="norm-text testo-icone">
            In alto a destra è <span class="evidenzia padding-lati">sempre</span> presente l'icona per la navigazione <img src="https://quizmakeandplay.altervista.org/immagini/iconaMenu.png" class="iconaMenu-spiegazione padding-lati"> che al click aprirà un menù da cui si potrà andare in:
        </div>
        <div class="evidenzia big stacca-sopra">
            <a href="https://quizmakeandplay.altervista.org/index.php">Home</a>
        </div>
        <div class="evidenzia big stacca-sopra">
            <a href="https://quizmakeandplay.altervista.org/utente.php">Utente</a>
        </div>
        <div class="evidenzia big stacca-sopra">
            <a href="https://quizmakeandplay.altervista.org/quiz.php">Quiz</a>
        </div>
        <div class="evidenzia big stacca-sopra">
            <a href="https://quizmakeandplay.altervista.org/partecipazione.php">Partecipazione</a>
        </div>

        <div class="intro small-intro stacca-sopra">Filtro Ricerca</div>
        <div class="norm-text">Come per il menù anche filtro ricerca sarà a <span class="evidenzia">scomparsa</span>, esso diventerà <span class="evidenzia">visibile</span> al click dell'icona<span class="iconaFiltro-spiegazione padding-lati"><i class="fa-solid fa-magnifying-glass"></i></span><br> Questa scelta è dovuta a due principali motivi:
            <ol class="lista-ordinata">
                <li class="stacca-sopra schiaccia"><span class="evidenzia">Posizione</span> del filtro: da richiesta il filtro deve stare a sinistra, ma all'allungarsi delle tabelle, non era possibile disporre la i filtri con una posizione "absolute", quando si scende nella pagina il filtro rimane su fino a scomparire; qundi era necessario disporre in modalita "fixed", cosa che graficalmente non ci piaceva.</li>
                <li class="stacca-sopra schiaccia">Le <span class="evidenzia">dimensioni</span>: l'obbiettivo di queste pagine è di mostrare i dati, quindi le tabelle devono essere <span class="evidenzia">ben</span> <span class="evidenzia">visibili</span>. Allora un filtro "fisso" avrebbe occupato spazio utile per le tabelle</li>
            </ol>
        </div>
        <div class="stacca-sopra norm-text">
            Le ricerce vengono eseguite in modalità <span class="evidenzia">like</span> (cerca tutti i testi che includono la porzione di testo), mentre per le ricerche sulle <span class="evidenzia">date</span> si hanno 3 opzioni:
        </div>
        <div class="stacca-sopra"><span class="padding-lati icone-ricerca-data margin-contorno"><i class="fa-solid fa-backward"></i></span>Ricerca tutte le date precedenti alla data specificata</div>
        <div class="stacca-sopra"><span class="padding-lati icone-ricerca-data margin-contorno"><i class="fa-solid fa-arrows-to-circle"></i></span>Ricerca tutte le date che sonon uguali alla data specificata</div>
        <div class="stacca-sopra"><span class="padding-lati icone-ricerca-data margin-contorno"><i class="fa-solid fa-forward"></i></span>Ricerca tutte le date successive alla data specificata</div>
        <div class="stacca-sopra norm-text">se non viene specificato nessuno la ricerca per data viene ignorata</div>

        <div class="intro small-intro stacca-sopra">Utente</div>
    </div>



    </div>

    <?php include 'elementiPrincipali/navigazione.html' ?>

    <?php include 'elementiPrincipali/footer.html' ?>

</body>

</html>