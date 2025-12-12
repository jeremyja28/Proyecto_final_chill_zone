from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.security import role_required
from services.admin_service import listar_usuarios, actualizar_rol, bloquear_usuario, leer_config, guardar_config, registrar_usuario, resetear_password_usuario
from services.reservas_service import listar_todas_reservas, cancelar_reserva_admin
from services.incidencias_service import crear_incidencia
from utils.audit import audit_log
from werkzeug.utils import secure_filename
import os
from flask import current_app
from datetime import datetime

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/', methods=['GET'])
@role_required('ADMIN')
def index():
    usuarios = listar_usuarios()
    return render_template('admin/usuarios.html', usuarios=usuarios)


@admin_bp.route('/config', methods=['GET'])
@role_required('ADMIN')
def configuracion():
    conf = leer_config()
    return render_template('admin/configuracion.html', config=conf)


@admin_bp.route('/rol/<int:user_id>', methods=['POST'])
@role_required('ADMIN')
def cambiar_rol(user_id: int):
    nuevo_rol = request.form.get('rol')
    ok, msg = actualizar_rol(user_id, nuevo_rol)
    flash(msg, 'success' if ok else 'danger')
    if ok:
        audit_log('CHANGE_ROLE', f'Usuario {user_id}', entity_id=user_id, details={'rol': nuevo_rol})
    return redirect(url_for('admin.index'))


@admin_bp.route('/bloquear/<int:user_id>', methods=['POST'])
@role_required('ADMIN')
def bloquear(user_id: int):
    ok, msg = bloquear_usuario(user_id)
    flash(msg, 'success' if ok else 'danger')
    if ok:
        audit_log('BLOCK_USER', f'Usuario {user_id}', entity_id=user_id)
    return redirect(url_for('admin.index'))


@admin_bp.route('/reset-password/<int:user_id>', methods=['POST'])
@role_required('ADMIN')
def reset_password(user_id: int):
    ok, msg = resetear_password_usuario(user_id)
    flash(msg, 'success' if ok else 'danger')
    if ok:
        audit_log('ADMIN_RESET_PASSWORD', f'Usuario {user_id}', entity_id=user_id)
    # Redirigir a la misma página para que el usuario vea el mensaje
    return redirect(request.referrer or url_for('admin.index'))


@admin_bp.route('/config/guardar', methods=['POST'])
@role_required('ADMIN')
def guardar_conf():
    form_values = dict(request.form)
    
    # Validación estricta: solo valores numéricos o formato de hora HH:MM
    import re
    errores = []
    for k, v in form_values.items():
        if k == 'csrf_token': continue
        
        # Si es horario (contiene 'horario' en el nombre), validar formato HH:MM
        if 'horario' in k:
            if not re.match(r'^\d{2}:\d{2}$', v):
                errores.append(f"El campo {k} debe tener formato HH:MM (ej: 07:00)")
        # Si no es horario, debe ser numérico
        else:
            if not v.isdigit():
                errores.append(f"El campo {k} debe ser un valor numérico entero")
    
    if errores:
        for e in errores:
            flash(e, 'danger')
        return redirect(url_for('admin.configuracion'))

    ok, msg = guardar_config(form_values)
    flash(msg, 'success' if ok else 'danger')
    if ok:
        audit_log('UPDATE_CONFIG', 'config_sistema', details=form_values)
    return redirect(url_for('admin.configuracion'))


@admin_bp.route('/usuarios/crear', methods=['POST'])
@role_required('ADMIN')
def crear_usuario():
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    correo = request.form.get('correo')
    rol = request.form.get('rol')
    password = request.form.get('password')
    ok, msg = registrar_usuario(nombre, apellido, correo, rol, password)
    flash(msg, 'success' if ok else 'danger')
    if ok:
        audit_log('CREATE_USER', correo, details={'nombre': nombre, 'apellido': apellido, 'rol': rol})
        return redirect(url_for('admin.index'))
    # En error: mantener valores ya ingresados
    usuarios = listar_usuarios()
    form_prefill = {'nombre': nombre, 'apellido': apellido, 'correo': correo, 'rol': rol}
    return render_template('admin/usuarios.html', usuarios=usuarios, form_prefill=form_prefill)


@admin_bp.route('/reservas', methods=['GET'])
@role_required('ADMIN')
def reservas():
    todas_reservas = listar_todas_reservas()
    return render_template('admin/reservas.html', reservas=todas_reservas)


@admin_bp.route('/reservas/cancelar/<int:reserva_id>', methods=['POST'])
@role_required('ADMIN')
def cancelar_reserva(reserva_id: int):
    ok, msg = cancelar_reserva_admin(reserva_id)
    flash(msg, 'success' if ok else 'danger')
    if ok:
        audit_log('ADMIN_CANCEL_RESERVA', f'Reserva {reserva_id}', entity_id=reserva_id)
    return redirect(url_for('admin.reservas'))


@admin_bp.route('/reservas/incidencia', methods=['POST'])
@role_required('ADMIN')
def crear_incidencia_admin():
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
    if ok:
        audit_log('ADMIN_CREATE_INCIDENCIA', f'Incidencia en reserva {reserva_id}', entity_id=reserva_id)
    return redirect(url_for('admin.reservas'))
