import configparser
import os
import platform
import re
import random
from .Language import Language
from rich.console import Console
from rich.table import Table
from rich.box import ROUNDED
console = Console(highlight=False)
rinput = console.input
rprint = console.print

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
                elif re.match(r'^([1-9][0-9]*)-([1-9][0-9]*)$', sue):
                    first, second = map(int, sue.split('-'))
                    if first < second: 
                        return random.randint(first, second)
                return False      
            case 'txt_filename':
                if self.is_boolean(sue) or self.is_none(sue):
                    self.write_in_config(key, 'text.txt')
                    return 'text.txt'
                return sue if sue[-4:] == '.txt' else sue + '.txt'
            case 'gen_num':
                if sue.isdigit():
                    if int(sue) > 0:
                        return int(sue)
                elif re.match(r'^([1-9][0-9]*)-([1-9][0-9]*)$', sue):
                    first, second = map(int, sue.split('-'))
                    if first < second:
                        return random.randint(first, second)
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
            self.gen_num = self.parse_data('Settings', 'gen_num')
            self.language_data = self.parse_data('Settings', 'language')
            self.kitties_title = self.parse_data('Settings', 'kitties_title')
        except Exception as e:
            self.create_config()
            self.main.title(self.language.string[self.language.get_lang()]["something_went_wrong"].format(e=e))

    def user_open_file_config(self):
        if platform.system() == "Windows":
            os.startfile('config.ini')
        elif platform.system() == "Darwin":
            os.system(f'open "config.ini"')
        else:
            os.system(f'xdg-open "config.ini"')
            
    def change_values_in_config(self):
        while True:
            try:
                rprint(self.language.string[self.language.get_lang()]["current_config_values"].format(config = open('config.ini', 'r', encoding='utf-8').read()))
                choices = ['seed', 'text_len', 'txt_filename', 'gen_num', 'language', 'kitties_title']
                table = Table(box = ROUNDED)
                table.add_column("№", style='yellow1')
                table.add_column(self.language.string[self.language.get_lang()]["keys"])
                for i, choice in enumerate(choices, start=1):
                    table.add_row(str(i), choice)
                rprint(table)
                choice = self.main.input_with_check(self.language.string[self.language.get_lang()]["your_choice_config"])
                if choice.lower() in ('exit', '0'): break
                if int(choice) in range(1, 7):
                    index = int(choice) - 1
                    value = self.main.input_with_check(self.language.string[self.language.get_lang()]["enter_new_config_value"].format(config_key = choices[index]))
                    self.write_in_config(choices[index], value)
                    rprint(self.language.string[self.language.get_lang()]["config_value_successfully_updated"].format(config_key = choices[index], config_value = value))
                    self.main.input_with_check(self.language.string[self.language.get_lang()]["press_enter"])
                self.main.title()
            except:
                self.main.title(self.language.string[self.language.get_lang()]["wrong_input"])
                    