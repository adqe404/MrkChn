import sys
import os
import json

class Launguage():
    def __init__(self, config, main):
        self.config = config
        self.lang = self.config.launguage
        self.languages = self.load_json()
        self.main = main
    
    def change_lang(self):
        while True:
            lang = input('1 - Русский\n2 - English\n\nChoose the lang: ')
            match lang:
                case '1':
                    self.config.write_in_config('launguage', 'ru')
                case '2':
                    self.config.write_in_config('launguage', 'en')
                case _:
                    self.main.title('Wrong launguage!')
                    continue
            self.lang = lang
            break
            
        
    def get_resource_path(self, file):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        return os.path.join(base_path, file)
    
    def load_json(self):
        json_path = self.get_resource_path('languages.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)