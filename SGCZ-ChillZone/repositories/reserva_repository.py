from typing import List, Dict, Optional
from utils.db import query_all, query_one, execute


def listar_por_usuario(user_id: int) -> List[Dict]:
    sql = "SELECT r.*, rc.nombre as recurso_nombre FROM reservas r LEFT JOIN recursos rc ON rc.id=r.recurso_id WHERE r.usuario_id=%s ORDER BY r.fecha DESC, r.hora_inicio DESC"
    return query_all(sql, (user_id,))


def listar_con_detalles() -> List[Dict]:
    """Lista todas las reservas con información del recurso y usuario."""
    sql = """
        SELECT r.*, 
               rc.nombre as recurso_nombre,
               u.nombre as usuario_nombre,
               u.apellido as usuario_apellido,
               u.correo as usuario_correo
        FROM reservas r 
        JOIN recursos rc ON rc.id=r.recurso_id 
        JOIN usuarios u ON u.id=r.usuario_id
        ORDER BY r.fecha DESC, r.hora_inicio DESC
    """
    return query_all(sql)


def obtener(reserva_id: int) -> Optional[Dict]:
    sql = "SELECT * FROM reservas WHERE id=%s"
    return query_one(sql, (reserva_id,))


def listar_por_recurso_fecha(recurso_id: int, fecha: str) -> List[Dict]:
    """Lista TODAS las reservas vigentes (PENDIENTE o ACTIVA) de un recurso en una fecha específica."""
    sql = (
        "SELECT r.*, u.nombre as usuario_nombre, u.apellido as usuario_apellido "
        "FROM reservas r "
        "JOIN usuarios u ON r.usuario_id = u.id "
        "WHERE r.recurso_id=%s AND r.fecha=%s "
        "AND r.estado IN ('PENDIENTE', 'ACTIVA') "
        "ORDER BY r.hora_inicio"
    )
    return query_all(sql, (recurso_id, fecha))


def listar_conflictos(recurso_id: int, fecha: str, hora_inicio: str, hora_fin: str) -> List[Dict]:
    """Lista reservas vigentes (PENDIENTE o ACTIVA) que solapen con el rango horario especificado."""
    sql = (
        "SELECT * FROM reservas WHERE recurso_id=%s AND fecha=%s "
        "AND estado IN ('PENDIENTE', 'ACTIVA') "
        "AND NOT (hora_fin<=%s OR hora_inicio>=%s)"
    )
    return query_all(sql, (recurso_id, fecha, hora_inicio, hora_fin))


def listar_conflictos_usuario(usuario_id: int, fecha: str, hora_inicio: str, hora_fin: str) -> List[Dict]:
    """Lista reservas vigentes (PENDIENTE o ACTIVA) del usuario que solapen con el rango horario (cualquier recurso)."""
    sql = (
        "SELECT * FROM reservas WHERE usuario_id=%s AND fecha=%s "
        "AND estado IN ('PENDIENTE', 'ACTIVA') "
        "AND NOT (hora_fin<=%s OR hora_inicio>=%s)"
    )
    return query_all(sql, (usuario_id, fecha, hora_inicio, hora_fin))


def listar_conflictos_como_acompanante(usuario_id: int, fecha: str, hora_inicio: str, hora_fin: str) -> List[Dict]:
    """Lista reservas vigentes donde el usuario es ACOMPAÑANTE y solapan con el rango horario."""
    sql = (
        "SELECT r.* FROM reservas r "
        "JOIN reserva_acompanantes ra ON r.id = ra.reserva_id "
        "WHERE ra.usuario_id=%s AND r.fecha=%s "
        "AND r.estado IN ('PENDIENTE', 'ACTIVA') "
        "AND NOT (r.hora_fin<=%s OR r.hora_inicio>=%s)"
    )
    return query_all(sql, (usuario_id, fecha, hora_inicio, hora_fin))


def crear(usuario_id: int, recurso_id: int, fecha: str, hora_inicio: str, hora_fin: str) -> int:
    sql = "INSERT INTO reservas (usuario_id, recurso_id, fecha, hora_inicio, hora_fin, estado) VALUES (%s,%s,%s,%s,%s,'PENDIENTE')"
    return execute(sql, (usuario_id, recurso_id, fecha, hora_inicio, hora_fin))


def actualizar_horario(reserva_id: int, hora_inicio: str, hora_fin: str):
    sql = "UPDATE reservas SET hora_inicio=%s, hora_fin=%s WHERE id=%s AND estado IN ('PENDIENTE', 'ACTIVA')"
    execute(sql, (hora_inicio, hora_fin, reserva_id))


def cancelar(reserva_id: int):
    sql = "UPDATE reservas SET estado='CANCELADA' WHERE id=%s AND estado IN ('PENDIENTE', 'ACTIVA')"
    execute(sql, (reserva_id,))


def marcar_finalizada(reserva_id: int):
    sql = "UPDATE reservas SET estado='FINALIZADA' WHERE id=%s AND estado IN ('ACTIVA')"
    execute(sql, (reserva_id,))


def cancelar_por_sancion(usuario_id: int) -> int:
    """Cancela todas las reservas PENDIENTE/ACTIVA de un usuario por sanción. Retorna cantidad cancelada."""
    sql = "UPDATE reservas SET estado='CANCELADA_SANCION' WHERE usuario_id=%s AND estado IN ('PENDIENTE', 'ACTIVA')"
    return execute(sql, (usuario_id,))


