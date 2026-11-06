import unicodedata
import math
import re

def remove_accents(text: str) -> str:   # Toglie tutti gli accenti da una stringa
    text = text.lower()
    return ''.join(
        char for char in unicodedata.normalize('NFD', text)
        if unicodedata.category(char) != 'Mn'
    )

def check_empty(v):
    return v is None or v == ""

"""
Regex con campi nominati per controllare se un campo ha una numerazione decimale"""
ARABIC_FIELD_REGEX = re.compile(
    r"^(?P<lettera>[a-z])"
    r"(?:(?P<numero>[0-9]{1,2})(?P<sottolettera>[a-z])?)?"
    r"(?P<specificazione>bis|ter|quater|_di_cui)?"
    r"(?=_|$)"
)

"""
Regex con campi nominati per controllare se un campo ha numerazione con numeri arabi"""
ROMAN_FIELD_REGEX = re.compile(
    r"^(?P<lettera>[a-z])"
    r"(?P<romano>viii|vii|vi|iv|ix|iii|ii|v|x|i)"
    r"(?P<numero>10|[1-9])?"
    r"(?P<sottolettera>[a-z])?"
    r"(?P<specificazione>bis|ter|quater|_di_cui)?"
    r"(?=_|$)"
)

def extract_numbering_token(field_name: str) -> str | None:
    """
    Estrae il token di numerazione iniziale, arabo o romano.
    """
    if not isinstance(field_name, str) or not field_name:
        return None

    match = (
        ROMAN_FIELD_REGEX.match(field_name)
        or ARABIC_FIELD_REGEX.match(field_name)
    )

    return match.group(0) if match else None

def extract_o_number(field_name: str) -> int | None:
    """
    Estrae il numero dal token _o[numero]_.
    Il numero può avere 1 o 2 cifre.

    Restituisce None se il token non è presente.
    """
    match = re.search(r"_o(?P<numero>\d{1,2})_", field_name)

    return int(match.group("numero")) if match else None

def create_o_number(number: int) -> str:
    return f"_o{number}_"

import re


def extract_complete_numbering(field_name: str) -> str | None:
    """
    Estrae la numerazione araba/romana e l'eventuale numerazione artificiale _o[numero]_.
    Restituisce None se entrambe sono assenti.
    """
    if not isinstance(field_name, str) or not field_name:
        return None

    match = (
        ROMAN_FIELD_REGEX.match(field_name)
        or ARABIC_FIELD_REGEX.match(field_name)
    )
    numbering = match.group(0) if match else None
    artificial_match = re.search(
        r"_o(?P<numero>[0-9]{1,2})_",
        field_name
    )
    artificial = (
        artificial_match.group(0).rstrip("_")
        if artificial_match
        else None
    )
    if numbering and artificial:
        return numbering + artificial

    return numbering or artificial

def is_specification_field(cellContent: str):
    """
    Controlla se il campo è un campo "di cui" passando il contenuto della cella oppure il field_name. Gestisce anche il caso in cui
    di cui sia scritto in maiuscolo.
    :param cellContent:
    :return:
    """
    return cellContent.lower().find("di cui") >= 0 or cellContent.lower().find("di_cui") >= 0

def has_valid_numbering(field_name: str) -> bool:
    """
    Verifica se field_name inizia con una numerazione valida, araba o romana.
    """
    if not isinstance(field_name, str) or not field_name:
        return False

    return (
        ROMAN_FIELD_REGEX.match(field_name) is not None
        or ARABIC_FIELD_REGEX.match(field_name) is not None
    )

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