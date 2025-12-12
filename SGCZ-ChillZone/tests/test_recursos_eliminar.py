from unittest.mock import patch
from services import recursos_service


@patch('repositories.uso_repository.contar_activos_por_recurso')
@patch('repositories.reserva_repository.contar_activas_por_recurso')
def test_eliminar_bloqueado_por_reservas(mock_cnt_res, mock_cnt_uso):
    mock_cnt_res.return_value = 1
    mock_cnt_uso.return_value = 0
    ok, msg = recursos_service.eliminar_recurso(1)
    assert ok is False
    assert 'reservas activas' in msg


@patch('repositories.uso_repository.contar_activos_por_recurso')
@patch('repositories.reserva_repository.contar_activas_por_recurso')
def test_eliminar_bloqueado_por_uso(mock_cnt_res, mock_cnt_uso):
    mock_cnt_res.return_value = 0
    mock_cnt_uso.return_value = 2
    ok, msg = recursos_service.eliminar_recurso(1)
    assert ok is False
    assert 'en uso' in msg
