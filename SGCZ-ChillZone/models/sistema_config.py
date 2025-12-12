from dataclasses import dataclass
from datetime import datetime


@dataclass
class SistemaConfig:
    id: int
    nombre: str
    valor: str
    actualizado_en: datetime | None = None