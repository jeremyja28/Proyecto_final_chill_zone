from typing import Optional
from utils.security import check_password, hash_password, generate_reset_token, verify_reset_token
from repositories.user_repository import get_by_email, update_password, set_user_state
from repositories.sancion_repository import listar_por_usuario, levantar
from datetime import datetime, timedelta
from utils.logger import get_logger

logger = get_logger()


def authenticate(email: str, password: str) -> Optional[dict]:
    user = get_by_email(email)
    if not user:
        return None
    # Intentar levantar sanción expirada automáticamente
    if user.get('estado') != 'ACTIVO':
        sanciones = listar_por_usuario(user['id'])
        ahora = datetime.utcnow()
        for s in sanciones:
            if s.get('estado') == 'ACTIVA':
                # Calcular fin estimado según tipo
                tipo = s.get('tipo')
                dur = 3 if tipo == 'LEVE' else 7 if tipo == 'GRAVE' else 14 if tipo == 'CRITICA' else 0
                creado = s.get('creado_en')
                if isinstance(creado, str):
                    try:
                        creado_dt = datetime.strptime(creado.split('.')[0], '%Y-%m-%d %H:%M:%S')
                    except Exception:
                        creado_dt = ahora
                else:
                    creado_dt = creado or ahora
                if ahora >= creado_dt + timedelta(days=dur):
                    # Levantar sanción y activar usuario
                    levantar(s['id'])
                    set_user_state(user['id'], 'ACTIVO')
                    user['estado'] = 'ACTIVO'
        if user.get('estado') != 'ACTIVO':
            return None
    if check_password(password, user['hash_password'].encode('utf-8') if isinstance(user['hash_password'], str) else user['hash_password']):
        return user
    return None


def start_password_recovery(email: str) -> bool:
    user = get_by_email(email)
    if not user:
        return False
    # Simular envío de correo
    logger.info(f"Solicitud de recuperación para {email}. Código simulado enviado.")
    return True


def verify_recovery_code(code: str) -> bool:
    return code == '270320'


def reset_password(email: str, new_password: str) -> bool:
    user = get_by_email(email)
    if not user:
        return False
    new_hash = hash_password(new_password)
    update_password(user['id'], new_hash)
    logger.info(f"Contraseña restablecida para {email}")
    return True
