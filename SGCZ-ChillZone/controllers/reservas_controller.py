from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime, timedelta
from utils.security import role_required
from services.reservas_service import (
    consultar_disponibilidad, crear_reserva, modificar_reserva,
    cancelar_reserva, listar_reservas_usuario
)
from services.recursos_service import listar_recursos
from services.zonas_service import listar_zonas
import repositories.config_repository as conf_repo
import repositories.user_repository as user_repo
import repositories.reserva_repository as reserva_repo
from services.incidencias_service import crear_incidencia

reservas_bp = Blueprint('reservas', __name__)


@reservas_bp.route('/', methods=['GET'])
@role_required('USUARIO', 'ADMIN')
def index():
    from datetime import time as dt_time
    reservas = listar_reservas_usuario()
    ahora = datetime.now()
    
    # Agregar acompañantes y calcular estado dinámico para cada reserva
    for r in reservas:
        r['acompanantes'] = reserva_repo.listar_acompanantes(r['id'])
        
        # Calcular estado dinámico basado en fecha/hora actual
        if r['estado'] in ['PENDIENTE', 'ACTIVA']:
            try:
                import datetime as dt_module
                fecha_reserva = r['fecha'] if isinstance(r['fecha'], dt_module.date) else datetime.strptime(str(r['fecha']), '%Y-%m-%d').date()
                
                # Parsear hora_inicio
                hora_inicio = r['hora_inicio']
                if isinstance(hora_inicio, timedelta):
                    total_sec = int(hora_inicio.total_seconds())
                    hora_inicio_time = dt_time(hour=total_sec // 3600, minute=(total_sec % 3600) // 60)
                else:
                    hora_str = str(hora_inicio)[:5]
                    hora_inicio_time = datetime.strptime(hora_str, '%H:%M').time()

                # Parsear hora_fin
                hora_fin = r['hora_fin']
                if isinstance(hora_fin, timedelta):
                    total_sec = int(hora_fin.total_seconds())
                    hora_fin_time = dt_time(hour=total_sec // 3600, minute=(total_sec % 3600) // 60)
                else:
                    hora_str = str(hora_fin)[:5]
                    hora_fin_time = datetime.strptime(hora_str, '%H:%M').time()
                
                # Combinar fecha y hora
                datetime_inicio = datetime.combine(fecha_reserva, hora_inicio_time)
                datetime_fin = datetime.combine(fecha_reserva, hora_fin_time)
                
                # Determinar estado real
                if ahora < datetime_inicio:
                    r['estado'] = 'PENDIENTE'
                elif ahora >= datetime_inicio and ahora < datetime_fin:
                    r['estado'] = 'ACTIVA'
                elif ahora >= datetime_fin:
                    r['estado'] = 'FINALIZADA'
            except Exception as e:
                print(f"Error calculando estado para reserva {r['id']}: {e}")
                import traceback
                traceback.print_exc()
    
    # Mostrar incidencias recientes del usuario para confirmar persistencia
    try:
        from services.incidencias_service import listar_incidencias_usuario
        incidencias = listar_incidencias_usuario()[:5]
    except Exception:
        incidencias = []
    return render_template('reservas/index.html', reservas=reservas, incidencias=incidencias)


@reservas_bp.route('/disponibilidad', methods=['GET', 'POST'])
@role_required('USUARIO', 'ADMIN')
def disponibilidad():
    data = None
    recursos = [r for r in listar_recursos() if r.get('eliminado') == 0 and r.get('estado') == 'DISPONIBLE']
    zonas = listar_zonas()
    
    elegido = None
    zona_sel = request.form.get('zona') if request.method == 'POST' else None
    # Navegación por días (prev/next) y fecha por defecto (hoy si no se envía)
    recurso_id = 0
    fecha = None
    hoy = datetime.now().date()
    max_fecha = hoy + timedelta(days=7)
    if request.method == 'POST':
        recurso_id = int(request.form.get('recurso_id')) if request.form.get('recurso_id') else 0
        fecha = request.form.get('fecha') or datetime.now().strftime('%Y-%m-%d')
        nav = request.form.get('nav')  # valores esperados 'prev' | 'next' | 'today'
        # Mantener zona seleccionada si se pasó como hidden
        if not zona_sel:
            zona_sel = request.form.get('zona_hidden')
        if nav in ('prev','next'):
            try:
                base = datetime.strptime(fecha, '%Y-%m-%d').date()
                delta = -1 if nav == 'prev' else 1
                nueva = base + timedelta(days=delta)
                # saltar domingo automáticamente en navegación
                if nueva.weekday() == 6:  # domingo
                    nueva = nueva + timedelta(days=delta)
                # acotar a ventana [hoy, hoy+7]
                if nueva < hoy:
                    nueva = hoy
                if nueva > max_fecha:
                    nueva = max_fecha
                    # si cae domingo, retroceder al sábado
                    if nueva.weekday() == 6:
                        nueva = nueva - timedelta(days=1)
                fecha = nueva.strftime('%Y-%m-%d')
            except Exception:
                fecha = datetime.now().strftime('%Y-%m-%d')
        elif nav == 'today':
            # Ir a hoy; si hoy es domingo, avanzar a lunes
            nueva = hoy
            if nueva.weekday() == 6:
                nueva = nueva + timedelta(days=1)
            # Clamp por seguridad al rango permitido
            if nueva > max_fecha:
                nueva = max_fecha
                if nueva.weekday() == 6:
                    nueva = nueva - timedelta(days=1)
            fecha = nueva.strftime('%Y-%m-%d')
        elegido = recurso_id
        # Validación de fecha no pasada
        try:
            f = datetime.strptime(fecha, '%Y-%m-%d').date()
            if f < datetime.now().date():
                flash('La fecha no puede ser anterior a hoy', 'warning')
            else:
                data = consultar_disponibilidad(recurso_id, fecha)
                if not data.get('recurso'):
                    flash('Recurso inválido', 'danger')
                    data = None
        except Exception:
            flash('Fecha inválida', 'danger')
    # Parámetros configurables para la UI (duración y horario)
    try:
        dur_min = int((conf_repo.obtener('reserva_duracion_min_min') or {}).get('valor', 15))
    except Exception:
        dur_min = 15
    try:
        dur_max = int((conf_repo.obtener('reserva_duracion_max_min') or {}).get('valor', 120))
    except Exception:
        dur_max = 120
    hora_ini_ui = (conf_repo.obtener('horario_inicio') or {}).get('valor', '07:00')
    hora_fin_ui = (conf_repo.obtener('horario_fin') or {}).get('valor', '22:00')

    # Listar usuarios activos para selección de acompañantes
    usuarios_activos = user_repo.listar_activos()
    
    return render_template(
        'reservas/disponibilidad.html',
        data=data,
        recursos=recursos,
        zonas=zonas,
        zona_sel=zona_sel,
        elegido=elegido,
        fecha_actual=fecha or datetime.now().strftime('%Y-%m-%d'),
        hoy_str=hoy.strftime('%Y-%m-%d'),
        max_fecha=(hoy + timedelta(days=7)),
        max_fecha_str=(hoy + timedelta(days=7)).strftime('%Y-%m-%d'),
        dur_min=dur_min,
        dur_max=dur_max,
        hora_ini_ui=hora_ini_ui,
        hora_fin_ui=hora_fin_ui,
        now_iso=datetime.now().isoformat(),
        usuarios_activos=usuarios_activos
    )


@reservas_bp.route('/crear', methods=['POST'])
@role_required('USUARIO', 'ADMIN')
def crear():
    recurso_id = int(request.form.get('recurso_id'))
    fecha = request.form.get('fecha')
    hora_inicio = request.form.get('hora_inicio')
    hora_fin = request.form.get('hora_fin')
    
    # Capturar acompañantes (IDs de usuarios)
    acompanantes_ids = request.form.getlist('acompanantes')
    acompanantes = [int(uid) for uid in acompanantes_ids if uid.isdigit()]
    
    ok, msg = crear_reserva(recurso_id, fecha, hora_inicio, hora_fin, acompanantes)
    flash(msg, 'success' if ok else 'danger')
    
    # Si hay error, volver a mostrar la disponibilidad con los datos
    if not ok:
        data = consultar_disponibilidad(recurso_id, fecha)
        recursos = [r for r in listar_recursos() if r.get('eliminado') == 0 and r.get('estado') == 'DISPONIBLE']
        zonas = sorted({ r.get('zona_nombre','') for r in recursos if r.get('zona_nombre') })
        
        # Obtener zona del recurso seleccionado
        zona_sel = None
        for r in recursos:
            if r.get('id') == recurso_id:
                zona_sel = r.get('zona_nombre')
                break
        
        hoy = datetime.now().date()
        try:
            dur_min = int((conf_repo.obtener('reserva_duracion_min_min') or {}).get('valor', 15))
        except:
            dur_min = 15
        try:
            dur_max = int((conf_repo.obtener('reserva_duracion_max_min') or {}).get('valor', 120))
        except:
            dur_max = 120
        hora_ini_ui = (conf_repo.obtener('horario_inicio') or {}).get('valor', '07:00')
        hora_fin_ui = (conf_repo.obtener('horario_fin') or {}).get('valor', '22:00')
        
        usuarios_activos = user_repo.listar_activos()
        
        return render_template(
            'reservas/disponibilidad.html',
            data=data,
            recursos=recursos,
            zonas=zonas,
            zona_sel=zona_sel,
            elegido=recurso_id,
            fecha_actual=fecha,
            hoy_str=hoy.strftime('%Y-%m-%d'),
            max_fecha=(hoy + timedelta(days=7)),
            max_fecha_str=(hoy + timedelta(days=7)).strftime('%Y-%m-%d'),
            dur_min=dur_min,
            dur_max=dur_max,
            hora_ini_ui=hora_ini_ui,
            hora_fin_ui=hora_fin_ui,
            now_iso=datetime.now().isoformat(),
            form_data={'hora_inicio': hora_inicio, 'hora_fin': hora_fin},
            usuarios_activos=usuarios_activos
        )
    
    return redirect(url_for('reservas.index'))


@reservas_bp.route('/modificar/<int:reserva_id>', methods=['POST'])
@role_required('USUARIO', 'ADMIN')
def modificar(reserva_id: int):
    hora_inicio = request.form.get('hora_inicio')
    hora_fin = request.form.get('hora_fin')
    ok, msg = modificar_reserva(reserva_id, hora_inicio, hora_fin)
    flash(msg, 'success' if ok else 'danger')
    return redirect(url_for('reservas.index'))


@reservas_bp.route('/cancelar/<int:reserva_id>', methods=['POST'])
@role_required('USUARIO', 'ADMIN')
def cancelar(reserva_id: int):
    ok, msg = cancelar_reserva(reserva_id)
    flash(msg, 'success' if ok else 'danger')
    return redirect(url_for('reservas.index'))


@reservas_bp.route('/incidencia', methods=['POST'])
@role_required('USUARIO', 'ADMIN')
def crear_incidencia_desde_reserva():
    from datetime import datetime
    from werkzeug.utils import secure_filename
    from flask import current_app
    import os
    
    recurso_id = int(request.form.get('recurso_id')) if request.form.get('recurso_id') else 0
    reserva_id = int(request.form.get('reserva_id')) if request.form.get('reserva_id') else None
    descripcion = request.form.get('descripcion', '')
    evidencia_url = request.form.get('evidencia_url', '')
    
    # Si viene archivo, guardarlo con nombre único
    file = request.files.get('evidencia_file')
    if file and file.filename:
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'incidencias')
        os.makedirs(upload_dir, exist_ok=True)
        save_path = os.path.join(upload_dir, unique_filename)
        file.save(save_path)
        evidencia_url = f"/static/uploads/incidencias/{unique_filename}"
    
    # Capturar múltiples responsables
    responsables_ids_raw = request.form.getlist('responsables')
    responsables_ids = [int(uid) for uid in responsables_ids_raw if uid.isdigit()]
    
    ok, msg = crear_incidencia(recurso_id, descripcion, evidencia_url, responsables_ids if responsables_ids else None, reserva_id=reserva_id)
    flash(msg, 'success' if ok else 'danger')
    return redirect(url_for('reservas.index'))


@reservas_bp.route('/acompanantes/<int:reserva_id>', methods=['GET'])
@role_required('USUARIO', 'ADMIN')
def obtener_acompanantes_json(reserva_id: int):
    """Endpoint para obtener titular y acompañantes de una reserva (para dropdown de responsable)."""
    from flask import jsonify
    reserva = reserva_repo.obtener_con_acompanantes(reserva_id)
    if not reserva:
        return jsonify({'error': 'Reserva no encontrada'}), 404
    
    # Obtener titular
    titular = user_repo.get_by_id(reserva['usuario_id'])
    acompanantes = reserva.get('acompanantes', [])
    
    usuarios = []
    if titular:
        usuarios.append({'id': titular['id'], 'nombre': titular['nombre']})
    for acomp in acompanantes:
        usuarios.append({'id': acomp['usuario_id'], 'nombre': acomp['nombre']})
    
    return jsonify({'usuarios': usuarios})
