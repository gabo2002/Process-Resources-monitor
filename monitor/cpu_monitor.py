import time
import psutil
from datetime import datetime
from typing import Callable, List, Optional
from sql_lite_manager import SQLiteManager


class CPUMonitor:
    def __init__(self, db_name: str, processes: List[str], callback: Optional[Callable] = None, env: str = "debug"):
        """
        Inizializza il monitor CPU.

        :param db_name: Nome del file SQLite (es: "cpu_stats.db")
        :param processes: Lista di nomi dei processi da monitorare
        :param callback: Funzione di callback da eseguire dopo ogni log (es. per alert)
        """
        schema = {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "timestamp": "TEXT",
            "process": "TEXT",
            "cpu_percent": "REAL"
        }

        self.db = SQLiteManager(db_name, "cpu_usage", schema)
        self.processes = processes
        self.callback = callback
        self.env = env

    def _get_total_cpu(self) -> float:
        """Ritorna la percentuale totale di CPU usata in questo momento."""
        return round(psutil.cpu_percent(interval=1), 2)

    def _get_process_cpu(self, process_name: str) -> float:
        """
        Ritorna la percentuale di CPU usata dal processo con nome specifico.
        Somma la CPU di tutti i processi con lo stesso nome.
        """
        total = 0.0
        for proc in psutil.process_iter(['name', 'cpu_percent']):
            try:
                if proc.info['name'] and process_name.lower() in proc.info['name'].lower():
                    # chiama cpu_percent con intervallo 0 per valori immediati
                    total += proc.cpu_percent(interval=1)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                print(f"Processo {proc} non trovato o accesso negato.")
                continue
        return round(total, 2)

    def log_cpu_usage(self):
        """Salva nel DB la CPU totale e quella dei processi monitorati, e chiama callback se definita."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        results = []

        # CPU totale
        total_cpu = self._get_total_cpu()
        self.db.create({
            "timestamp": timestamp,
            "process": "TOTAL",
            "cpu_percent": total_cpu
        })
        results.append(("TOTAL", total_cpu))

        # CPU dei processi
        for proc in self.processes:
            cpu = self._get_process_cpu(proc)
            self.db.create({
                "timestamp": timestamp,
                "process": proc,
                "cpu_percent": cpu
            })
            results.append((proc, cpu))

        # Se definita, chiama la callback
        if self.callback:
            self.callback(timestamp, results)

        if self.env == "debug":
            print(f"[{timestamp}] CPU Totale: {total_cpu}%")
            for proc, cpu in results:
                if proc != "TOTAL":
                    print(f"    {proc}: {cpu}%")

    def run(self, interval: int = 60):
        """Avvia il monitoraggio ogni N secondi (default: 60)."""
        print(f"Avvio monitor CPU ogni {interval} secondi...")
        while True:
            self.log_cpu_usage()
            time.sleep(interval)