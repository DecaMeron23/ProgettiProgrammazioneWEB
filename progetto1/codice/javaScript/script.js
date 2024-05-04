src = "https://cdn.jsdelivr.net/npm/flatpickr";

var inizzializzazione = function () {
    flatpickr("#data_inizio", {});
    flatpickr("#data_fine", {});
    flatpickr("#data", {});
}

/**
 * @param {bool} isMenu
 * 
 */
function attivaMaschera(tipo) {
    $(".maschera").toggleClass("maschera_on");
    $("body").toggleClass("menuOpen");
    switch (tipo) {
        case 0:
            zindex = $(".iconaRicerca").css("z-index");
            if (zindex == 100) {
                $(".iconaRicerca").css("z-index", 70);
            } else if (zindex == 70) {
                $(".iconaRicerca").css("z-index", 100);
            }
            break;
        case 1:
            zindex = $(".navbar").css("z-index");
            if (zindex == 100) {
                $(".navbar").css("z-index", 70);
            } else if (zindex == 70) {
                $(".navbar").css("z-index", 100);
            }
            break;
    }
}

// Funzione viene eseguita quando si apre il menu
var toggleMenu = function () {
    $(".navbar").click(function () {
        $(".nav").toggleClass("wide");
        $(".navbar").toggleClass("navbar_rotate");
        attivaMaschera(0);
    });
};

var toggleFilter = function () {
    $(".iconaRicerca").click(function () {
        $(".filtroRicerca").toggleClass("ricercaShow");
        $(".iconaRicerca").toggleClass("iconaRicercaShow");
        attivaMaschera(1);
        // se l'icona contiene la classe iconaRicecaShow
        if ($(".iconaRicerca").hasClass("iconaRicercaShow")) {
            $(".iconaRicerca").html("<i class='fa-regular fa-circle-xmark'></i>")
        } else {
            $(".iconaRicerca").html("<i class='fa-solid fa-magnifying-glass'>")
        }
    });
}

// Fare funzione reset ricerca
function resetRicerca() {
    // Ricarica la pagina
    location.reload();

    // Rimuove i dati POST dalla history del browser
    history.replaceState({}, document.title, window.location.href.split("?")[0]);
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

// Funzione che intercetta il submit della della pagina info_quiz, al momento che si vuole modificare un quiz
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


$(inizzializzazione);
$(toggleFilter);
$(toggleMenu);