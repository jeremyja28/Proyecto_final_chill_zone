from typing import Tuple, List
import repositories.recurso_repository as recurso_repo
import repositories.reserva_repository as reserva_repo
import repositories.uso_repository as uso_repo


def listar_recursos() -> List[dict]:
    return recurso_repo.listar()


def crear_recurso(data: dict) -> Tuple[bool, str]:
    if not data.get('nombre'):
        return False, 'Nombre requerido'
    if not data.get('zona_id'):
        return False, 'Zona requerida'
    recurso_repo.crear(data['nombre'], data.get('tipo', ''), data.get('ubicacion', ''), data['zona_id'], data.get('imagen_url'))
    return True, 'Recurso creado'


def editar_recurso(recurso_id: int, data: dict) -> Tuple[bool, str]:
    if not data.get('nombre'):
        return False, 'Nombre requerido'
    if not data.get('zona_id'):
        return False, 'Zona requerida'
    recurso_repo.editar(recurso_id, data['nombre'], data.get('tipo', ''), data.get('ubicacion', ''), data['zona_id'], data.get('imagen_url'))
    return True, 'Recurso actualizado'


def eliminar_recurso(recurso_id: int) -> Tuple[bool, str]:
    # No permitir eliminación si hay reservas activas o usos en curso (CU-14)
    if reserva_repo.contar_activas_por_recurso(recurso_id) > 0:
        return False, 'No se puede eliminar: existen reservas activas asociadas'
    if uso_repo.contar_activos_por_recurso(recurso_id) > 0:
        return False, 'No se puede eliminar: el recurso está en uso'
    recurso_repo.eliminar_logico(recurso_id)
    return True, 'Recurso eliminado'


def cambiar_estado(recurso_id: int, estado: str, mant_inicio: str = None, mant_fin: str = None) -> Tuple[bool, str]:
    """Cambia el estado del recurso.
    mant_inicio/fin: para EN_MANTENIMIENTO, formato 'YYYY-MM-DD HH:MM:SS'.
    FUERA_DE_SERVICIO es indefinido y cancela todo a futuro."""
    if estado not in ('DISPONIBLE', 'EN_MANTENIMIENTO', 'FUERA_DE_SERVICIO'):
        return False, 'Estado inválido'
    from repositories import reserva_repository as reserva_repo_local
    afectados = 0
    
    if estado == 'FUERA_DE_SERVICIO':
        # Cancelar TODAS las reservas futuras inmediatamente
        try:
            afectados = reserva_repo_local.cancelar_futuras_por_recurso(recurso_id)
        except Exception:
            afectados = 0
        # Actualizar estado sin fechas (indefinido)
        recurso_repo.cambiar_estado(recurso_id, estado, None, None)
        return True, f'Recurso marcado como FUERA DE SERVICIO. {afectados} reservas futuras canceladas.'

    if estado == 'EN_MANTENIMIENTO':
        if not mant_inicio or not mant_fin:
            # Si no se especifica rango, usar NOW hasta NOW+24h como default
            from datetime import datetime, timedelta
            now = datetime.now()
            mant_inicio = now.strftime('%Y-%m-%d %H:%M:%S')
            mant_fin = (now + timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')
        try:
            afectados = reserva_repo_local.cancelar_por_mantenimiento(recurso_id, mant_inicio, mant_fin)
        except Exception:
            afectados = 0
    
    recurso_repo.cambiar_estado(recurso_id, estado, mant_inicio, mant_fin)
    msg = 'Estado actualizado'
    if afectados:
        msg += f' | {afectados} reservas canceladas por mantenimiento'
    return True, msg
