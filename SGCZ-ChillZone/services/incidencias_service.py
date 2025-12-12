from typing import List, Tuple
from flask import session, has_request_context
from repositories.incidencia_repository import crear as repo_crear, listar_por_usuario, listar_todas, listar_por_recurso, obtener as incidencia_obtener, actualizar_estado as incidencia_actualizar_estado
from repositories.recurso_repository import listar as recursos_listar, obtener as recurso_obtener

ALLOWED_EVIDENCE_EXT = {'.jpg', '.jpeg', '.png', '.gif', '.pdf'}


def _current_user_id_safe() -> int:
    try:
        if has_request_context():
            return session.get('user_id') or 0
    except Exception:
        pass
    return 0


def listar_incidencias_usuario() -> List[dict]:
    return listar_por_usuario(_current_user_id_safe())


def listar_incidencias_admin() -> List[dict]:
    return listar_todas()


def listar_incidencias_recurso(recurso_id: int) -> List[dict]:
    return listar_por_recurso(recurso_id)


def recursos_disponibles() -> List[dict]:
    return recursos_listar()


def _valid_evidence_url(url: str) -> bool:
    if not url:
        return True
    lower = url.lower()
    return any(lower.endswith(ext) for ext in ALLOWED_EVIDENCE_EXT)


def crear_incidencia(recurso_id: int, descripcion: str, evidencia_url: str | None, responsables_ids: list = None, reserva_id: int = None) -> Tuple[bool, str]:
    if not recurso_id or not descripcion:
        return False, 'Recurso y descripción son obligatorios'
    # Validar primero el formato de evidencia para alinear expectativas de tests
    if evidencia_url and not _valid_evidence_url(evidencia_url):
        return False, 'Formato de evidencia inválido. Solo imagen o PDF'
    uid = _current_user_id_safe()
    if not uid:
        return False, 'Debes iniciar sesión para reportar incidencias'
    recurso = recurso_obtener(recurso_id)
    if not recurso or recurso.get('eliminado'):
        return False, 'Recurso no válido'
    repo_crear(recurso_id, uid, descripcion.strip(), (evidencia_url or '').strip() or None, responsables_ids, reserva_id)
    return True, 'Incidencia reportada'


def reportar_incidencia(recurso_id: int, descripcion: str, evidencia_url: str | None) -> Tuple[bool, str]:
    # Alias para compatibilidad con tests anteriores
    return crear_incidencia(recurso_id, descripcion, evidencia_url)

def toggle_estado_incidencia(incidencia_id: int) -> Tuple[bool, str]:
    inc = incidencia_obtener(incidencia_id)
    if not inc:
        return False, 'Incidencia no encontrada'
    nuevo = 'REVISADA' if inc.get('estado') == 'PENDIENTE' else 'PENDIENTE'
    incidencia_actualizar_estado(incidencia_id, nuevo)
    return True, f'Estado cambiado a {"Arreglada" if nuevo=="REVISADA" else "Pendiente"}'
