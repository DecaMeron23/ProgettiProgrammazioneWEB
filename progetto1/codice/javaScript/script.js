var setHeaderSelected = function () {
    // settiamo le diverse directori
    mieDirectory = {
        home: "/",
        utente: "/utente",
        quiz: "/quiz",
        partecipazione: "/partecipazione",
    }

    // reset della classe
    $("#listaHeader li a").each(function (index, element) {
        $(this).removeClass("cliccato");
    });

    // prendiamo la directory
    var loc = window.location.pathname;
    var dir = loc.split('/');
    dir = "/" + dir[dir.length - 2];

    var i = 0;
    for (var chiave in mieDirectory) {
        if (mieDirectory[chiave] == dir) {
            $("#listaHeader li a").eq(i).addClass("cliccato");
        }
        i++;
    }
}

function attivaMaschera(){
    $(".maschera").toggleClass("maschera_on");
    $("body").toggleClass("menuOpen");
}

// Funzione viene eseguita quando si apre il menu
var toggleMenu = function () {
    $(".navbar").click(function () {
        $(".nav").toggleClass("wide");
        $(".navbar").toggleClass("navbar_rotate");
        attivaMaschera();
    });
};

var toggleFilter = function () {
    $(".iconaRicerca").click(function () {
        $(".filtroRicerca").toggleClass("ricercaShow");
        $(".iconaRicerca").toggleClass("iconaRicercaShow");
        attivaMaschera();
    });
}


$(setHeaderSelected)
$(toggleFilter)
$(toggleMenu)