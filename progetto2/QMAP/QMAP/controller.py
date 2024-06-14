from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


templateIndex = "index.html"
templateDati = "presentazioneDati.html"
templateGioca = "gioca.html"
templateInfoQuiz = "infoQuiz.html"


from . import funzionalita
from . import server

def estrazioneParametriGet(request):
    parametri = request.GET

    parametri = {k: v[0] if len(v) == 1 else v for k, v in parametri.lists()}
    
    return parametri

def index(request):
    res = HttpResponse(content_type="text/html")

    context = {};
    context["infoPagina"] = {"nomePagina":"index"}
    
    template = loader.get_template(templateIndex)
    page = template.render(context= context , request= request)

    res.write(page)

    return res

#! Info struttura del template:
#? -filtro: contiene tutti i valori per il filtro
#? -infoPagina:
#   -nomePagina: il nome della pagina
#   -directory: la "directory" della pagina
#? -risultati:
#   -numeroRighe: numero delle righe ricevute
#   -valori: i valori estratti matrice (array di array per identificare la singola cella) inoltre la singola cella sarà un dizionario con: #       -valore: il valore della cella
#       -impostazioni: le diverse impostazioni (ad esempio class o onClick)
#   -frasiRicerca: le diverse frasi come risultato della ricerca
#       -info: le informazioni della ricerca ad esempio quanti elementi abbiamo trovato


def quiz(request):
    res = HttpResponse(content_type="text/html")

    parametri = estrazioneParametriGet(request);
    #? Oggetti contesto da passare al template
    context = {};

    # todo: Estrazione dati dal server e aggiunta al contesto
    
    rispostaServer = server.getQuiz(parametri.copy())
    valoriEstratti = []

    for riga in rispostaServer:
        o = []
        titolo = riga["titolo"]
        autore = riga["creatore"]
        dataInizio = funzionalita.DataToString(riga["dataInizio"])
        dataFine = funzionalita.DataToString(riga["dataFine"])
        nDomande = riga["nDomande"]
        nPartecipazioni = riga["nPartecipazioni"]

        o.append({"valore" : titolo , "impostazioni": {}})
        o.append({"valore" : autore , "impostazioni": {"class": "text-center ciao" , "implementa" : "niente"}})
        o.append({"valore" : dataInizio , "impostazioni": {"class": "text-center"}})
        o.append({"valore" : dataFine , "impostazioni": {"class": "text-center"}})
        o.append({"valore" : nDomande , "impostazioni": {"class": "text-center"}})
        o.append({"valore" : nPartecipazioni , "impostazioni": {"class": "text-center"}})

        valoriEstratti.append(o)
        # print(o)

    if "nDomande" in parametri:
        parametri["isSet_nDomande"] = parametri["nDomande"] != "";

    if "nPartecipazioni" in parametri:
        parametri["isSet_nPartecipazioni"] = parametri["nPartecipazioni"] != "";
    

    parametri["directory"] = "filtri/filtroQUiz.html"


    #? preparazione contesto: risultati
    numeroRighe = len(valoriEstratti)
    if(numeroRighe <= 0): 
        infoRicerca = "Nessun quiz trovato"
    elif numeroRighe == 1:
        infoRicerca = "Trovato un solo quiz"
    else:
        infoRicerca = "sono stati trovati {} quiz".format(numeroRighe)

    

    listaIntestazioni = [{"valore":"Titolo" , "impostazioni":{}}, {"valore":"Autore" , "impostazioni":{}}, {"valore":"Data Inizio" , "impostazioni":{}} , {"valore":"Data Fine" , "impostazioni":{}} , {"valore":"N° di Domande" , "impostazioni":{}} , {"valore": "N° di Partecipanti" , "impostazioni":{}}]


    context["risultati"] = {"numeroRighe": numeroRighe , "valori": valoriEstratti , "frasiRicerca": {"info": infoRicerca} , "listaIntestazioni": listaIntestazioni}



    #? preparazione contesto: infoPagina
    context["infoPagina"] = {"nomePagina" : "Quiz" , "directory" : "Home>Quiz"}
    
    #? preparazione contesto: filtro
    context["filtro"] = parametri

    #? preparazione del template
    template = loader.get_template(templateDati)
    page = template.render(context= context , request= request)

    res.write(page)
    return res

