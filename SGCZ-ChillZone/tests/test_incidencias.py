from unittest.mock import patch
from services.incidencias_service import reportar_incidencia


@patch('repositories.incidencia_repository.crear')
@patch('repositories.recurso_repository.obtener')
@patch('flask.session', {'user_id': 7})
def test_reportar_incidencia_ok(mock_rec, mock_crear):
    mock_rec.return_value = {'id': 1, 'eliminado': 0, 'estado': 'DISPONIBLE'}
    ok, msg = reportar_incidencia(1, 'Daño en la mesa', 'https://example.com/foto.jpg')
    assert ok is True
    assert 'reportada' in msg.lower() or 'incidencia' in msg.lower()


@patch('repositories.recurso_repository.obtener')
@patch('flask.session', {'user_id': 7})
def test_reportar_incidencia_recurso_no_encontrado(mock_rec):
    mock_rec.return_value = None
    ok, msg = reportar_incidencia(99, 'algo', None)
    assert ok is False
    assert 'no válido' in msg.lower() or 'recurso' in msg.lower()


@patch('repositories.recurso_repository.obtener')
@patch('flask.session', {'user_id': 7})
def test_reportar_incidencia_recurso_fuera_servicio(mock_rec):
    mock_rec.return_value = {'id': 1, 'eliminado': 0, 'estado': 'FUERA_DE_SERVICIO'}
    ok, msg = reportar_incidencia(1, 'algo', None)
    assert ok is False
    assert 'no válido' in msg.lower() or 'recurso' in msg.lower()


@patch('flask.session', {'user_id': 7})
def test_reportar_incidencia_evidencia_invalida():
    ok, msg = reportar_incidencia(1, 'algo', 'archivo.exe')
    assert ok is False
    assert 'formato' in msg.lower() or 'inválido' in msg.lower()
