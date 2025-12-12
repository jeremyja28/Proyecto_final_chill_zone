from unittest.mock import patch
from services.admin_service import registrar_usuario


@patch('repositories.user_repository.create_user')
@patch('repositories.user_repository.get_by_email')
def test_admin_registra_usuario_ok(mock_get, mock_create):
    mock_get.return_value = None
    ok, msg = registrar_usuario('Carlos', 'carlos@pucesa.edu.ec', 'ESTUDIANTE', 'secreto123')
    assert ok is True


@patch('repositories.user_repository.get_by_email')
def test_admin_registro_duplicado(mock_get):
    mock_get.return_value = {'id': 1}
    ok, msg = registrar_usuario('Ana', 'ana@pucesa.edu.ec', 'ESTUDIANTE', 'password123')
    assert ok is False
    assert 'ya registrado' in msg


def test_admin_registro_email_invalido():
    ok, msg = registrar_usuario('Ana', 'bad-email', 'ESTUDIANTE', 'password123')
    assert ok is False
    assert 'correo inválido' in msg.lower()
