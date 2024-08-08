import os
import logging
import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy import text
from app import create_app
from app.models import db, Migration

app = create_app()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Асинхронный движок SQLAlchemy с использованием драйвера asyncpg
DATABASE_URL = os.getenv('DATABASE_URL').replace("psycopg2", "asyncpg")
async_engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async def check_any_table_exists() -> bool:
    """
    Проверяет, существуют ли какие-либо таблицы в базе данных.
    Возвращает True, если таблицы существуют, иначе False.
    """
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                text("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public');")
            )
            return result.scalar()

async def apply_migrations():
    """
    Применяет новые миграции из папки migrations к базе данных, используя SQLAlchemy.
    """
    migrations_folder = 'migrations'

    # Проверка наличия любых таблиц в базе данных
    tables_exist = await check_any_table_exists()

    async with async_session() as session:
        if tables_exist:
            # Проверяем, существует ли таблица migrations
            result = await session.execute(
                text("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'migration');")
            )
            migrations_table_exists = result.scalar()

            if migrations_table_exists:
                # Получаем список применённых миграций из таблицы migration
                result = await session.execute(select(Migration.migration_name))
                applied_migrations = set(row[0] for row in result.all())
            else:
                applied_migrations = set()
                logging.info("Таблица 'migration' не найдена. Применение всех миграций.")
        else:
            applied_migrations = set()
            logging.info("Таблицы не найдены в базе данных. Применение всех миграций.")

        # Получение списка всех SQL файлов в папке миграций
        all_migrations = [f for f in os.listdir(migrations_folder) if f.endswith('.sql')]

        # Фильтрация новых миграций, которые ещё не были применены
        new_migrations = [m for m in all_migrations if m not in applied_migrations]

        # Сортировка миграций по имени файла для их применения в порядке
        new_migrations.sort()

        if new_migrations:
            logging.info(f"Найдено {len(new_migrations)} новых миграций: {new_migrations}")

            async with async_engine.connect() as conn:  # Используем async_engine для подключения к базе данных
                async with conn.begin():  # Начало транзакции
                    try:
                        for migration in new_migrations:
                            migration_file_path = os.path.join(migrations_folder, migration)

                            # Открытие файла миграции и чтение SQL команд
                            with open(migration_file_path, 'r', encoding='utf-8') as migration_file:
                                sql_commands = migration_file.read()

                            # Разделение команд по ';' и выполнение каждой команды отдельно
                            for command in sql_commands.split(';'):
                                command = command.strip()
                                if command:  # Игнорируем пустые строки
                                    logging.info(f"Применение SQL команды:\n{command}")
                                    await conn.execute(text(command))  # Выполнение SQL команды

                        await conn.commit()

                        # Добавление миграций в базу данных после выполнения всех команд
                        for migration in new_migrations:
                            new_migration = Migration(migration_name=migration)
                            session.add(new_migration)
                        await session.commit()
                        logging.info(f"Миграции {new_migrations} успешно применены.")

                    except Exception as e:
                        logging.error(f"Ошибка при применении миграции: {e}")
                        await conn.rollback()  # Откат транзакции при ошибке
                    else:
                        await conn.commit()  # Подтверждение транзакции
        else:
            logging.info("Новые миграции отсутствуют.")


def main():
    """
    Основная функция для запуска приложения.
    """
    with app.app_context():
        asyncio.run(apply_migrations())  # Применяем миграции
    app.run(debug=True)

if __name__ == '__main__':
    main()
