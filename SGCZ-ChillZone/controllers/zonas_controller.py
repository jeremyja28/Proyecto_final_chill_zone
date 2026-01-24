from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from utils.security import role_required
from services.zonas_service import (
    listar_zonas, crear_zona, actualizar_zona, eliminar_zona, 
    deshabilitar_zona, habilitar_zona, obtener_zona, obtener_recursos_restaurables
)
from utils.file_uploader import save_file

zonas_bp = Blueprint('zonas', __name__)


@zonas_bp.route('/', methods=['GET'])
@role_required('ADMIN')
def index():
    # Admin siempre ve todas las zonas (incluidas deshabilitadas)
    zonas = listar_zonas(incluir_deshabilitados=True)
    return render_template('zonas/index.html', zonas=zonas)


@zonas_bp.route('/crear', methods=['POST'])
@role_required('ADMIN')
def crear():
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    
    imagen = request.files.get('imagen')
    imagen_url = save_file(imagen, 'zonas') if imagen else None
    
    ok, msg = crear_zona(nombre, descripcion, imagen_url)
    flash(msg, 'success' if ok else 'danger')
    return redirect(request.referrer or url_for('zonas.index'))


@zonas_bp.route('/editar/<int:zona_id>', methods=['POST'])
@role_required('ADMIN')
def editar(zona_id):
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    
    imagen = request.files.get('imagen')
    imagen_url = save_file(imagen, 'zonas') if imagen else None
    
    ok, msg = actualizar_zona(zona_id, nombre, descripcion, imagen_url)
    flash(msg, 'success' if ok else 'danger')
    return redirect(url_for('zonas.index'))


@zonas_bp.route('/deshabilitar/<int:zona_id>', methods=['POST'])
@role_required('ADMIN')
def deshabilitar(zona_id):
    """Deshabilita una zona con efecto cascada en recursos y reservas."""
    ok, msg, _ = deshabilitar_zona(zona_id)
    flash(msg, 'success' if ok else 'danger')
    return redirect(url_for('zonas.index'))


@zonas_bp.route('/habilitar/<int:zona_id>', methods=['POST'])
@role_required('ADMIN')
def habilitar(zona_id):
    """Habilita una zona, opcionalmente restaurando recursos."""
    restaurar = request.form.get('restaurar_recursos') == 'true'
    ok, msg = habilitar_zona(zona_id, restaurar_recursos=restaurar)
    flash(msg, 'success' if ok else 'danger')
    return redirect(url_for('zonas.index'))


@zonas_bp.route('/recursos-restaurables/<int:zona_id>', methods=['GET'])
@role_required('ADMIN')
def recursos_restaurables(zona_id):
    """API endpoint para obtener recursos que pueden restaurarse al habilitar zona."""
    recursos = obtener_recursos_restaurables(zona_id)
    return jsonify({
        'zona_id': zona_id,
        'recursos': [{'id': r['id'], 'nombre': r['nombre']} for r in recursos],
        'count': len(recursos)
    })


@zonas_bp.route('/obtener/<int:zona_id>', methods=['GET'])
@role_required('ADMIN')
def obtener(zona_id):
    """API endpoint para obtener datos de zona (para modal AJAX)."""
    zona = obtener_zona(zona_id)
    if zona:
        return jsonify({
            'id': zona.get('id'),
            'nombre': zona.get('nombre'),
            'descripcion': zona.get('descripcion'),
            'imagen_url': zona.get('imagen_url'),
            'eliminado': zona.get('eliminado', 0)
        })
    return jsonify({'error': 'Zona no encontrada'}), 404


@zonas_bp.route('/eliminar/<int:zona_id>', methods=['POST'])
@role_required('ADMIN')
def eliminar(zona_id):
    """Eliminación física - no recomendado, usar deshabilitar en su lugar."""
    ok, msg = eliminar_zona(zona_id)
    flash(msg, 'success' if ok else 'danger')
    return redirect(url_for('zonas.index'))
