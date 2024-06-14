src = "https://cdn.jsdelivr.net/npm/flatpickr";


//! Data Picker
var inizzializzazione = function () {

    formato = {
        locale: "it",  // Imposta la lingua su italiano
        dateFormat: "d/m/Y" ,
        weekNumbers: true
    }

    flatpickr("#dataInizio", formato);
    flatpickr("#dataFine", formato);
    flatpickr("#data", formato);
}


//! Reset della ricerca
function resetRicerca() {
    var currentPageUrl = window.location.origin + window.location.pathname;
    window.location.replace(currentPageUrl);
}

function openModificaQUIZ() {
    attivaMaschera(1)
    $("#popup_modifica_quiz").toggleClass("popup_quiz_show");
}

function openCancellaQUIZ() {
    attivaMaschera(1)
    $("#popup_cancella_quiz").toggleClass("popup_quiz_show");
}

function openEliminaQUIZ() {
    attivaMaschera(1)
    $("#popup_elimina_quiz").toggleClass("popup_quiz_show");
}

//! Funzione che intercetta il submit della della pagina info_quiz, al momento che si vuole modificare un quiz
function modificaQuiz(event) {
    event.preventDefault();
}

/**
 * Funzione che intercetta il submit della della pagina info_quiz, al momento che si vuole eliminare un quiz
 * 
 * 
 */

function eliminaQuiz() {
    var id_quiz = $("#form_elimina_quiz").attr("codice");
    $.ajax({
        type: "GET",
        url: 'https://quizmakeandplay.altervista.org/php/funzionalitaPHP_JS.php',
        dataType: 'text',
        data: { functionname: 'deleteQUIZ', id_quiz: id_quiz },
        success: function (obj, textstatus) {
            if (obj == "ok") {
                alert("Quiz Eliminato");
                window.location.replace("https://quizmakeandplay.altervista.org/quiz.php");
            } else {
                alert("Qualche cosa è andato storto:" + obj);
            }
        }
    });

}

//! Aggiungi Quiz
function aggiungiQUIZ(event) {
    event.preventDefault();
    var creatore = $("#creatore").val();
    var titolo = $("#titolo").val();
    var dataInizio_string = $("#data_inizio").val();
    var dataFine_string = $("#data_fine").val();

    dataInizio = new Date(dataInizio_string);
    dataFine = new Date(dataFine_string);

    if (dataFine <= dataInizio) {
        alert("Attenzione inserire una data di fine maggiore di data inizo")
    } else {
        $.ajax({
            type: "GET",
            url: 'https://quizmakeandplay.altervista.org/php/funzionalitaPHP_JS.php',
            dataType: 'text',
            data: { functionname: 'addQUIZ', nome_utente: creatore, titolo: titolo, data_inizio: dataInizio_string, data_fine: dataFine_string },
            success: function (obj, textstatus) {
                if (obj == "ok") {
                    alert("Quiz Inserito correttamente");
                    openModificaQUIZ();
                } else {
                    alert("Qualche cosa è andato storto:" + obj);
                }
                location.reload()
            }
        });
    }
}


/**
 * 
 * @param {Element} event 
 */
function updateQUIZ(elemento) {
    var id_quiz = elemento.getAttribute("id-quiz");
    var creatore = $("#creatore").val();
    var titolo = $("#titolo").val();
    var dataInizio_string = $("#data_inizio").val();
    var dataFine_string = $("#data_fine").val();

    dataInizio = new Date(dataInizio_string);
    dataFine = new Date(dataFine_string);

    if(dataInizio_string == "" || dataFine_string == "" || titolo == "" || creatore == ""){
        alert("Completare tutti i campi!")
    } else if (dataFine <= dataInizio) {
        alert("Attenzione inserire una data di fine maggiore di data inizo!")
    } else {
        $.ajax({
            type: "GET",
            url: 'https://quizmakeandplay.altervista.org/php/funzionalitaPHP_JS.php',
            dataType: 'text',
            data: { functionname: 'updateQUIZ', id_quiz: id_quiz, nome_utente: creatore, titolo: titolo, data_inizio: dataInizio_string, data_fine: dataFine_string },
            success: function (obj, textstatus) {
                if (obj == "ok") {
                    alert("Quiz Modificato correttamente");
                    clickTitoloQUIZ(elemento)
                } else {
                    alert("Qualche cosa è andato storto:" + obj);
                }
            }
        });
    }
}