# ! UTENTE
def utente(request):
    res = HttpResponse(content_type="text/html")

    parametri = estrazioneParametriGet(request); 
    
    # print(parametri)
    #? Oggetti contesto da passare al template
    context = {};

    # Estrazione dati dal server e aggiunta al contesto
    risultati = server.getUtente(parametri.copy())

    valoriEstratti = []

    for riga in risultati:

        nick = riga["nomeUtente"]
        nome = riga["nome"]
        cognome = riga["cognome"]
        email = riga["email"]
        nQcreati = riga["nQcreati"]
        nQgiocati = riga["nQgiocati"]

        o = []
        o.append({"valore" : nick , "impostazioni": {"data-toggle" : "tooltip", "title":email}}) #TODO
        o.append({"valore" : nome , "impostazioni": {"class": "text-center" , "implementa" : "niente"}})
        o.append({"valore" : cognome , "impostazioni": {"class": "text-center" , "implementa": "niente"}})
        o.append({"valore" : email , "impostazioni": {"class": "d-none d-md-table-cell" , "implementa": "niente"}})
        o.append({"valore" : nQcreati , "impostazioni": {"class": "text-center" , "implementa": ""}}) #TODO
        o.append({"valore" : nQgiocati , "impostazioni": {"class": "text-center" , "implementa": ""}}) #TODO

        valoriEstratti.append(o)
        # print(o)


    if "nQcreati" in parametri:
        parametri["isSet_nQcreati"] = parametri["nQcreati"] != "";

    if "nQgiocati" in parametri:
        parametri["isSet_nQgiocati"] = parametri["nQgiocati"] != "";
    

    parametri["directory"] = "filtri/filtroUtente.html"



    #? preparazione contesto: risultati
    numeroRighe = len(valoriEstratti)
    if(numeroRighe <= 0): 
        infoRicerca = "Nessun utente trovato"
    elif numeroRighe == 1:
        infoRicerca = "Trovato un solo utente"
    else:
        infoRicerca = "sono stati trovati {} utenti".format(numeroRighe)


    # noInferioreMd = {"class": "d-none d-md-table-cell"}

    listaIntestazioni = [{"valore":"Nickname" , "impostazioni":{}},
                         {"valore":"Nome" , "impostazioni":{"class": ""}},
                         {"valore":"Cognome" , "impostazioni":{"class": ""}},
                         {"valore":"Email" , "impostazioni":{"class": "d-none d-md-table-cell"}},
                         {"valore":"N° Quiz Creati" , "impostazioni":{}},
                         {"valore": "N° Quiz Giocati" , "impostazioni":{}}]


    context["risultati"] = {"numeroRighe": numeroRighe , "valori": valoriEstratti  , "frasiRicerca": {"info": infoRicerca} , "listaIntestazioni": listaIntestazioni}


    #? preparazione contesto: infoPagina
    context["infoPagina"] = {"nomePagina" : "Utente" , "directory" : "Home>Utente"}
    
    #? preparazione contesto: filtro
    context["filtro"] = parametri

    #? preparazione del template
    template = loader.get_template(templateDati)
    page = template.render(context= context , request= request)

    res.write(page)

    return res


