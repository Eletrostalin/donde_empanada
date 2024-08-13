from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from flask import current_app

def get_async_engine():
    DATABASE_URL = current_app.config['DATABASE_URL']
    return create_async_engine(DATABASE_URL, echo=True)

def get_async_session(engine):
    return sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession
    )
