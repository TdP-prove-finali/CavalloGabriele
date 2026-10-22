import dataclasses


@dataclasses.dataclass
class ImportException(Exception):
    section: str
    cursor: tuple[int, int]
    message: str

    def __str__(self):
        return f"Errore durante l'importazione. Posizione del cursore: {self.cursor}. Sezione: {self.section}. Motivo: {self.message}"