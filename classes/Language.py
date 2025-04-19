import sys
import os
import json
from rich.console import Console
console = Console(highlight=False)
rinput = console.input
rprint = console.print

class Language():
    def __init__(self, config, main):
        self.config = config
        self.lang = self.config.language
        self.string = self.load_json()
        self.main = main
        
    def get_lang(self):
        return self.lang if self.lang in ('ru', 'en') else 'en'
    
    def change_lang(self):
        while True:
            lang = self.main.input_with_check(self.string[self.get_lang()]["lang_choice"])
            match lang:
                case '1':
                    self.config.write_in_config('language', 'ru')
                    self.lang = 'ru'
                case '2':
                    self.config.write_in_config('language', 'en')
                    self.lang = 'en'
                case _:
                    self.main.title(self.string[self.get_lang()]["wrong_input"])
                    continue
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