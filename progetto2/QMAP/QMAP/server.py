from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

import pymysql

# Definisci le variabili per le credenziali di accesso
MYSQL_HOST = 'quizmakeandplay-emiliomeroni99-5f9c.g.aivencloud.com'
MYSQL_PORT = 21469
MYSQL_USERNAME = 'avnadmin'
MYSQL_PASSWORD = 'AVNS_M0qytOJWua25SLzRrGN'
MYSQL_DATABASE = 'my_quizmakeandplay'

def connectDB():
    timeout = 10
    try:
        connection = pymysql.connect(
        charset="utf8mb4",
        connect_timeout=timeout,
        cursorclass=pymysql.cursors.DictCursor,
        db=MYSQL_DATABASE,
        host=MYSQL_HOST,
        password=MYSQL_PASSWORD,
        read_timeout=timeout,
        port=MYSQL_PORT,
        user=MYSQL_USERNAME,
        write_timeout=timeout,
        )
        print("connesso")
        return connection
    except:
        print("Errore durante la connessione al database")


def getQuiz(request):
    res = HttpResponse(content_type="application/json")

    conn = connectDB();

    


    res.write(risposta)

    return res