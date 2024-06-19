from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

import pymysql

from . import funzionalita

LIKE = " LIKE "
AND = " AND "
WHERE = " WHERE "
HAVING = " HAVING "


TIPOLOGIA_ELEMENTO = {"data": "DATA",
                      "testo" : "TESTO",
                      "numero": "NUMERO"}

TIPOLOGIA_RICERCA = {"minore": "1",
             "uguale": "2",
             "maggiore": "3",
             "like": "like",
             "noLike": "2"}

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

    if tipologia == TIPOLOGIA_RICERCA["minore"]:
        if not isinstance(valore , int):
            valore = f"'{valore}'"
        vincolo = nome + " < " + valore
    elif tipologia == TIPOLOGIA_RICERCA["maggiore"]:
        if not isinstance(valore , int):
            valore = f"'{valore}'"
        vincolo = nome + " > " + valore
   
    elif tipologia == TIPOLOGIA_RICERCA["uguale"]:  # Valida anche per noLike
        if not isinstance(valore , int):
            valore = f"'{valore}'"
        vincolo = nome + " = " + valore
    elif tipologia == TIPOLOGIA_RICERCA["like"]:
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


# Lista dei parametri per le ricerce di QUIZ:
# - codice
# - titolo
# -- vincoloTitolo
# - creatore
# - dataInizio
# -- radio_quale_data_inizio
# - dataFine
# -- radio_quale_data_fine
# - nDomande
# -- radio_quale_nDomande
# - nPartecipazioni
# -- radio_quale_nPartecipazioni

def getQuiz(parametri):
    """
    Preleva i quiz secondo i parametri passati.
    

    Args:
        parametri (dizionario): Un dizionario con argomenti:

                - codice
                - titolo
                    - vincoloTitolo
                - creatore
                - dataInizio
                    - radio_quale_data_inizio
                - dataFine
                    - radio_quale_data_fine
                - nDomande
                    - radio_quale_nDomande
                - nPartecipazioni
                    - radio_quale_nPartecipazioni

    Returns:
        Un array di dizionario, con elementi:
            - codice
            - creatore
            - titolo
            - dataInizio
            - dataFine
            - nDomande
            - nPartecipazioni

    """    
    QUERY_QUIZ = "SELECT QUIZ.CODICE AS codice, QUIZ.CREATORE AS creatore, QUIZ.TITOLO AS titolo, QUIZ.DATA_INIZIO AS dataInizio, QUIZ.DATA_FINE AS dataFine, COUNT(DISTINCT DOMANDA.NUMERO) AS nDomande, COUNT(DISTINCT PARTECIPAZIONE.CODICE) AS nPartecipazioni FROM QUIZ LEFT JOIN DOMANDA ON QUIZ.CODICE = DOMANDA.QUIZ LEFT JOIN PARTECIPAZIONE ON QUIZ.CODICE = PARTECIPAZIONE.QUIZ "

    GROUP_BY = " GROUP BY QUIZ.CODICE, QUIZ.CREATORE, QUIZ.TITOLO, QUIZ.DATA_INIZIO, QUIZ.DATA_FINE "

    ORDER_BY = " ORDER BY QUIZ.TITOLO ASC"

    # Modifichiamo il formato delle date in Y/M/D
    if "dataInizio" in parametri:
        parametri["dataInizio"] = funzionalita.DataFormatoDataBase(parametri["dataInizio"])    
    
    if "dataFine" in parametri:
        parametri["dataFine"] = funzionalita.DataFormatoDataBase(parametri["dataFine"])    
        
    condizioniWhere = "";
    condizioniHaving = "";

    # ? CODICE
    if "codice" in parametri:
        condizioniWhere = aggiungiCondizioneWhere(condizione = condizioniWhere , nome= "QUIZ.CODICE", valore=parametri["codice"] , tipologia=TIPOLOGIA_RICERCA["noLike"])
    
    # ? TITOLO
    if "titolo" in parametri:
        tipologia = TIPOLOGIA_RICERCA["like"]
        # Se c'è il vincolo sui parametri
        if "vincoloTitolo" in parametri:
            tipologia = TIPOLOGIA_RICERCA["noLike"]

        condizioniWhere = aggiungiCondizioneWhere(condizione = condizioniWhere , nome= "QUIZ.TITOLO", valore=parametri["titolo"] , tipologia=tipologia)
    
    # ? CREATORE
    if "creatore" in parametri:
        tipologia = TIPOLOGIA_RICERCA["like"]
        if "vincoloCreatore" in parametri:
            tipologia = TIPOLOGIA_RICERCA["noLike"]

        condizioniWhere = aggiungiCondizioneWhere(condizione = condizioniWhere , nome= "QUIZ.CREATORE", valore=parametri["creatore"] , tipologia=tipologia)
    
    # ? DATA INIZIO
    if "dataInizio" in parametri:
        if "radio_quale_dataInizio" in parametri:
            tipologia = parametri["radio_quale_dataInizio"]
            condizioniWhere = aggiungiCondizioneWhere(condizione = condizioniWhere , nome= "QUIZ.DATA_INIZIO", valore=parametri["dataInizio"] , tipologia=tipologia)
    
    # ? DATA FINE
    if "dataFine" in parametri:
        if "radio_quale_dataFine" in parametri:
            tipologia = parametri["radio_quale_dataFine"]
            condizioniWhere = aggiungiCondizioneWhere(condizione = condizioniWhere , nome= "QUIZ.DATA_FINE", valore=parametri["dataFine"] , tipologia=tipologia)

    # ? NUMERO DOMANDE
    if "nDomande" in parametri:
        if "radio_quale_nDomande" in parametri:
            tipologia = parametri["radio_quale_nDomande"]

            condizioniHaving = aggiungiCondizioneHaving(condizione = condizioniWhere , nome= "nDomande", valore=parametri["nDomande"] , tipologia=tipologia)

    # ? NUMERO PARTECIPAZIONI
    if "nPartecipazioni" in parametri:
        if "radio_quale_nPartecipazioni" in parametri:
            tipologia = parametri["radio_quale_nPartecipazioni"]

            condizioniHaving = aggiungiCondizioneHaving(condizione = condizioniWhere , nome= "nPartecipazioni", valore=parametri["nPartecipazioni"] , tipologia=tipologia)

    query = QUERY_QUIZ  + condizioniWhere + GROUP_BY + condizioniHaving + ORDER_BY
    
    risultati = eseguiQuery(query)

    return risultati


