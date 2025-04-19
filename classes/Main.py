from .ConfigParser import ConfigParser
from .Language import Language
from .TextProcessor import TextProcessor
from .MarkovChain import MarkovChain
import os
import random

class Main():
    def __init__(self):
        self.config = ConfigParser(self)
        self.language = self.config.language
        self.regele = '================================'
        
    def input_with_check(self, text):
        input_text = input(text)
        self.config.check_config()
        return input_text

    def menu(self):
        self.config.check_config()
        if self.config.language not in ('ru', 'en') or not self.config.language:
            self.language.change_lang()
            self.input_with_check(self.language.string[self.language.get_lang()]["press_enter"])
            self.title()
        menu_choice = self.input_with_check(self.language.string[self.language.get_lang()]["menu_input"])
        return menu_choice

    def main(self, some_notif = None):
        self.title(some_notif)
        while True:
            try:
                menu_choice = self.menu()
                match menu_choice:
                    case '1':
                        self.create_model()
                        self.title()
                        for i in range(self.config.gen_num):
                            print(f'{i + 1}.', self.markov_chain.generate_text(self.text.probabilities))
                        self.input_with_check(self.language.string[self.language.get_lang()]["press_enter"])
                        self.title()
                    case '2':
                        self.create_model()
                        self.title()
                        self.infinity_mode = self.input_with_check(self.language.string[self.language.get_lang()]["infinity_mode_input"])
                        match self.infinity_mode:
                            case 'y':
                                self.infinity_mode = True
                            case _:
                                self.infinity_mode = False
                        self.markov_chain.manual_generate_text(self.text.probabilities, self.infinity_mode)
                        self.input_with_check(self.language.string[self.language.get_lang()]["press_enter"])
                        self.title()
                    case '101':
                        self.title()
                        self.language.change_lang()
                        self.input_with_check(self.language.string[self.language.get_lang()]["press_enter"])
                        self.title()
                    case '0':
                        break
                    case _:
                        self.title()
            except Exception as e:
                self.title(self.language.string[self.language.get_lang()]["something_went_wrong"].format(e=e))
                
    def title(self, some_notif = None):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(r"""
     __  __      _            ____ _           
    |  \/  |_ __| | ____   __/ ___| |__  _ __  
    | |\/| | '__| |/ /\ \ / / |   | '_ \| '_ \ 
    | |  | | |  |   <  \ V /| |___| | | | | | |
    |_|  |_|_|  |_|\_\  \_/  \____|_| |_|_| |_|
    
    
        Created by adqe404.
        GitHub: github.com/adqe404/MrkChn
        """)
        kittie = random.choice(self.language.string["kitties"]["kitties"]) if self.config.kitties_title else 'mud blood and poison'
        print(f'''{self.regele}
{some_notif if some_notif else ' ' * ((len(self.regele)//2) - len(kittie))+kittie}
{self.regele}\n\n''')
        
    def create_model(self):
        self.config.check_config()
        self.text = TextProcessor(self.config, self, self.language)
        self.markov_chain = MarkovChain(self.config, self.text.probabilities, self, self.language)