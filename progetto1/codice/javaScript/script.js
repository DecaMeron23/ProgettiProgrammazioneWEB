var setHeaderSelected = function () {
    // settiamo le diverse directori
    mieDirectory = {
        home: "/progetto1", //#sistemare: al momento è progetto 1 poi quando caricherò sul sito sarà ""
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
    dir = "/"+ dir[dir.length-2] ;
    
    var i = 0;
    for (var chiave in mieDirectory) {
        if (mieDirectory[chiave] == dir) {
            $("#listaHeader li a").eq(i).addClass("cliccato");
        }
        i++;
    }
}

$(setHeaderSelected)