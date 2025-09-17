# ScriptMonitoringEat

Monitoraggio di CPU e RAM con alert su Slack

## Descrizione
Questo progetto permette di monitorare l'utilizzo di CPU e RAM sia a livello totale che per specifici processi su una macchina. I dati vengono salvati su database SQLite e, al superamento di soglie configurabili, vengono inviati alert su Slack tramite webhook.

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
```

## Utilizzo

Avvia lo script principale:

```bash
python main.py
```

Il monitoraggio verrà eseguito in loop, loggando i dati e inviando alert su Slack se vengono superate le soglie.

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
