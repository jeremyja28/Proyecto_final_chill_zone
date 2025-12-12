from unittest.mock import patch
from services import reservas_service


@patch('repositories.reserva_repository.obtener')
@patch('repositories.uso_repository.obtener_activo_por_reserva')
def test_cancelar_reserva_denegada_por_uso(mock_uso, mock_get):
    mock_get.return_value = {
        'id': 1,
        'estado': 'ACTIVA',
        'fecha': '2025-11-03',
        'hora_inicio': '23:59',
        'recurso_id': 1,
    }
    mock_uso.return_value = {'id': 10}  # uso activo
    ok, msg = reservas_service.cancelar_reserva(1)
    assert ok is False
    assert 'en uso' in msg.lower()


@patch('repositories.reserva_repository.obtener')
@patch('repositories.uso_repository.obtener_activo_por_reserva')
@patch('repositories.reserva_repository.cancelar')
def test_cancelar_reserva_denegada_por_tiempo(mock_cancel, mock_uso, mock_get):
    from datetime import datetime, timedelta
    # Reserva que empieza en 5 minutos
    start_dt = datetime.now() + timedelta(minutes=5)
    mock_get.return_value = {
        'id': 2,
        'estado': 'ACTIVA',
        'fecha': start_dt.strftime('%Y-%m-%d'),
        'hora_inicio': start_dt.strftime('%H:%M'),
        'recurso_id': 1,
    }
    mock_uso.return_value = None
    ok, msg = reservas_service.cancelar_reserva(2)
    assert ok is False
    assert '10 minutos' in msg
