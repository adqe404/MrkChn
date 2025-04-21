from .ConfigParser import ConfigParser
from .Language import Language
from .TextProcessor import TextProcessor
from .MarkovChain import MarkovChain
import os
import random
from rich.console import Console
console = Console(highlight=False)
rinput = console.input
rprint = console.print


class Main():
    def __init__(self):
        self.config = ConfigParser(self)
        self.language = self.config.language
        
    def input_with_check(self, text, rich_input = True):
        input_text = rinput(text) if rich_input else input(text)
        self.config.check_config()
        return input_text

    def menu(self):
        self.config.check_config()
        if self.config.language not in ('ru', 'en') or not self.config.language:
            self.language.change_lang()
            self.input_with_check(self.language.string[self.language.get_lang()]["press_enter"])
            self.title()
        menu_choice = self.input_with_check(self.language.string[self.language.get_lang()]["menu_input"].format(regele = self.regele))
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
                            rprint(f'[gold1]{i + 1}.[/gold1]', self.markov_chain.generate_text(self.text.probabilities))
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
                    case '3':
                        self.create_model()
                        self.title()
                        json_filename = self.input_with_check(self.language.string[self.language.get_lang()]["json_file_name_input"])
                        json_path =self.text.model_export(json_filename)
                        rprint(self.language.string[self.language.get_lang()]["model_successfully_exported"].format(json_path = json_path))
                        self.input_with_check(self.language.string[self.language.get_lang()]["press_enter"])
                        self.title()
                    case '4':
                        self.create_model()
                        self.title()
                        tokens_filename = self.input_with_check(self.language.string[self.language.get_lang()]["tokens_file_name_input"])
                        tokens_path = self.text.tokens_export(tokens_filename)
                        rprint(self.language.string[self.language.get_lang()]["tokens_successfully_exported"].format(tokens_path = tokens_path))
                        self.input_with_check(self.language.string[self.language.get_lang()]["press_enter"])
                        self.title()
                    case '101':
                        self.title()
                        self.language.change_lang()
                        self.input_with_check(self.language.string[self.language.get_lang()]["press_enter"])
                        self.title()
                    case '102':
                        self.title()
                        self.config.user_open_file_config()
                        rprint(self.language.string[self.language.get_lang()]["config_successfully_opened"])
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
        rprint(r"""[bold green]
        __  __      _     ____ _           
       |  \/  |_ __| | __/ ___| |__  _ __  
       | |\/| | '__| |/ / |   | '_ \| '_ \ 
       | |  | | |  |   <| |___| | | | | | |
       |_|  |_|_|  |_|\_\\____|_| |_|_| |_|

        Created by adqe404 :D
        GitHub: [link=https://github.com/adqe404]github.com/adqe404/MrkChn[/link][/bold green]
        """)
        
        notif = random.choice(self.language.string["kitties"]["kitties"]) if self.config.kitties_title else 'mud blood and poison'
        width = 50
        self.regele = f'[white]{"=" * width}[white]'
        padding = (width - len(notif)) // 2
        rprint(f'''{self.regele}
{some_notif if some_notif else ' ' * padding + f'[white]{notif}[white]'}
{self.regele}\n\n''')
        
    def create_model(self):
        self.config.check_config()
        self.text = TextProcessor(self.config, self, self.language)
        self.markov_chain = MarkovChain(self.config, self.text.probabilities, self, self.language)