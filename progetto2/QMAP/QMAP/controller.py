from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


templateDati = "presentazioneDati.html"

def estrazioneParametriGet(request):
    parametri = request.GET

    parametri = {k: v[0] if len(v) == 1 else v for k, v in parametri.lists()}
    
    return parametri

def index(request):
    res = HttpResponse(content_type="text/html")

    context = {};

    
    template = loader.get_template("index.html")
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
    if "nDomande" in parametri:
        parametri["isSet_nDomande"] = parametri["nDomande"] != "";

    if "nPartecipazioni" in parametri:
        parametri["isSet_nPartecipazioni"] = parametri["nPartecipazioni"] != "";
    

    #? Oggetti contesto da passare al template
    context = {};

    # todo: Estrazione dati dal server e aggiunta al contesto
    valoriEstratti = []

    for i in range(0,15):
        o = []
        o.append({"valore" : "Titolo" , "impostazioni": {}})
        o.append({"valore" : "Autorevole" , "impostazioni": {"class": "text-center ciao" , "implementa" : "niente"}})
        o.append({"valore" : "02/07/2022" , "impostazioni": {"class": "text-center"}})
        o.append({"valore" : "inf" , "impostazioni": {"class": "text-center"}})
        o.append({"valore" : 10 , "impostazioni": {"class": "text-center"}})
        o.append({"valore" : -2 , "impostazioni": {"class": "text-center"}})

        valoriEstratti.append(o)
        # print(o)

    #? preparazione contesto: risultati
    numeroRighe = len(valoriEstratti)
    if(numeroRighe <= 0): 
        infoRicerca = "Nessun quiz trovato"
    elif numeroRighe == 1:
        infoRicerca = "Trovato un solo quiz"
    else:
        infoRicerca = "sono stati trovati {} quiz".format(numeroRighe)

    listaIntestazioni = ["Titolo" , "Autore", "Data Inizio" , "Data Fine" , "N° di Domande" , "N° di Partecipanti"]


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
