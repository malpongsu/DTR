import os
from pathlib import Path

from flask import Flask

from .models import init_app


def resolve_database_path():
    database_url = os.environ.get('DATABASE_URL') or os.environ.get('DATABASE') or 'website/attendance.db'

    if database_url.startswith('sqlite:///'):
        candidate = database_url.replace('sqlite:///', '', 1)
        return candidate if os.path.isabs(candidate) else str(Path.cwd() / candidate)

    if database_url.startswith('sqlite://'):
        candidate = database_url.replace('sqlite://', '', 1)
        return candidate if os.path.isabs(candidate) else str(Path.cwd() / candidate)

    if database_url.startswith('file://'):
        candidate = database_url.replace('file://', '', 1)
        return candidate if os.path.isabs(candidate) else str(Path.cwd() / candidate)

    if database_url.startswith('postgres') or database_url.startswith('mysql'):
        return database_url

    if os.path.isabs(database_url):
        return database_url

    return str(Path.cwd() / database_url)


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'animax'),
        DATABASE=resolve_database_path(),
        ADMIN_USERNAME=os.environ.get('ADMIN_USERNAME', 'admin'),
        ADMIN_PASSWORD=os.environ.get('ADMIN_PASSWORD', 'admin123'),
    )

    if test_config:
        app.config.update(test_config)

    from .views import views
    from .auth import auth
    from .admin import admin

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/admin')

    init_app(app)
    return app

