from typing import Tuple, List, Optional, Dict
import repositories.recurso_repository as recurso_repo
import repositories.reserva_repository as reserva_repo
import repositories.uso_repository as uso_repo
from utils.security_utils import generar_hash_entidad, verificar_checksum


def listar_recursos(incluir_deshabilitados: bool = False) -> List[dict]:
    return recurso_repo.listar(incluir_deshabilitados)


def obtener_recurso_con_checksum(recurso_id: int) -> Optional[Dict]:
    """
    Obtiene un recurso por ID e inyecta su checksum para control de concurrencia.
    
    Returns:
        Dict con datos del recurso + '_checksum', o None si no existe.
    """
    recurso = recurso_repo.obtener(recurso_id)
    if recurso:
        recurso['_checksum'] = generar_hash_entidad(recurso)
    return recurso


def crear_recurso(data: dict) -> Tuple[bool, str]:
    if not data.get('nombre'):
        return False, 'Nombre requerido'
    if not data.get('zona_id'):
        return False, 'Zona requerida'
    recurso_repo.crear(data['nombre'], data.get('tipo', ''), data.get('ubicacion', ''), data['zona_id'], data.get('imagen_url'))
    return True, 'Recurso creado'


def editar_recurso(recurso_id: int, data: dict, checksum_original: str = None) -> Tuple[bool, str]:
    """
    Edita un recurso con validación de concurrencia optimista.
    
    Args:
        recurso_id: ID del recurso a editar
        data: Datos nuevos del recurso
        checksum_original: Hash del estado cuando el usuario abrió el formulario.
                          Si no coincide con el actual, se rechaza la edición.
    
    Returns:
        Tuple (success: bool, message: str)
    """
    if not data.get('nombre'):
        return False, 'Nombre requerido'
    if not data.get('zona_id'):
        return False, 'Zona requerida'
    
    # Verificación de concurrencia optimista
    if checksum_original:
        recurso_actual = recurso_repo.obtener(recurso_id)
        if not recurso_actual:
            return False, 'Recurso no encontrado'
        if not verificar_checksum(recurso_actual, checksum_original):
            return False, 'Error de integridad: Alguien más ha modificado este registro mientras lo editabas. Por favor, recarga la página y vuelve a intentarlo.'
    
    recurso_repo.editar(recurso_id, data['nombre'], data.get('tipo', ''), data.get('ubicacion', ''), data['zona_id'], data.get('imagen_url'))
    return True, 'Recurso actualizado'


def eliminar_recurso(recurso_id: int) -> Tuple[bool, str]:
    """DEPRECADO: Usar toggle_habilitacion en su lugar."""
    return toggle_habilitacion(recurso_id)


def toggle_habilitacion(recurso_id: int) -> Tuple[bool, str]:
    """Alterna el estado de habilitación de un recurso.
    Al deshabilitar: cancela automáticamente todas las reservas PENDIENTE/ACTIVA.
    Al habilitar: verifica que la zona padre esté activa primero."""
    recurso = recurso_repo.obtener(recurso_id)
    if not recurso:
        return False, 'Recurso no encontrado'
    
    if recurso.get('eliminado') == 0:
        # Deshabilitar: cancelar reservas pendientes/activas primero
        recurso_nombre = recurso.get('nombre', 'Sin nombre')
        motivo = f"El recurso '{recurso_nombre}' fue desactivado."
        canceladas = reserva_repo.cancelar_por_deshabilitacion(recurso_id, motivo)
        recurso_repo.eliminar_logico(recurso_id)
        msg = 'Recurso deshabilitado'
        if canceladas > 0:
            msg += f'. Se cancelaron {canceladas} reserva(s) asociadas.'
        return True, msg
    else:
        # HABILITAR: primero verificar que la zona esté activa
        import repositories.zona_repository as zona_repo
        zona = zona_repo.obtener(recurso.get('zona_id'))
        if zona and zona.get('eliminado') == 1:
            return False, f'No se puede habilitar el recurso. La zona "{zona.get("nombre")}" está deshabilitada. Primero active la zona.'
        
        recurso_repo.habilitar(recurso_id)
        return True, 'Recurso habilitado'


def cambiar_estado(recurso_id: int, estado: str, mant_inicio: str = None, mant_fin: str = None) -> Tuple[bool, str]:
    """Cambia el estado del recurso.
    mant_inicio/fin: para EN_MANTENIMIENTO, formato 'YYYY-MM-DD HH:MM:SS'.
    FUERA_DE_SERVICIO es indefinido y cancela todo a futuro."""
    if estado not in ('DISPONIBLE', 'EN_MANTENIMIENTO', 'FUERA_DE_SERVICIO'):
        return False, 'Estado inválido'
    from repositories import reserva_repository as reserva_repo_local
    afectados = 0
    
    if estado == 'FUERA_DE_SERVICIO':
        # Cancelar TODAS las reservas futuras inmediatamente con mensaje específico
        try:
            afectados = reserva_repo_local.cancelar_por_fuera_servicio(recurso_id)
            print(f"DEBUG FUERA_DE_SERVICIO: recurso_id={recurso_id}, afectados={afectados}")
        except Exception as e:
            print(f"ERROR cancelar_por_fuera_servicio: {e}")
            import traceback
            traceback.print_exc()
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
