from typing import Dict, Any, List, Tuple
from utils.db import get_cursor

"""Servicio de estadísticas (CU-16).
Devuelve agregados para visualizaciones rápidas.
Fallback seguro: ante error retorna estructuras vacías.
"""

def resumen_general() -> Dict[str, Any]:
    data: Dict[str, Any] = {
        'recursos': {'total': 0, 'disponibles': 0, 'mantenimiento': 0, 'fuera_servicio': 0},
        'reservas_7_dias': [],  # Lista de dict: {fecha, total}
        'incidencias_top': []   # Lista de dict: {recurso, total}
    }
    try:
        with get_cursor(dictionary=True) as cur:
            # Recursos breakdown
            cur.execute(
                """
                SELECT 
                  COUNT(*) AS total,
                  SUM(CASE WHEN estado='DISPONIBLE' THEN 1 ELSE 0 END) AS disponibles,
                  SUM(CASE WHEN estado='EN_MANTENIMIENTO' THEN 1 ELSE 0 END) AS mantenimiento,
                  SUM(CASE WHEN estado='FUERA_DE_SERVICIO' THEN 1 ELSE 0 END) AS fuera_servicio
                FROM recursos
                """
            )
            row = cur.fetchone()
            if row:
                data['recursos'] = {
                    'total': row['total'],
                    'disponibles': row['disponibles'],
                    'mantenimiento': row['mantenimiento'],
                    'fuera_servicio': row['fuera_servicio']
                }

            # Reservas últimos 7 días
            cur.execute(
                """
                SELECT fecha, COUNT(*) AS total
                FROM reservas
                WHERE fecha >= DATE_SUB(CURDATE(), INTERVAL 6 DAY)
                GROUP BY fecha
                ORDER BY fecha ASC
                """
            )
            data['reservas_7_dias'] = cur.fetchall() or []

            # Incidencias top por recurso (top 5)
            cur.execute(
                """
                SELECT r.nombre AS recurso, COUNT(i.id) AS total
                FROM incidencias i
                JOIN recursos r ON r.id = i.recurso_id
                GROUP BY r.nombre
                ORDER BY total DESC
                LIMIT 5
                """
            )
            data['incidencias_top'] = cur.fetchall() or []
    except Exception:
        # Silenciar error para evitar romper el dashboard
        pass
    return data


def formatear_chart_reservas(reservas_7_dias: List[Dict[str, Any]]) -> Tuple[List[str], List[int]]:
    labels = []
    valores = []
    for r in reservas_7_dias:
        # Convertir fecha de forma segura
        fecha_val = r.get('fecha', '')
        if hasattr(fecha_val, 'strftime'):
            labels.append(fecha_val.strftime('%d/%m'))
        elif callable(fecha_val):
            labels.append('')
        else:
            labels.append(str(fecha_val))
        
        # Convertir total de forma segura
        total_val = r.get('total', 0)
        if callable(total_val):
            valores.append(0)
        else:
            try:
                valores.append(int(total_val))
            except (ValueError, TypeError):
                valores.append(0)
    return labels, valores


def formatear_chart_incidencias(incidencias_top: List[Dict[str, Any]]) -> Tuple[List[str], List[int]]:
    labels = []
    valores = []
    for r in incidencias_top:
        # Convertir recurso de forma segura
        recurso_val = r.get('recurso', '')
        if callable(recurso_val):
            labels.append('')
        else:
            labels.append(str(recurso_val))
        
        # Convertir total de forma segura
        total_val = r.get('total', 0)
        if callable(total_val):
            valores.append(0)
        else:
            try:
                valores.append(int(total_val))
            except (ValueError, TypeError):
                valores.append(0)
    return labels, valores