def cancelar_por_bloqueo(usuario_id: int) -> int:
    """Cancela todas las reservas PENDIENTE/ACTIVA de un usuario bloqueado. Retorna cantidad cancelada."""
    sql = "UPDATE reservas SET estado='CANCELADA_SANCION' WHERE usuario_id=%s AND estado IN ('PENDIENTE', 'ACTIVA')"
    return execute(sql, (usuario_id,))


def agregar_acompanantes(reserva_id: int, usuario_ids: List[int]):
    """Agrega múltiples acompañantes a una reserva."""
    if not usuario_ids:
        return
    sql = "INSERT INTO reserva_acompanantes (reserva_id, usuario_id) VALUES (%s, %s)"
    for uid in usuario_ids:
        try:
            execute(sql, (reserva_id, uid))
        except Exception as e:
            # Ignorar duplicados por UNIQUE constraint
            print(f"Acompañante {uid} ya existe o error: {e}")


def listar_acompanantes(reserva_id: int) -> List[Dict]:
    """Lista los acompañantes de una reserva con información del usuario."""
    sql = (
        "SELECT ra.id, ra.usuario_id, u.nombre, u.correo "
        "FROM reserva_acompanantes ra "
        "JOIN usuarios u ON u.id = ra.usuario_id "
        "WHERE ra.reserva_id = %s "
        "ORDER BY u.nombre"
    )
    return query_all(sql, (reserva_id,))


def obtener_con_acompanantes(reserva_id: int) -> Optional[Dict]:
    """Obtiene una reserva con su titular y lista de acompañantes."""
    reserva = obtener(reserva_id)
    if not reserva:
        return None
    reserva['acompanantes'] = listar_acompanantes(reserva_id)
    return reserva


def eliminar_acompanantes(reserva_id: int):
    """Elimina todos los acompañantes de una reserva."""
    sql = "DELETE FROM reserva_acompanantes WHERE reserva_id = %s"
    execute(sql, (reserva_id,))


def finalizar_expiradas():
    """Marca como FINALIZADA toda reserva ACTIVA o PENDIENTE cuya fecha/hora_fin ya pasó y que no tiene uso activo."""
    sql = (
        "UPDATE reservas r "
        "SET r.estado='FINALIZADA' "
        "WHERE r.estado IN ('ACTIVA', 'PENDIENTE') AND (r.fecha<CURDATE() OR (r.fecha=CURDATE() AND r.hora_fin<=CURTIME())) "
        "AND NOT EXISTS (SELECT 1 FROM uso u WHERE u.reserva_id=r.id AND u.hora_fin IS NULL)"
    )
    execute(sql)


def contar_reservas_activas_por_recurso(recurso_id: int) -> int:
    """Cuenta reservas activas futuras o del día para un recurso."""
    row = query_one(
        "SELECT COUNT(1) as c FROM reservas WHERE recurso_id=%s AND estado='ACTIVA' AND fecha>=CURDATE()",
        (recurso_id,)
    )
    return int((row or {}).get('c', 0))


def contar_activas_por_recurso(recurso_id: int) -> int:
    """Alias para mantener compatibilidad con el servicio de recursos."""
    return contar_reservas_activas_por_recurso(recurso_id)


def contar_activas_por_recurso(recurso_id: int) -> int:
    row = query_one("SELECT COUNT(1) AS c FROM reservas WHERE recurso_id=%s AND estado='ACTIVA'", (recurso_id,))
    return int(row['c']) if row else 0

def contar_activas_futuras_por_recurso(recurso_id: int) -> int:
    """Cantidad de reservas activas futuras (incluyendo hoy)."""
    row = query_one(
        "SELECT COUNT(1) AS c FROM reservas WHERE recurso_id=%s AND estado='ACTIVA' AND fecha>=CURDATE()",
        (recurso_id,)
    )
    return int(row['c']) if row else 0

def cancelar_por_mantenimiento(recurso_id: int, mant_inicio: str, mant_fin: str) -> int:
    """Cancela reservas PENDIENTE/ACTIVA del recurso que solapen con el periodo [mant_inicio, mant_fin).
    mant_inicio/fin: 'YYYY-MM-DD HH:MM:SS'.
    Retorna cuántas fueron afectadas."""
    # Contar reservas que solapen: r.inicio < mant_fin AND r.fin > mant_inicio
    row = query_one(
        """
        SELECT COUNT(1) AS c FROM reservas
        WHERE recurso_id=%s AND estado IN ('PENDIENTE', 'ACTIVA')
        AND CONCAT(fecha, ' ', hora_inicio) < %s
        AND CONCAT(fecha, ' ', hora_fin) > %s
        """,
        (recurso_id, mant_fin, mant_inicio)
    )
    afectados = int(row['c']) if row else 0
    execute(
        """
        UPDATE reservas SET estado='CANCELADA_MANTENIMIENTO'
        WHERE recurso_id=%s AND estado IN ('PENDIENTE', 'ACTIVA')
        AND CONCAT(fecha, ' ', hora_inicio) < %s
        AND CONCAT(fecha, ' ', hora_fin) > %s
        """,
        (recurso_id, mant_fin, mant_inicio)
    )
    return afectados


def cancelar_futuras_por_recurso(recurso_id: int) -> int:
    """Cancela todas las reservas PENDIENTE/ACTIVA futuras (incluyendo hoy) de un recurso."""
    sql = (
        "UPDATE reservas SET estado='CANCELADA_MANTENIMIENTO' "
        "WHERE recurso_id=%s AND estado IN ('PENDIENTE', 'ACTIVA') "
        "AND (fecha > CURDATE() OR (fecha = CURDATE() AND hora_fin > CURTIME()))"
    )
    return execute(sql, (recurso_id,))
