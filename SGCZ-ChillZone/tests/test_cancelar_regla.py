from datetime import datetime, timedelta, date, time as dtime
from unittest.mock import patch

from services import reservas_service


def _fake_now(base):
    class FakeDT:
        @staticmethod
        def now():
            return base
        @staticmethod
        def strptime(s, fmt):
            return datetime.strptime(s, fmt)
        @staticmethod
        def combine(d, t):
            return datetime.combine(d, t)
    return FakeDT


@patch('repositories.uso_repository.obtener_activo_por_reserva')
@patch('repositories.reserva_repository.obtener')
@patch('repositories.reservas_service.repo_cancelar', create=True)
def test_cancelar_rechazada_por_ventana(mock_repo_cancelar, mock_obtener, mock_uso):
    # Reserva inicia en 5 minutos -> debe rechazar
    now = datetime(2025, 10, 27, 9, 55)
    mock_obtener.return_value = {
        'id': 10,
        'estado': 'ACTIVA',
        'fecha': date(2025, 10, 27),
        'hora_inicio': '10:00'
    }
    mock_uso.return_value = None
    # parchear datetime en módulo
    reservas_service.datetime = _fake_now(now)
    ok, msg = reservas_service.cancelar_reserva(10)
    assert ok is False
    assert '10 minutos' in msg


@patch('repositories.uso_repository.obtener_activo_por_reserva')
@patch('repositories.reserva_repository.obtener')
@patch('repositories.reserva_repository.cancelar')
def test_cancelar_rechazada_por_uso_activo(mock_cancel, mock_obtener, mock_uso):
    now = datetime(2025, 10, 27, 8, 0)
    mock_obtener.return_value = {
        'id': 11,
        'estado': 'ACTIVA',
        'fecha': date(2025, 10, 27),
        'hora_inicio': '10:00'
    }
    mock_uso.return_value = {'id': 99}
    reservas_service.datetime = _fake_now(now)
    ok, msg = reservas_service.cancelar_reserva(11)
    assert ok is False
    assert 'en uso' in msg
