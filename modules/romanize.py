import pykakasi

def romanji_translate(text):
    romanize = pykakasi.kakasi()
    result = romanize.convert(text)
    romaji_text = " ".join([item['hepburn'] for item in result])
    return romaji_text  
