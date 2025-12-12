from unittest.mock import patch
from services.recursos_service import crear_recurso, eliminar_recurso, cambiar_estado, editar_recurso

@patch('repositories.recurso_repository.crear')
def test_crear_recurso_ok(mock_crear):
    ok, msg = crear_recurso({'nombre': 'Proyector', 'tipo': 'ELECTRÓNICO', 'ubicacion': 'Sala 1'})
    assert ok is True
    assert 'creado' in msg.lower()

@patch('repositories.recurso_repository.crear')
def test_crear_recurso_sin_nombre(mock_crear):
    ok, msg = crear_recurso({'tipo': 'ELECTRÓNICO'})
    assert ok is False
    assert 'nombre' in msg.lower()

@patch('repositories.reserva_repository.contar_activas_por_recurso')
@patch('repositories.uso_repository.contar_activos_por_recurso')
@patch('repositories.recurso_repository.eliminar_logico')
def test_eliminar_recurso_bloqueado_por_reservas(mock_eliminar, mock_usos, mock_reservas):
    mock_reservas.return_value = 1
    mock_usos.return_value = 0
    ok, msg = eliminar_recurso(10)
    assert ok is False
    assert 'reservas' in msg.lower()

@patch('repositories.reserva_repository.contar_activas_por_recurso')
@patch('repositories.uso_repository.contar_activos_por_recurso')
@patch('repositories.recurso_repository.eliminar_logico')
def test_eliminar_recurso_bloqueado_por_uso(mock_eliminar, mock_usos, mock_reservas):
    mock_reservas.return_value = 0
    mock_usos.return_value = 2
    ok, msg = eliminar_recurso(10)
    assert ok is False
    assert 'en uso' in msg.lower()

@patch('repositories.reserva_repository.contar_activas_por_recurso')
@patch('repositories.uso_repository.contar_activos_por_recurso')
@patch('repositories.recurso_repository.eliminar_logico')
def test_eliminar_recurso_ok(mock_eliminar, mock_usos, mock_reservas):
    mock_reservas.return_value = 0
    mock_usos.return_value = 0
    ok, msg = eliminar_recurso(10)
    assert ok is True
    assert 'eliminado' in msg.lower()

@patch('repositories.recurso_repository.cambiar_estado')
def test_cambiar_estado_valido(mock_cambiar):
    ok, msg = cambiar_estado(10, 'EN_MANTENIMIENTO')
    assert ok is True
    assert 'actualizado' in msg.lower()

@patch('repositories.recurso_repository.cambiar_estado')
def test_cambiar_estado_invalido(mock_cambiar):
    ok, msg = cambiar_estado(10, 'DESCONOCIDO')
    assert ok is False
    assert 'inválido' in msg.lower()

@patch('repositories.recurso_repository.editar')
def test_editar_recurso_ok(mock_editar):
    ok, msg = editar_recurso(5, {'nombre': 'Pantalla 4K', 'tipo': 'ELECTRÓNICO', 'ubicacion': 'Sala 2'})
    assert ok is True
    assert 'actualizado' in msg.lower()

@patch('repositories.recurso_repository.editar')
def test_editar_recurso_falta_nombre(mock_editar):
    ok, msg = editar_recurso(5, {'tipo': 'ELECTRÓNICO'})
    assert ok is False
    assert 'nombre' in msg.lower()
