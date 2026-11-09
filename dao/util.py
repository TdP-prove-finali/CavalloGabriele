import unicodedata
import math
import re
from enum import IntEnum

class BalanceLocation(IntEnum):
    SP_ATTIVO = 0,
    SP_PASSIVO_DEBITI = 1,
    SP_PASSIVO_PATRIM = 2,
    CE = 3,
    SP_PASSIVO = 4,
    SP = 5

    @staticmethod
    def from_str(input: str):
        d = {
            "attivo": BalanceLocation.SP_ATTIVO,
            "passivo": BalanceLocation.SP_PASSIVO,
            "debiti": BalanceLocation.SP_PASSIVO_DEBITI,
            "patrimonio_netto": BalanceLocation.SP_PASSIVO_PATRIM,
            "conto_economico": BalanceLocation.CE
        }
        if d.get(input) is None:
            raise Exception("BalanceLocation non riconosciuta")

        return d.get(input)

SECTION_HEAD = ["attivo", "passivo", "patrimonio_netto", "debiti", "conto_economico"]

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
    r"(?P<specificazione>bis|ter|quater)?"
    r"(?=_|$)"
)

"""
Regex con campi nominati per controllare se un campo ha numerazione con numeri arabi"""
ROMAN_FIELD_REGEX = re.compile(
    r"^(?P<lettera>[a-z])"
    r"(?P<romano>viii|vii|vi|iv|ix|iii|ii|v|x|i)"
    r"(?P<numero>10|[1-9])?"
    r"(?P<sottolettera>[a-z])?"
    r"(?P<specificazione>bis|ter|quater)?"
    r"(?=_|$)"
)

def step_up_numbering(old_numeration: str, where: BalanceLocation | None = None) -> str:
    """
    Restituisce la numerazione del parent a cui appartiene il campo, gestendo sia la numerazione araba che quella romana

    :param old_numeration: Vecchia numerazione, opzionalmente accetta anche field_name
    :return:
    """
    if ARABIC_FIELD_REGEX.match(old_numeration):
        # La numerazione è araba
        match = ARABIC_FIELD_REGEX.match(old_numeration)
        letter = match.group("lettera")
        number = int(match.group("numero")) if match.group("numero") else None
        sub_letter = match.group("sottolettera") or None
        spec = match.group("specificazione") or None

        if spec is not None and where is not None and where == BalanceLocation.SP_PASSIVO_DEBITI:
            return f"{letter}"
        elif spec is not None:
            return f"{letter}{number or ""}{sub_letter or ""}"
        elif sub_letter is not None:
            return f"{letter}{number or ""}"
        elif number is not None:
            return f"{letter}"
        else:
            return ""

    elif ROMAN_FIELD_REGEX.match(old_numeration):
        # La numerazione è romana
        match = ROMAN_FIELD_REGEX.match(old_numeration)
        letter = match.group("lettera")
        number = match.group("romano") if match.group("romano") else None
        sub_number = match.group("numero") if match.group("numero") else None
        sub_letter = match.group("sottolettera") or None
        spec = match.group("specificazione") or None

        if spec is not None:
            return f"{letter}{number or ""}"
        elif sub_letter is not None:
            return f"{letter}{number or ""}{sub_number or ""}"
        elif sub_number is not None:
            return f"{letter}{number or ""}"
        elif number is not None:
            return f"{letter}"
        else:
            return ""

    raise Exception("Numerazione non riconosciuta")

def step_up_field(field_name: str, where: BalanceLocation | None = None)-> str:
    """Dato un field_name completo restituisce l'identificatore del campo parent, applicando le giuste regole"""
    dc = is_specification_field(field_name)
    ha = extract_o_number(field_name)
    ntk = extract_numbering_token(field_name)

    if dc:
        return f"{ntk or ""}{create_o_number(ha) if ha is not None else ""}"
    elif ha is not None:    # I campi con numerazione artificiale possono essere campi top-level oppure collegati ad un campo con numerazione
        return f"{ntk[0] if ntk is not None and len(ntk) > 0 else ""}"
    elif ntk is not None:
        return step_up_numbering(ntk, where)

    if field_name in ["data", "moneta", "periodo", "ics"] or field_name in SECTION_HEAD:
        return ""

    raise Exception(f"Numerazione non riconosciuta per il campo {field_name}")

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

def extract_only_name(field_name: str)-> str:
    """Restituisce il nome del campo senza la numerazione (originale o artificiale)"""
    return (field_name.removeprefix(
        extract_complete_numbering(field_name) or "")
            .removeprefix("_"))

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


def extract_field_identif(field_name: str) -> str | None:
    """
    Estrae:
    - La numerazione araba o romana, se presente.
    - Il token artificiale _o[numero], se presente.
    - Il token _dc, se presente.

    Restituisce None se tutti i token sono assenti.
    Restituisce sempre l'underscore finale se trova almeno un token.
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

    dc_match = re.search(r"_dc_", field_name)
    dc = "_dc" if dc_match else None

    result = "".join(
        token for token in (numbering, artificial, dc)
        if token is not None
    )

    return f"{result}_" if result else None

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