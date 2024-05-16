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
function clickNomeUtenteUTENTE(el) {
    var nome_utente = el.innerHTML;
    $("#creatore").attr("value", nome_utente);
    attivaMaschera(1)

    $(".popup_quiz").toggleClass("popup_quiz_show");
}

/**
 * Funzione che reinderizza la pagina sui quiz che ha fatto l'utente
 * 
 * @param {Element} el 
 */
function clickNumeroQuizUTENTE(el) {
    var numero = el.innerHTML;
    var nome_utente = el.getAttribute("nome_utente");
    if (numero == 0) {
        alert(`${nome_utente} ancora non ha creato dei quiz`);
    } else {
        dati = { creatore: nome_utente, like: "false" };
        reindirizzaQUIZ(dati)
    }
}

/**
 * Funzione che reinderizza la pagina sui quiz che ha fatto l'utente
 * 
 * @param {Element} el
 */
function clickNumeroPartecipazioniUTENTE(el) {
    var numero = el.innerHTML;
    var nome_utente = el.getAttribute("nome_utente");
    if (numero == 0) {
        alert(`${nome_utente} ancora non ha partecipato a quiz`);
    } else {
        dati = { nome_utente: nome_utente };
        reindirizzaPARTECIPAZIONI(dati);
    }
}


// Altre Funzioni d'uso comune

function reindirizzaPARTECIPAZIONI(dati) {
    var pagina = "https://quizmakeandplay.altervista.org/partecipazione.php"
    $.redirectGET(pagina, dati);
}

function reindirizzaQUIZ(dati) {
    var pagina = "https://quizmakeandplay.altervista.org/quiz.php"
    $.redirectGET(pagina, dati);
}

function reindirizzaUTENTE(dati) {
    var pagina = "https://quizmakeandplay.altervista.org/utente.php";
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