from flask import Blueprint, render_template, request, Response
from utils.security import role_required
from services.reportes_service import resumen_uso, exportar_csv, reservas_historial
from services.estadisticas_service import resumen_general
import json

reportes_bp = Blueprint('reportes', __name__)


@reportes_bp.route('/', methods=['GET'])
@role_required('ADMIN')
def index():
    usuario_id = request.args.get('usuario_id')
    usuario_filtro = None
    
    if usuario_id:
        try:
            usuario_id = int(usuario_id)
            from repositories.user_repository import get_by_id
            user = get_by_id(usuario_id)
            if user:
                usuario_filtro = user  # Pass the whole user object or dict
        except ValueError:
            usuario_id = None

    # Datos de reportes (uso)
    data_uso = resumen_uso(usuario_id)
    
    # Datos de estadísticas (general)
    data_stats = resumen_general()
    
    return render_template('reportes/index.html', data=data_uso, stats=data_stats, usuario_filtro=usuario_filtro)


@reportes_bp.route('/exportar', methods=['GET'])
@role_required('ADMIN')
def exportar():
    csv_data = exportar_csv()
    return Response(
        csv_data,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment;filename=reportes.csv'}
    )

@reportes_bp.route('/reservas', methods=['GET'])
@role_required('ADMIN')
def reservas_hist():
    f_ini = request.args.get('fecha_ini') or None
    f_fin = request.args.get('fecha_fin') or None
    estado = request.args.get('estado') or None
    rows = reservas_historial(f_ini, f_fin, estado)
    return render_template('reportes/reservas.html', reservas=rows, fecha_ini=f_ini, fecha_fin=f_fin, estado=estado)
