from typing import List, Dict, Optional
from utils.db import query_all, query_one, execute


def listar_por_usuario(user_id: int) -> List[Dict]:
    sql = "SELECT u.*, r.recurso_id FROM uso u JOIN reservas r ON r.id=u.reserva_id WHERE r.usuario_id=%s ORDER BY u.hora_inicio DESC"
    return query_all(sql, (user_id,))


def obtener(uso_id: int) -> Optional[Dict]:
    return query_one("SELECT * FROM uso WHERE id=%s", (uso_id,))


def crear(reserva_id: int, hora_inicio: str) -> int:
    sql = "INSERT INTO uso (reserva_id, hora_inicio) VALUES (%s,%s)"
    return execute(sql, (reserva_id, hora_inicio))


def finalizar(uso_id: int, hora_fin: str, duracion_min: int):
    sql = "UPDATE uso SET hora_fin=%s, duracion_min=%s WHERE id=%s"
    execute(sql, (hora_fin, duracion_min, uso_id))


def existe_uso_iniciado_por_reserva(reserva_id: int) -> bool:
    """Devuelve True si existe un uso sin finalizar para la reserva dada."""
    row = query_one("SELECT COUNT(1) as c FROM uso WHERE reserva_id=%s AND hora_inicio IS NOT NULL AND hora_fin IS NULL", (reserva_id,))
    return (row or {}).get('c', 0) > 0


def contar_usos_activos_por_recurso(recurso_id: int) -> int:
    """Cuenta usos en progreso asociados a reservas del recurso indicado."""
    row = query_one(
        """
        SELECT COUNT(u.id) as c
        FROM uso u
        JOIN reservas r ON r.id = u.reserva_id
        WHERE r.recurso_id=%s AND u.hora_fin IS NULL
        """,
        (recurso_id,)
    )
    return int((row or {}).get('c', 0))


def obtener_activo_por_reserva(reserva_id: int) -> Optional[Dict]:
    """Obtiene el uso activo (sin hora_fin) de una reserva, si existe."""
    return query_one("SELECT * FROM uso WHERE reserva_id=%s AND hora_fin IS NULL ORDER BY hora_inicio DESC LIMIT 1", (reserva_id,))


def contar_activos_por_recurso(recurso_id: int) -> int:
    """Alias para mantener compatibilidad con el servicio de recursos."""
    return contar_usos_activos_por_recurso(recurso_id)


def obtener_activo_por_reserva(reserva_id: int):
    sql = "SELECT * FROM uso WHERE reserva_id=%s AND hora_fin IS NULL ORDER BY hora_inicio DESC LIMIT 1"
    return query_one(sql, (reserva_id,))


def contar_activos_por_recurso(recurso_id: int) -> int:
    sql = (
        "SELECT COUNT(1) AS c FROM uso u "
        "JOIN reservas r ON r.id=u.reserva_id "
        "WHERE r.recurso_id=%s AND u.hora_fin IS NULL"
    )
    row = query_one(sql, (recurso_id,))
    return int(row['c']) if row else 0
