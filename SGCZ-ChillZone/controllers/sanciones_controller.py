from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from utils.security import role_required
from services.sanciones_service import listar_sanciones, crear_sancion, levantar_sancion
from repositories.user_repository import list_users, buscar_usuarios


sanciones_bp = Blueprint('sanciones', __name__)


@sanciones_bp.route('/buscar_usuarios', methods=['GET'])
@role_required('ADMIN')
def buscar():
    q = request.args.get('q', '')
    if len(q) < 2:
        return jsonify([])
    users = buscar_usuarios(q)
    return jsonify(users)


@sanciones_bp.route('/', methods=['GET'])
@role_required('ADMIN')
def index():
    sanciones = listar_sanciones()
    usuarios = list_users(0, 200)
    return render_template('sanciones/index.html', sanciones=sanciones, usuarios=usuarios)


@sanciones_bp.route('/crear', methods=['POST'])
@role_required('ADMIN')
def crear():
    usuario_id = int(request.form.get('usuario_id')) if request.form.get('usuario_id') else 0
    motivo = request.form.get('motivo', '')
    tipo = request.form.get('tipo', 'LEVE')
    incidencia_id = int(request.form.get('incidencia_id')) if request.form.get('incidencia_id') else None
    ok, msg = crear_sancion(usuario_id, motivo, tipo, incidencia_id)
    flash(msg, 'success' if ok else 'danger')
    return redirect(url_for('sanciones.index'))


@sanciones_bp.route('/levantar/<int:sancion_id>', methods=['POST'])
@role_required('ADMIN')
def levantar(sancion_id: int):
    ok, msg = levantar_sancion(sancion_id)
    flash(msg, 'success' if ok else 'danger')
    return redirect(url_for('sanciones.index'))
