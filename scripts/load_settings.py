import json


def load_settings() -> dict:
    """ Загрузка настроек из файла """
    
    with open(file='settings.json', mode='r', encoding='utf-8') as file:
        data = json.load(file)
        
    return data