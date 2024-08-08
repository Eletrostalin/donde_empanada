from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import logging
from logging import StreamHandler
import sys

# Инициализация расширений
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Настройка логирования
    stream_handler = StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.DEBUG)

    # Логирование для Alembic
    alembic_logger = logging.getLogger('alembic')
    alembic_logger.addHandler(stream_handler)
    alembic_logger.setLevel(logging.INFO)

    # Инициализация расширений
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    with app.app_context():
        from . import models
        from .models import User

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

    from . import routes
    app.register_blueprint(routes.bp)

    return app
