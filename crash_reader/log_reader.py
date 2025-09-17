import re
from pathlib import Path

class LogReader:
    def __init__(self, folder_path, file_pattern):
        self.folder = Path(folder_path)
        self.regex = re.compile(file_pattern)

    def read_logs(self):
        logs = []
        for file in self.folder.iterdir():
            temp = dict()
            temp['file'] = str(file)
            temp['contents'] = ""
            if file.is_file() and self.regex.match(file.name):
                with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                    temp['contents'] = f.read()
                logs.append(temp)

        return logs
                