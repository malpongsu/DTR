from flask import Flask

from .models import init_app


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='animax',
        DATABASE='website/attendance.db',
        ADMIN_USERNAME='admin',
        ADMIN_PASSWORD='admin123',
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

