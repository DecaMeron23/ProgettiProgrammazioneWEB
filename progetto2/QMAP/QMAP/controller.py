from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt


templateIndex = "index.html"
templateDati = "presentazioneDati.html"
templateGioca = "gioca.html"
templateInfoQuiz = "infoQuiz.html"
templateOps = "ops.html"
template404 = "404.html"

OPEN_QUIZ = "reindirizzaQUIZ(this)";
OPEN_UTENTE = "reindirizzaUTENTE(this)";
OPEN_PARTECIPAZIONE = "reindirizzaPARTECIPAZIONI(this)";
OPEN_INFO_QUIZ = "reindirizzaINFO_QUIZ(this)";
OPEN_CREA_QUIZ = "openCreaQuiz(this)";

from . import funzionalita
from . import server

import random



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

    rispostaServer = server.getQuiz(parametri.copy())
    valoriEstratti = []

    for riga in rispostaServer:

        o = []
        idQuiz = riga["codice"]
        titolo = riga["titolo"]
        autore = riga["creatore"]
        dataInizio = funzionalita.DataFormatoView(riga["dataInizio"])
        dataFine = funzionalita.DataFormatoView(riga["dataFine"])
        nDomande = riga["nDomande"]
        nPartecipazioni = riga["nPartecipazioni"]
        
        date = dataInizio + " " + dataFine

        o.append({"valore" : titolo , "impostazioni": {"id-quiz" : idQuiz , "implementa": "onClick" , "onClick" : OPEN_INFO_QUIZ}})
        o.append({"valore" : autore , "impostazioni": {"class": "text-center ciao" , "implementa" : "onClick" , "onClick" : OPEN_UTENTE}})
        o.append({"valore" : dataInizio , "impostazioni": {"class": "text-center"  , "implementa" : "niente"}})
        o.append({"valore" : dataFine , "impostazioni": {"class": "text-center " , "implementa" : "niente"}})
        o.append({"valore" : nDomande , "impostazioni": {"class": "text-center" , "implementa" : "niente"}})
        o.append({"valore" : nPartecipazioni , "impostazioni": {"class": "text-center", "id-quiz" : idQuiz ,  "implementa": "onClick" , "onClick" : OPEN_PARTECIPAZIONE}})

        valoriEstratti.append(o)

    if "nDomande" in parametri:
        parametri["isSet_nDomande"] = parametri["nDomande"] != "";

    if "nPartecipazioni" in parametri:
        parametri["isSet_nPartecipazioni"] = parametri["nPartecipazioni"] != "";
    

    parametri["directory"] = "filtri/filtroQuiz.html"


    #? preparazione contesto: risultati
    numeroRighe = len(valoriEstratti)
    if(numeroRighe <= 0): 
        infoRicerca = "Nessun quiz trovato"
    elif numeroRighe == 1:
        infoRicerca = "Trovato un solo quiz"
    else:
        infoRicerca = "sono stati trovati {} quiz".format(numeroRighe)


    listaIntestazioni = [{"valore":"Titolo" , "impostazioni":{}}, {"valore":"Autore" , "impostazioni":{}}, {"valore":"Data Inizio" , "impostazioni": {}} , {"valore":"Data Fine" , "impostazioni":{}} , {"valore":"N° di Domande" , "impostazioni":{}} , {"valore": "N° di Partecipanti" , "impostazioni":{}}]


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
        o.append({"valore" : nick , "impostazioni": {"data-toggle" : "tooltip", "title":email ,"implementa" : "onClick" , "onClick": OPEN_CREA_QUIZ}})
        o.append({"valore" : nome , "impostazioni": {"class": "text-center" , "implementa" : "niente"}})
        o.append({"valore" : cognome , "impostazioni": {"class": "text-center" , "implementa": "niente"}})
        o.append({"valore" : email , "impostazioni": {"class": "d-none d-md-table-cell" , "implementa": "niente"}})
        o.append({"valore" : nQcreati , "impostazioni": {"class": "text-center" , "implementa": "onClick" ,"onClick": OPEN_QUIZ , "nome_utente" : nick}})
        o.append({"valore" : nQgiocati , "impostazioni": {"class": "text-center" , "implementa": "onClick" ,"onClick": OPEN_PARTECIPAZIONE, "nome_utente" : nick}})

        valoriEstratti.append(o)


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

    risultati = server.getPartecipazione(parametri.copy())

    valoriEstratti = []

    for riga in risultati:

        codiceQuiz = riga["codiceQuiz"];
        nick = riga["nomeUtente"]
        titolo = riga["quiz"]
        data = funzionalita.DataFormatoView(riga["data"])
        nRisposte = riga["nRisposte"]

        o = []
        o.append({"valore" : nick , "impostazioni": {"onClick": OPEN_UTENTE}})
        o.append({"valore" : titolo , "impostazioni": {"implementa" : "onClick" , "id-quiz": codiceQuiz , "onClick" : OPEN_QUIZ}})
        o.append({"valore" : data , "impostazioni": {"class": "text-center"}}) #TODO
        o.append({"valore" : nRisposte , "impostazioni": {"class": "text-center" , "implementa": ""}}) #TODO

        valoriEstratti.append(o)

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
    
    # Prendiamo tutti i QUIZ
    data = server.getQuiz({})

    # Seleziona un QUIZ a caso
    quiz = random.choice(data)

    # Prendiamo tutte le domande per quel quiz
    domandeDB = server.getDomandeQuiz(quiz["codice"])

    # mischiamo le domande
    random.shuffle(domandeDB)
    
    domande = []
    for domanda in domandeDB:
        risposteDB = server.getRisposteDomandaQuiz(codiceQuiz=quiz["codice"] , numeroDomanda = domanda["numero"])
        random.shuffle(risposteDB)
        risposte = []
        domandaPunteggio = 2

        for risposta in risposteDB:
            o_r = {}
            o_r["testo"] = risposta["testo"]
            o_r["corretta"] = risposta["tipo"] == "1" 
            o_r["numero"] = risposta["numero"]

            if not risposta["punteggio"] == None:
                domandaPunteggio = risposta["punteggio"]

            risposte.append(o_r)



        o_d = {}


        o_d["testo"] = domanda["testo"]
        o_d["numero"] = domanda["numero"]
        o_d["punteggio"] = domandaPunteggio
        o_d["risposte"] = risposte

        domande.append(o_d)

    infoQuiz = {"idQuiz" : quiz["codice"],
                "autore" : quiz["creatore"],
                "dataInizio" : funzionalita.DataFormatoView(quiz["dataInizio"]),
                "dataFine" : funzionalita.DataFormatoView(quiz["dataFine"]),
                "titolo" : quiz["titolo"],
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
@csrf_exempt
def info(request):
    '''
    Funzione che crea la vista per info quiz, riceve un parametro POST con nome codice

    '''
    
    # Devo farlo per sicurezza...sennò non va la pagina, bah
    pass 
    
    res = HttpResponse(content_type="text/html")
    context = {}
    
    richiestaServer = { "codice" : request.POST.get("codice")};
    
    quiz = server.getQuiz(richiestaServer);

    # prendiamo il primo elemento 

    if len(quiz) < 1:
        #? preparazione del template
        template = loader.get_template(templateOps)
        
        context["codiceQuiz"] = richiestaServer["codice"];
        context["testo"] = "Ops, il quiz non esiste più..."

        page = template.render(context= context , request= request)

        res.write(page)
        return res


    quiz = quiz[0];

    # Prendiamo tutte le domande per quel quiz
    domandeDB = server.getDomandeQuiz(quiz["codice"])

    domande = []
    for domanda in domandeDB:
        risposteDB = server.getRisposteDomandaQuiz(codiceQuiz=quiz["codice"] , numeroDomanda = domanda["numero"])
        
        random.shuffle(risposteDB)

        risposte = []
        domandaPunteggio = 2

        for risposta in risposteDB:
            o_r = {}
            o_r["testo"] = risposta["testo"]
            o_r["corretta"] = risposta["tipo"] == "1" 
            o_r["numero"] = risposta["numero"]

            if not risposta["punteggio"] == None:
                domandaPunteggio = risposta["punteggio"]

            risposte.append(o_r)

        o_d = {}

        o_d["testo"] = domanda["testo"]
        o_d["numero"] = domanda["numero"]
        o_d["punteggio"] = domandaPunteggio
        o_d["risposte"] = risposte

        domande.append(o_d)

    infoQuiz = {"idQuiz" : quiz["codice"],
                "autore" : quiz["creatore"],
                "dataInizio" : funzionalita.DataFormatoView(quiz["dataInizio"]),
                "dataFine" : funzionalita.DataFormatoView(quiz["dataFine"]),
                "titolo" : quiz["titolo"],
                "domande" : domande
                }    
    context = infoQuiz
    context["infoPagina"] = {"nomePagina" : "Info Quiz"}

    #? preparazione del template
    template = loader.get_template(templateInfoQuiz)
    page = template.render(context= context , request= request)

    res.write(page)

    return res

def  page_not_found(request, exception):
    context = {}
    context["testo"] = "Ops... Questa pagina non esiste!"
    context["pagina"] = request.build_absolute_uri()
    return render(request, template404, context)