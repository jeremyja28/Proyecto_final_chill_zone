from app import create_app

app = create_app()

def test_sidebar_admin_contains_estadisticas():
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['nombre'] = 'Admin'
            sess['rol'] = 'ADMIN'
        resp = client.get('/')
        html = resp.get_data(as_text=True)
        assert 'Estadísticas' in html and 'Incidencias' in html and 'Administración' in html

def test_sidebar_estudiante_excludes_admin_links():
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['nombre'] = 'Alumno'
            sess['rol'] = 'ESTUDIANTE'
        resp = client.get('/')
        html = resp.get_data(as_text=True)
        assert 'Estadísticas' not in html
        assert 'Incidencias' not in html
        assert 'Administración' not in html
        # Debe mostrar Reservas y Recursos
        assert 'Reservas' in html and 'Recursos' in html
