from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int
    nombre: str
    apellido: str
    correo: str
    hash_password: bytes
    rol: str  # 'USUARIO' | 'ADMIN'
    estado: str  # 'ACTIVO' | 'BLOQUEADO'
    creado_en: datetime | None = None