def getUtente(parametri):
    
    QUERY = "SELECT UTENTE.NOME_UTENTE AS nomeUtente , UTENTE.NOME AS nome , UTENTE.COGNOME AS cognome , UTENTE.EMAIL AS email , COUNT(DISTINCT QUIZ.CODICE) as nQcreati , COUNT(DISTINCT PARTECIPAZIONE.QUIZ) as nQgiocati FROM UTENTE LEFT JOIN QUIZ ON UTENTE.NOME_UTENTE = QUIZ.CREATORE LEFT JOIN PARTECIPAZIONE ON UTENTE.NOME_UTENTE = PARTECIPAZIONE.UTENTE"

    GROUP_BY = " GROUP BY UTENTE.NOME_UTENTE "

    ORDER_BY = " ORDER BY UTENTE.NOME_UTENTE ASC"

    condizioniWhere = ""
    condizioniHaving = ""

    # ? NOME UTENTE
    if "nomeUtente" in parametri:
        tipologia = TIPOLOGIA_RICERCA["like"]
        if "vincoloNomeUtente" in parametri:
            tipologia = TIPOLOGIA_RICERCA["noLike"]

        condizioniWhere = aggiungiCondizioneWhere(condizione = condizioniWhere , nome= "UTENTE.NOME_UTENTE", valore=parametri["nomeUtente"] , tipologia=tipologia)
    
    # ? NOME
    if "nome" in parametri:
        tipologia = TIPOLOGIA_RICERCA["like"]
        if "vincoloNome" in parametri:
            tipologia = TIPOLOGIA_RICERCA["noLike"]

        condizioniWhere = aggiungiCondizioneWhere(condizione = condizioniWhere , nome= "UTENTE.NOME", valore=parametri["nome"] , tipologia=tipologia)
    
    # ? COGNOME
    if "cognome" in parametri:
        tipologia = TIPOLOGIA_RICERCA["like"]
        if "vincoloCognome" in parametri:
            tipologia = TIPOLOGIA_RICERCA["noLike"]

        condizioniWhere = aggiungiCondizioneWhere(condizione = condizioniWhere , nome= "UTENTE.COGNOME", valore=parametri["cognome"] , tipologia=tipologia)

    # ? EMAIL
    if "email" in parametri:
        tipologia = TIPOLOGIA_RICERCA["like"]
        if "vincoloEmail" in parametri:
            tipologia = TIPOLOGIA_RICERCA["noLike"]

        condizioniWhere = aggiungiCondizioneWhere(condizione = condizioniWhere , nome= "UTENTE.EMAIL", valore=parametri["email"] , tipologia=tipologia)
        
    # ? NUMERO QUIZ CREATI
    if "nQcreati" in parametri:
        if "radio_quale_nQcreati" in parametri:
            tipologia = parametri["radio_quale_nQcreati"]

            condizioniHaving = aggiungiCondizioneHaving(condizione = condizioniWhere , nome= "nQcreati", valore=parametri["nQcreati"] , tipologia=tipologia)

    # ? NUMERO QUIZ GIOCATI
    if "nQgiocati" in parametri:
        if "radio_nQgiocati" in parametri:
            tipologia = parametri["radio_nQgiocati"]

            condizioniHaving = aggiungiCondizioneHaving(condizione = condizioniWhere , nome= "nQgiocati", valore=parametri["nQgiocati"] , tipologia=tipologia)

    query = QUERY  + condizioniWhere + GROUP_BY + condizioniHaving + ORDER_BY
    
    # print(query)
    risultati = eseguiQuery(query)

    # print(risultati)

    return risultati

