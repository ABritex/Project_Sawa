import re
import alkana

def convert_to_katakana(text):
    pattern = re.compile(r'[a-zA-Z]+')
    
    def to_katakana(match):
        english_word = match.group()
        return alkana.get_kana(english_word)
    return pattern.sub(to_katakana, text)

def apply_katakana(text):
    katakana_text = convert_to_katakana(text)
    return katakana_text