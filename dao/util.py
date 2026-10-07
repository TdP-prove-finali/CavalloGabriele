import unicodedata

def remove_accents(text: str) -> str:   # Toglie tutti gli accenti da una stringa
    text = text.lower()
    return ''.join(
        char for char in unicodedata.normalize('NFD', text)
        if unicodedata.category(char) != 'Mn'
    )