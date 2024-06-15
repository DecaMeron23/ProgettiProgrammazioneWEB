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
        return connection
    except:
        print("Errore durante la connessione al database")
        exit()

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

def eseguiQuery(query):
    conn = connectDB()

    cursore = conn.cursor()
    # print(query)
    cursore.execute(query)

    risultati = cursore.fetchall()

    conn.close()
    return risultati


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
    DIZIONARIO_WHERE = {"codice" : "QUIZ.CODICE", "titolo" : "QUIZ.TITOLO" , "creatore" : "QUIZ.CREATORE" , "dataInizio" : "QUIZ.DATA_INIZIO" , "dataFine" : "QUIZ.DATA_FINE"}
    
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

    # print(condizioni_where)
    # print(condizioni_having)

    query = QUERY_QUIZ  + condizioni_where + GROUP_BY + condizioni_having + ORDER_BY
    
    risultati = eseguiQuery(query)

    return risultati

# {'nomeUtente': 'dd', 'nome': 'nn', 'cognome': 'cc', 'email': '@', 'nQcreati': '2', 'nQgiocati': '3', 'radio_quale_nQcreati': '1', 'radio_nQgiocati': '2'}

def getUtente(parametri):
    
    QUERY = "SELECT UTENTE.NOME_UTENTE AS nomeUtente , UTENTE.NOME AS nome , UTENTE.COGNOME AS cognome , UTENTE.EMAIL AS email , COUNT(DISTINCT QUIZ.CODICE) as nQcreati , COUNT(DISTINCT PARTECIPAZIONE.QUIZ) as nQgiocati FROM UTENTE LEFT JOIN QUIZ ON UTENTE.NOME_UTENTE = QUIZ.CREATORE LEFT JOIN PARTECIPAZIONE ON UTENTE.NOME_UTENTE = PARTECIPAZIONE.UTENTE"

    # Definizione delle condizioni per il where 
    DIZIONARIO_WHERE = {"nomeUtente" : "UTENTE.NOME_UTENTE" , "nome" : "UTENTE.NOME" , "cognome" : "UTENTE.COGNOME" , "email" :"UTENTE.EMAIL"}
    
    #Definizione delle condizioni per il having 
    DIZIONARIO_HAVING = {"nQcreati": "nQcreati" , "nQgiocati": "nQgiocati"}

    DIZIONARIO_VINCOLI = {"nQcreati" : "radio_quale_nQcreati" , "nQgiocati" : "radio_nQgiocati"}

    GROUP_BY = " GROUP BY UTENTE.NOME_UTENTE "

    ORDER_BY = " ORDER BY UTENTE.NOME_UTENTE ASC"

    [condizioni_where , condizioni_having] = CondizioniWhereHaving(parametri, DIZIONARIO_WHERE , DIZIONARIO_VINCOLI , DIZIONARIO_HAVING)

    # print(condizioni_where)
    # print(condizioni_having)

    query = QUERY  + condizioni_where + GROUP_BY + condizioni_having + ORDER_BY
    
    # print(query)
    risultati = eseguiQuery(query)

    # print(risultati)

    return risultati

def getPartecipazione(parametri):
    
    QUERY = " SELECT PARTECIPAZIONE.CODICE AS codice , PARTECIPAZIONE.UTENTE AS nomeUtente , QUIZ.TITOLO AS quiz, QUIZ.CODICE AS codiceQuiz, PARTECIPAZIONE.DATA AS data, COUNT(RISPOSTA_UTENTE_QUIZ.RISPOSTA) AS nRisposte FROM (PARTECIPAZIONE JOIN RISPOSTA_UTENTE_QUIZ ON PARTECIPAZIONE.CODICE = RISPOSTA_UTENTE_QUIZ.PARTECIPAZIONE) JOIN QUIZ ON PARTECIPAZIONE.QUIZ = QUIZ.CODICE "

    # Definizione delle condizioni per il where 
    DIZIONARIO_WHERE = {"codice" : "PARTECIPAZIONE.CODICE" , "nomeUtente" : "PARTECIPAZIONE.UTENTE" , "quiz" : "QUIZ.TITOLO" , "codiceQuiz" :"QUIZ.CODICE" , "data" : "PARTECIPAZIONE.DATA"}
    
    #Definizione delle condizioni per il having 
    DIZIONARIO_HAVING = {"nRisposte": "nRisposte"}

    DIZIONARIO_VINCOLI = {"data" : "radio_quale_data" , "nRisposte" : "radio_nRisposte"}

    GROUP_BY = " GROUP BY PARTECIPAZIONE.CODICE "

    ORDER_BY = " ORDER BY PARTECIPAZIONE.UTENTE ASC"

    if "data" in parametri:
        parametri["data"] = funzionalita.DataFormatoDataBase(parametri["data"])

    [condizioni_where , condizioni_having] = CondizioniWhereHaving(parametri, DIZIONARIO_WHERE , DIZIONARIO_VINCOLI , DIZIONARIO_HAVING)


    print(condizioni_where)
    print(condizioni_having)

    query = QUERY  + condizioni_where + GROUP_BY + condizioni_having + ORDER_BY
    
    # print(query)
    risultati = eseguiQuery(query)

    # print(risultati)

    return risultati



# parametri = {'nomeUtente': 'dd', 'nome': 'nn', 'cognome': 'cc', 'email': '@', 'nQcreati': '2', 'nQgiocati': '3', 'radio_quale_nQcreati': '1', 'radio_nQgiocati': '2'}
# getUtente(parametri)