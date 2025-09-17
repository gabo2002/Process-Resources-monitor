
# ScriptMonitoringEat

Monitoraggio di CPU e RAM con alert su Slack e invio file di log

## Descrizione

Questo progetto permette di monitorare l'utilizzo di CPU e RAM sia a livello totale che per specifici processi su una macchina. I dati vengono salvati su database SQLite e, al superamento di soglie configurabili, vengono inviati alert su Slack tramite webhook.

**Novità:** Ora è possibile anche inviare file di log direttamente su Slack, oltre ai classici messaggi di alert. Questa funzione consente di allegare file di log utili per il debug o l’analisi direttamente nel canale Slack configurato.

## Struttura del progetto

- `main.py`: entrypoint principale, gestisce il ciclo di monitoraggio e invio alert
- `monitor/`: contiene i moduli per il monitoraggio di CPU e RAM
	- `cpu_monitor.py`: logga l'utilizzo CPU totale e per processo
	- `ram_monitor.py`: logga l'utilizzo RAM totale e per processo
- `alert/`: contiene il sistema di alert
	- `slack_alert.py`: invia messaggi di alert su Slack
- `sql_lite_manager.py`: gestore per database SQLite
- `requirements.txt`: dipendenze Python

## Requisiti

- Python 3.8+
- venv (opzionale ma consigliato)

## Installazione

1. Clona la repository
2. Crea e attiva un ambiente virtuale:
	 ```bash
	 python3 -m venv venv
	 source venv/bin/activate
	 ```
3. Installa le dipendenze:
	 ```bash
	 pip install -r requirements.txt
	 ```


## Configurazione

Configura le variabili d'ambiente in un file `.env` nella root del progetto:

```env
SLACK_WEBHOOK_URL="<webhook_slack>"
CPU_DB="cpu_stats.db"
RAM_DB="ram_stats.db"
POLL_INTERVAL=60
PROCESSES_TO_MONITOR="Chrome,Safari"
IDENTIFIER="NomeServer"
RAM_TOTAL_THRESHOLD=8000
CPU_TOTAL_THRESHOLD=90
RAM_THRESHOLDS='{"Chrome": 500, "Safari": 300}'
CPU_THRESHOLDS='{"Chrome": 30, "Safari": 20}'
ENV="production"
LOG_FOLDER="/percorso/alla/cartella/log"
LOG_FILE_REGEX=".*\\.log$"
```

### Invio automatico dei file di log

Per abilitare l'invio automatico dei file di log su Slack, imposta le seguenti variabili nel file `.env`:

- `LOG_FOLDER`: percorso della cartella dove si trovano i file di log da monitorare (es. `/var/log/app`)
- `LOG_FILE_REGEX`: espressione regolare per selezionare i file di log da inviare (es. `.*\\.log$` per tutti i file con estensione `.log`)

Il sistema controllerà periodicamente la cartella specificata e, per ogni nuovo file che corrisponde alla regex, invierà il file (o il suo contenuto) su Slack tramite webhook. Questo permette di ricevere automaticamente log di crash, errori o altri eventi rilevanti direttamente nel canale Slack configurato.

> Puoi personalizzare la regex per inviare solo determinati file (ad esempio solo quelli che iniziano con `crash_` o che terminano con `.error.log`).

## Utilizzo

Avvia lo script principale:

```bash
python main.py
```

Il monitoraggio verrà eseguito in loop, loggando i dati e inviando alert su Slack se vengono superate le soglie.

### Invio file di log su Slack

Quando necessario, il sistema può allegare e inviare automaticamente file di log (ad esempio file di crash o log di sistema) direttamente nel canale Slack configurato. Questa funzionalità è utile per ricevere informazioni dettagliate sugli errori o sullo stato del sistema senza dover accedere manualmente al server.


## Database

I dati vengono salvati in due file SQLite:
- `cpu_stats.db`: tabella `cpu_usage` con timestamp, processo e percentuale CPU
- `ram_stats.db`: tabella `ram_usage` con timestamp, processo e RAM in MB

## Personalizzazione

- Modifica le soglie nel file `.env` per adattare il sistema alle tue esigenze
- Aggiungi/rimuovi processi da monitorare tramite la variabile `PROCESSES_TO_MONITOR`

## Dipendenze principali

- psutil: per il monitoraggio delle risorse
- python-dotenv: per la gestione delle variabili d'ambiente
- requests: per l'invio degli alert su Slack

## Autore

Gabriele Corti

## Licenza

MIT
