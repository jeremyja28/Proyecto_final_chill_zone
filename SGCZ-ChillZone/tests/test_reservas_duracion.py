from unittest.mock import patch
from services import reservas_service


@patch('repositories.recurso_repository.obtener')
@patch('repositories.reserva_repository.listar_conflictos')
def test_duracion_minima(mock_conflictos, mock_recurso):
    mock_conflictos.return_value = []
    mock_recurso.return_value = {'eliminado': 0, 'estado': 'DISPONIBLE'}
    ok, msg = reservas_service._validar_conflictos(1, '2025-11-15', '10:00', '10:10')
    assert ok is False
    assert '15 minutos' in msg


@patch('repositories.recurso_repository.obtener')
@patch('repositories.reserva_repository.listar_conflictos')
def test_duracion_maxima(mock_conflictos, mock_recurso):
    mock_conflictos.return_value = []
    mock_recurso.return_value = {'eliminado': 0, 'estado': 'DISPONIBLE'}
    ok, msg = reservas_service._validar_conflictos(2, '2025-11-15', '09:00', '12:30')
    assert ok is False
    assert '2 horas' in msg


@patch('repositories.recurso_repository.obtener')
@patch('repositories.reserva_repository.listar_conflictos')
def test_duracion_valida(mock_conflictos, mock_recurso):
    mock_conflictos.return_value = []
    mock_recurso.return_value = {'eliminado': 0, 'estado': 'DISPONIBLE'}
    ok, msg = reservas_service._validar_conflictos(3, '2025-11-15', '10:00', '11:30')
    assert ok is True
    assert msg == 'OK'
