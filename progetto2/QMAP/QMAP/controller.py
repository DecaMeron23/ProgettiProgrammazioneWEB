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

    context = {};

    template = loader.get_template("quiz.html")
    page = template.render(context= context , request= request)

    res.write(page)

    return res
