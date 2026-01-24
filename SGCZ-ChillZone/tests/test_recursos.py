from unittest.mock import patch, MagicMock
from services.recursos_service import crear_recurso, eliminar_recurso, cambiar_estado, editar_recurso, toggle_habilitacion

@patch('repositories.recurso_repository.crear')
def test_crear_recurso_ok(mock_crear):
    ok, msg = crear_recurso({'nombre': 'Proyector', 'tipo': 'ELECTRONICO', 'ubicacion': 'Sala 1', 'zona_id': 1})
    assert ok is True
    assert 'creado' in msg.lower()

@patch('repositories.recurso_repository.crear')
def test_crear_recurso_sin_nombre(mock_crear):
    ok, msg = crear_recurso({'tipo': 'ELECTRONICO'})
    assert ok is False
    assert 'nombre' in msg.lower()

@patch('repositories.recurso_repository.crear')
def test_crear_recurso_sin_zona(mock_crear):
    ok, msg = crear_recurso({'nombre': 'Proyector', 'tipo': 'ELECTRONICO'})
    assert ok is False
    assert 'zona' in msg.lower()


# Tests para toggle_habilitacion (nueva funcionalidad)
@patch('repositories.recurso_repository.obtener')
def test_toggle_recurso_no_encontrado(mock_obtener):
    mock_obtener.return_value = None
    ok, msg = toggle_habilitacion(999)
    assert ok is False
    assert 'no encontrado' in msg.lower()

@patch('repositories.recurso_repository.habilitar')
@patch('repositories.recurso_repository.obtener')
def test_toggle_habilitar_recurso(mock_obtener, mock_habilitar):
    mock_obtener.return_value = {'id': 10, 'eliminado': 1}
    ok, msg = toggle_habilitacion(10)
    assert ok is True
    assert 'habilitado' in msg.lower()
    mock_habilitar.assert_called_once_with(10)

@patch('repositories.reserva_repository.cancelar_por_deshabilitacion')
@patch('repositories.recurso_repository.eliminar_logico')
@patch('repositories.recurso_repository.obtener')
def test_toggle_deshabilitar_recurso_cancela_reservas(mock_obtener, mock_eliminar, mock_cancelar):
    mock_obtener.return_value = {'id': 10, 'eliminado': 0}
    mock_cancelar.return_value = 3
    ok, msg = toggle_habilitacion(10)
    assert ok is True
    assert 'deshabilitado' in msg.lower()
    assert '3' in msg  # Debe mencionar cantidad de reservas canceladas
    mock_eliminar.assert_called_once_with(10)
    mock_cancelar.assert_called_once_with(10)

@patch('repositories.reserva_repository.cancelar_por_deshabilitacion')
@patch('repositories.recurso_repository.eliminar_logico')
@patch('repositories.recurso_repository.obtener')
def test_toggle_deshabilitar_sin_reservas(mock_obtener, mock_eliminar, mock_cancelar):
    mock_obtener.return_value = {'id': 10, 'eliminado': 0}
    mock_cancelar.return_value = 0
    ok, msg = toggle_habilitacion(10)
    assert ok is True
    assert 'deshabilitado' in msg.lower()
    assert 'cancelaron' not in msg.lower()  # No debe mencionar reservas canceladas


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
    ok, msg = editar_recurso(5, {'nombre': 'Pantalla 4K', 'tipo': 'ELECTRONICO', 'ubicacion': 'Sala 2', 'zona_id': 1})
    assert ok is True
    assert 'actualizado' in msg.lower()

@patch('repositories.recurso_repository.editar')
def test_editar_recurso_falta_nombre(mock_editar):
    ok, msg = editar_recurso(5, {'tipo': 'ELECTRONICO', 'zona_id': 1})
    assert ok is False
    assert 'nombre' in msg.lower()

@patch('repositories.recurso_repository.editar')
def test_editar_recurso_falta_zona(mock_editar):
    ok, msg = editar_recurso(5, {'nombre': 'Pantalla 4K', 'tipo': 'ELECTRONICO'})
    assert ok is False
    assert 'zona' in msg.lower()
