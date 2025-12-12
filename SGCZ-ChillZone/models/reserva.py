from dataclasses import dataclass
from datetime import date


@dataclass
class Reserva:
    id: int
    usuario_id: int
    recurso_id: int
    fecha: date
    hora_inicio: str
    hora_fin: str
    estado: str  # 'ACTIVA' | 'CANCELADA' | 'FINALIZADA' | 'CANCELADA_MANTENIMIENTO'