def getPartecipazione(parametri):
    
    QUERY = " SELECT PARTECIPAZIONE.CODICE AS codice , PARTECIPAZIONE.UTENTE AS nomeUtente , QUIZ.TITOLO AS quiz, QUIZ.CODICE AS codiceQuiz, PARTECIPAZIONE.DATA AS data, COUNT(RISPOSTA_UTENTE_QUIZ.RISPOSTA) AS nRisposte FROM (PARTECIPAZIONE JOIN RISPOSTA_UTENTE_QUIZ ON PARTECIPAZIONE.CODICE = RISPOSTA_UTENTE_QUIZ.PARTECIPAZIONE) JOIN QUIZ ON PARTECIPAZIONE.QUIZ = QUIZ.CODICE "

    GROUP_BY = " GROUP BY PARTECIPAZIONE.CODICE "

    ORDER_BY = " ORDER BY PARTECIPAZIONE.UTENTE ASC"

    if "data" in parametri:
        parametri["data"] = funzionalita.DataFormatoDataBase(parametri["data"])

    condizioniWhere = ""
    condizioniHaving = ""

    # ? CODICE QUIZ
    if "codiceQuiz" in parametri:
        tipologia = TIPOLOGIA_RICERCA["noLike"]
        condizioniWhere = aggiungiCondizioneWhere(condizione = condizioniWhere , nome= "QUIZ.CODICE", valore=parametri["codiceQuiz"] , tipologia=tipologia)

    # ? CODICE
    if "codice" in parametri:
        condizioniWhere = aggiungiCondizioneWhere(condizione = condizioniWhere , nome= "PARTECIPAZIONE.CODICE", valore=parametri["codice"] , tipologia=TIPOLOGIA_RICERCA["noLike"])
    
    # ? TITOLO
    if "quiz" in parametri:
        tipologia = TIPOLOGIA_RICERCA["like"]
        # Se c'è il vincolo sui parametri
        if "vincoloQuiz" in parametri:
            tipologia = TIPOLOGIA_RICERCA["noLike"]

        condizioniWhere = aggiungiCondizioneWhere(condizione = condizioniWhere , nome= "QUIZ.TITOLO", valore=parametri["quiz"] , tipologia=tipologia)

    # ? NOME UTENTE
    if "nomeUtente" in parametri:
        tipologia = TIPOLOGIA_RICERCA["like"]
        # Se c'è il vincolo sui parametri
        if "vincoloNomeUtente" in parametri:
            tipologia = TIPOLOGIA_RICERCA["noLike"]

        condizioniWhere = aggiungiCondizioneWhere(condizione = condizioniWhere , nome= "PARTECIPAZIONE.UTENTE", valore=parametri["nomeUtente"] , tipologia=tipologia)

    # ? DATA
    if "data" in parametri:
        if "radio_quale_data" in parametri:
            tipologia = parametri["radio_quale_data"]
            condizioniWhere = aggiungiCondizioneWhere(condizione = condizioniWhere , nome= "PARTECIPAZIONE.DATA", valore=parametri["data"] , tipologia=tipologia)

    # ? NUMERO RISPOSTE
    if "nRisposte" in parametri:
        if "radio_nRisposte" in parametri:
            tipologia = parametri["radio_nRisposte"]

            condizioniHaving = aggiungiCondizioneHaving(condizione = condizioniWhere , nome= "nRisposte", valore=parametri["nRisposte"] , tipologia=tipologia)

    query = QUERY  + condizioniWhere + GROUP_BY + condizioniHaving + ORDER_BY
    
    risultati = eseguiQuery(query)

    return risultati


def getDomandeQuiz(codice):

    '''
    Funzione che esegue una query per prelevare tutte le domande dato un codice

    Args:
        - codice (string): codice del quiz

    Returns:
        array di dizionari con chiavi:
        - numero
        - testo
    '''

    query = "SELECT NUMERO as numero, TESTO as testo FROM DOMANDA WHERE QUIZ = {} ORDER BY NUMERO ASC".format(codice)

    print(query)

    risultati = eseguiQuery(query)

    return risultati

def getRisposteDomandaQuiz(codiceQuiz , numeroDomanda):
    '''
    Funzione che preleva tutte le risposte per una specifica domanda di un quiz

    args:
    -codiceQuiz(string, int)
    -numeroDomanda(string, int)

    Returns:
        array di dizionari contententi le risposte:
        - numero
        - testo
        - tipo
        - punteggio 
    '''
    query = "SELECT NUMERO AS numero ,TESTO AS testo, TIPO AS tipo , PUNTEGGIO AS punteggio FROM RISPOSTA WHERE QUIZ = {} AND DOMANDA = {} ORDER BY NUMERO ASC".format(codiceQuiz , numeroDomanda);

    risultati = eseguiQuery(query)

    print(query)

    return risultati
