
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

function openModificaQUIZ() {
    attivaMaschera(1)
    $(".popup_quiz").toggleClass("popup_quiz_show");
}

function aggiungiQUIZ(event) {
    event.preventDefault();
    var creatore = $("#creatore").val();
    var titolo = $("#titolo").val();
    var dataInizio_string = $("#data_inizio").val();
    var dataFine_string = $("#data_fine").val();

    dataInizio = new Date(dataInizio_string);
    dataFine = new Date(dataFine_string);

    if (dataFine <= dataInizio_string) {
        alert("Attenzione inserire una data di fine maggiore di data inizo")
    } else {
        $.ajax({
            type: "GET",
            url: 'https://quizmakeandplay.altervista.org/php/funzionalitaPHP_JS.php',
            dataType: 'json',
            data: { functionname: 'addQUIZ', nome_utente: creatore, titolo: titolo, data_inizio: dataInizio_string, data_fine: dataFine_string },
            success: function (obj, textstatus) {
                reinderizzaINFO_QUIZ(obj[0]);
            }
        });
    }
}


$(inizzializzazione);
$(toggleFilter);
$(toggleMenu);