import configparser
import os
from .Language import Language

class ConfigParser():
    def __init__(self, main):
        self.check_config()
        self.main = main
        self.language = Language(self, self.main)

    def create_config(self):
        with open('config.ini', 'w', encoding='utf-8') as file:
            file.write("""[Settings]
seed = <START>
text_len = False
txt_filename = kitten_anekdots.txt
json_dump = False
json_filename = dumped_markov.json
gen_num = 1
language = None
kitties_title = True""")
            
    def check_config(self):
        if not os.path.exists('config.ini'):
            self.create_config()
        self.init_config()
                
    def write_in_config(self, key, value):
        self.config.set('Settings', key, value)
        with open('config.ini', 'w', encoding='utf-8') as file:
            self.config.write(file)
            
    def is_boolean(self, sue):
        if sue.lower() in ('true', 'yes', 'on', 'no', 'false', 'off'):
            return True
        return False
    
    def is_none(self, sue):
        if sue.lower() == 'none' or not(sue):
            return True
        return False

    def parse_data(self, settings, key):
        sue = self.config.get(settings, key)
        match key:
            case 'seed':
                if self.is_boolean(sue) or self.is_none(sue):
                    self.write_in_config(key, '<START>')
                    return '<START>'
                return sue
            case 'text_len':
                if sue.isdigit():
                    if int(sue) > 0:
                        return int(sue)
                return False      
            case 'txt_filename':
                if self.is_boolean(sue) or self.is_none(sue):
                    self.write_in_config(key, 'text.txt')
                    return 'text.txt'
                return sue if sue[-4:] == '.txt' else sue + '.txt'
            case 'json_dump':
                if self.is_boolean(sue):
                    return self.config.getboolean(settings, key)
                else:
                    self.write_in_config(key, 'False')
                    return False
            case 'json_filename':
                if self.is_boolean(sue) or self.is_none(sue):
                    self.write_in_config(key, 'probabilities.json')
                    return 'probabilities.json'
                return sue if sue[-5:] != '.json' else sue[:-5]
            case 'gen_num':
                if sue.isdigit():
                    if int(sue) > 0:
                        return int(sue)
                self.write_in_config(key, '1')
                return 1
            case 'language':
                if sue.lower() not in ('en', 'ru'):
                    self.write_in_config(key, 'None')
                    return 'None'
                return sue
            case 'kitties_title':
                if self.is_boolean(sue):
                    return self.config.getboolean(settings, key)
                else:
                    self.write_in_config(key, 'False')
                    return False
    
    def init_config(self):
        try:
            self.config = configparser.ConfigParser()
            self.config.read('config.ini', encoding='utf-8')
            self.seed = self.parse_data('Settings', 'seed')
            self.text_len = self.parse_data('Settings', 'text_len')
            self.txt_filename = self.parse_data('Settings', 'txt_filename')
            self.json_dump = self.parse_data('Settings', 'json_dump')
            self.json_filename = self.parse_data('Settings', 'json_filename')
            self.gen_num = self.parse_data('Settings', 'gen_num')
            self.language = self.parse_data('Settings', 'language')
            self.kitties_title = self.parse_data('Settings', 'kitties_title')
        except Exception as e:
            self.create_config()
            self.main.title(self.language.string[self.language.get_lang()]["something_went_wrong"].format(e=e))