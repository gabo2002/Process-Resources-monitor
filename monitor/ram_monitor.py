import time
import psutil
from datetime import datetime
from typing import Callable, List, Optional
from sql_lite_manager import SQLiteManager

class RAMMonitor:
    def __init__(self, db_name: str, processes: List[str], callback: Optional[Callable] = None, env: str = "debug"):
        """
        Inizializza il monitor RAM.

        :param db_name: Nome del file SQLite (es: "ram_stats.db")
        :param processes: Lista di nomi dei processi da monitorare (es: ["Eat", "Safari"])
        :param callback: Funzione di callback da eseguire dopo ogni log (es. per alert)
        """
        schema = {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "timestamp": "TEXT",
            "process": "TEXT",
            "ram_mb": "REAL"
        }

        self.db = SQLiteManager(db_name, "ram_usage", schema)
        self.processes = processes
        self.callback = callback
        self.env = env

    def _get_total_ram(self) -> float:
        """Ritorna la RAM totale utilizzata in MB."""
        mem = psutil.virtual_memory()
        return round(mem.used / (1024 * 1024), 2)

    def _get_process_ram(self, process_name: str) -> float:
        """
        Ritorna la RAM usata dal processo con nome specifico.
        Se ci sono più processi con lo stesso nome, somma la RAM.
        """
        total = 0.0
        for proc in psutil.process_iter(['name', 'memory_info']):
            try:
                if proc.info['name'] and process_name.lower() in proc.info['name'].lower():
                    total += proc.info['memory_info'].rss / (1024 * 1024)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return round(total, 2)

    def log_ram_usage(self):
        """Salva nel DB la RAM totale e quella dei processi monitorati, e chiama callback se definita."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        results = []

        # RAM totale
        total_ram = self._get_total_ram()
        self.db.create({
            "timestamp": timestamp,
            "process": "TOTAL",
            "ram_mb": total_ram
        })
        results.append(("TOTAL", total_ram))

        # RAM dei processi
        for proc in self.processes:
            ram = self._get_process_ram(proc)
            self.db.create({
                "timestamp": timestamp,
                "process": proc,
                "ram_mb": ram
            })
            results.append((proc, ram))

        # Se definita, chiama la callback
        if self.callback:
            self.callback(timestamp, results)

        if self.env == "debug":
            print(f"[{timestamp}] RAM Totale: {total_ram} MB")
            for proc, ram in results:
                if proc != "TOTAL":
                    print(f"    {proc}: {ram} MB")

    def run(self, interval: int = 60):
        """Avvia il monitoraggio ogni N secondi (default: 60)."""
        print(f"Avvio monitor RAM ogni {interval} secondi...")
        while True:
            self.log_ram_usage()
            time.sleep(interval)