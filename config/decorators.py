import sys
import os

def check_data(self, func):
    def wrappers(*args, **kwargs):
        if self.conn is None or self.login is None:
            raise ValueError('Ошибка, даннные не могут быть None')
        return func(*args, **kwargs)
    return wrappers


def format_date(date: str) -> str:
    sp = []
    if date[0] == '-' or date[0] == '+':
        sp.append(date[0])
        date = date[1:]
    if date[0] == '0':
        date = date[1:]
    sp.append(date)
    return ' '.join(sp)
    


def resource_path(relative_path):
    """ Возвращает абсолютный путь к ресурсу """
    try:
        # PyInstaller создает временную директорию для ресурсов
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)