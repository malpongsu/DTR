import tempfile
from pathlib import Path

from website import create_app


def make_app():
    temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
    temp_db.close()
    db_path = Path(temp_db.name)
    app = create_app({
        'TESTING': True,
        'DATABASE': str(db_path),
        'WTF_CSRF_ENABLED': False,
        'ADMIN_USERNAME': 'admin',
        'ADMIN_PASSWORD': 'admin123',
    })
    return app, db_path


def test_attendance_page_renders():
    app, _ = make_app()
    client = app.test_client()

    response = client.get('/attendance')
    assert response.status_code == 200
    assert b'RFID' in response.data or b'Tap' in response.data


def test_admin_requires_login():
    app, _ = make_app()
    client = app.test_client()

    response = client.get('/admin/dashboard', follow_redirects=False)
    assert response.status_code == 302
    assert response.headers['Location'].startswith('/admin')


def test_admin_login_and_dashboard_access():
    app, _ = make_app()
    client = app.test_client()

    login = client.post('/admin/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=False)
    assert login.status_code == 302
    assert login.headers['Location'].endswith('/admin/dashboard')

    dashboard = client.get('/admin/dashboard')
    assert dashboard.status_code == 200
    assert b'Admin Dashboard' in dashboard.data


def test_hid_scanner_prefix_and_enter_are_ignored():
    app, _ = make_app()
    client = app.test_client()

    client.post('/add-user', data={'name': 'Alice', 'rfid_tag': 'ab 12 cd 34'})

    response = client.post('/attendance', data={'rfid_number': 'RFID:ab12cd34\r'}, follow_redirects=False)
    assert response.status_code == 302
    assert response.headers['Location'].endswith('/attendance')


def test_app_uses_database_url_from_environment(monkeypatch):
    monkeypatch.setenv('DATABASE_URL', '/tmp/vercel-attendance.db')

    app = create_app()

    assert app.config['DATABASE'] == '/tmp/vercel-attendance.db'
