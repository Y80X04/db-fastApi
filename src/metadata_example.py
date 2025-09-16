"""
Пример использования подхода с метаданными (как в старом проекте src_old)
Этот подход позволяет явно определять структуру таблиц через MetaData и Table
"""

from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, MetaData
from datetime import datetime
from src.database import Base

# Создаем объект метаданных
metadata = MetaData()

# Определяем таблицы явно через Table (как в старом проекте)
role_table = Table(
    "role_metadata_example",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON),
)

user_table = Table(
    "user_metadata_example",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow),
    Column("role_id", Integer, ForeignKey(role_table.c.id)),
    Column("hashed_password", String, nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
)

operation_table = Table(
    "operation_metadata_example",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("quantity", String),
    Column("figi", String),
    Column("instrument_type", String, nullable=True),
    Column("date", TIMESTAMP),
    Column("type", String),
)

# Функция для создания всех таблиц (как в старом проекте)
def create_tables(engine):
    """
    Создает все таблицы, определенные через метаданные
    """
    metadata.create_all(bind=engine)
    print("Таблицы созданы через метаданные")

# Функция для удаления всех таблиц
def drop_tables(engine):
    """
    Удаляет все таблицы, определенные через метаданные
    """
    metadata.drop_all(bind=engine)
    print("Таблицы удалены через метаданные")
