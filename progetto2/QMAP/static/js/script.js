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
    flatpickr("#modalDataFine", formato);
    flatpickr("#modalDataInizio", formato);
    
}


//! Reset della ricerca
function resetRicerca() {
    var currentPageUrl = window.location.origin + window.location.pathname;
    window.location.replace(currentPageUrl);
}



function eliminaQuiz() {
    var id_quiz = $("body").attr("codice");
    data = {funzione : "eliminaQuiz" , codice : id_quiz}
    $.getJSON("funzionalita_js",data,
        function (data, textStatus, jqXHR) {
            if ("esito" in data){
                alert("Quiz Eliminato")
                window.location.pathname = "/quiz"
            }else{
                alert("Qualche cosa è andato storto...");
            }
        }
    );


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