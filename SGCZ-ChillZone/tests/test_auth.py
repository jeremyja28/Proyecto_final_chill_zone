import pytest
from unittest.mock import patch

from services import auth_service


@patch('repositories.user_repository.get_by_email')
def test_authenticate_success(mock_get):
    # bcrypt hash for password 'secret' (precomputed)
    hashed = b'$2b$12$C9GZq3nY3sGmGvFQ4GZ3Xui5KzqC61x8FZ8n2dJr1m6k3f6XHkTgK'
    mock_get.return_value = {
        'id': 1,
        'nombre': 'Juan',
        'correo': 'juan@pucesa.edu.ec',
        'hash_password': hashed,
        'rol': 'ESTUDIANTE',
        'estado': 'ACTIVO',
    }
    user = auth_service.authenticate('juan@pucesa.edu.ec', 'secret')
    assert user is not None


@patch('repositories.user_repository.get_by_email')
def test_authenticate_fail_wrong_password(mock_get):
    hashed = b'$2b$12$C9GZq3nY3sGmGvFQ4GZ3Xui5KzqC61x8FZ8n2dJr1m6k3f6XHkTgK'
    mock_get.return_value = {
        'id': 1,
        'nombre': 'Juan',
        'correo': 'juan@pucesa.edu.ec',
        'hash_password': hashed,
        'rol': 'ESTUDIANTE',
        'estado': 'ACTIVO',
    }
    user = auth_service.authenticate('juan@pucesa.edu.ec', 'bad')
    assert user is None
