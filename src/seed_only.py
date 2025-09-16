"""
Модуль для заполнения только начальными данными
Без создания базы данных и миграций
"""

import asyncio
import asyncpg
import logging
import json
import hashlib
import os
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Загружаем конфигурацию из environment variables
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5439")
DB_NAME = os.environ.get("DB_NAME", "postgres")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASS = os.environ.get("DB_PASS", "postgres")
DEFAULT_ADMIN_PASSWORD = os.environ.get("DEFAULT_ADMIN_PASSWORD", "admin123")
DEFAULT_USER_PASSWORD = os.environ.get("DEFAULT_USER_PASSWORD", "user123")

async def seed_initial_data_only():
    """
    Заполняет базу данных только начальными данными (без создания базы и миграций)
    """
    try:
        # Хэшируем пароли
        def hash_password(password):
            return hashlib.sha256(password.encode()).hexdigest()
        
        connection_string = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        conn = await asyncpg.connect(connection_string)
        logger.info("Подключение к базе данных для заполнения начальными данными")
        
        # Создаем роли
        logger.info("Создание базовых ролей...")
        
        # Проверяем существование роли admin
        try:
            admin_role_exists = await conn.fetchval(
                "SELECT EXISTS (SELECT 1 FROM role WHERE name = $1)", 
                "admin"
            )
        except Exception as e:
            logger.warning(f"Таблица role не существует или ошибка доступа: {e}")
            await conn.close()
            return False
        
        if not admin_role_exists:
            try:
                admin_role_id = await conn.fetchval(
                    "INSERT INTO role (name, permissions) VALUES ($1, $2) RETURNING id",
                    "admin", 
                    json.dumps({"admin": True, "read": True, "write": True, "delete": True})
                )
                logger.info(f"Создана роль admin с id={admin_role_id}")
            except Exception as e:
                logger.error(f"Ошибка при создании роли admin: {e}")
                await conn.close()
                return False
        else:
            admin_role_id = await conn.fetchval("SELECT id FROM role WHERE name = $1", "admin")
            logger.info(f"Роль admin уже существует с id={admin_role_id}")
        
        # Проверяем существование роли user
        try:
            user_role_exists = await conn.fetchval(
                "SELECT EXISTS (SELECT 1 FROM role WHERE name = $1)", 
                "user"
            )
        except Exception as e:
            logger.warning(f"Ошибка при проверке существования роли user: {e}")
            await conn.close()
            return False
        
        if not user_role_exists:
            try:
                user_role_id = await conn.fetchval(
                    "INSERT INTO role (name, permissions) VALUES ($1, $2) RETURNING id",
                    "user",
                    json.dumps({"read": True, "write": True, "delete": False})
                )
                logger.info(f"Создана роль user с id={user_role_id}")
            except Exception as e:
                logger.error(f"Ошибка при создании роли user: {e}")
                await conn.close()
                return False
        else:
            user_role_id = await conn.fetchval("SELECT id FROM role WHERE name = $1", "user")
            logger.info(f"Роль user уже существует с id={user_role_id}")
        
        # Создаем пользователей
        logger.info("Создание базовых пользователей...")
        
        # Пользователь admin
        try:
            admin_exists = await conn.fetchval(
                "SELECT EXISTS (SELECT 1 FROM \"user\" WHERE username = $1)", 
                "admin"
            )
        except Exception as e:
            logger.warning(f"Ошибка при проверке существования пользователя admin: {e}")
            await conn.close()
            return False
        
        if not admin_exists:
            try:
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
                logger.info("Создан пользователь admin")
            except Exception as e:
                logger.error(f"Ошибка при создании пользователя admin: {e}")
                await conn.close()
                return False
        else:
            logger.info("Пользователь admin уже существует")
        
        # Пользователь user
        try:
            user_exists = await conn.fetchval(
                "SELECT EXISTS (SELECT 1 FROM \"user\" WHERE username = $1)", 
                "user"
            )
        except Exception as e:
            logger.warning(f"Ошибка при проверке существования пользователя user: {e}")
            await conn.close()
            return False
        
        if not user_exists:
            try:
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
                logger.info("Создан пользователь user")
            except Exception as e:
                logger.error(f"Ошибка при создании пользователя user: {e}")
                await conn.close()
                return False
        else:
            logger.info("Пользователь user уже существует")
        
        await conn.close()
        logger.info("Начальные данные успешно добавлены")
        return True
        
    except Exception as e:
        logger.error(f"Ошибка при добавлении начальных данных: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

async def seed_database():
    """
    Основная функция для заполнения базы данных начальными данными
    """
    logger.info("Начало заполнения базы данных начальными данными...")
    
    try:
        seed_ok = await seed_initial_data_only()
        if not seed_ok:
            logger.error("Не удалось заполнить начальными данными")
            return False
        
        logger.info("Заполнение базы данных начальными данными завершено успешно")
        return True
        
    except Exception as e:
        logger.error(f"Ошибка при заполнении базы данных: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False
