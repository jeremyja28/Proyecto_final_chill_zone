import os
import time as _time
from datetime import time, datetime
from flask import Flask, render_template, redirect, url_for, session, g, request, flash
from flask_wtf import CSRFProtect
from dotenv import load_dotenv

from config import Config
from utils.logger import get_logger

# Blueprints (registered below)
from controllers.auth_controller import auth_bp
from controllers.reservas_controller import reservas_bp
from controllers.recursos_controller import recursos_bp
from controllers.reportes_controller import reportes_bp
from controllers.admin_controller import admin_bp
from controllers.incidencias_controller import incidencias_bp
from controllers.sanciones_controller import sanciones_bp
from controllers.estadisticas_controller import estadisticas_bp
from controllers.zonas_controller import zonas_bp
from utils.performance import record, avg_ms

csrf = CSRFProtect()
logger = get_logger()

def create_app():
    load_dotenv()
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(Config())
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Límite 16MB para archivos

    # CSRF
    csrf.init_app(app)

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(reservas_bp, url_prefix='/reservas')
    app.register_blueprint(recursos_bp, url_prefix='/recursos')
    app.register_blueprint(reportes_bp, url_prefix='/reportes')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(incidencias_bp, url_prefix='/incidencias')
    app.register_blueprint(sanciones_bp, url_prefix='/sanciones')
    app.register_blueprint(estadisticas_bp, url_prefix='/estadisticas')
    app.register_blueprint(zonas_bp, url_prefix='/zonas')

    @app.before_request
    def maintenance_window_guard():
        # start timing
        g._start = _time.perf_counter()
        # Block non-admin mutating actions during maintenance window 22:00-06:00
        # Allow static, login, logout, read-only GET requests
        try:
            # Mantenimiento deshabilitado temporalmente para pruebas
            pass
            # now = datetime.now().time()
            # in_maintenance = (time(22, 0) <= now) or (now <= time(6, 0))
            # path = request.path
            # is_admin = session.get('rol') == 'ADMIN'
            # method = request.method
            # if in_maintenance and not is_admin:
            #     # allow safe reads
            #     if method != 'GET':
            #         flash('El sistema está en mantenimiento programado (22h00–06h00). Intenta más tarde.', 'warning')
            #         return redirect(url_for('auth.login'))
        except Exception:
            # Always fail open to avoid blocking
            pass

    @app.after_request
    def perf_after(resp):
        try:
            if hasattr(g, '_start'):
                duration_ms = (_time.perf_counter() - g._start) * 1000.0
                record(duration_ms)
        except Exception:
            pass
        return resp

    @app.context_processor
    def inject_globals():
        return {
            'current_user': {
                'id': session.get('user_id'),
                'nombre': session.get('nombre'),
                'apellido': session.get('apellido'),
                'rol': session.get('rol'),
                'imagen_url': session.get('imagen_url')
            },
            'perf_avg_ms': round(avg_ms(), 1),
            'current_year': datetime.now().year
        }

    @app.route('/')
    def index():
        if not session.get('user_id'):
            return render_template('landing.html')
        # Render role-based dashboard (AdminLTE) with real metrics service, fallback seguro
        rol = session.get('rol')
        try:
            from services.metrics_service import admin_metrics, user_stats
            if rol == 'ADMIN':
                metrics, recientes_incidencias, chart_data = admin_metrics()
                return render_template('dashboard/admin.html', metrics=metrics, recientes_incidencias=recientes_incidencias, chart_data=chart_data)
            else:
                # Para usuarios, ir directo a sus reservas para ahorrar clics
                return redirect(url_for('reservas.index'))
        except Exception:
            # Si falla (ej. DB no inicializada), mostrar plantilla básica
            return render_template('layouts/home.html')

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('partials/error.html', code=403, message='Acceso denegado'), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template('partials/error.html', code=404, message='Página no encontrada'), 404

    @app.errorhandler(500)
    def server_error(e):
        logger.exception('Error interno del servidor')
        return redirect(url_for('auth.login'))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=os.environ.get('FLASK_ENV') == 'development')
