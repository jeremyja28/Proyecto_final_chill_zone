from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from utils.security import role_required
from services.incidencias_service import (
    listar_incidencias_usuario, listar_incidencias_admin, recursos_disponibles, crear_incidencia, toggle_estado_incidencia
)
from config import Config

incidencias_bp = Blueprint('incidencias', __name__)


@incidencias_bp.route('/', methods=['GET'])
@role_required('USUARIO', 'ADMIN')
def index():
    # Admin ve todas; usuario ve las propias
    from flask import session
    if session.get('rol') == 'ADMIN':
        incidencias = listar_incidencias_admin()
    else:
        incidencias = listar_incidencias_usuario()
    recursos = recursos_disponibles()
    return render_template('incidencias/index.html', incidencias=incidencias, recursos=recursos)


@incidencias_bp.route('/crear', methods=['POST'])
@role_required('USUARIO', 'ADMIN')
def crear():
    from datetime import datetime
    from flask import current_app
    recurso_id = int(request.form.get('recurso_id')) if request.form.get('recurso_id') else 0
    reserva_id = int(request.form.get('reserva_id')) if request.form.get('reserva_id') else None
    descripcion = request.form.get('descripcion', '')
    evidencia_url = request.form.get('evidencia_url', '')
    
    # Si viene archivo, guardarlo con nombre único
    file = request.files.get('evidencia_file')
    if file and file.filename:
        filename = secure_filename(file.filename)
        # Crear nombre único: fecha_hora_nombreoriginal
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'incidencias')
        os.makedirs(upload_dir, exist_ok=True)
        save_path = os.path.join(upload_dir, unique_filename)
        file.save(save_path)
        evidencia_url = f"/static/uploads/incidencias/{unique_filename}"
    
    ok, msg = crear_incidencia(recurso_id, descripcion, evidencia_url, reserva_id=reserva_id)
    flash(msg, 'success' if ok else 'danger')
    return redirect(url_for('incidencias.index'))

@incidencias_bp.route('/estado/<int:incidencia_id>', methods=['POST'])
@role_required('ADMIN')
def cambiar_estado(incidencia_id: int):
    ok, msg = toggle_estado_incidencia(incidencia_id)
    flash(msg, 'success' if ok else 'danger')
    return redirect(url_for('incidencias.index'))
