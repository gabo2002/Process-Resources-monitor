from alert.slack_alert import SlackMessageAlert
from monitor.cpu_monitor import CPUMonitor
from monitor.ram_monitor import RAMMonitor
from crash_reader.log_reader import LogReader
from dotenv import load_dotenv
import os
import time

def main():
    # Configurazioni
    load_dotenv()
    SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")
    CPU_DB = os.environ.get("CPU_DB")
    RAM_DB = os.environ.get("RAM_DB")
    POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL"))
    PROCESSES_TO_MONITOR = os.environ.get("PROCESSES_TO_MONITOR", "").split(",")
    PROCESSES_TO_MONITOR = [p.strip() for p in PROCESSES_TO_MONITOR if p.strip()]
    ENV = os.environ.get("ENV", "debug")

    # Inizializza alert system
    slack_alert_ram = SlackMessageAlert(SLACK_WEBHOOK_URL, "MB", os.environ.get("IDENTIFIER"), total_threshold=os.environ.get("RAM_TOTAL_THRESHOLD", 0), processes_thresholds=os.environ.get("RAM_THRESHOLDS", {}))
    slack_alert_cpu = SlackMessageAlert(SLACK_WEBHOOK_URL, "CPU (%)", os.environ.get("IDENTIFIER"), total_threshold=os.environ.get("CPU_TOTAL_THRESHOLD", 0), processes_thresholds=os.environ.get("CPU_THRESHOLDS", {}))
    slack_alert_logs = SlackMessageAlert(SLACK_WEBHOOK_URL, "logs", os.environ.get("IDENTIFIER"))

    # Inizializza monitor 
    cpu_monitor = CPUMonitor(CPU_DB, PROCESSES_TO_MONITOR, callback=slack_alert_cpu.evaluate_and_alert, env=ENV)
    ram_monitor = RAMMonitor(RAM_DB, PROCESSES_TO_MONITOR, callback=slack_alert_ram.evaluate_and_alert, env=ENV)

    # Reader loop
    log_reader = LogReader(os.environ.get("LOG_FOLDER"), os.environ.get("LOG_FILE_REGEX"))
    finded_logs = list()

    while True:
        print("Logging CPU usage...")
        cpu_monitor.log_cpu_usage()
        print("Logging RAM usage...")
        ram_monitor.log_ram_usage()
        print("Reading logs...")
        logs = log_reader.read_logs()
        for log in logs:
            if log not in finded_logs:
                finded_logs.append(log)
                print(f"New log found: {log['file']}")
                # Send log to Slack
                slack_alert_logs.alert(f"*ALERT* - {os.environ.get('IDENTIFIER')} {time.strftime('%Y-%m-%d %H:%M:%S')}", [("FileName", log['file'])])
                slack_alert_logs.alert(f"*ALERT* - {os.environ.get('IDENTIFIER')} {time.strftime('%Y-%m-%d %H:%M:%S')}", [("Contents", log['contents'][:3000] + ("..." if len(log['contents']) > 3000 else ""))])

        print(f"Sleeping for {POLL_INTERVAL} seconds...")
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()