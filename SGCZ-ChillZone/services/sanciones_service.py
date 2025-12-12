from typing import List, Tuple
from datetime import datetime, timedelta
from flask import session
from repositories.sancion_repository import listar as repo_listar, crear as repo_crear, levantar as repo_levantar
from repositories.user_repository import get_by_id, set_user_state
from repositories.reserva_repository import cancelar_por_sancion

_DURACIONES = {
    'LEVE': 3,      # días
    'GRAVE': 7,
    'CRITICA': 14
}

def _fin_sancion(creado_en: datetime, tipo: str) -> datetime:
    dias = _DURACIONES.get(tipo, 0)
    return creado_en + timedelta(days=dias)

def listar_sanciones() -> List[dict]:
    rows = repo_listar()
    ahora = datetime.utcnow()
    for r in rows:
        creado = r.get('creado_en')
        tipo = r.get('tipo')
        if isinstance(creado, str):
            # MySQL timestamp string -> parse simple
            try:
                creado_dt = datetime.strptime(creado.split('.')[0], '%Y-%m-%d %H:%M:%S')
            except Exception:
                creado_dt = datetime.utcnow()
        else:
            creado_dt = creado or datetime.utcnow()
        fin = _fin_sancion(creado_dt, tipo)
        r['fin_estimado'] = fin.strftime('%Y-%m-%d')
        # Calcular días restantes (si ya pasó => 0)
        dias_rest = (fin.date() - ahora.date()).days
        r['dias_restantes'] = dias_rest if dias_rest > 0 else 0
        if r.get('estado') == 'ACTIVA':
            if ahora >= fin:
                # Auto levantar
                repo_levantar(r['id'])
                set_user_state(r['usuario_id'], 'ACTIVO')
                r['estado'] = 'LEVANTADA'
                r['estado_display'] = 'Culminada'
            else:
                r['estado_display'] = 'En curso'
        else:
            r['estado_display'] = 'Culminada'
    return rows


def crear_sancion(usuario_id: int, motivo: str, tipo: str, incidencia_id: int = None) -> Tuple[bool, str]:
    if not usuario_id or not motivo:
        return False, 'Usuario y motivo son obligatorios'
    if tipo not in _DURACIONES:
        return False, 'Tipo inválido'
    if not get_by_id(usuario_id):
        return False, 'Usuario no encontrado'
    
    # Validar que admin no se sancione a sí mismo
    admin_id = session.get('user_id')
    if admin_id == usuario_id:
        return False, 'No puedes sancionarte a ti mismo'
    
    repo_crear(usuario_id, admin_id, motivo.strip(), tipo, 1, incidencia_id)
    set_user_state(usuario_id, 'BLOQUEADO')
    
    # Cancelar todas las reservas pendientes y activas del usuario
    canceladas = cancelar_por_sancion(usuario_id)
    
    dias = _DURACIONES[tipo]
    mensaje = f'Sanción {tipo.lower()} aplicada. Usuario inactivo por {dias} día(s)'
    if canceladas > 0:
        mensaje += f'. Se cancelaron {canceladas} reserva(s)'
    return True, mensaje


def levantar_sancion(sancion_id: int) -> Tuple[bool, str]:
    # Manual lift: set sanction lifted and user active
    repo_levantar(sancion_id)
    return True, 'Sanción levantada manualmente'
