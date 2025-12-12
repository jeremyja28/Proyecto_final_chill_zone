import os
import bcrypt
from functools import wraps
from flask import session, redirect, url_for, flash, request
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from config import Config


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def check_password(password: str, hashed: bytes) -> bool:
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed)
    except Exception:
        return False


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                flash('Debes iniciar sesión', 'warning')
                return redirect(url_for('auth.login', next=request.path))
            if roles and session.get('rol') not in roles:
                flash('No tienes permisos para acceder a esta sección', 'danger')
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        return wrapper
    return decorator


# Token utilities for password reset
_serializer = URLSafeTimedSerializer(Config.SECRET_KEY)


def generate_reset_token(email: str) -> str:
    return _serializer.dumps({'email': email})


def verify_reset_token(token: str, max_age_seconds: int = 3600):
    try:
        data = _serializer.loads(token, max_age=max_age_seconds)
        return data.get('email')
    except (SignatureExpired, BadSignature):
        return None
