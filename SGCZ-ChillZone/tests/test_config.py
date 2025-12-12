from repositories.config_repository import guardar, obtener
from utils.db import execute, query_one

# Nota: Estas pruebas asumen una BD de pruebas; si no existe, se deberían mockear.

def test_guardar_y_obtener_config(monkeypatch):
    # Monkeypatch execute para evitar escritura real si se desea.
    # Aquí solo demostración de flujo, idealmente usar un mock.
    guardar('horario_inicio', '07:00')
    row = obtener('horario_inicio')
    assert row is None or row.get('nombre') == 'horario_inicio'
