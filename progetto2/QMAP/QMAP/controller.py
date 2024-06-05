from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def index(request):
    res = HttpResponse(content_type="text/html")

    context = {};

    
    template = loader.get_template("index.html")
    page = template.render(context= context , request= request)

    res.write(page)

    return res

def quiz(request):
    res = HttpResponse(content_type="text/html")

    if request.method == "GET":
        parametri = request.GET
        parametri = {k: v[0] if len(v) == 1 else v for k, v in parametri.lists()}

    if "nDomande" in parametri:
        parametri["isSet_nDomande"] = parametri["nDomande"] != "";

    if "nPartecipazioni" in parametri:
        parametri["isSet_nPartecipazioni"] = parametri["nPartecipazioni"] != "";
    


    context = {};

    list = []

    for i in range(0,10):
        o = {}
        o["titolo"] = "Titolo"
        o["autore"] = "Autorevole"
        o["dataInizio"] = "02/07/2022"
        o["dataFine"] = "inf"
        o["nDomande"] = 10
        o["nPartecipazioni"] = -2

        list.append(o)
        # print(o)



    context["risultati"] = {"numeroRighe": len(list) , "valori": list}
    context["filtro"] = parametri


    template = loader.get_template("quiz.html")
    page = template.render(context= context , request= request)

    res.write(page)

    return res
