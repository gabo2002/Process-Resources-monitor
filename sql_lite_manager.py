import sqlite3
from typing import Dict, Any, List, Tuple


class SQLiteManager:
    def __init__(self, db_name: str, table_name: str, schema: Dict[str, str]):
        """
        Inizializza il gestore SQLite.

        :param db_name: Nome del file database SQLite (es: 'database.db')
        :param table_name: Nome della tabella da gestire
        :param schema: Dizionario colonna -> tipo (es: {"id": "INTEGER PRIMARY KEY AUTOINCREMENT", "name": "TEXT"})
        """
        self.db_name = db_name
        self.table_name = table_name
        self.schema = schema

        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.db_name)

    def _create_table(self):
        columns = ", ".join([f"{col} {ctype}" for col, ctype in self.schema.items()])
        query = f"CREATE TABLE IF NOT EXISTS {self.table_name} ({columns});"
        with self._connect() as conn:
            conn.execute(query)
            conn.commit()

    def create(self, data: Dict[str, Any]) -> int:
        """
        Inserisce un nuovo record nella tabella.
        :param data: Dizionario colonna -> valore
        :return: ID della riga inserita
        """
        cols = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        query = f"INSERT INTO {self.table_name} ({cols}) VALUES ({placeholders})"
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(query, tuple(data.values()))
            conn.commit()
            return cur.lastrowid

    def read(self, conditions: Dict[str, Any] = None) -> List[Tuple]:
        """
        Legge i record dalla tabella.
        :param conditions: Dizionario colonna -> valore per filtrare i risultati
        :return: Lista di tuple con i record trovati
        """
        query = f"SELECT * FROM {self.table_name}"
        params = []
        if conditions:
            cond_str = " AND ".join([f"{col} = ?" for col in conditions.keys()])
            query += f" WHERE {cond_str}"
            params = list(conditions.values())

        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(query, params)
            return cur.fetchall()

    def update(self, data: Dict[str, Any], conditions: Dict[str, Any]) -> int:
        """
        Aggiorna i record della tabella.
        :param data: Dizionario colonna -> nuovo valore
        :param conditions: Dizionario colonna -> valore da rispettare
        :return: Numero di righe aggiornate
        """
        set_str = ", ".join([f"{col} = ?" for col in data.keys()])
        cond_str = " AND ".join([f"{col} = ?" for col in conditions.keys()])
        query = f"UPDATE {self.table_name} SET {set_str} WHERE {cond_str}"

        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(query, list(data.values()) + list(conditions.values()))
            conn.commit()
            return cur.rowcount

    def delete(self, conditions: Dict[str, Any]) -> int:
        """
        Elimina i record dalla tabella.
        :param conditions: Dizionario colonna -> valore da rispettare
        :return: Numero di righe eliminate
        """
        cond_str = " AND ".join([f"{col} = ?" for col in conditions.keys()])
        query = f"DELETE FROM {self.table_name} WHERE {cond_str}"

        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(query, list(conditions.values()))
            conn.commit()
            return cur.rowcount