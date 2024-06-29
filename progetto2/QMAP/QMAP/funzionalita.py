# Per midificare le date
from datetime import datetime


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
    data = datetime.strptime(data, formatoIn)
    return data.strftime(formatoOut)

# Converte in stringa una data lo mette nel formato view
def DataToString(data):
    return data