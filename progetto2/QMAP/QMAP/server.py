# Il DB è online hostato da https://aiven.io/ 


from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

import pymysql
import json


import funzionalita

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

    try:
        risultati = cursore.fetchall()
    except:
        return ["ok"]
    finally:
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
    Funzione che esegue una query per prelevare tutte le domande dato il codice del quiz, i risulati saranno in ordine crescente per numero di domanda 
    Args:
        - codice (string,int): codice del quiz

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

def aggiungiPartecipazione(nomeUtente , partecipazione , codiceQuiz, dataPartecipazione):
    '''
    Funzione che aggiunge la partecipazione dell'utente 
    
    returns:
    - int: 0 se è andata a buon fine, 1 se l'untente non esiste, 2 altro  
    '''

    if not esisteUtente(nomeUtente):
        return 1

    query = "INSERT INTO `PARTECIPAZIONE`(`CODICE` , `UTENTE`, `QUIZ`, `DATA`) VALUES ('{}' , '{}','{}','{}')".format(partecipazione , nomeUtente , codiceQuiz , dataPartecipazione)

    eseguiQuery(query)

    return 0

def aggiungiRispostaPartecipazione(partecipazione , id_quiz , domanda , risposta):
    '''
    Funzione che aggiunge la risposta ad una partecipazione

    Returns (int):

    - 0: tutto ok
    - 1: partecipazione non è nel DB
    - 2: id_quiz non è nel DB

    '''

    if not esistePartecipazione(partecipazione):
        return 1
    if not esisteQuiz(id_quiz):
        return 2

    query = "INSERT INTO `RISPOSTA_UTENTE_QUIZ`(`PARTECIPAZIONE`, `QUIZ`, `DOMANDA`, `RISPOSTA`) VALUES ('{}','{}','{}','{}}')".format(partecipazione , id_quiz , domanda , risposta)

    risultato = eseguiQuery(query)
    print("aggiunta partecipazione codice {}".format(risultato))
    return 0

def getUtenti():
    '''
    Funzione che preleva tutti gli utenti dal DB

    Returns:
    - Array di dizionari
    '''

    query = "SELECT * FROM UTENTE"
    
    risultato = eseguiQuery(query)
    
    return risultato



