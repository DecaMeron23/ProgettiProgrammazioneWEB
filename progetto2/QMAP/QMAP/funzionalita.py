'''
Questo modulo da supporto per piccole funzionalita che possono servire alle diverse pagine o server
'''

from datetime import datetime

# Definizioen delle costanti
FORMATO_DATA_VIEW = "%d/%m/%Y"
FORMATO_DATA_DATABASE = "%Y-%m-%d"


def DataFormatoView(data):
    '''
    Funzione che converte da DB a formato VIEW
    '''
    return ConvertiFormatoDataDaA(data , FORMATO_DATA_DATABASE , FORMATO_DATA_VIEW)

def DataFormatoDataBase(data):
    '''
    Funzione che converte da formato VIEW a formato DB
    '''
    return ConvertiFormatoDataDaA(data , FORMATO_DATA_VIEW , FORMATO_DATA_DATABASE)

def ConvertiFormatoDataDaA(data , formatoIn , formatoOut):
    '''
    Funzione che converte una data da un fromato detto "formatoIn" in un formato detto "formatoOut"
    '''
    data = datetime.strptime(data, formatoIn)
    return data.strftime(formatoOut)

def DataToString(data):
    '''
    Questa funzione serviva per trasformare la data in stringa.
    dopo il cambio del server non è stato più necessario effettuare questo scambio... la funzione non serve più a nulla
    '''
    return data