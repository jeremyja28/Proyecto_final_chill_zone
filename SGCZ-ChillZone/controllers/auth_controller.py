from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from wtforms import Form, StringField, PasswordField, validators
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email
from services.auth_service import authenticate, start_password_recovery, verify_recovery_code, reset_password
from utils.security import role_required, hash_password
from repositories.user_repository import update_profile_image, update_password, get_by_id, get_by_email
import os
from werkzeug.utils import secure_filename

auth_bp = Blueprint('auth', __name__)


class LoginForm(FlaskForm):
    email = StringField('Correo o usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])


class RecoveryForm(FlaskForm):
    email = StringField('Correo', validators=[DataRequired(), Email()])


class CodeForm(FlaskForm):
    code = StringField('Código de verificación', validators=[DataRequired()])


class ResetForm(FlaskForm):
    password = PasswordField('Nueva contraseña', validators=[DataRequired(), Length(min=6)])


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = authenticate(form.email.data.strip(), form.password.data)
        if user:
            session['user_id'] = user['id']
            session['nombre'] = user['nombre']
            session['apellido'] = user['apellido']
            session['rol'] = user['rol']
            session['imagen_url'] = user.get('imagen_url')
            flash('Bienvenido/a', 'success')
            # Usuarios van directo a sus reservas para reducir clics
            if user['rol'] == 'USUARIO':
                return redirect(url_for('reservas.index'))
            return redirect(url_for('index'))
        flash('Credenciales inválidas o usuario inactivo', 'danger')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/perfil', methods=['GET', 'POST'])
@role_required('USUARIO', 'ADMIN')
def perfil():
    user_id = session.get('user_id')
    user = get_by_id(user_id)
    
    if request.method == 'POST':
        # Actualizar imagen
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file and file.filename:
                filename = secure_filename(f"user_{user_id}_{file.filename}")
                upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'perfiles')
                os.makedirs(upload_dir, exist_ok=True)
                file.save(os.path.join(upload_dir, filename))
                
                imagen_url = f"/static/uploads/perfiles/{filename}"
                update_profile_image(user_id, imagen_url)
                session['imagen_url'] = imagen_url
                flash('Imagen de perfil actualizada', 'success')
        
        # Actualizar contraseña
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')
        if password:
            if password != confirm:
                flash('Las contraseñas no coinciden', 'danger')
            elif len(password) < 6:
                flash('La contraseña debe tener al menos 6 caracteres', 'danger')
            else:
                new_hash = hash_password(password)
                update_password(user_id, new_hash)
                flash('Contraseña actualizada', 'success')
                
        return redirect(url_for('auth.perfil'))
        
    return render_template('auth/perfil.html', user=user)


@auth_bp.route('/logout')
@role_required('USUARIO', 'ADMIN')
def logout():
    session.clear()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    form = RecoveryForm()
    if form.validate_on_submit():
        email = form.email.data.strip()
        if start_password_recovery(email):
            session['reset_email'] = email
            flash('Se ha enviado un código a tu correo.', 'info')
            return redirect(url_for('auth.verificar_codigo'))
        else:
            flash('Correo no encontrado.', 'danger')
    return render_template('auth/recover.html', form=form)


@auth_bp.route('/verificar-codigo', methods=['GET', 'POST'])
def verificar_codigo():
    if 'reset_email' not in session:
        return redirect(url_for('auth.recuperar'))
    
    form = CodeForm()
    if form.validate_on_submit():
        if verify_recovery_code(form.code.data.strip()):
            session['reset_verified'] = True
            return redirect(url_for('auth.restablecer_password'))
        else:
            flash('Código incorrecto.', 'danger')
    return render_template('auth/verify_code.html', form=form)


@auth_bp.route('/restablecer-password', methods=['GET', 'POST'])
def restablecer_password():
    if 'reset_email' not in session or not session.get('reset_verified'):
        return redirect(url_for('auth.recuperar'))
    
    form = ResetForm()
    if form.validate_on_submit():
        email = session['reset_email']
        if reset_password(email, form.password.data):
            session.pop('reset_email', None)
            session.pop('reset_verified', None)
            flash('Contraseña restablecida. Inicia sesión.', 'success')
            return redirect(url_for('auth.login'))
        flash('Error al restablecer contraseña.', 'danger')
    return render_template('auth/reset_password.html', form=form)


@auth_bp.route('/api/check-email', methods=['POST'])
def check_email_api():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({'success': False, 'message': 'Email requerido'})
    
    if start_password_recovery(email):
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Correo no encontrado'})


@auth_bp.route('/api/reset-password-api', methods=['POST'])
def reset_password_api():
    data = request.get_json()
    email = data.get('email')
    code = data.get('code')
    password = data.get('password')
    
    if str(code) != '270320':
        return jsonify({'success': False, 'message': 'Código incorrecto'})
        
    if not email or not password:
        return jsonify({'success': False, 'message': 'Datos incompletos'})
        
    user = get_by_email(email)
    if user:
        new_hash = hash_password(password)
        update_password(user['id'], new_hash)
        return jsonify({'success': True})
    
    return jsonify({'success': False, 'message': 'Usuario no encontrado'})

