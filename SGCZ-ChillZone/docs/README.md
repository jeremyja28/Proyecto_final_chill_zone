# SGCZ - Chill Zone (PUCESA)

Sistema de Gestión para el Área Recreativa “Chill Zone” basado en Flask + MySQL + Bootstrap.

## Requisitos
- Python 3.10+
- MySQL (Laragon) en puerto 3307

## Configuración
1. Crea entorno y instala dependencias
```
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
```
2. Crea el archivo `.env` a partir de `.env.example` y ajusta variables si aplica.
3. Importa el esquema SQL en MySQL:
```
mysql -h localhost -P 3307 -u root < sql/chill_zone_schema.sql
```
4. Ejecuta la app:
```
python app.py
```

Credenciales demo:
- Admin: usuario "admin" / contraseña "admin123"
- Estudiante: correo "estu1@pucesa.edu.ec" / contraseña "estudiante123"

## Estructura
- `controllers/` Blueprints por módulo
- `services/` Reglas de negocio
- `repositories/` Acceso a datos (SQL preparado)
- `utils/` DB pool, seguridad, validadores, logger
- `templates/` Jinja2 + Bootstrap 5
- `sql/` Esquema y datos semilla
- `tests/` Pytest unitarios

## RNF y seguridad
- CSRF en formularios (Flask-WTF)
- Hash de contraseñas (bcrypt)
- Autorización por rol (decorador `role_required`)
- Ventana de mantenimiento (22h00–06h00)

## Cómo contribuir
- Estilo PEP8
- Principios SOLID en servicios/repositorios

## Logo
- Coloca tu archivo del logo como `static/img/logo_chill_zone.png`. Si no existe, se mostrará solo el texto de marca.
