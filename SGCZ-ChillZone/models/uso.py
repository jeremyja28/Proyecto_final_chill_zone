from dataclasses import dataclass
from datetime import datetime


@dataclass
class Uso:
    id: int
    reserva_id: int
    hora_inicio: datetime
    hora_fin: datetime | None
    duracion_min: int | None