/**
 * Questo file serve per effettuare le operazioni chiamate dai click sugli elementi TD
 */

/**
 * 
 * Funzione che reindirizza su partecipazioni
 * 
 * @param {*} el elemento cui si è fatto il click
 */
function reindirizzaPARTECIPAZIONI(el) {

    var numero = el.innerText;

    pagina = getUrlName();

    if (pagina == "utente") {
        var nome_utente = el.getAttribute("nome_utente");
        dati = { "nomeUtente": nome_utente, "vincoliNomeUtente": "NoLike" };
    } else if (pagina == "quiz") {
        var idQuiz = el.getAttribute("id-quiz");
        dati = { "codiceQuiz": idQuiz, "vincoliCodice": "NoLike" };
    }
    if (numero == 0) {
        alert(`${nome_utente} ancora non ha partecipato a quiz`);
    } else {
        var pagina = "/partecipazione"
        $.redirectGET(pagina, dati);
    }
}

/**
 * 
 * Funzione che reindirizza su quiz
 * 
 * @param {*} el elemento cui si è fatto il click
 */
function reindirizzaQUIZ(el) {
    
    var pagina = "/quiz"
    // Distinguiamo i casi:
    // Se siamo nella pagina Partecipazioni o No
    if (window.location.pathname == "/partecipazione") {
        var idQuiz = $(el).attr("id-quiz"); 
        dati = {"codice": idQuiz}
    } else {
        var numero = el.innerText;
        var nome_utente = el.getAttribute("nome_utente");
        if (numero == 0) {
            alert(`${nome_utente} ancora non ha creato dei quiz`);
            return
        } else {
            dati = { creatore: nome_utente, "vincoloCreatore": "noLike" };
        }
    }
    $.redirectGET(pagina, dati);
}

/**
 * 
 * Funzione che reindirizza su Utente
 * 
 * @param {*} el elemento cui si è fatto il click
 */
function reindirizzaUTENTE(el) {
    var utente = el.innerText;
    dati = { nomeUtente: utente, "vincoliNomeUtente": "noLike" }
    var pagina = "/utente";
    $.redirectGET(pagina, dati);
}

/**
 * 
 * Funzione che reindirizza su info quiz
 * 
 * @param {*} el elemento cui si è fatto il click
 */
function reindirizzaINFO_QUIZ(el) {
    var idQuiz = $(el).attr("id-quiz");
    var pagina = "/info";

    dati = {"codice" : idQuiz};

    $.redirectPOST(pagina , dati);

}

/**
  * estendo JQUery con la funzione reirectget la quale reindirizza la pagina inviado il metodo get alla pagina obbiettivo
*/
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
/**
* estendo JQUery con la funzione reirectget la quale reindirizza la pagina inviado il metodo get alla pagina obbiettivo
 */
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


/**
 * Funzione che preleva il nome della pagina
 * @returns {String} il nome della pagina
 */
function getUrlName() {
    // Ottieni il percorso completo della pagina
    var path = window.location.pathname;

    // Ottieni il nome del file dalla fine del percorso
    var pageName = path.split("/").pop();

    // alert("Nome della pagina: " + pageName);
    return pageName;
}