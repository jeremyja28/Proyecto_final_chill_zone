from dataclasses import dataclass
from datetime import datetime


@dataclass
class Incidencia:
    id: int
    recurso_id: int
    usuario_id: int
    reserva_id: int | None
    descripcion: str
    evidencia_url: str | None
    estado: str  # 'PENDIENTE' | 'REVISADA'
    creado_en: datetime | None = None