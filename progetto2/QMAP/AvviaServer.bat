@echo off

REM Verifica se Python e' installato
python --version > nul 2>&1
if errorlevel 1 (
    echo Python non e' installato.
    echo Per installare Python:
    echo 1. Vai su https://www.python.org/downloads/
    echo 2. Scarica il programma di installazione per la versione più recente.
    echo 3. Esegui il programma di installazione e segui le istruzioni.
    pause
    exit /b
) else (
    echo Python e' installato.
)

REM Verifica se Django e' installato
python -c "import django" > nul 2>&1
if errorlevel 1 (
    echo Django non e' installato. Procedo con l'installazione.
    pip install django
    if errorlevel 1 (
        echo Errore durante l'installazione di Django.
        pause
        exit /b
    ) else (
        echo Django e' stato installato con successo.
    )
) else (
    echo Django e' installato.
)

REM Verifica se requests e' installato
python -c "import requests" > nul 2>&1
if errorlevel 1 (
    echo Il modulo requests non e' installato. Procedo con l'installazione.
    pip install requests
    if errorlevel 1 (
        echo Errore durante l'installazione del modulo requests.
        pause
        exit /b
    ) else (
        echo Il modulo requests e' stato installato con successo.
    )
) else (
    echo Il modulo requests e' installato.
)


echo Avviamo il server


python manage.py runserver