# ! Partecipazione
def partecipazione(request):
    res = HttpResponse(content_type="text/html")

    parametri = estrazioneParametriGet(request);
    
    #? Oggetti contesto da passare al template
    context = {};

    print(parametri)
    # todo: Estrazione dati dal server e aggiunta al contesto
    
    risultati = server.getPartecipazione(parametri.copy())

    valoriEstratti = []

    for riga in risultati:

        nick = riga["nomeUtente"]
        titolo = riga["quiz"]
        data = funzionalita.DataToString(riga["data"])
        nRisposte = riga["nRisposte"]

        o = []
        o.append({"valore" : nick , "impostazioni": {}}) #TODO
        o.append({"valore" : titolo , "impostazioni": {"class": "" , "implementa" : ""}}) #TODO
        o.append({"valore" : data , "impostazioni": {"class": "text-center"}}) #TODO
        o.append({"valore" : nRisposte , "impostazioni": {"class": "text-center" , "implementa": ""}}) #TODO

        valoriEstratti.append(o)
        # print(o)

    #? preparazione contesto: risultati
    numeroRighe = len(valoriEstratti)
    if(numeroRighe <= 0): 
        infoRicerca = "Nessuna partecipazione trovata"
    elif numeroRighe == 1:
        infoRicerca = "Trovata una sola patecipazione"
    else:
        infoRicerca = "sono state trovate {} partecipazioni".format(numeroRighe)

    if "nRisposte" in parametri:
        parametri["isSet_nRisposte"] = parametri["nRisposte"] != "";

    parametri["directory"] = "filtri/filtroPartecipazione.html"

    # noInferioreMd = {"class": "d-none d-md-table-cell"}

    listaIntestazioni = [{"valore":"Nickname" , "impostazioni":{}},
                         {"valore":"Titolo Quiz" , "impostazioni":{"class": ""}},
                         {"valore":"Data Partecipazione" , "impostazioni":{"class": ""}},
                         {"valore":"N° Risposte Date" , "impostazioni":{}}]

    context["risultati"] = {"numeroRighe": numeroRighe , "valori": valoriEstratti , "frasiRicerca": {"info": infoRicerca} , "listaIntestazioni": listaIntestazioni}



    #? preparazione contesto: infoPagina
    context["infoPagina"] = {"nomePagina" : "Partecipazione" , "directory" : "Home>Partecipazione"}
    
    #? preparazione contesto: filtro
    context["filtro"] = parametri

    #? preparazione del template
    template = loader.get_template(templateDati)
    page = template.render(context= context , request= request)

    res.write(page)

    return res

# ! Gioca

def gioca(request):
    res = HttpResponse(content_type="text/html")
 
    context = {}
    
    #todo richiesta delle informazioni
    testoDomanda = "Chi sono io"
    testoRisposta = "emilio"
    punteggio = 3
    nomeAutore = "Benny"
    dataInizio = "02/07/2022"
    dataFine = "Non c'è"
    titolo = "Quanto mi Conosci?"

    domande = []
    risposte = []


    risposta = {"testo": testoRisposta , "corretta": True}
    for i in range(0,4):
        risposte.append(risposta)

    domanda = {"testo": testoDomanda ,
                "risposte" : risposte,
                "punteggio" : punteggio}

    for i in range(0,4):
        domande.append(domanda)


    infoQuiz = {"autore" : nomeAutore,
                "dataInizio" : dataInizio,
                "dataFine" : dataFine,
                "titolo" : titolo,
                "domande" : domande
                }

    context = infoQuiz
    context["infoPagina"] = {"nomePagina" : "gioca"}


    #? preparazione del template
    template = loader.get_template(templateGioca)
    page = template.render(context= context , request= request)

    res.write(page)

    return res

# ! Info Quiz
def info(request):
    res = HttpResponse(content_type="text/html")
 
    context = {}
    
    #todo richiesta delle informazioni
    testoDomanda = "Chi sono io"
    testoRisposta = "emilio"
    punteggio = 3
    nomeAutore = "Benny"
    dataInizio = "02/07/2022"
    dataFine = "Non c'è"
    titolo = "Quanto mi Conosci?"

    domande = []
    risposte = []


    rispostaTrue = {"testo": testoRisposta , "corretta": True}
    rispostaFalse = {"testo": testoRisposta , "corretta": False}
    for i in range(0,2):
        risposte.append(rispostaTrue)
        risposte.append(rispostaFalse)

    domanda = {"testo": testoDomanda ,
                "risposte" : risposte,
                "punteggio" : punteggio}

    for i in range(0,4):
        domande.append(domanda)


    infoQuiz = {"autore" : nomeAutore,
                "dataInizio" : dataInizio,
                "dataFine" : dataFine,
                "titolo" : titolo,
                "domande" : domande
                }

    context = infoQuiz
    context["infoPagina"] = {"nomePagina" : "info"}

    #? preparazione del template
    template = loader.get_template(templateInfoQuiz)
    page = template.render(context= context , request= request)

    res.write(page)

    return res