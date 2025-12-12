from dataclasses import dataclass


@dataclass
class Recurso:
    id: int
    nombre: str
    tipo: str
    ubicacion: str
    estado: str  # 'DISPONIBLE' | 'EN_MANTENIMIENTO' | 'FUERA_DE_SERVICIO'
    eliminado: bool
