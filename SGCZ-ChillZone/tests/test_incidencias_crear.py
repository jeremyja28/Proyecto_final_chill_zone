from unittest.mock import patch
from services.incidencias_service import crear_incidencia


@patch('repositories.incidencia_repository.crear')
@patch('repositories.recurso_repository.obtener')
def test_incidencia_ok(mock_get, mock_crear):
    mock_get.return_value = {'id': 1, 'eliminado': 0}
    ok, msg = crear_incidencia(1, 'Daño en el tablero', 'https://example.com/foto.png')
    assert ok is True


@patch('repositories.recurso_repository.obtener')
def test_incidencia_recurso_invalido(mock_get):
    mock_get.return_value = None
    ok, msg = crear_incidencia(99, 'algo', None)
    assert ok is False
    assert 'no válido' in msg
