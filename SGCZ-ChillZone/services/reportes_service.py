from utils.db import query_all
import csv
from io import StringIO


def resumen_uso(usuario_id: int = None):
    data = {}
    
    # Gráfico 1: Uso Global (sin cambios)
    data['por_recurso'] = query_all("""
        SELECT rc.nombre, 
               COUNT(r.id) as usos, 
               COALESCE(SUM(TIME_TO_SEC(TIMEDIFF(r.hora_fin, r.hora_inicio))/60), 0) as minutos
        FROM recursos rc
        LEFT JOIN reservas r ON r.recurso_id=rc.id AND r.estado != 'CANCELADA'
        GROUP BY rc.id
        ORDER BY usos DESC
    """)
    
    # Gráfico 2: Uso específico del usuario por recurso (si hay filtro)
    data['usuario_por_recurso'] = []
    if usuario_id:
        sql_user_res = """
            SELECT rc.nombre, COUNT(r.id) as usos
            FROM recursos rc
            JOIN reservas r ON r.recurso_id = rc.id
            WHERE r.usuario_id = %s
            AND r.estado != 'CANCELADA'
            GROUP BY rc.id
            ORDER BY usos DESC
        """
        data['usuario_por_recurso'] = query_all(sql_user_res, (usuario_id,))
    
    sql_usuario = """
        SELECT us.nombre, 
               COUNT(r.id) as usos, 
               COALESCE(SUM(TIME_TO_SEC(TIMEDIFF(r.hora_fin, r.hora_inicio))/60), 0) as minutos
        FROM usuarios us
        LEFT JOIN reservas r ON r.usuario_id=us.id AND r.estado != 'CANCELADA'
        WHERE (%s IS NULL OR us.id = %s)
        GROUP BY us.id
        ORDER BY usos DESC
    """
    data['por_usuario'] = query_all(sql_usuario, (usuario_id, usuario_id))
    
    # Nuevas métricas para gráficos solicitados con filtro opcional
    sql_zona = """
        SELECT z.nombre as zona, COUNT(r.id) as total
        FROM reservas r
        JOIN recursos rc ON r.recurso_id = rc.id
        JOIN zonas z ON rc.zona_id = z.id
        WHERE (%s IS NULL OR r.usuario_id = %s)
        GROUP BY z.nombre
    """
    data['por_zona'] = query_all(sql_zona, (usuario_id, usuario_id))
    
    sql_estado = """
        SELECT r.estado, COUNT(r.id) as total
        FROM reservas r
        WHERE (%s IS NULL OR r.usuario_id = %s)
        GROUP BY r.estado
    """
    data['por_estado'] = query_all(sql_estado, (usuario_id, usuario_id))
    
    return data


def exportar_csv():
    data = resumen_uso()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Recurso', 'Usos', 'Minutos'])
    for r in data['por_recurso']:
        writer.writerow([r['nombre'], r['usos'], r['minutos']])
    writer.writerow([])
    writer.writerow(['Usuario', 'Usos', 'Minutos'])
    for u in data['por_usuario']:
        writer.writerow([u['nombre'], u['usos'], u['minutos']])
    return output.getvalue()

def reservas_historial(fecha_ini: str | None, fecha_fin: str | None, estado: str | None = None):
    filtros = []
    params = []
    if fecha_ini:
        filtros.append("r.fecha >= %s")
        params.append(fecha_ini)
    if fecha_fin:
        filtros.append("r.fecha <= %s")
        params.append(fecha_fin)
    if estado:
        if estado == 'CANCELADA':
            filtros.append("r.estado LIKE 'CANCELADA%'")
        else:
            filtros.append("r.estado = %s")
            params.append(estado)
            
    where = ("WHERE " + " AND ".join(filtros)) if filtros else ""
    sql = f"""
        SELECT r.id, r.fecha, r.hora_inicio, r.hora_fin, r.estado,
               u.nombre AS usuario, rc.nombre AS recurso
        FROM reservas r
        JOIN usuarios u ON u.id=r.usuario_id
        JOIN recursos rc ON rc.id=r.recurso_id
        {where}
        ORDER BY r.fecha DESC, r.hora_inicio DESC
    """
    return query_all(sql, tuple(params))
