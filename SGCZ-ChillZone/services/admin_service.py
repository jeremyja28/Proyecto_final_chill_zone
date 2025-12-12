from typing import Tuple, List
from datetime import datetime, timedelta
import secrets
import string
from repositories.user_repository import list_users, count_users, update_role, block_user, get_by_email, create_user, get_by_id, set_user_state, update_password
from repositories.config_repository import listar as conf_listar, guardar as conf_guardar, obtener as conf_obtener
from repositories.sancion_repository import listar_por_usuario
from repositories.reserva_repository import cancelar_por_bloqueo
from utils.security import hash_password
from utils.validators import is_valid_email


def listar_usuarios() -> List[dict]:
    return list_users(0, 100)


def actualizar_rol(user_id: int, rol: str) -> Tuple[bool, str]:
    if rol not in ('ADMIN', 'USUARIO'):
        return False, 'Rol inválido'
    update_role(user_id, rol)
    return True, 'Rol actualizado'


def bloquear_usuario(user_id: int) -> Tuple[bool, str]:
    usr = get_by_id(user_id)
    if not usr:
        return False, 'Usuario no encontrado'
    if usr.get('estado') == 'ACTIVO':
        set_user_state(user_id, 'BLOQUEADO')
        
        # Cancelar todas las reservas pendientes y activas del usuario
        canceladas = cancelar_por_bloqueo(user_id)
        
        mensaje = 'Usuario inactivado'
        if canceladas > 0:
            mensaje += f'. Se cancelaron {canceladas} reserva(s)'
        return True, mensaje
    else:
        # Verificar si tiene sanciones activas antes de activar
        sanciones = listar_por_usuario(user_id)
        _DURACIONES = {'LEVE': 3, 'GRAVE': 7, 'CRITICA': 14}
        
        for s in sanciones:
            if s.get('estado') == 'ACTIVA':
                tipo = s.get('tipo', 'LEVE')
                duracion = _DURACIONES.get(tipo, 3)
                creado = s.get('creado_en')
                if isinstance(creado, str):
                    creado = datetime.strptime(creado, '%Y-%m-%d %H:%M:%S')
                fin_estimado = creado + timedelta(days=duracion)
                
                # Si la sanción aún está vigente
                if datetime.now() < fin_estimado:
                    dias_restantes = (fin_estimado - datetime.now()).days + 1
                    return False, f'No se puede activar. El usuario tiene una sanción {tipo} activa con {dias_restantes} día(s) restante(s). Debe levantar la sanción primero.'
        
        set_user_state(user_id, 'ACTIVO')
        return True, 'Usuario activado'


def leer_config():
    rows = conf_listar()
    names = {r.get('nombre'): r for r in rows}
    # Asegurar claves importantes visibles en UI aunque no existan en DB
    defaults = {
        'horario_inicio': '07:00',
        'horario_fin': '22:00',
        'reserva_anticipacion_max_dias': '7',
        'reserva_duracion_min_min': '15',
        'reserva_duracion_max_min': '120',
    }
    for k, v in defaults.items():
        if k not in names:
            rows.append({'nombre': k, 'valor': v})
    return rows


def guardar_config(values: dict):
    for k, v in values.items():
        if isinstance(v, list):
            v = v[0]
        # Validar que sea numérico si es configuración de tiempos/días
        if k in ['reserva_anticipacion_max_dias', 'reserva_duracion_min_min', 'reserva_duracion_max_min']:
            if not str(v).isdigit():
                return False, f'El valor para {k} debe ser numérico'
        conf_guardar(k, v)
    return True, 'Parámetros del sistema guardados'


def registrar_usuario(nombre: str, apellido: str, correo: str, rol: str, password: str) -> Tuple[bool, str]:
    if not nombre or not apellido or not correo or not password:
        return False, 'Todos los campos son obligatorios'
    if not is_valid_email(correo):
        return False, 'Correo inválido'
    if rol not in ('ADMIN', 'USUARIO'):
        return False, 'Rol inválido'
    if len(password) < 8:
        return False, 'La contraseña debe tener al menos 8 caracteres'
    if get_by_email(correo):
        return False, 'Usuario ya registrado'
    pwd_hash = hash_password(password)
    create_user(nombre, apellido, correo, pwd_hash, rol=rol, estado='ACTIVO')
    return True, 'Usuario registrado'


def resetear_password_usuario(user_id: int) -> Tuple[bool, str]:
    usr = get_by_id(user_id)
    if not usr:
        return False, 'Usuario no encontrado'
    
    # Generar contraseña aleatoria
    alphabet = string.ascii_letters + string.digits
    new_password = ''.join(secrets.choice(alphabet) for i in range(10))
    
    pwd_hash = hash_password(new_password)
    update_password(user_id, pwd_hash)
    
    return True, f'Contraseña restablecida: {new_password}'
