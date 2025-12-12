from unittest.mock import patch
from services.admin_service import registrar_usuario

@patch('repositories.user_repository.get_by_email')
@patch('repositories.user_repository.create_user')
def test_registrar_usuario_ok(mock_create, mock_get):
    mock_get.return_value = None
    ok, msg = registrar_usuario('Juan', 'juan@example.com', 'ESTUDIANTE', 'supersegura')
    assert ok is True
    assert 'registrado' in msg.lower()

@patch('repositories.user_repository.get_by_email')
def test_registrar_usuario_email_duplicado(mock_get):
    mock_get.return_value = {'id':1, 'correo':'juan@example.com'}
    ok, msg = registrar_usuario('Juan', 'juan@example.com', 'ESTUDIANTE', 'supersegura')
    assert ok is False
    assert 'ya registrado' in msg.lower()

@patch('repositories.user_repository.get_by_email')
def test_registrar_usuario_contrasena_corta(mock_get):
    mock_get.return_value = None
    ok, msg = registrar_usuario('Juan', 'juan@example.com', 'ESTUDIANTE', '123')
    assert ok is False
    assert 'contraseña' in msg.lower()
