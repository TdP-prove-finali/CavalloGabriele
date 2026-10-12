import unicodedata
import math

def remove_accents(text: str) -> str:   # Toglie tutti gli accenti da una stringa
    text = text.lower()
    return ''.join(
        char for char in unicodedata.normalize('NFD', text)
        if unicodedata.category(char) != 'Mn'
    )


def is_number(value) -> bool:
    if isinstance(value, bool):
        return False

    try:
        return math.isfinite(float(value))
    except (ValueError, TypeError, OverflowError):
        return False