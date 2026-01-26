"""
Utilidades de seguridad para control de concurrencia.
Implementa Bloqueo Optimista mediante hash de contenido (checksum).
"""
import hashlib
import json
from typing import Dict


def generar_hash_entidad(data_dict: Dict) -> str:
    """
    Genera un hash SHA256 del estado actual de una entidad.
    
    Este hash sirve como "firma" del registro para detectar modificaciones
    concurrentes (Race Conditions) sin modificar la base de datos.
    
    Args:
        data_dict: Diccionario con los datos de la entidad.
                   Se ordenan las claves para garantizar consistencia.
    
    Returns:
        String hexadecimal del hash SHA256 (64 caracteres).
    
    Example:
        >>> generar_hash_entidad({'nombre': 'Sala A', 'tipo': 'Reunión'})
        'a1b2c3d4...'
    """
    # Filtrar campos internos/no relevantes para el hash
    campos_excluir = {'_checksum', 'created_at', 'updated_at'}
    datos_limpios = {k: v for k, v in data_dict.items() if k not in campos_excluir}
    
    # Ordenar claves para garantizar consistencia
    datos_ordenados = dict(sorted(datos_limpios.items()))
    
    # Convertir a JSON string (con sort_keys para doble seguridad)
    json_str = json.dumps(datos_ordenados, sort_keys=True, default=str)
    
    # Generar hash SHA256
    return hashlib.sha256(json_str.encode('utf-8')).hexdigest()


def verificar_checksum(entidad_actual: Dict, checksum_original: str) -> bool:
    """
    Verifica si el checksum original coincide con el estado actual de la entidad.
    
    Args:
        entidad_actual: Diccionario con los datos actuales de la entidad en BD.
        checksum_original: Hash que tenía la entidad cuando el usuario abrió el formulario.
    
    Returns:
        True si coinciden (no hubo modificaciones), False si difieren.
    """
    if not checksum_original:
        # Si no se proporciona checksum, permitir (compatibilidad hacia atrás)
        return True
    
    hash_actual = generar_hash_entidad(entidad_actual)
    return hash_actual == checksum_original
