import random

class MarkovChain():
    def __init__(self, config, probabilities, main, language):
        self.config = config
        self.probabilities = probabilities
        self.main = main
        self.language = language
        self.seed = config.seed if config.seed in (list(probabilities.keys())) else '<START>'
        self.text_len = config.text_len
        self.gen_num = config.gen_num
    
    def cycle(self, generated_text, current_word, probabilities):
        if self.text_len is False:
            return '<END>' != current_word if '<END>' in probabilities.keys() else len(generated_text) < int(random.randint(2,10)) + 1
        return len(generated_text) < int(self.text_len) + 1 if self.seed == '<START>' else len(generated_text) < int(self.text_len)
        
    def generate_text(self, probabilities: dict):
        current_word = self.seed
        generated_text = [current_word]
        while self.cycle(generated_text, current_word, probabilities):
            next_word = random.choices(list(probabilities[current_word].keys()), list(probabilities[current_word].values()), k=1)[0]
            generated_text.append(next_word) if not(next_word in ('<START>', '<END>')) else None
            current_word = next_word
        return ' '.join(generated_text[1:] if self.seed == '<START>' else generated_text)
    
    def manual_generate_text(self, probabilities: dict, infinity_mode):
        current_word = self.seed
        generated_text = [current_word]
        while current_word != '<END>' or infinity_mode:
            self.main.title()
            print(self.language.string[self.language.get_lang()]["current_word_is"].format(generated_text = " ".join(generated_text), current_word = current_word))
            words = []
            for word, chance in zip((probabilities[current_word].keys()), (probabilities[current_word].values())):
                words.append([word, chance])
            words = sorted(words, key=lambda x: x[1], reverse=True)
            i = 1
            for word in words:
                print(f'{i}. {word[0]} ({round((word[1] * 100), 2)}%)')
                i += 1
            try:
                choice = input(self.language.string[self.language.get_lang()]["enter_word_number"])
                if choice == 'exit':
                    break
                next_word = list([a[0] for a in words])[int(choice) - 1] if int(choice) > 0 else list([a[0] for a in words])[int(choice)]
            except:
                next_word = random.choices(list([a[0] for a in words]), list([a[1] for a in words]), k=1)[0]
            generated_text.append(next_word) if not(next_word in ('<START>', '<END>')) else None
            current_word = next_word
            if generated_text[0] == '<START>':
                del generated_text[0]
        self.main.title()
        print(self.language.string[self.language.get_lang()]["generated_text"].format(generated_text = " ".join(generated_text)))