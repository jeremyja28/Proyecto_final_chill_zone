import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'change-me')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')

    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', '3307'))
    DB_NAME = os.getenv('DB_NAME', 'chill_zone_db')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')

    # Session Security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = False  # Cambiar a True en producción con HTTPS
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)


    # CSRF
    WTF_CSRF_TIME_LIMIT = None

    # Pagination
    PAGE_SIZE_DEFAULT = 10

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')