//! funzione che gestisce i pulsanti dei filtri
/**
 * 
 * @param {Element} elemento 
 */
function clickRadio(elemento) {
    var name = $(elemento).attr("name");
    // ? verifichiamo quale elemento ha invocato la chiamata della funzione
    switch ($(elemento).attr("value")) {
        case '1':
            radioBTN = "#" + name + "_prima";
            break;
        case '2':
            radioBTN = "#" + name + "_uguale";
            break;
        case '3':
            radioBTN = "#" + name + "_dopo";
            break;

    }
    // ? verifichiamo se è già checked
    var isCheck = !$(radioBTN).prop('checked');

    // ? eseguiamo il check oppure no
    $(radioBTN).prop('checked', isCheck);

    $(elemento).toggleClass("selected-radio");
    var idElemento = "#" + $(elemento).attr("id")
    pulsanti = ["#" + name + "_prima_icona", "#" + name + "_uguale_icona", "#" + name + "_dopo_icona"];
    for (let i = 0; i < pulsanti.length; i++) {
        // alert(pulsanti[i] +"  " + idElemento);
        if (pulsanti[i] != idElemento) {
            if ($(pulsanti[i]).hasClass("selected-radio")) {
                $(pulsanti[i]).toggleClass("selected-radio");
            }
        }
    }
}

/**
 * Funzione che strae un quiz a caso e ci fa giocare
 */
function gioca_quiz() {
    // * Richiesta di tutti i quiz
    $.getJSON("https://quizmakeandplay.altervista.org/php/funzionalitaPHP_JS.php", { functionname: 'getQUIZ'},
        function (data, textStatus, jqXHR) {
            //* seleziono un quiz a caso
            codice = data[Math.floor(Math.random()*data.length)];
            codice = codice["codice"];
            //*per quel quiz apro la pagina gioca
            $.ajax({
                type: "GET",
                url: 'https://quizmakeandplay.altervista.org/php/funzionalitaPHP_JS.php',
                dataType: 'json',
                data: { functionname: 'getQUIZ', id_quiz: codice },
                success: function (obj, textstatus) {
                    reinderizzaGIOCA(obj[0]);
                }
            });
        }
    );



}


// ! Funzione che al click della form di ricerca esegue la chiamata get con altri valori aggiuntivi
$(document).ready(function() {
    $('#form_ricerca').on('submit', function(event) {
        event.preventDefault(); // Evita che la pagina venga ricaricata
        
        var formValues = {};
        $('#form_ricerca').find(':input').each(function() {
            var input = $(this);
            if(!(input.val() == "" || !input.attr("name"))){
                formValues[input.attr('name')] = input.val();
            }
        });

        //? cerchiamo le impostazioni del filtro di ricerca (maggiore uguale )
        $('.radio-button').each(function() {
            var selectedDiv = $(this).find('.selected-radio');
            if(selectedDiv.attr("name")){
                formValues["radio_"+selectedDiv.attr("name")] = selectedDiv.attr("value");
            }
        });
        
        // alert(JSON.stringify(formValues)); // Mostra i valori del form in un alert


        var baseUrl = window.location.origin + window.location.pathname;
        var queryString = $.param(formValues);
        var targetUrl = baseUrl + '?' + queryString;

        // Reindirizza alla nuova pagina con i parametri GET
        window.location.href = targetUrl;
    });
});

$(inizzializzazione);