# Code from /Users/nickstanchenkov/donde_empanada4/donde_empanada4/run.py
from app import create_app
from app.models import db, Migration
import os
import logging

app = create_app()

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def apply_migrations():
    # Путь к папке с миграциями
    migrations_path = os.path.join(os.path.dirname(__file__), 'migrations')

    # Получаем список всех файлов в папке миграций
    migration_files = [f for f in os.listdir(migrations_path) if f.endswith('.sql')]

    # Проверка на наличие таблицы миграций в базе данных
    if not db.engine.dialect.has_table(db.engine, 'migrations'):
        # Если таблицы нет, создаем ее
        db.session.execute('''
            CREATE TABLE migrations (
                id SERIAL PRIMARY KEY,
                migration_name VARCHAR(255) NOT NULL UNIQUE,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        db.session.commit()
        logger.info('Таблица migrations создана, так как она отсутствовала.')

    # Проверяем каждую миграцию
    for migration_file in migration_files:
        migration_name = os.path.basename(migration_file)

        # Логирование начала проверки миграции
        logger.info(f'Проверка миграции: {migration_name}')

        # Проверяем, применена ли эта миграция
        if not Migration.query.filter_by(migration_name=migration_name).first():
            # Читаем SQL из файла
            with open(os.path.join(migrations_path, migration_file), 'r', encoding='utf-8') as f:
                migration_sql = f.read()

            try:
                # Логирование начала выполнения миграции
                logger.info(f'Выполнение миграции: {migration_name}')

                # Выполняем SQL команду
                db.session.execute(migration_sql)
                db.session.commit()

                # Записываем информацию о выполненной миграции в базу данных
                new_migration = Migration(migration_name=migration_name)
                db.session.add(new_migration)
                db.session.commit()

                # Логирование успешного выполнения миграции
                logger.info(f'Миграция {migration_name} успешно выполнена.')
            except Exception as e:
                # Откат изменений в случае ошибки
                db.session.rollback()
                logger.error(f'Ошибка при выполнении миграции {migration_name}: {e}')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создаем все таблицы, включая таблицу миграций
        apply_migrations()  # Выполняем миграции
    app.run(debug=True)
# End of code from /Users/nickstanchenkov/donde_empanada4/donde_empanada4/run.py
