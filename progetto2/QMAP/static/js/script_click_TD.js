/**
 * Questo file serve per effettuare le operazioni chiamate dai click sugli elementi TD
 */


// QUIZ

/**
 * Funzione che implementa l'apertura della pagina del singolo quiz con le relative domande
 * 
 * @param {Element} el elemento cui si è effettuato il click
 */
function clickTitoloQUIZ(el) {
    var codice = el.getAttribute("id-quiz");
    $.ajax({
        type: "GET",
        url: 'https://quizmakeandplay.altervista.org/php/funzionalitaPHP_JS.php',
        dataType: 'json',
        data: { functionname: 'getQUIZ', id_quiz: codice },
        success: function (obj, textstatus) {
            reinderizzaINFO_QUIZ(obj[0]);
        }
    });
}

/**
 * Funzione che implementa l'apertura della pagina Utenti sul singolo utente
 * 
 * @param {Element} el elemento cui si è effettuato il click
 */
function clickCreatoreQUIZ(el) {
    var creatore = el.innerHTML;
    dati = { nome_utente: creatore };
    reindirizzaUTENTE(dati);
}

/**
 * Funzione che implementa l'apertura della pagina partecipazioni 
 * 
 * @param {Element} el elemento cui si è effettuato il click
 */
function clickPartecipantiQUIZ(el) {
    var numero = el.innerHTML;
    if (numero == 0) {
        alert("Nessuno ha ancora partecipato a questo quiz");
    } else {
        var codice = el.getAttribute("id-quiz");
        var pagina = "https://quizmakeandplay.altervista.org/partecipazione.php";
        $.redirectGET(pagina, { id_quiz: codice });
    }
}

//PARTECIPAZIONE

/**
 * Funzione che prevede il reindirizzamento sulla pagina utente
 * 
 * @param {Element} el elemento cui si è fatto click
 */
function clickNomeUtentePARTECIPAZIONI(el) {
    var utente = el.innerHTML;
    dati = { nome_utente: utente };
    reindirizzaUTENTE(dati);
}

function clickTitoloQuizPARTECIPAZIONI(el) {
    var codice = el.getAttribute("id-quiz");
    $.ajax({
        type: "GET",
        url: 'https://quizmakeandplay.altervista.org/php/funzionalitaPHP_JS.php',
        dataType: 'json',
        data: { functionname: 'getQUIZ', id_quiz: codice },
        success: function (obj, textstatus) {
            reinderizzaINFO_QUIZ(obj[0]);
        }
    });
}

//UTENTE
/**
 * 
 * @param {Element} el
 */
function openCreaQuiz(el) {
    var nome_utente = el.innerText;
    
}

/**
 * Funzione che reinderizza la pagina sui quiz che ha fatto l'utente
 * 
 * @param {Element} el
 */
function clickNumeroPartecipazioniUTENTE(el) {
    
}


// Altre Funzioni d'uso comune

function reindirizzaPARTECIPAZIONI(el){
    
    var numero = el.innerText;

    pagina = getUrlName();

    if (pagina == "utente"){
        var nome_utente = el.getAttribute("nome_utente");
        dati = { "nomeUtente": nome_utente , "vincoliNomeUtente" : "NoLike"};
    }else if (pagina == "quiz"){
        var idQuiz = el.getAttribute("id-quiz");
        dati = { "codiceQuiz": idQuiz , "vincoliCodice" : "NoLike"};
    }
    if (numero == 0) {
        alert(`${nome_utente} ancora non ha partecipato a quiz`);
    } else {
        var pagina = "/partecipazione"
        $.redirectGET(pagina, dati);
    }
}

function reindirizzaQUIZ(el) {
    var numero = el.innerText;
    var nome_utente = el.getAttribute("nome_utente");
    if (numero == 0) {
        alert(`${nome_utente} ancora non ha creato dei quiz`);
    } else {
        dati = { creatore: nome_utente , "vincoloCreatore" : "noLike"};
        var pagina = "/quiz"
        $.redirectGET(pagina, dati);
    }
}

function reindirizzaUTENTE(el) {
    var utente = el.innerText;
    dati = { nomeUtente: utente  , "vincoliNomeUtente" : "noLike"}
    var pagina = "/utente";
    $.redirectGET(pagina, dati);
}

function reinderizzaINFO_QUIZ(dati) {
    var pagina = "https://quizmakeandplay.altervista.org/info_quiz.php";
    $.redirectPOST(pagina, dati);
}

function reinderizzaGIOCA(dati) {
    var pagina = "https://quizmakeandplay.altervista.org/gioca.php";
    $.redirectPOST(pagina, dati);
}

// estendo JQUery con la funzione reirectget la quale reindirizza la pagina inviado il metodo get alla pagina obbiettivo
$.extend(
    {
        redirectGET: function (location, args) {
            var form = '';
            $.each(args, function (key, value) {
                form += `<input type="hidden" name="${key}" value="${value}">`;
            });
            $(`<form action="${location}"method="get">${form}</form>`).appendTo($(document.body)).submit();
        }
    });

// estendo JQUery con la funzione reirectget la quale reindirizza la pagina inviado il metodo get alla pagina obbiettivo
$.extend(
    {
        redirectPOST: function (location, args) {
            var form = '';
            $.each(args, function (key, value) {
                form += `<input type="hidden" name="${key}" value="${value}">`;
            });
            $(`<form action="${location}"method="post">${form}</form>`).appendTo($(document.body)).submit();
        }
    });



function getUrlName(){
    // Ottieni il percorso completo della pagina
    var path = window.location.pathname;

    // Ottieni il nome del file dalla fine del percorso
    var pageName = path.split("/").pop();

    // alert("Nome della pagina: " + pageName);
    return pageName; 
}