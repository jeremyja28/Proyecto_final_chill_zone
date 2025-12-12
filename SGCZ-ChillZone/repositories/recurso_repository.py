from typing import List, Dict, Optional
from utils.db import query_all, query_one, execute


def listar() -> List[Dict]:
    sql = (
        "SELECT r.*, z.nombre AS zona_nombre, z.id AS zona_id "
        "FROM recursos r LEFT JOIN zonas z ON z.id=r.zona_id "
        "WHERE r.eliminado = 0 ORDER BY z.nombre, r.nombre"
    )
    return query_all(sql)


def obtener(recurso_id: int) -> Optional[Dict]:
    return query_one("SELECT * FROM recursos WHERE id = %s", (recurso_id,))


def crear(nombre: str, tipo: str, ubicacion: str, zona_id: int, imagen_url: str = None) -> int:
    sql = "INSERT INTO recursos (nombre, tipo, ubicacion, zona_id, imagen_url, estado, eliminado) VALUES (%s, %s, %s, %s, %s, 'DISPONIBLE', 0)"
    return execute(sql, (nombre, tipo, ubicacion, zona_id, imagen_url))


def editar(recurso_id: int, nombre: str, tipo: str, ubicacion: str, zona_id: int, imagen_url: str = None):
    if imagen_url:
        sql = "UPDATE recursos SET nombre=%s, tipo=%s, ubicacion=%s, zona_id=%s, imagen_url=%s WHERE id=%s"
        execute(sql, (nombre, tipo, ubicacion, zona_id, imagen_url, recurso_id))
    else:
        sql = "UPDATE recursos SET nombre=%s, tipo=%s, ubicacion=%s, zona_id=%s WHERE id=%s"
        execute(sql, (nombre, tipo, ubicacion, zona_id, recurso_id))


def eliminar_logico(recurso_id: int):
    sql = "UPDATE recursos SET eliminado=1 WHERE id=%s"
    execute(sql, (recurso_id,))


def cambiar_estado(recurso_id: int, estado: str, mant_inicio: str = None, mant_fin: str = None):
    """Cambia el estado del recurso y opcionalmente registra periodo de mantenimiento.
    mant_inicio/fin: formato 'YYYY-MM-DD HH:MM:SS' o None."""
    if estado in ('EN_MANTENIMIENTO', 'FUERA_DE_SERVICIO') and mant_inicio and mant_fin:
        sql = "UPDATE recursos SET estado=%s, mantenimiento_inicio=%s, mantenimiento_fin=%s WHERE id=%s"
        execute(sql, (estado, mant_inicio, mant_fin, recurso_id))
    else:
        # Clear maintenance window if returning to DISPONIBLE or no dates provided
        sql = "UPDATE recursos SET estado=%s, mantenimiento_inicio=NULL, mantenimiento_fin=NULL WHERE id=%s"
        execute(sql, (estado, recurso_id))


def listar_unidades(recurso_id: int) -> List[Dict]:
    sql = "SELECT id, etiqueta, estado, eliminado FROM recurso_unidades WHERE recurso_id=%s AND eliminado=0 ORDER BY id"
    return query_all(sql, (recurso_id,))
