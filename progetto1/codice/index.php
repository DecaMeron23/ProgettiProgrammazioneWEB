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
        <div class="norm-text">Siamo <span class="evidenzia big">Benedetta Vitale</span> ed <span class="evidenzia big">Emilio Meroni</span>; il nostro gruppo è: <span class="evidenzia">bevm24web</span>.</div>
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
            In alto a destra è <span class="evidenzia padding-lati">sempre</span> presente l'icona per la navigazione <img src="https://quizmakeandplay.altervista.org/immagini/iconaMenu.png" class="iconaMenu-spiegazione padding-lati"> che al click aprirà un menù da cui si potrà accedere a:
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
        <div class="norm-text">Come per il menù, anche il filtro ricerca sarà a <span class="evidenzia">scomparsa</span>, esso diventerà <span class="evidenzia">visibile</span> al click dell'icona<span class="iconaFiltro-spiegazione padding-lati"><i class="fa-solid fa-magnifying-glass"></i></span><br> Questa scelta è dovuta a due principali motivi:
            <ol class="lista-ordinata">
                <li class="stacca-sopra schiaccia"><span class="evidenzia">Posizione</span> del filtro: da richiesta il filtro deve essere a sinistra, ma all'allungarsi della tabella non era possibile disporlo con una posizione "absolute". Quando si scende nella pagina, il filtro rimane in alto fino a scomparire; qundi era necessario disporlo in modalità "fixed", cosa che graficalmente non ci piaceva.</li>
                <li class="stacca-sopra schiaccia">Le <span class="evidenzia">dimensioni</span>: l'obbiettivo delle interfacce è di mostrare i dati, quindi le tabelle devono essere <span class="evidenzia">ben</span> <span class="evidenzia">visibili</span>. Perciò un filtro "fisso" avrebbe occupato spazio utile per le tabelle.</li>
            </ol>
        </div>
        <div class="stacca-sopra norm-text">
            Le ricerce vengono eseguite in modalità <span class="evidenzia">like</span> (cerca tutti i testi che includono la porzione di testo), mentre per le ricerche sulla <span class="evidenzia">data</span> si hanno 3 opzioni:
        </div>
        <div class="stacca-sopra"><span class="padding-lati icone-ricerca-data margin-contorno"><i class="fa-solid fa-backward"></i></span>Ricerca tutte le data precedenti alla data specificata</div>
        <div class="stacca-sopra"><span class="padding-lati icone-ricerca-data margin-contorno"><i class="fa-solid fa-arrows-to-circle"></i></span>Ricerca tutte le data che sonon uguali alla data specificata</div>
        <div class="stacca-sopra"><span class="padding-lati icone-ricerca-data margin-contorno"><i class="fa-solid fa-forward"></i></span>Ricerca tutte le data successive alla data specificata</div>
        <div class="stacca-sopra norm-text">se non viene specificata nessuna opzione la ricerca per data viene <span class="evidenzia">ignorata</span>.</div>

        <div class="intro small-intro">Utente</div>
        <div class="norm-text">
            In utente abbiamo ritenuto importante, oltre che i dati pricipali, visualizzare il numero dei <span class="evidenzia">quiz creati</span> e il numero dei <span class="evidenzia">quiz giocati</span>; entrambi sono linkati: se selezionati reindirizzano corrispettivamente all'interfaccia dei quiz creati dall'utente e all'iterfaccia delle partecipazioni che ha effettuato l'utente.
        </div>
        <div class="stacca-sopra norm-text">
            Per <span class="evidenzia big">creare un quiz</span>, dato che è una operazione dell'utente, bisogna cliccare sul <span class="evidenzia">nickname</span> e si aprirà una schermata per la creazione del quiz.
        </div>
        <div class="small-intro intro">Quiz</div>
        <div class="norm-text">Per le tabelle dei quiz abbiamo messo come colonne: "titolo", "creatore", "data inizio", "data fine", "N° di domande" e "N° di partecipanti".</div>
        <div class="norm-text stacca-sopra">Per <span class="evidenzia big">visualizzare un quiz</span> bisogna cliccare sul titolo, dal quale si apre una nuova pagina, dove possiamo visualizzare le domande; ed eventualmente, <span class="evidenzia">modificare</span><i class="fa-regular fa-pen-to-square padding-lati" id="bottone-modifica-info"></i>o <span class="evidenzia">eliminare</span><i class="fa-regular fa-trash-can padding-lati" id="bottone-elimina-info"></i>il quiz.
        </div>
        <p class="norm-text stacca-sopra">
            Se si clicca sul nome utente, invece, si verrà reindirizzati nella pagina <span class="evidenzia">utenti</span> con lo specifico utente. <br>
            Infine, al click del numero di partecipanti si verrà portati in una pagina che visualizza tutte le partecipazioni di quel quiz.
        </p>
        <div class="intro small-intro">Partecipazione</div>
        <p class="norm-text">
            Nella pagina partecipazioni visualizzeremo: il nickname del partecipante, il titolo del quiz, la data di partecipazione e le risposte date <br>
            Come specificato in precedenza il <span class="evidenzia">nickname</span> e il <span class="evidenzia">titolo del quiz</span> saranno linkati.
        </p>
        <div class="intro small-intro">Gioca!!</div>
        <p class="notm-text">Per finire è presente la sezione <span class="evidenzia big">gioca!!</span> la quale, se cliccata, selezionerà automaticamente un quiz a caso tra tutti quelli presenti; da la possibilità di ripondere alle domande e verificare le risposte. <br>Al click del pulsante invio la partecipazione verrà <span class="evidenzia">inserita</span> all'interno del <span class="evidenzia">data base</span>.</p>

    </div>



    </div>

    <?php include 'elementiPrincipali/navigazione.html' ?>

    <?php include 'elementiPrincipali/footer.html' ?>

</body>

</html>