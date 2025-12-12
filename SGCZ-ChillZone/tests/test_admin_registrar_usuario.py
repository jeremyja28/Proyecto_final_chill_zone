from unittest.mock import patch

from services.admin_service import registrar_usuario


@patch('repositories.user_repository.get_by_email')
@patch('repositories.user_repository.create_user')
def test_registrar_usuario_valid(mock_create, mock_get):
    mock_get.return_value = None
    ok, msg = registrar_usuario('Ana', 'ana@pucesa.edu.ec', 'ESTUDIANTE', 'password123')
    assert ok is True


@patch('repositories.user_repository.get_by_email')
@patch('repositories.user_repository.create_user')
def test_registrar_usuario_duplicado(mock_create, mock_get):
    mock_get.return_value = {'id': 1}
    ok, msg = registrar_usuario('Ana', 'ana@pucesa.edu.ec', 'ESTUDIANTE', 'password123')
    assert ok is False
    assert 'ya registrado' in msg


def test_registrar_usuario_correo_invalido():
    ok, msg = registrar_usuario('Ana', 'badmail', 'ESTUDIANTE', 'password123')
    assert ok is False
    assert 'Correo inválido' in msg


def test_registrar_usuario_password_corta():
    ok, msg = registrar_usuario('Ana', 'ana@pucesa.edu.ec', 'ESTUDIANTE', '123')
    assert ok is False
    assert 'contraseña' in msg.lower()
