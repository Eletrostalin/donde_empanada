import os
import logging
import asyncio
from sqlalchemy import text
from sqlalchemy.future import select

from app import create_app
from app.models import Migrations
from app.database import get_async_engine, get_async_session

app = create_app()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def check_any_table_exists(session) -> bool:
    async with session.begin():
        result = await session.execute(
            text("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public');")
        )
        return result.scalar()


async def record_migration(session, migration_name: str):
    new_migration = Migrations(migration_name=migration_name)
    session.add(new_migration)
    await session.commit()
    logging.info(f"Миграция {migration_name} записана в таблицу migrations.")


async def apply_migrations():
    engine = get_async_engine()
    async_session = get_async_session(engine)
    migrations_folder = 'migrations'

    async with async_session() as session:
        tables_exist = await check_any_table_exists(session)

        if tables_exist:
            result = await session.execute(
                text("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'migrations');")
            )
            migrations_table_exists = result.scalar()

            if migrations_table_exists:
                result = await session.execute(select(Migrations.migration_name))
                applied_migrations = set(row[0] for row in result.all())
            else:
                applied_migrations = set()
                logging.info("Таблица 'migration' не найдена. Применение всех миграций.")
        else:
            applied_migrations = set()
            logging.info("Таблицы не найдены в базе данных. Применение всех миграций.")

        all_migrations = [f for f in os.listdir(migrations_folder) if f.endswith('.sql')]
        new_migrations = [m for m in all_migrations if m not in applied_migrations]
        new_migrations.sort()

        if new_migrations:
            logging.info(f"Найдено {len(new_migrations)} новых миграций: {new_migrations}")

            async with engine.connect() as conn:
                async with conn.begin():
                    try:
                        for migration in new_migrations:
                            migration_file_path = os.path.join(migrations_folder, migration)

                            with open(migration_file_path, 'r', encoding='utf-8') as migration_file:
                                sql_commands = migration_file.read()

                            for command in sql_commands.split(';'):
                                command = command.strip()
                                if command:
                                    logging.info(f"Применение SQL команды:\n{command}")
                                    await conn.execute(text(command))

                        await conn.commit()

                        for migration in new_migrations:
                            await record_migration(session, migration)

                        logging.info(f"Миграции {new_migrations} успешно применены.")

                    except Exception as e:
                        logging.error(f"Ошибка при применении миграции: {e}")
                        await conn.rollback()
                    else:
                        await conn.commit()
        else:
            logging.info("Новые миграции отсутствуют.")


def main():
    with app.app_context():
        asyncio.run(apply_migrations())
    app.run(debug=True)


if __name__ == '__main__':
    main()
