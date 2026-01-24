from typing import List, Dict, Optional
from utils.db import query_all, query_one, execute


def listar(incluir_deshabilitados: bool = False) -> List[Dict]:
    if incluir_deshabilitados:
        return query_all("SELECT * FROM zonas ORDER BY eliminado, nombre")
    else:
        return query_all("SELECT * FROM zonas WHERE eliminado = 0 ORDER BY nombre")


def obtener(zona_id: int) -> Optional[Dict]:
    return query_one("SELECT * FROM zonas WHERE id=%s", (zona_id,))


def crear(nombre: str, descripcion: str, imagen_url: str = None) -> int:
    return execute("INSERT INTO zonas (nombre, descripcion, imagen_url, eliminado) VALUES (%s, %s, %s, 0)", (nombre, descripcion, imagen_url))


def actualizar(zona_id: int, nombre: str, descripcion: str, imagen_url: str = None):
    if imagen_url:
        execute("UPDATE zonas SET nombre=%s, descripcion=%s, imagen_url=%s WHERE id=%s", (nombre, descripcion, imagen_url, zona_id))
    else:
        execute("UPDATE zonas SET nombre=%s, descripcion=%s WHERE id=%s", (nombre, descripcion, zona_id))


def eliminar_logico(zona_id: int):
    """Deshabilita una zona (soft delete)."""
    execute("UPDATE zonas SET eliminado=1 WHERE id=%s", (zona_id,))


def habilitar(zona_id: int):
    """Habilita una zona previamente deshabilitada."""
    execute("UPDATE zonas SET eliminado=0 WHERE id=%s", (zona_id,))


def eliminar(zona_id: int):
    # Note: Foreign key constraint in recursos will prevent deletion if resources exist.
    # The controller/service should handle the IntegrityError or check before deleting.
    execute("DELETE FROM zonas WHERE id=%s", (zona_id,))
