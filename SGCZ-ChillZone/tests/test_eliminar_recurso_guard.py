from unittest.mock import patch

from services import recursos_service


@patch('repositories.uso_repository.contar_activos_por_recurso')
@patch('repositories.reserva_repository.contar_activas_por_recurso')
def test_eliminar_bloqueado_por_reservas(mock_count_res, mock_count_uso):
    mock_count_res.return_value = 1
    mock_count_uso.return_value = 0
    ok, msg = recursos_service.eliminar_recurso(1)
    assert ok is False
    assert 'reservas activas' in msg


@patch('repositories.uso_repository.contar_activos_por_recurso')
@patch('repositories.reserva_repository.contar_activas_por_recurso')
def test_eliminar_bloqueado_por_uso(mock_count_res, mock_count_uso):
    mock_count_res.return_value = 0
    mock_count_uso.return_value = 2
    ok, msg = recursos_service.eliminar_recurso(1)
    assert ok is False
    assert 'en uso' in msg
