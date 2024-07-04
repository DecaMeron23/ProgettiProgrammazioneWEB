/**
 * Questo file prevede tutte le funzionalità richeste per giocare ai quiz 
*/

// definizioni costanti: classi
const pallino_check = "fa-solid fa-circle-check";
const pallino_vuoto = "fa-regular fa-circle";
const pallino_errato = "fa-solid fa-circle-xmark";

// preleviamo l'host
const host = `${window.location.host}`;


var utente = "utenteMain";
var codice_partecipazione = 0;
get_codice_partecipazione();

/**
 * 
 * Funzione che preleva l'id del quiz
 * 
 * @returns l'id del quiz
 */
function getIdQuiz() {
    id_quiz = $("body").attr("idQuiz");
    return id_quiz;
}

/**
 * Funzione chiamata al click di un qualsiasi pallino per la selezione della risposta
 * 
 * @param {Element} elemento la \<i\> che indica il pallino
 */
function seleziona_risposta(elemento) {
    if (is_selezionato(elemento)) {
        de_seleziona(elemento);
    } else { //se non è selezionato
        rimuovi_selezioni(elemento);
        seleziona(elemento);
    }
}

/**
 * funzione che rimuove tutte le selezioni per la domanda a cui si è cliccato il pallino
 * 
 * @param {Element} elemento la \<i\> che indica il pallino
 */
function rimuovi_selezioni(elemento) {
    var div = $(elemento).parents(".domanda_risposte");
    var ripsoste = estrai_risposte(div);
    for (var i = 0; i < ripsoste.length; i++) {
        // Selezioniamo tutti i pallini di risposta
        pallino = $(ripsoste[i]).children(".col").children("#opzione").children();
        if (is_selezionato(pallino)) {
            de_seleziona(pallino);
        }
    }
}

/**
 * Funzione che estrae tutte le risposte possibili di una domanda
 * 
 * @param {Element} domanda 
 * @returns {Array} un array di elementi parenti di domanda che anno come classe "risposta_quiz" 
 */
function estrai_risposte(domanda) {
    return $(domanda).children("#risposta_quiz");
}

/**
 * Funzione che verifica se l'elemento passato come parametro è selezionato
 * 
 * @param {Element} elemento 
 * @returns true, se l'elemeto ha la classe pallino_check (quindi se è selezionato)
 */
function is_selezionato(elemento) {
    return $(elemento).hasClass(pallino_check);
}

/**
 * Funzione che cambia la classe dell'elemento il pallino_check, quindi pallino selezionato
 * 
 * @param {Element} elemento la \<i\> che indica il pallino
 */
function seleziona(elemento) {
    $(elemento).removeClass();
    $(elemento).addClass(pallino_check);
}

/**
 * Funzione che cambia la classe dell'elemento il pallino_vuoto, quindi pallino non selezionato
 * 
 * @param {Element} elemento la \<i\> che indica il pallino
 */
function de_seleziona(elemento) {
    $(elemento).removeClass();
    $(elemento).addClass(pallino_vuoto);
}

/**
 * Funzione che cambia la classe dell'elemento il pallino_errato, quindi risposta sbagliata
 * 
 * @param {Element} elemento la \<i\> che indica il pallino
 */
function risposta_sbagliata(elemento) {
    $(elemento).removeClass();
    $(elemento).addClass(pallino_errato);
}


/**
 * funzione che verifica le risposte date al gioco
 */
function verifica_quiz() {

    pulsante_invia_attiva(false)
    // prendiamo tutte le domande
    var domande = $(".domanda_risposte");

    var dati = {
        funzione: "getRisposteCorrette",
        codiceQuiz: getIdQuiz(),
    };

    // Costruisci l'URL con i parametri della query string
    var queryString = $.param(dati);
    var url = `/funzionalita_js?${queryString}`;

    // * Esecuzione chiamata ajax
    $.getJSON(url,
        function (data, textStatus, jqXHR) {
            var corretta = data["risposteCorrette"];


            inserisci_partecipazione(getIdQuiz());

            // scorriamo tutte le domande
            for (let i = 0; i < domande.length; i++) {
                const element = domande[i];

                // * Estraiamo il numero di domanda, le domande partono a contare da 1
                var domanda = parseInt($(element).attr("domanda_numero"));

                // * Verifichiamo se la risposta data è gista
                verifica_risposte(element, parseInt(corretta[domanda - 1]["numeroDomanda"]), parseInt(domanda));
            }
        }
    ).fail(function (jqXHR, textStatus, errorThrown) {
        // Qui puoi mostrare un messaggio di errore all'utente o fare altro
        console.log(jqXHR.responseText);
    });;


}

