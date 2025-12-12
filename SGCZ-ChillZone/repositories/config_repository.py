from typing import Dict, List
from utils.db import query_all, query_one, execute


def listar() -> List[Dict]:
    return query_all("SELECT * FROM config_sistema ORDER BY nombre")


def obtener(nombre: str) -> Dict:
    return query_one("SELECT * FROM config_sistema WHERE nombre=%s", (nombre,))


def guardar(nombre: str, valor: str):
    row = obtener(nombre)
    if row:
        execute("UPDATE config_sistema SET valor=%s, actualizado_en=NOW() WHERE id=%s", (valor, row['id']))
    else:
        execute("INSERT INTO config_sistema (nombre, valor) VALUES (%s,%s)", (nombre, valor))
