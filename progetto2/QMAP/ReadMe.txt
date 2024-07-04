Questo file serve da aiuto a chi vuole utilizzare il nostro sito fatto con Django.

Tutto ciò che serve è avviare il Server, per il DB non è necessario avviarlo, poiché abbiamo utilizzato lo stesso DB del primo progetto aggiungendo una piccola porzione di codice nel primo progetto che fa da "API" per il secondo!

Ci sono due metodi per avviare il server (consigliamo l'opzione 1):
1) Tramite l'eseguibile "AvviaServer.bat" che verifica la presenza dei moduli necessari per l'utilizzo dell'applicazione, e se non presenti li installa in automatico o spiega come installarli. Dopo ciò avvia il server, raggiungibile al link: "http://127.0.0.1:8000/".
Se l'applicazione si è avviata, potete evitare di continuare a leggere.

2) Se per qualche motivo non funzionasse l'eseguibile si può procedere manualmente:

Per usare l'applicazione è necessario avere queste cose prima di iniziare:

- Python: Per far funzionare il server

- Django: modulo per il server, per installare usare il comando sul prompt dei comandi: "pip install django"
	
- Requests: modulo per fare richieste a pagine esterne. per installare usare il comando sul prompt dei comandi: "pip install requests"

Dopo aver installato tutti i moduli necessari, siamo pronti a far partire il Server:
	
Aprire il prompt dei comandi, assicurarsi di essere nella directory contenente il file "manage.py" e digitare il seguente comando:
- "python manage.py runserver"

Detto ciò godetevi la nostra applicazione! essa è raggiungibile da un browser andando al link: "http://127.0.0.1:8000/" (a meno che non venga specificato diversamente dalla console, all'avvio del server)