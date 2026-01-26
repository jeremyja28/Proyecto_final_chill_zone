from typing import List, Dict, Tuple, Optional
import repositories.zona_repository as zona_repo
import repositories.recurso_repository as recurso_repo
import repositories.reserva_repository as reserva_repo
from utils.db import query_all
from utils.security_utils import generar_hash_entidad, verificar_checksum


def listar_zonas(incluir_deshabilitados: bool = False) -> List[Dict]:
    return zona_repo.listar(incluir_deshabilitados)


def obtener_zona(zona_id: int, incluir_checksum: bool = False) -> Optional[Dict]:
    """
    Obtiene una zona por ID.
    
    Args:
        zona_id: ID de la zona
        incluir_checksum: Si True, inyecta _checksum para control de concurrencia
    
    Returns:
        Dict con datos de la zona (+ _checksum si solicitado), o None si no existe.
    """
    zona = zona_repo.obtener(zona_id)
    if zona and incluir_checksum:
        zona['_checksum'] = generar_hash_entidad(zona)
    return zona


def crear_zona(nombre: str, descripcion: str, imagen_url: str = None) -> Tuple[bool, str]:
    if not nombre:
        return False, "El nombre es obligatorio"
    try:
        zona_repo.crear(nombre, descripcion, imagen_url)
        return True, "Zona creada exitosamente"
    except Exception as e:
        return False, f"Error al crear zona: {str(e)}"


def actualizar_zona(zona_id: int, nombre: str, descripcion: str, imagen_url: str = None, checksum_original: str = None) -> Tuple[bool, str]:
    """
    Actualiza una zona con validación de concurrencia optimista.
    
    Args:
        zona_id: ID de la zona a actualizar
        nombre: Nuevo nombre
        descripcion: Nueva descripción
        imagen_url: Nueva URL de imagen (opcional)
        checksum_original: Hash del estado cuando el usuario abrió el formulario.
                          Si no coincide con el actual, se rechaza la edición.
    
    Returns:
        Tuple (success: bool, message: str)
    """
    if not nombre:
        return False, "El nombre es obligatorio"
    
    # Verificación de concurrencia optimista
    if checksum_original:
        zona_actual = zona_repo.obtener(zona_id)
        if not zona_actual:
            return False, 'Zona no encontrada'
        if not verificar_checksum(zona_actual, checksum_original):
            return False, 'Error de integridad: Alguien más ha modificado este registro mientras lo editabas. Por favor, recarga la página y vuelve a intentarlo.'
    
    try:
        zona_repo.actualizar(zona_id, nombre, descripcion, imagen_url)
        return True, "Zona actualizada exitosamente"
    except Exception as e:
        return False, f"Error al actualizar zona: {str(e)}"


def deshabilitar_zona(zona_id: int) -> Tuple[bool, str, dict]:
    """Deshabilita una zona con cascada a recursos y reservas.
    Retorna: (success, message, stats)
    """
    zona = zona_repo.obtener(zona_id)
    if not zona:
        return False, 'Zona no encontrada', {}
    
    if zona.get('eliminado') == 1:
        return False, 'La zona ya está deshabilitada', {}
    
    zona_nombre = zona.get('nombre', 'Sin nombre')
    motivo_cancelacion = f"La zona '{zona_nombre}' fue inhabilitada temporalmente."
    
    # 1. Obtener todos los recursos ACTIVOS de esta zona
    recursos = query_all("SELECT id, nombre FROM recursos WHERE zona_id=%s AND eliminado=0", (zona_id,))
    
    total_reservas_canceladas = 0
    recursos_deshabilitados = 0
    
    # 2. Para cada recurso activo: cancelar reservas y deshabilitar CON marca de zona
    for recurso in recursos:
        recurso_id = recurso['id']
        # Cancelar reservas de este recurso CON MOTIVO DE ZONA
        canceladas = reserva_repo.cancelar_por_deshabilitacion(recurso_id, motivo_cancelacion)
        total_reservas_canceladas += canceladas
        # Deshabilitar recurso CON marca de zona (para restauración futura)
        recurso_repo.eliminar_logico_por_zona(recurso_id)
        recursos_deshabilitados += 1
    
    # 3. Deshabilitar la zona
    zona_repo.eliminar_logico(zona_id)
    
    msg = 'Zona deshabilitada'
    if recursos_deshabilitados > 0:
        msg += f'. {recursos_deshabilitados} recurso(s) deshabilitado(s)'
    if total_reservas_canceladas > 0:
        msg += f', {total_reservas_canceladas} reserva(s) cancelada(s)'
    
    return True, msg, {
        'recursos_deshabilitados': recursos_deshabilitados,
        'reservas_canceladas': total_reservas_canceladas
    }


def obtener_recursos_restaurables(zona_id: int) -> List[Dict]:
    """Obtiene la lista de recursos que pueden ser restaurados al habilitar la zona."""
    return recurso_repo.obtener_recursos_deshabilitados_por_zona(zona_id)


def habilitar_zona(zona_id: int, restaurar_recursos: bool = False) -> Tuple[bool, str]:
    """Habilita una zona.
    
    Args:
        zona_id: ID de la zona
        restaurar_recursos: Si True, restaura también los recursos que fueron 
                           deshabilitados por cascada de zona
    """
    zona = zona_repo.obtener(zona_id)
    if not zona:
        return False, 'Zona no encontrada'
    
    if zona.get('eliminado') == 0:
        return False, 'La zona ya está habilitada'
    
    # Habilitar la zona
    zona_repo.habilitar(zona_id)
    
    if restaurar_recursos:
        # Restaurar recursos que fueron deshabilitados por cascada
        recursos = recurso_repo.obtener_recursos_deshabilitados_por_zona(zona_id)
        for r in recursos:
            recurso_repo.habilitar(r['id'])
        
        if len(recursos) > 0:
            return True, f'Zona habilitada. {len(recursos)} recurso(s) restaurado(s)'
    
    return True, 'Zona habilitada. Los recursos deben habilitarse manualmente.'


def validar_zona_activa_para_recurso(zona_id: int) -> Tuple[bool, str]:
    """Valida que una zona esté activa para poder habilitar un recurso en ella."""
    zona = zona_repo.obtener(zona_id)
    if not zona:
        return False, 'Zona no encontrada'
    if zona.get('eliminado') == 1:
        return False, f'No se puede habilitar el recurso. La zona "{zona.get("nombre")}" está deshabilitada. Primero active la zona.'
    return True, 'OK'


def eliminar_zona(zona_id: int) -> Tuple[bool, str]:
    """Eliminación física - usar deshabilitar_zona para soft delete."""
    try:
        zona_repo.eliminar(zona_id)
        return True, "Zona eliminada exitosamente"
    except Exception as e:
        if "foreign key constraint" in str(e).lower():
            return False, "No se puede eliminar la zona porque tiene recursos asociados."
        return False, f"Error al eliminar zona: {str(e)}"
