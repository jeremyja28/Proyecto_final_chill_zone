from typing import Optional, List, Dict
from utils.db import query_one, query_all, execute


def get_by_email(email: str) -> Optional[Dict]:
    sql = "SELECT * FROM usuarios WHERE correo = %s LIMIT 1"
    return query_one(sql, (email,))


def get_by_id(user_id: int) -> Optional[Dict]:
    sql = "SELECT * FROM usuarios WHERE id = %s"
    return query_one(sql, (user_id,))


def list_users(offset: int = 0, limit: int = 50) -> List[Dict]:
    sql = "SELECT * FROM usuarios ORDER BY creado_en DESC LIMIT %s OFFSET %s"
    return query_all(sql, (limit, offset))


def count_users() -> int:
    row = query_one("SELECT COUNT(1) as c FROM usuarios")
    return int(row['c']) if row else 0


def create_user(nombre: str, apellido: str, correo: str, password_hash: bytes, rol: str = 'USUARIO', estado: str = 'ACTIVO') -> int:
    sql = """
    INSERT INTO usuarios (nombre, apellido, correo, hash_password, rol, estado)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    return execute(sql, (nombre, apellido, correo, password_hash, rol, estado))


def update_password(user_id: int, password_hash: bytes):
    sql = "UPDATE usuarios SET hash_password = %s WHERE id = %s"
    execute(sql, (password_hash, user_id))


def update_role(user_id: int, rol: str):
    sql = "UPDATE usuarios SET rol = %s WHERE id = %s"
    execute(sql, (rol, user_id))


def block_user(user_id: int):
    sql = "UPDATE usuarios SET estado = 'BLOQUEADO' WHERE id = %s"
    execute(sql, (user_id,))

def set_user_state(user_id: int, estado: str):
    sql = "UPDATE usuarios SET estado=%s WHERE id=%s"
    execute(sql, (estado, user_id))


def update_profile_image(user_id: int, image_url: str):
    sql = "UPDATE usuarios SET imagen_url = %s WHERE id = %s"
    execute(sql, (image_url, user_id))


def buscar_usuarios(query: str) -> List[Dict]:
    term = f"%{query}%"
    sql = """
        SELECT id, nombre, apellido, correo, estado 
        FROM usuarios 
        WHERE (nombre LIKE %s OR apellido LIKE %s OR correo LIKE %s)
        ORDER BY nombre, apellido
        LIMIT 20
    """
    return query_all(sql, (term, term, term))


def listar_activos() -> List[Dict]:
    """Lista todos los usuarios activos (para selección de acompañantes)."""
    sql = "SELECT id, nombre, apellido, correo FROM usuarios WHERE estado='ACTIVO' ORDER BY nombre, apellido"
    return query_all(sql)
