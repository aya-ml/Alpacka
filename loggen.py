import os
from datetime import datetime

class LogsCreator:
    def __init__(self, filename='logs.log'):
        self.filename = filename
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Создает файл логов, если он не существует"""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as f:
                f.write(f"[{self._get_current_time()}] Session started\n")
        else:
            self.clear_logs()
    
    def _get_current_time(self):
        """Возвращает текущее время в формате для логов"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def add_log(self, message):
        """Добавляет запись в лог-файл"""
        with open(self.filename, 'a', encoding='utf-8') as f:
            f.write(f"[{self._get_current_time()}] {message}\n")
    
    def read_logs(self):
        """Считывает и возвращает все записи из лог-файла"""
        with open(self.filename, 'r', encoding='utf-8') as f:
            return f.read()
    
    def clear_logs(self):
        """Очищает лог-файл"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(f"[{self._get_current_time()}] Session started\n")