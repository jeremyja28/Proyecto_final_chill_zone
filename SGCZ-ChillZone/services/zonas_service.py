from typing import List, Dict, Tuple
import repositories.zona_repository as zona_repo

def listar_zonas() -> List[Dict]:
    return zona_repo.listar()

def crear_zona(nombre: str, descripcion: str, imagen_url: str = None) -> Tuple[bool, str]:
    if not nombre:
        return False, "El nombre es obligatorio"
    try:
        zona_repo.crear(nombre, descripcion, imagen_url)
        return True, "Zona creada exitosamente"
    except Exception as e:
        return False, f"Error al crear zona: {str(e)}"

def actualizar_zona(zona_id: int, nombre: str, descripcion: str, imagen_url: str = None) -> Tuple[bool, str]:
    if not nombre:
        return False, "El nombre es obligatorio"
    try:
        zona_repo.actualizar(zona_id, nombre, descripcion, imagen_url)
        return True, "Zona actualizada exitosamente"
    except Exception as e:
        return False, f"Error al actualizar zona: {str(e)}"

def eliminar_zona(zona_id: int) -> Tuple[bool, str]:
    try:
        zona_repo.eliminar(zona_id)
        return True, "Zona eliminada exitosamente"
    except Exception as e:
        if "foreign key constraint" in str(e).lower():
            return False, "No se puede eliminar la zona porque tiene recursos asociados."
        return False, f"Error al eliminar zona: {str(e)}"
