import requests
from typing import List
    
class SlackMessageAlert:
    def __init__(self, slack_webhook_url: str, unit: str, identifier: str, total_threshold: float = 8000, processes_thresholds: dict = None):
        """
        Inizializza l'alert system.
        :param slack_webhook_url: URL webhook Slack per inviare messaggi
        :param total_threshold: Soglia totale oltre la quale mandare alert
        """
        self.slack_webhook_url = slack_webhook_url
        self.total_threshold = float(total_threshold)
        # str to dict: processes_thresholds is a string like '{"Eat": 500, "Safari": 300}'
        # convert to dict
        if isinstance(processes_thresholds, str):
            import ast
            try:
                self.processes_thresholds = {k: float(v) for k, v in ast.literal_eval(processes_thresholds).items()}
            except Exception as e:
                print(f"Errore parsing processes_thresholds: {e}")
                self.processes_thresholds = {}
        elif isinstance(processes_thresholds, dict):
            self.processes_thresholds = {k: float(v) for k, v in processes_thresholds.items()}
        else:
            self.processes_thresholds = {}
        self.processes = list(self.processes_thresholds.keys())
        self.unit = unit
        self.identifier = identifier

    def alert(self, timestamp: str, message: str):
        """Manda un messaggio di alert a Slack."""
        self._send_slack_message(f"{timestamp} - {message}")

    def evaluate_and_alert(self, timestamp: str, results: List[tuple]):
        """
        Valuta i risultati e manda messaggi di allerta se necessario.
        :param timestamp: Timestamp della misura
        :param results: Lista di tuple (process, value)
        """
        alerts = []

        for process, value in results:
            if process == "TOTAL" and value > self.total_threshold:
                alerts.append(f"*ALERT* - {self.identifier} {process} usage is {value} {self.unit} (threshold: {self.total_threshold} {self.unit}) at {timestamp}")
            elif process in self.processes_thresholds and value > self.processes_thresholds[process]:
                threshold = self.processes_thresholds[process]
                alerts.append(f"*ALERT* - {self.identifier} {process} usage is {value} {self.unit} (threshold: {threshold} {self.unit}) at {timestamp}")
        for alert in alerts:
            self._send_slack_message(alert)
        
    def _send_slack_message(self, message: str):
        """Invia un messaggio a Slack tramite webhook."""
        try:
            print(f"Invio messaggio Slack: {message}")
            response = requests.post(self.slack_webhook_url, json={"text": message})
            if response.status_code != 200:
                print(f"Errore invio Slack: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Errore durante l'invio a Slack: {e}")