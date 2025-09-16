"""
Модуль для автоматического создания таблиц и заполнения начальными данными при первом запуске
Это аналог подхода из старого проекта src_old, где таблицы создавались автоматически с данными
"""

from src.database import Base, engine
import asyncio
import asyncpg
import json
import hashlib
from datetime import datetime
from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER, DEFAULT_ADMIN_PASSWORD, DEFAULT_USER_PASSWORD

async def create_tables_and_seed_data():
    """
    Создает все таблицы и заполняет их начальными данными, если они еще не существуют
    Это аналог подхода с метаданными из старого проекта
    """
    try:
        # Импортируем модели, чтобы они были зарегистрированы в Base.metadata
        from src.auth import models as auth_models
        from src.operations import models as operations_models
        
        # Создаем таблицы
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Все таблицы успешно созданы")
        
        # Заполняем начальными данными
        await seed_initial_data()
        print("Начальные данные успешно добавлены")
        
        return True
    except Exception as e:
        print(f"Ошибка при создании таблиц и данных: {e}")
        import traceback
        traceback.print_exc()
        return False

def sync_create_tables_and_seed_data():
    """
    Синхронная версия создания таблиц и заполнения данными
    """
    try:
        # Импортируем модели, чтобы они были зарегистрированы в Base.metadata
        from src.auth import models as auth_models
        from src.operations import models as operations_models
        
        # Создаем синхронный engine
        from sqlalchemy import create_engine
        sync_url = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        sync_engine = create_engine(sync_url)
        
        # Создаем все таблицы синхронно
        Base.metadata.create_all(bind=sync_engine)
        print("Все таблицы успешно созданы (синхронно)")
        
        # Заполняем начальными данными через асинхронный вызов
        asyncio.run(seed_initial_data())
        print("Начальные данные успешно добавлены (синхронно)")
        
        return True
    except Exception as e:
        print(f"Ошибка при создании таблиц и данных: {e}")
        import traceback
        traceback.print_exc()
        return False

async def seed_initial_data():
    """
    Асинхронное заполнение начальными данными
    """
    try:
        # Хэшируем пароли
        def hash_password(password):
            return hashlib.sha256(password.encode()).hexdigest()
        
        connection_string = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        conn = await asyncpg.connect(connection_string)
        
        # Создаем роли
        print("Создание базовых ролей...")
        
        # Проверяем существование роли admin
        admin_role_exists = await conn.fetchval(
            "SELECT EXISTS (SELECT 1 FROM role WHERE name = $1)", 
            "admin"
        )
        
        if not admin_role_exists:
            admin_role_id = await conn.fetchval(
                "INSERT INTO role (name, permissions) VALUES ($1, $2) RETURNING id",
                "admin", 
                json.dumps({"admin": True, "read": True, "write": True, "delete": True})
            )
            print(f"Создана роль admin с id={admin_role_id}")
        else:
            admin_role_id = await conn.fetchval("SELECT id FROM role WHERE name = $1", "admin")
            print(f"Роль admin уже существует с id={admin_role_id}")
        
        # Проверяем существование роли user
        user_role_exists = await conn.fetchval(
            "SELECT EXISTS (SELECT 1 FROM role WHERE name = $1)", 
            "user"
        )
        
        if not user_role_exists:
            user_role_id = await conn.fetchval(
                "INSERT INTO role (name, permissions) VALUES ($1, $2) RETURNING id",
                "user",
                json.dumps({"read": True, "write": True, "delete": False})
            )
            print(f"Создана роль user с id={user_role_id}")
        else:
            user_role_id = await conn.fetchval("SELECT id FROM role WHERE name = $1", "user")
            print(f"Роль user уже существует с id={user_role_id}")
        
        # Создаем пользователей
        print("Создание базовых пользователей...")
        
        # Пользователь admin
        admin_exists = await conn.fetchval(
            "SELECT EXISTS (SELECT 1 FROM \"user\" WHERE username = $1)", 
            "admin"
        )
        
        if not admin_exists:
            await conn.execute(
                """INSERT INTO "user" (email, username, role_id, hashed_password, is_active, is_superuser, is_verified, registered_at) 
                   VALUES ($1, $2, $3, $4, $5, $6, $7, $8)""",
                "admin@example.com",
                "admin",
                admin_role_id,
                hash_password(DEFAULT_ADMIN_PASSWORD),
                True,  # is_active
                True,  # is_superuser
                True,  # is_verified
                datetime.now()
            )
            print("Создан пользователь admin")
        else:
            print("Пользователь admin уже существует")
        
        # Пользователь user
        user_exists = await conn.fetchval(
            "SELECT EXISTS (SELECT 1 FROM \"user\" WHERE username = $1)", 
            "user"
        )
        
        if not user_exists:
            await conn.execute(
                """INSERT INTO "user" (email, username, role_id, hashed_password, is_active, is_superuser, is_verified, registered_at) 
                   VALUES ($1, $2, $3, $4, $5, $6, $7, $8)""",
                "user@example.com",
                "user",
                user_role_id,
                hash_password(DEFAULT_USER_PASSWORD),
                True,  # is_active
                False, # is_superuser
                True,  # is_verified
                datetime.now()
            )
            print("Создан пользователь user")
        else:
            print("Пользователь user уже существует")
        
        await conn.close()
        return True
        
    except Exception as e:
        print(f"Ошибка при добавлении начальных данных: {e}")
        import traceback
        traceback.print_exc()
        return False

# Эта функция может быть вызвана при запуске приложения
async def initialize_database_on_startup():
    """
    Инициализирует базу данных при запуске приложения
    """
    print("Проверка и создание таблиц с данными при необходимости...")
    success = await create_tables_and_seed_data()
    if success:
        print("База данных готова к работе")
    else:
        print("Не удалось инициализировать базу данных")
    return success
