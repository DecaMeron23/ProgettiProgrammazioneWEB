from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

import pymysql

from . import funzionalita

LIKE = " LIKE "
AND = " AND "
WHERE = " WHERE "
HAVING = " HAVING "

TIPOLOGIE = {"minore": "1",
             "uguale": "2",
             "maggiore": "3",
             "testo": "like"}

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

# Tipologie di ricerche:
# -minore
# -uguale
# -maggiore
# -like
def aggiungiCondizioneWhere(condizione, nome , valore , tipologia):
    condizione = aggiungiCondizione(condizione , nome , valore , tipologia)
    
    if not (WHERE in condizione):
        condizione = WHERE + condizione
    
    return condizione

def aggiungiCondizioneHaving(condizione, nome , valore , tipologia):
    condizione = aggiungiCondizione(condizione , nome , valore , tipologia)
    
    if not(HAVING in condizione):
        condizione = HAVING + condizione
    
    return condizione

def aggiungiCondizione(condizione, nome , valore , tipologia):

    # if not isinstance(valore , int):
    #     valore = f"'{valore}'"

    if tipologia == TIPOLOGIE["minore"]:
        if not isinstance(valore , int):
            valore = f"'{valore}'"
        vincolo = nome + " < " + valore
    elif tipologia == TIPOLOGIE["maggiore"]:
        if not isinstance(valore , int):
            valore = f"'{valore}'"
        vincolo = nome + " > " + valore
    elif tipologia == TIPOLOGIE["uguale"]:
        if not isinstance(valore , int):
            valore = f"'{valore}'"
        vincolo = nome + " = " + valore
    elif tipologia == TIPOLOGIE["testo"]:
        if not isinstance(valore , int):
            valore = f"'%{valore}%'"
        vincolo = nome + LIKE + valore

    if condizione == "":
        condizione = vincolo
    else:
        condizione += AND + vincolo
    
    return condizione

def CondizioniWhereHaving(parametri , DIZIONARIO_WHERE , DIZIONARIO_VINCOLI , DIZIONARIO_HAVING):
    condizioni_where = ""
    condizioni_having = ""
    for key , value in parametri.items():
        # Se è una condizione where
        if key in DIZIONARIO_WHERE:
            tipologia = TIPOLOGIE["testo"]
            # verifichiamo se non è un testo
            if key in DIZIONARIO_VINCOLI:
                # estraiamo la chiave per estrare il valore
                nomeVincolo = DIZIONARIO_VINCOLI[key]
                # preleviamo il valore se è settato
                if nomeVincolo in parametri:
                        tipologia = parametri[nomeVincolo]
                        condizioni_where = aggiungiCondizioneWhere(condizioni_where , DIZIONARIO_WHERE[key] , value , tipologia)
            else:
                # Aggiungiamo la condizione
                condizioni_where = aggiungiCondizioneWhere(condizioni_where , DIZIONARIO_WHERE[key] , value , tipologia)
        elif key  in DIZIONARIO_HAVING:
            # verifichiamo se non è un testo (non dovrebbe esserlo)
            if key in DIZIONARIO_VINCOLI:
                # estraiamo la chiave per estrare il valore
                nomeVincolo = DIZIONARIO_VINCOLI[key]
                
                # preleviamo il valore se è settato
                if nomeVincolo in parametri:
                    tipologia = parametri[nomeVincolo]
                    condizioni_having = aggiungiCondizioneHaving(condizioni_having , DIZIONARIO_HAVING[key] , value , tipologia)
            else:
                print("Errore Durante la creazione della query:" + key + " " + value)
                # Aggiungiamo la condizione

    return [condizioni_where , condizioni_having]


def getQuiz(parametri):
    
    # Definizione delle condizioni per il where 
    DIZIONARIO_WHERE = {"titolo" : "QUIZ.TITOLO" , "creatore" : "QUIZ.CREATORE" , "dataInizio" : "QUIZ.DATA_INIZIO" , "dataFine" : "QUIZ.DATA_FINE"}
    
    #Definizione delle condizioni per il having 
    DIZIONARIO_HAVING = {"nDomande": "nDomande" , "nPartecipazioni": "nPartecipazioni"}


    DIZIONARIO_VINCOLI = {"dataInizio" : "radio_quale_dataInizio" , "dataFine" : "radio_quale_dataFine" , "nDomande": "radio_quale_nDomande" , "nPartecipazioni" : "radio_quale_nPartecipazioni"}

    QUERY_QUIZ = "SELECT QUIZ.CODICE AS codice, QUIZ.CREATORE AS creatore, QUIZ.TITOLO AS titolo, QUIZ.DATA_INIZIO AS dataInizio, QUIZ.DATA_FINE AS dataFine, COUNT(DISTINCT DOMANDA.NUMERO) AS nDomande, COUNT(DISTINCT PARTECIPAZIONE.CODICE) AS nPartecipazioni FROM QUIZ LEFT JOIN DOMANDA ON QUIZ.CODICE = DOMANDA.QUIZ LEFT JOIN PARTECIPAZIONE ON QUIZ.CODICE = PARTECIPAZIONE.QUIZ "

    GROUP_BY = " GROUP BY QUIZ.CODICE, QUIZ.CREATORE, QUIZ.TITOLO, QUIZ.DATA_INIZIO, QUIZ.DATA_FINE "

    ORDER_BY = " ORDER BY QUIZ.TITOLO ASC"


    # Modifichiamo il formato delle date in Y/M/D
    if "dataInizio" in parametri:
        parametri["dataInizio"] = funzionalita.DataFormatoDataBase(parametri["dataInizio"])    
    
    if "dataFine" in parametri:
        parametri["dataFine"] = funzionalita.DataFormatoDataBase(parametri["dataFine"])    
        
    [condizioni_where , condizioni_having] = CondizioniWhereHaving(parametri, DIZIONARIO_WHERE , DIZIONARIO_VINCOLI , DIZIONARIO_HAVING)

    print(condizioni_where)
    print(condizioni_having)

    query = QUERY_QUIZ  + condizioni_where + GROUP_BY + condizioni_having + ORDER_BY
    
    conn = connectDB()

    cursore = conn.cursor()
    # print(query)
    cursore.execute(query)

    risultati = cursore.fetchall()

    conn.close()

    return risultati

parametri = {}
getQuiz(parametri)
