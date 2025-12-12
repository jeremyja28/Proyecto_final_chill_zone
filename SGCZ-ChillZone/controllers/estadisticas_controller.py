from flask import Blueprint, render_template
from utils.security import role_required
from services.estadisticas_service import resumen_general
import json

estadisticas_bp = Blueprint('estadisticas', __name__)

@estadisticas_bp.route('/', methods=['GET'])
@role_required('ADMIN')
def index():
    data = resumen_general()
    
    # Procesar datos de reservas de forma ultra-segura
    reservas_labels = []
    reservas_values = []
    for r in data.get('reservas_7_dias', []):
        # Procesar fecha
        fecha = r.get('fecha', '')
        if hasattr(fecha, 'strftime'):
            reservas_labels.append(fecha.strftime('%d/%m'))
        else:
            reservas_labels.append(str(fecha) if fecha else '')
        
        # Procesar total
        total = r.get('total', 0)
        try:
            reservas_values.append(int(total) if total else 0)
        except:
            reservas_values.append(0)
    
    # Procesar datos de incidencias de forma ultra-segura
    incidencias_labels = []
    incidencias_values = []
    for i in data.get('incidencias_top', []):
        # Procesar recurso
        recurso = i.get('recurso', '')
        incidencias_labels.append(str(recurso) if recurso else '')
        
        # Procesar total
        total = i.get('total', 0)
        try:
            incidencias_values.append(int(total) if total else 0)
        except:
            incidencias_values.append(0)
    
    # Convertir todo a JSON string directamente aquí para evitar problemas en template
    chart_data = {
        'reservas': {
            'labels': json.dumps(reservas_labels),
            'values': json.dumps(reservas_values)
        },
        'incidencias': {
            'labels': json.dumps(incidencias_labels),
            'values': json.dumps(incidencias_values)
        }
    }
    return render_template('estadisticas/index.html', data=data, chart_data=chart_data)
