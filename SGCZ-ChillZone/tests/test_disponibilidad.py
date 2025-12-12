from unittest.mock import patch

from services.reservas_service import consultar_disponibilidad


@patch('repositories.recurso_repository.obtener')
@patch('repositories.reserva_repository.listar_conflictos')
def test_consultar_disponibilidad(mock_list, mock_rec):
    mock_rec.return_value = {'id': 1, 'nombre': 'Mesa Ping Pong'}
    mock_list.return_value = [{'hora_inicio':'10:00','hora_fin':'11:00'}]
    data = consultar_disponibilidad(1, '2025-10-27')
    assert data['recurso']['id'] == 1
    assert len(data['reservas']) == 1
