# Code from /Users/nickstanchenkov/donde_empanada4/donde_empanada4/run.py
from app import create_app
from app.models import db, Migration
import os

app = create_app()

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
        app.logger.info('Таблица migrations создана, так как она отсутствовала.')

    # Проверяем каждую миграцию
    for migration_file in migration_files:
        migration_name = os.path.basename(migration_file)

        # Проверяем, применена ли эта миграция
        if not Migration.query.filter_by(migration_name=migration_name).first():
            # Читаем SQL из файла
            with open(os.path.join(migrations_path, migration_file), 'r', encoding='utf-8') as f:
                migration_sql = f.read()

            try:
                # Выполняем SQL команду
                db.session.execute(migration_sql)
                db.session.commit()

                # Записываем информацию о выполненной миграции в базу данных
                new_migration = Migration(migration_name=migration_name)
                db.session.add(new_migration)
                db.session.commit()

                app.logger.info(f'Migration {migration_name} applied successfully.')
            except Exception as e:
                db.session.rollback()
                app.logger.error(f'Error applying migration {migration_name}: {e}')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создаем все таблицы, включая таблицу миграций
        apply_migrations()  # Выполняем миграции
    app.run(debug=True)
# End of code from /Users/nickstanchenkov/donde_empanada4/donde_empanada4/run.py
