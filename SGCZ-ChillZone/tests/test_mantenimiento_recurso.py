from unittest.mock import patch
from services.recursos_service import cambiar_estado

@patch('repositories.recurso_repository.cambiar_estado')
@patch('repositories.reserva_repository.cancelar_por_mantenimiento')
def test_cambiar_a_mantenimiento_cancela_reservas(mock_cancelar, mock_cambiar):
    mock_cancelar.return_value = 3
    ok, msg = cambiar_estado(5, 'EN_MANTENIMIENTO')
    assert ok is True
    assert '3 reservas' in msg

@patch('repositories.recurso_repository.cambiar_estado')
@patch('repositories.reserva_repository.cancelar_por_mantenimiento')
def test_cambiar_a_fuera_servicio_cancela_reservas(mock_cancelar, mock_cambiar):
    mock_cancelar.return_value = 2
    ok, msg = cambiar_estado(8, 'FUERA_DE_SERVICIO')
    assert ok is True
    assert '2 reservas' in msg

@patch('repositories.recurso_repository.cambiar_estado')
def test_cambiar_a_disponible_no_cancela(mock_cambiar):
    ok, msg = cambiar_estado(10, 'DISPONIBLE')
    assert ok is True
    assert 'reservas canceladas' not in msg
