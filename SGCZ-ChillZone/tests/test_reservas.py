from unittest.mock import patch
from flask import session

from services import reservas_service


@patch('repositories.reserva_repository.listar_conflictos')
@patch('repositories.recurso_repository.obtener')
@patch('repositories.config_repository.obtener')
def test_crear_reserva_conflicto(mock_conf, mock_rec, mock_confres):
    mock_confres.side_effect = [ {'valor':'08:00'}, {'valor':'20:00'} ]
    mock_rec.return_value = {'id':1, 'estado':'DISPONIBLE', 'eliminado':0}
    mock_conf.return_value = [{'id':99}]
    ok, msg = reservas_service._validar_conflictos(1, '2025-10-27', '10:00', '11:00')
    assert ok is False
    assert 'conflicto' in msg


@patch('repositories.reserva_repository.listar_conflictos')
@patch('repositories.recurso_repository.obtener')
@patch('repositories.config_repository.obtener')
def test_crear_reserva_ok(mock_conf, mock_rec, mock_confres):
    mock_confres.side_effect = [ {'valor':'08:00'}, {'valor':'20:00'} ]
    mock_rec.return_value = {'id':1, 'estado':'DISPONIBLE', 'eliminado':0}
    mock_conf.return_value = []
    ok, msg = reservas_service._validar_conflictos(1, '2025-10-27', '10:00', '11:00')
    assert ok is True
