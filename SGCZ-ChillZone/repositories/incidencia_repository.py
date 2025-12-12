from typing import List, Dict
from utils.db import query_all, query_one, execute


def listar_por_recurso(recurso_id: int) -> List[Dict]:
    sql = "SELECT * FROM incidencias WHERE recurso_id=%s ORDER BY creado_en DESC"
    return query_all(sql, (recurso_id,))


def crear(recurso_id: int, usuario_id: int, descripcion: str, evidencia_url: str = None, responsables_ids: list = None, reserva_id: int = None):
    sql = "INSERT INTO incidencias (recurso_id, usuario_id, descripcion, evidencia_url, estado, reserva_id) VALUES (%s,%s,%s,%s,'PENDIENTE',%s)"
    incidencia_id = execute(sql, (recurso_id, usuario_id, descripcion, evidencia_url, reserva_id))
    
    # Agregar responsables si se proporcionaron
    if responsables_ids:
        agregar_responsables(incidencia_id, responsables_ids)
    
    return incidencia_id


def listar_por_usuario(usuario_id: int) -> List[Dict]:
    sql = "SELECT i.*, r.nombre as recurso_nombre, res.fecha as reserva_fecha, res.hora_inicio as reserva_hora_inicio, res.hora_fin as reserva_hora_fin FROM incidencias i JOIN recursos r ON r.id=i.recurso_id LEFT JOIN reservas res ON res.id=i.reserva_id WHERE i.usuario_id=%s ORDER BY i.creado_en DESC"
    return query_all(sql, (usuario_id,))


def listar_todas() -> List[Dict]:
    sql = (
        "SELECT i.*, r.nombre as recurso_nombre, u.nombre as usuario_nombre, u.apellido as usuario_apellido, u.correo as usuario_correo, "
        "res.fecha as reserva_fecha, res.hora_inicio as reserva_hora_inicio, res.hora_fin as reserva_hora_fin "
        "FROM incidencias i "
        "JOIN recursos r ON r.id=i.recurso_id "
        "JOIN usuarios u ON u.id=i.usuario_id "
        "LEFT JOIN reservas res ON res.id=i.reserva_id "
        "ORDER BY i.estado ASC, i.creado_en DESC"
    )
    incidencias = query_all(sql)
    
    # Agregar responsables a cada incidencia
    for inc in incidencias:
        inc['responsables'] = listar_responsables(inc['id'])
    
    return incidencias

def obtener(incidencia_id: int) -> Dict | None:
    sql = "SELECT * FROM incidencias WHERE id=%s"
    return query_one(sql, (incidencia_id,))

def actualizar_estado(incidencia_id: int, estado: str):
    sql = "UPDATE incidencias SET estado=%s WHERE id=%s"
    execute(sql, (estado, incidencia_id))


def agregar_responsables(incidencia_id: int, usuario_ids: list):
    """Agrega múltiples responsables a una incidencia."""
    if not usuario_ids:
        return
    sql = "INSERT INTO incidencia_responsables (incidencia_id, usuario_id) VALUES (%s, %s)"
    for uid in usuario_ids:
        try:
            execute(sql, (incidencia_id, uid))
        except Exception as e:
            print(f"Responsable {uid} ya existe o error: {e}")


def listar_responsables(incidencia_id: int) -> List[Dict]:
    """Lista los responsables de una incidencia con información del usuario."""
    sql = (
        "SELECT ir.id, ir.usuario_id, u.nombre, u.correo "
        "FROM incidencia_responsables ir "
        "JOIN usuarios u ON u.id = ir.usuario_id "
        "WHERE ir.incidencia_id = %s "
        "ORDER BY u.nombre"
    )
    return query_all(sql, (incidencia_id,))


def eliminar_responsables(incidencia_id: int):
    """Elimina todos los responsables de una incidencia."""
    sql = "DELETE FROM incidencia_responsables WHERE incidencia_id = %s"
    execute(sql, (incidencia_id,))
