import unicodedata
import math

def remove_accents(text: str) -> str:   # Toglie tutti gli accenti da una stringa
    text = text.lower()
    return ''.join(
        char for char in unicodedata.normalize('NFD', text)
        if unicodedata.category(char) != 'Mn'
    )

def check_empty(v):
    return v is None or v == ""

def check_invalid_factor(v: str):
    try:
        return float(v.replace(",", ".")) == 0.00
    except:
        return True

def parse(v):
    return float(v.replace(",", "."))


def is_number(value) -> bool:
    if isinstance(value, bool):
        return False

    try:
        return math.isfinite(float(value))
    except (ValueError, TypeError, OverflowError):
        return False

def format_number( value: int | float | str) -> str:
    """
    Formatta un numero per renderlo più facile da leggere. Nel caso sia una valuta,
    inserisce anche i punti di separazione delle migliaia.
    :param value:
    :return:
    """
    try:
        if isinstance(value, str):
            value = value.strip()

            if "," in value:
                value = value.replace(".", "").replace(",", ".")

        decimals = 0 if isinstance(value, int) or (
                isinstance(value, str) and value.lstrip("+-").isdigit()
        ) else 2

        number = float(value)

        return f"{number:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")

    except (ValueError, TypeError, OverflowError):
        return str(value)