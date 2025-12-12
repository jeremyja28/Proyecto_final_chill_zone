from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from utils.db import query_one, query_all


def _int(row, key):
    try:
        return int(row.get(key, 0)) if row else 0
    except Exception:
        return 0


def admin_metrics() -> Tuple[Dict, List[str], Dict]:
    """Devuelve métricas generales para el dashboard admin.
    - nuevos_usuarios: creados en últimos 7 días
    - reservas_hoy: reservas del día
    - incidencias_pendientes: estado PENDIENTE
    - tasa_ocupacion: proxy simple (reservas activas hoy / recursos totales * 100)
    - recientes_incidencias: lista simple de descripciones recientes
    - chart_data: horas totales de uso por día (últimos 7 días)
    """
    hoy = datetime.now().date()
    hace_7 = hoy - timedelta(days=7)

    nuevos = _int(query_one("SELECT COUNT(1) c FROM usuarios WHERE DATE(creado_en) >= %s", (hace_7,)), 'c')
    reservas_hoy = _int(query_one("SELECT COUNT(1) c FROM reservas WHERE fecha=%s", (hoy,)), 'c')
    incidencias_p = _int(query_one("SELECT COUNT(1) c FROM incidencias WHERE estado='PENDIENTE'", ()), 'c')
    
    # Recurso más utilizado (por cantidad de reservas FINALIZADA)
    top_recurso_row = query_one(
        """
        SELECT rc.nombre, COUNT(r.id) as total
        FROM reservas r
        JOIN recursos rc ON rc.id = r.recurso_id
        WHERE r.estado = 'FINALIZADA'
        GROUP BY rc.id, rc.nombre
        ORDER BY total DESC
        LIMIT 1
        """
    )
    recurso_top = top_recurso_row['nombre'] if top_recurso_row else 'N/A'

    recientes = [r['descripcion'] for r in query_all(
        "SELECT descripcion FROM incidencias ORDER BY creado_en DESC LIMIT 5")]

    # Serie: suma de minutos de uso por día últimos 7
    # Se usa la tabla reservas en lugar de uso para reflejar la actividad planificada/realizada
    rows = query_all(
        """
        SELECT fecha as d, COALESCE(SUM(TIME_TO_SEC(TIMEDIFF(hora_fin, hora_inicio))/60), 0) as minutos
        FROM reservas
        WHERE fecha >= %s AND estado != 'CANCELADA'
        GROUP BY fecha
        ORDER BY d
        """,
        (hace_7,)
    )
    labels = []
    data = []
    for i in range(7):
        d = hace_7 + timedelta(days=i)
        labels.append(d.strftime('%d/%m'))
        match = next((x for x in rows if str(x['d']) == str(d)), None)
        data.append(_int(match, 'minutos'))

    metrics = {
        'nuevos_usuarios': nuevos,
        'recurso_mas_utilizado': recurso_top,
        'reservas_hoy': reservas_hoy,
        'incidencias_pendientes': incidencias_p,
    }
    chart = {'labels': labels, 'data': data}
    return metrics, recientes, chart


def user_stats(user_id: int) -> Tuple[Dict, List[dict]]:
    hoy = datetime.now().date()
    lunes = hoy - timedelta(days=hoy.weekday())
    reservas_hoy = _int(query_one("SELECT COUNT(1) c FROM reservas WHERE usuario_id=%s AND fecha=%s", (user_id, hoy)), 'c')
    minutos_semana = _int(query_one(
        """
        SELECT COALESCE(SUM(TIME_TO_SEC(TIMEDIFF(hora_fin, hora_inicio))/60), 0) c
        FROM reservas
        WHERE usuario_id=%s AND fecha >= %s AND estado != 'CANCELADA'
        """, (user_id, lunes)
    ), 'c')
    incidencias_mias = _int(query_one("SELECT COUNT(1) c FROM incidencias WHERE usuario_id=%s", (user_id,)), 'c')
    recientes = query_all(
        """
        SELECT rc.nombre AS recurso, DATE_FORMAT(r.fecha,'%Y-%m-%d') AS fecha, CONCAT(r.hora_inicio,'-',r.hora_fin) AS hora, r.estado
        FROM reservas r
        LEFT JOIN recursos rc ON rc.id=r.recurso_id
        WHERE r.usuario_id=%s
        ORDER BY r.creado_en DESC
        LIMIT 5
        """,
        (user_id,)
    )
    stats = {
        'mis_reservas_hoy': reservas_hoy,
        'tiempo_uso_semana': round(minutos_semana/60, 1),
        'incidencias_reportadas': incidencias_mias,
    }
    return stats, recientes