/**
 * Funzione che verifca le risposte per una determinata domanda, in particolare colora di verde la risposta giusta, e se si ha sbagliato si colora di rosso la risposta data
 * 
 * @param {Element} domande
 * @param {strign} corretta 
 * @param {strign} numero_domanda 
 */
function verifica_risposte(domande, corretta, numero_domanda) {
    var risposte = estrai_risposte(domande);
    for (var i = 0; i < risposte.length; i++) {
        var col = $(risposte[i]).children(".col");
        var opzione = col.children("#opzione");
        var pallino = opzione.children();

        var numero_risposta = $(risposte[i]).attr("risposta_numero");

        remove_on_click(pallino);

        if (is_selezionato(pallino)) {
            inserisci_risposta_utente(codice_partecipazione, id_quiz, numero_domanda, numero_risposta);
        }
        if (numero_risposta == corretta) {
            colora_risposta(risposte[i], pallino, true);
        } else if (is_selezionato(pallino)) { // * se la risposta attuale non è quella corretta ma è selezionata vuol dire che è sbagliata 
            colora_risposta(risposte[i], pallino, false);
        }
    }
}


/**
 * Funzione che colora elemento di rosso o verde(se è giusta) 
 * 
 * @param {Element} elemento la \<div\> della risposta
 * @param {Element} pallino  la \<i\> della risposta
 * @param {Boolean} is_giusta se true indica che la risposta che si vuole colorare è quella giusta
 */
function colora_risposta(elemento, pallino, is_giusta) {
    if (is_giusta) {
        $(elemento).css({ color: "green" });
    } else {
        risposta_sbagliata(pallino);
        $(elemento).css({ color: "red" });
    }
}

/**
 * Funzione che rimuove l'attributo "onclick" all'elemento passato
 * 
 * @param {Element} element 
 */
function remove_on_click(element) {
    $(element).removeAttr("onclick");
}

/**
 * Funzione che inserisce la pertecipazione dell'utente eseguendo una chiamata sincorna
 * 
 * @param {string} id_quiz
 * 
 */
function inserisci_partecipazione(id_quiz) {
    // prendiamo la data di oggi
    let data = new Date();
    data = data.toISOString().split('T')[0];

    let dati = {
        funzione: "aggiungiPartecipazione",
        nomeUtente: utente,
        partecipazione: codice_partecipazione,
        codiceQuiz: id_quiz,
        dataPartecipazione: data
    };

    $.ajax({
        url: "funzionalita_js",
        data: dati,
        dataType: "json",
        async: false, // Chiamata sincrona
        success: function (data, textStatus, jqXHR) {
            if (!("esito" in data)) {
                console.error(data["errore"] + " codice: " + data["codiceErrore"]);
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.error("Errore durante la chiamata sincrona:", textStatus, errorThrown);
        }
    });
}

/**
 * Funzione che setta il codice partecipazione della partecipazione
 */
function get_codice_partecipazione() {
    data = { funzione: "get_max_partecipazione" };
    $.getJSON("funzionalita_js", data,
        function (data, textStatus, jqXHR) {
            // * Aggiorniamo il codice partecipazione
            codice_partecipazione = parseInt(data["codice_partecipazione"]) + 1;
        });
}

/**
 * Funzione che inserisce la singola risposta
 * 
 * @param {string} domanda
 * @param {string} id_quiz
 * @param {strign} partecipazione
 * @param {string} risposta    
 */
function inserisci_risposta_utente(partecipazione, id_quiz, domanda, risposta) {
    data = { funzione: "inserisci_risposta_utente", partecipazione: partecipazione, id_quiz: id_quiz, domanda: domanda, risposta: risposta };
    $.getJSON("funzionalita_js", data,
        function (data, textStatus, jqXHR) {
            if (!("esito" in data)) {
                console.error(data["errore"] + " Codice: " + data["codiceErrore"])
            }
        });
}

/**
 * Funzione che attiva o disattiva il pulsante invia
 * 
 * @param {Boolean} bool 
 */
function pulsante_invia_attiva(bool) {
    var element = $("#pulsane_invia");
    if (bool && !$(element).get(0).hasAttribute("onclick")) {
        $(element).addClass("pulsante_hover");
        $(element).removeClass("pulsante_diattivato")
        $(element).attr("onclick", "verifica_quiz()");
    } else {
        $(element).addClass("pulsante_diattivato")
        $(element).removeClass("pulsante_hover");
        remove_on_click(element)
    }
}