def funzionalitaJS(request):
    '''
    Funzione che permette di fare chiamate ajax

    tipo di funzioni:
    - getRisposteCorrette(codiceQuiz) 
    - aggiungiPartecipazione(nomeUtente , codiceQuiz , dataPartecipazione)
    - inserisci_risposta_utente( partecipazione , id_quiz , domanda , risposta)

    
    Returns(Se non ci sono stati errori):
    - Dizionario contentente i valori richiesti, se non si è richiesto nulla ritorna un dizionario con chiave "esito" e valore "ok"

    Se avviene un errore ritorna un dizionario con chiavi "errore" (descrizione dell'errore) e "codiceErrore", codici errore:
    - Manca nome funzione: 0
    - Manca paramentro funzione: 1
    - Errori DB : 2


    '''
    # ! Creiamo le funzioni che ci servono
    def prarmetroMancante(parametro):
        errore = {"errore" : "Manca il parametro '{}'.".format(parametro) , "codiceErrore" : 1}
        return json.dumps(errore)

    def inviaOK(res):
        risposta = {"esito": "ok"}
        res.write(json.dumps(risposta))
        return res


    res = HttpResponse(content_type="application/json")

    parametri = request.GET

    if not "funzione" in parametri:
        errore = {"errore": "Nome della funzione non inserito" , "codiceErrore" : 0};
        res.write(json.dumps(errore))
        return res  

    #  Estraiamo tutte le risposte corrette per domanda
    if parametri["funzione"] == "getRisposteCorrette":
        if not "codiceQuiz" in parametri:
            res.write(prarmetroMancante("codiceQuiz"))
            return res  
        domandeDB = getDomandeQuiz(codice=parametri["codiceQuiz"])
        risposteCorrette = []
        for domanda in domandeDB:
            o = {}
            o["numeroDomanda"] = domanda["numero"]
            risposteDB = getRisposteDomandaQuiz(codiceQuiz=parametri["codiceQuiz"] , numeroDomanda=domanda["numero"])
            for risposta in risposteDB:
                if risposta["tipo"] == 1:
                    o["numero"] = risposta["numero"]

            risposteCorrette.append(o)

        rispostaGET = {"risposteCorrette": risposteCorrette} 
        rispostaJSON = json.dumps(rispostaGET)
        res.write(rispostaJSON)
        return res
    
    # ! Aggiungi partecipazione
    elif parametri["funzione"] == "aggiungiPartecipazione":
        # ? Verifica errori
        if not "nomeUtente" in parametri:
            res.write(prarmetroMancante("nomeUtente"))
            return res
        if not "codiceQuiz" in parametri:
            res.write(prarmetroMancante("codiceQuiz"))
            return res
        if not "dataPartecipazione" in parametri:
            res.write(prarmetroMancante("dataPartecipazione"))
            return res 
        if not "partecipazione" in parametri:
            res.write(prarmetroMancante("partecipazione"))
            return res

        nomeUtente = parametri["nomeUtente"]
        codiceQuiz = parametri["codiceQuiz"]
        partecipazione = parametri["partecipazione"]
        dataPartecipazione = parametri["dataPartecipazione"];
        esito = aggiungiPartecipazione(nomeUtente , partecipazione , codiceQuiz, dataPartecipazione)
        if esito == 1:
            errore = {"errore" : "L'utente non esiste nel DB", "codiceErrore" : 2 }
            res.write(json.dumps(errore))
            return res
        
        return inviaOK(res)
        

    elif parametri["funzione"]== "inserisci_risposta_utente":
        #? verifica errori 

        if not "partecipazione" in parametri:
            res.write(prarmetroMancante("partecipazione"))
            return res
        if not "id_quiz" in parametri:
            res.write(prarmetroMancante("id_quiz"))
            return res
        if not "domanda" in parametri:
            res.write(prarmetroMancante("domanda"))
            return res
        if not "risposta" in parametri:
            res.write(prarmetroMancante("risposta"))
            return res

        partecipazione = parametri["partecipazione"]
        id_quiz = parametri["id_quiz"]
        domanda = parametri["domanda"]
        risposta = parametri["risposta"]

        esito = aggiungiRispostaPartecipazione(partecipazione , id_quiz , domanda , risposta)

        #? Non esiste la partecipazione
        if esito == 1:
            errore = {"errore" : "La partecipazione '{}' non esiste nel DB".format(partecipazione), "codiceErrore" : 2 }
            res.write(json.dumps(errore))
            return res
        if esito == 2:
            errore = {"errore" : "Il quiz '{}' non esiste nel DB".format(partecipazione), "codiceErrore" : 2 }
            res.write(json.dumps(errore))
            return res

        return inviaOK(res)
    
    elif "get_max_partecipazione" == parametri["funzione"]:
        query = "SELECT MAX(CODICE) as codice FROM PARTECIPAZIONE"
        risultato = eseguiQuery(query)
        print(risultato)
        risposta = {"codice_partecipazione": risultato[0]["codice"]}
        res.write(json.dumps(risposta))
        return res

def esisteUtente(nomeUtente):
    '''
    Funzione che verifica se un utente esiste nel DB

    Args:
    - nomeUtente (string) il nome dell'utente

    Returns:
    - True se l'utente è presente nel DB, altrimenti False  
    '''
    query = "SELECT * FROM UTENTE WHERE NOME_UTENTE = '{}'".format(nomeUtente)

    ris = eseguiQuery(query)
    
    return len(ris) > 0

def esistePartecipazione(partecipazione):
    '''
    Funzione che verifica se la partecipazione è presente nel DB

    Args:
    - partecipazione (int)

    Returns:
    - True se si sennò false 
    '''

    query = "SELECT * FROM PARTECIPAZIONE WHERE CODICE = {}".format(partecipazione)

    ris = eseguiQuery(query)

    return len(ris) > 0


def esisteQuiz(id_quiz):
    '''
    Funzione che verifica se il quiz è presente nel DB

    Args:
    - id_quiz (int)

    Returns:
    - True se si sennò false 
    '''

    query = "SELECT * FROM QUIZ WHERE CODICE = {}".format(id_quiz)

    ris = eseguiQuery(query)

    return len(ris) > 0


def eliminaQuiz(codice = 0):
    query_elimina_risposte = "DELETE FROM RISPOSTA WHERE QUIZ = {}".format(codice);
    query_elimina_risposte_utenti = "DELETE FROM RISPOSTA_UTENTE_QUIZ WHERE QUIZ = {}".format(codice);
    query_elimina_partecipazioni = "DELETE FROM PARTECIPAZIONE WHERE QUIZ = {}".format(codice);
    query_elimina_domanda = "DELETE FROM DOMANDA WHERE QUIZ = {}".format(codice);
    query_elimina_quiz = "DELETE FROM QUIZ WHERE CODICE = {}".format(codice);

    