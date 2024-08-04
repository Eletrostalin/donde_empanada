from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import logging
from logging import StreamHandler
import os
import psycopg2
from sqlalchemy.engine import make_url

from config import Config

# Инициализация расширений
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()

def apply_pending_migrations(app):
    """Проверяет и применяет новые миграции."""
    migration_folder = os.path.join(app.root_path, 'migrations')
    migration_list_file = os.path.join(migration_folder, 'migration_list')

    # Читаем список применённых миграций
    if os.path.exists(migration_list_file):
        with open(migration_list_file, 'r') as file:
            applied_migrations = file.read().splitlines()
    else:
        applied_migrations = []

    # Получаем список файлов миграций
    migration_files = [
        f for f in os.listdir(migration_folder) if f.endswith('.sql')
    ]

    # Фильтруем новые миграции
    new_migrations = [f for f in migration_files if f not in applied_migrations]

    if not new_migrations:
        app.logger.info('Нет новых миграций для применения.')
        return

    # Парсим DATABASE_URL
    url = make_url(app.config['SQLALCHEMY_DATABASE_URI'])

    try:
        # Подключаемся к базе данных
        conn = psycopg2.connect(
            dbname=url.database,
            user=url.username,
            password=url.password,
            host=url.host,
            port=url.port
        )
        cursor = conn.cursor()

        for migration_file in new_migrations:
            # Применяем каждую новую миграцию
            with open(os.path.join(migration_folder, migration_file), 'r') as file:
                migration_sql = file.read()
                cursor.execute(migration_sql)
                conn.commit()
                app.logger.info(f'Миграция {migration_file} применена.')

            # Добавляем файл миграции в список применённых
            applied_migrations.append(migration_file)

        # Обновляем список применённых миграций
        with open(migration_list_file, 'w') as file:
            for migration in applied_migrations:
                file.write(migration + '\n')

        cursor.close()
        conn.close()

    except Exception as e:
        app.logger.error(f'Ошибка при применении миграций: {e}')
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
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

    # Настройка логирования
    stream_handler = StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.DEBUG)

    # Применяем миграции перед запуском приложения
    apply_pending_migrations(app)

    return app
