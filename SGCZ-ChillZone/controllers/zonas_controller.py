from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.security import role_required
from services.zonas_service import listar_zonas, crear_zona, actualizar_zona, eliminar_zona
from utils.file_uploader import save_file

zonas_bp = Blueprint('zonas', __name__)

@zonas_bp.route('/', methods=['GET'])
@role_required('ADMIN')
def index():
    zonas = listar_zonas()
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

@zonas_bp.route('/eliminar/<int:zona_id>', methods=['POST'])
@role_required('ADMIN')
def eliminar(zona_id):
    ok, msg = eliminar_zona(zona_id)
    flash(msg, 'success' if ok else 'danger')
    return redirect(url_for('zonas.index'))
