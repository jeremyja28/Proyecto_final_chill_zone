from unittest.mock import patch
from services import reservas_service


@patch('services.reservas_service._hoy')
@patch('repositories.recurso_repository.obtener')
@patch('repositories.reserva_repository.listar_conflictos')
def test_reserva_mas_de_7_dias_invalida(mock_conflictos, mock_recurso, mock_hoy):
    mock_hoy.return_value = reservas_service.datetime(2025, 11, 15).date()
    mock_conflictos.return_value = []
    mock_recurso.return_value = {'eliminado': 0, 'estado': 'DISPONIBLE'}
    ok, msg = reservas_service._validar_conflictos(1, '2025-11-23', '10:00', '10:30')
    assert ok is False
    assert '7 días' in msg


@patch('services.reservas_service._hoy')
@patch('repositories.recurso_repository.obtener')
@patch('repositories.reserva_repository.listar_conflictos')
def test_reserva_exactamente_7_dias_valida(mock_conflictos, mock_recurso, mock_hoy):
    mock_hoy.return_value = reservas_service.datetime(2025, 11, 15).date()
    mock_conflictos.return_value = []
    mock_recurso.return_value = {'eliminado': 0, 'estado': 'DISPONIBLE'}
    ok, msg = reservas_service._validar_conflictos(1, '2025-11-22', '10:00', '11:00')
    assert ok is True
    assert msg == 'OK'
