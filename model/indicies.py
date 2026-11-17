
from dataclasses import dataclass

@dataclass
class Indices:
    """
    Contiene gli indici calcolati dal simulatore per ogni anno presente
    """
    years: list[str]
    equity_ratio: list[float]   # Autonomia finanziaria
    asset_structure_ratio: list[float]
    current_ratio: list[float]
    roe: list[float]
    roi: list[float]
    ros: list[float]