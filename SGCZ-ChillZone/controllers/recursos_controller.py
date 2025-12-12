from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.security import role_required
from services.recursos_service import listar_recursos, crear_recurso, editar_recurso, eliminar_recurso, cambiar_estado
from services.zonas_service import listar_zonas
from utils.audit import audit_log
from utils.file_uploader import save_file

recursos_bp = Blueprint('recursos', __name__)


@recursos_bp.route('/', methods=['GET'])
@role_required('USUARIO', 'ADMIN')
def index():
    recursos = listar_recursos()
    zonas = listar_zonas()
    return render_template('recursos/index.html', recursos=recursos, zonas=zonas)


@recursos_bp.route('/crear', methods=['POST'])
@role_required('ADMIN')
def crear():
    imagen = request.files.get('imagen')
    imagen_url = save_file(imagen, 'recursos') if imagen else None

    data = {
        'nombre': request.form.get('nombre'),
        'tipo': request.form.get('tipo'),
        'ubicacion': request.form.get('ubicacion'),
        'zona_id': request.form.get('zona_id'),
        'imagen_url': imagen_url
    }
    ok, msg = crear_recurso(data)
    flash(msg, 'success' if ok else 'danger')
    if ok:
        audit_log('CREATE_RESOURCE', data.get('nombre'), details=data)
    return redirect(url_for('recursos.index'))


@recursos_bp.route('/editar/<int:recurso_id>', methods=['POST'])
@role_required('ADMIN')
def editar(recurso_id: int):
    imagen = request.files.get('imagen')
    imagen_url = save_file(imagen, 'recursos') if imagen else None

    data = {
        'nombre': request.form.get('nombre'),
        'tipo': request.form.get('tipo'),
        'ubicacion': request.form.get('ubicacion'),
        'zona_id': request.form.get('zona_id'),
        'imagen_url': imagen_url
    }
    ok, msg = editar_recurso(recurso_id, data)
    flash(msg, 'success' if ok else 'danger')
    if ok:
        audit_log('EDIT_RESOURCE', data.get('nombre'), entity_id=recurso_id, details=data)
    return redirect(url_for('recursos.index'))


@recursos_bp.route('/eliminar/<int:recurso_id>', methods=['POST'])
@role_required('ADMIN')
def eliminar(recurso_id: int):
    ok, msg = eliminar_recurso(recurso_id)
    flash(msg, 'success' if ok else 'danger')
    if ok:
        audit_log('DELETE_RESOURCE', f'Recurso {recurso_id}', entity_id=recurso_id)
    return redirect(url_for('recursos.index'))


@recursos_bp.route('/estado/<int:recurso_id>', methods=['POST'])
@role_required('ADMIN')
def estado(recurso_id: int):
    nuevo_estado = request.form.get('estado')
    # Opcionales: rango de mantenimiento
    mant_inicio = request.form.get('mant_inicio')  # YYYY-MM-DDTHH:MM format from datetime-local
    mant_fin = request.form.get('mant_fin')
    # Convert to SQL datetime format if provided
    if mant_inicio:
        mant_inicio = mant_inicio.replace('T', ' ') + ':00'
    if mant_fin:
        mant_fin = mant_fin.replace('T', ' ') + ':00'
    ok, msg = cambiar_estado(recurso_id, nuevo_estado, mant_inicio, mant_fin)
    flash(msg, 'success' if ok else 'danger')
    if ok:
        details = {'estado': nuevo_estado, 'resultado': msg}
        if mant_inicio and mant_fin:
            details['mant_inicio'] = mant_inicio
            details['mant_fin'] = mant_fin
        audit_log('CHANGE_RESOURCE_STATE', f'Recurso {recurso_id}', entity_id=recurso_id, details=details)
    return redirect(url_for('recursos.index'))
