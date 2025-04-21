import re
import os
import json
import time
from rich.console import Console
console = Console(highlight=False)
rinput = console.input
rprint = console.print

class TextProcessor():
    def __init__(self, config, main, language):
        self.txt_filename = config.txt_filename
        self.tokenized_text = self.read_file(self.txt_filename)
        self.probabilities = self.words_count(self.tokenized_text)
        self.main = main
        self.language = language
        
    def read_file(self, txt_filename):
        text = open(f'{txt_filename}', 'r', encoding='utf-8').read().lower()
        tokenized_text = re.findall(r'\b[\w\-\\/\'"]+\b|\.{2,}|[.!?]|(?<![.!?])\n', text, re.UNICODE)
        tokenized_text = ['<END>' if token in ('.','?','!','\n') or re.fullmatch(r'\.{2,}', token) else token for token in tokenized_text]
        tokenized_text.insert(0, '<START>')
        for i in range(len(tokenized_text) - 1, -1, -1):
            if tokenized_text[i] == '<END>':
                tokenized_text.insert(i + 1, '<START>')
        del tokenized_text[-1]
        return tokenized_text
    
    def words_count(self, tokenized_text):
        probabilities = {}
        for i in range(len(tokenized_text) - 1):
            current_word = tokenized_text[i]
            next_word = tokenized_text[i + 1]
            if next_word == '<START>':
                pass
            if not current_word in probabilities:
                probabilities[current_word] = {}
            probabilities[current_word][next_word] = probabilities[current_word].get(next_word, 0) + 1
        current_words = list(probabilities.keys())
        
        for current_word in current_words:
            next_words = list(probabilities[current_word].keys())
            total = sum(probabilities[current_word].values())
            for next_word in next_words:
                probabilities[current_word][next_word] = round((probabilities[current_word][next_word]/total), 10) # Округление: 5 знаков после запятой
        if '<END>' in probabilities['<START>'].keys():
            del probabilities['<START>']['<END>']
        return probabilities
    
    def model_export(self, json_filename):
        json_filename = json_filename if json_filename[-5:] != '.json' else json_filename[:-5]
        time_file = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))
        os.makedirs('dumped_jsons', exist_ok=True)
        json_path = f'dumped_jsons/{json_filename}_{time_file}.json'
        with open(json_path, 'w', encoding='utf-8') as file:
            json.dump(self.probabilities, file, indent=4, ensure_ascii=False)
        return json_path
    
    def tokens_export(self, tokens_filename):
        tokens_filename = tokens_filename if tokens_filename[-4:] != '.txt' else tokens_filename[:-4]
        time_file = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))
        os.makedirs('tokens', exist_ok=True)
        tokens_path = f'tokens/{tokens_filename}_{time_file}.txt'
        with open(tokens_path, 'w', encoding='utf-8') as file:
            file.write(", ".join(self.tokenized_text))
        return tokens_path
    