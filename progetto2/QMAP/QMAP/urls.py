"""
URL configuration for QMAP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from . import controller
from . import server


# url
urlpatterns = [
    path("", controller.index , name= "index"),
    path("index", controller.index , name= "index"),
    path("quiz", controller.quiz , name= "quiz"),
    path("utente", controller.utente , name= "utente"),
    path("partecipazione", controller.partecipazione , name= "partecipazione"),
    path("gioca", controller.gioca , name= "gioca"),
    path("info", controller.info , name= "info"),
    path("get_quiz", server.getQuiz , name= "get_quiz"),
    path("funzionalita_js", server.funzionalitaJS , name= "funzionalita_js"),
    path("eliminaQuiz", server.eliminaQuiz , name= "eliminaQuiz"),
 
]
