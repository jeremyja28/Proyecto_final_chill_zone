from unittest.mock import patch
from datetime import datetime, timedelta
from services.reservas_service import cancelar_reserva

# Casos CU-08: cancelación antes de 10 minutos y bloqueo cuando falta <=10m o está en uso

FAKE_RESERVA_BASE = {
    'id': 1,
    'estado': 'ACTIVA',
    'fecha': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
    'hora_inicio': '15:00',
    'recurso_id': 10
}

@patch('repositories.uso_repository.obtener_activo_por_reserva')
@patch('repositories.reserva_repository.obtener')
@patch('repositories.reservas_service.repo_cancelar')
@patch('repositories.reserva_repository.cancelar')
def test_cancelar_reserva_ok(mock_cancel_real, mock_cancel_alias, mock_get_reserva, mock_get_uso):
    # Reserva mañana a las 15:00, ahora mucho antes -> debería permitir
    mock_get_reserva.return_value = FAKE_RESERVA_BASE
    mock_get_uso.return_value = None
    mock_cancel_alias.return_value = None
    ok, msg = cancelar_reserva(1)
    assert ok is True
    assert 'cancelada' in msg.lower()

@patch('repositories.uso_repository.obtener_activo_por_reserva')
@patch('repositories.reserva_repository.obtener')
def test_cancelar_reserva_en_uso(mock_get_reserva, mock_get_uso):
    mock_get_reserva.return_value = FAKE_RESERVA_BASE
    mock_get_uso.return_value = {'id':55}
    ok, msg = cancelar_reserva(1)
    assert ok is False
    assert 'en uso' in msg.lower()

@patch('repositories.uso_repository.obtener_activo_por_reserva')
@patch('repositories.reserva_repository.obtener')
def test_cancelar_reserva_menos_de_10_min(mock_get_reserva, mock_get_uso):
    # Reserva dentro de 5 minutos => no se permite
    fecha = datetime.now().strftime('%Y-%m-%d')
    hora_inicio_dt = datetime.now() + timedelta(minutes=5)
    reserva_cercana = dict(FAKE_RESERVA_BASE)
    reserva_cercana['fecha'] = fecha
    reserva_cercana['hora_inicio'] = hora_inicio_dt.strftime('%H:%M')
    mock_get_reserva.return_value = reserva_cercana
    mock_get_uso.return_value = None
    ok, msg = cancelar_reserva(1)
    assert ok is False
    assert '10 minutos' in msg
