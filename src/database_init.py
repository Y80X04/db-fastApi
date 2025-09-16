import asyncio
import asyncpg
import logging
import json
import hashlib
import os
import sys
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Получаем путь к директории src
src_dir = os.path.dirname(os.path.abspath(__file__))

# Импортируем конфигурацию напрямую
config_path = os.path.join(src_dir, 'config.py')
sys.path.insert(0, src_dir)

# Загружаем конфигурацию вручную
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5439")
DB_NAME = os.environ.get("DB_NAME", "postgres")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASS = os.environ.get("DB_PASS", "postgres")
DEFAULT_ADMIN_PASSWORD = os.environ.get("DEFAULT_ADMIN_PASSWORD", "admin123")
DEFAULT_USER_PASSWORD = os.environ.get("DEFAULT_USER_PASSWORD", "user123")

async def create_database_if_not_exists():
    """
    Создает базу данных, если она не существует
    """
    # Подключение к PostgreSQL серверу (без указания конкретной базы данных)
    connection_string = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/postgres"
    
    try:
        logger.info(f"Подключение к PostgreSQL серверу: {DB_HOST}:{DB_PORT}")
        # Создаем подключение к серверу PostgreSQL
        conn = await asyncpg.connect(connection_string)
        logger.info("Успешное подключение к PostgreSQL серверу")
        
        # Проверяем, существует ли база данных
        exists = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1", 
            DB_NAME
        )
        
        if not exists:
            logger.info(f"База данных '{DB_NAME}' не найдена, создаем...")
            # Создаем базу данных
            await conn.execute(f'CREATE DATABASE "{DB_NAME}"')
            logger.info(f"База данных '{DB_NAME}' успешно создана")
        else:
            logger.info(f"База данных '{DB_NAME}' уже существует")
            
        await conn.close()
        return True
        
    except Exception as e:
        logger.error(f"Ошибка при работе с базой данных: {e}")
        return False

def run_migrations():
    """
    Выполняет миграции Alembic
    """
    try:
        from alembic.config import Config
        from alembic import command
        
        logger.info("Запуск миграций Alembic...")
        
        # Путь к файлу alembic.ini (относительно корня проекта)
        alembic_cfg = Config(os.path.join(os.path.dirname(os.path.dirname(__file__)), "alembic.ini"))
        
        # Выполняем миграции
        command.upgrade(alembic_cfg, "head")
        logger.info("Миграции успешно выполнены")
        return True
        
    except Exception as e:
        logger.error(f"Ошибка при выполнении миграций: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

async def seed_initial_data():
    """
    Заполняет базу данных начальными данными:
    - Создает базовые роли (admin, user)
    - Создает пользователей (admin, user)
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
            logger.info(f"Создана роль admin с id={admin_role_id}")
        else:
            admin_role_id = await conn.fetchval("SELECT id FROM role WHERE name = $1", "admin")
            logger.info(f"Роль admin уже существует с id={admin_role_id}")
        
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
            logger.info(f"Создана роль user с id={user_role_id}")
        else:
            user_role_id = await conn.fetchval("SELECT id FROM role WHERE name = $1", "user")
            logger.info(f"Роль user уже существует с id={user_role_id}")
        
        # Создаем пользователей
        logger.info("Создание базовых пользователей...")
        
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
            logger.info("Создан пользователь admin")
        else:
            logger.info("Пользователь admin уже существует")
        
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
            logger.info("Создан пользователь user")
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

async def init_database():
    """
    Инициализирует базу данных: создает базу данных, выполняет миграции и заполняет начальными данными
    """
    logger.info("Начало инициализации базы данных...")
    
    try:
        # Создаем базу данных, если она не существует
        db_created = await create_database_if_not_exists()
        if not db_created:
            logger.error("Не удалось создать базу данных")
            return False
        
        # Выполняем миграции
        migrations_ok = run_migrations()
        if not migrations_ok:
            logger.error("Не удалось выполнить миграции")
            return False
        
        # Заполняем начальными данными
        seed_ok = await seed_initial_data()
        if not seed_ok:
            logger.error("Не удалось заполнить начальными данными")
            return False
        
        logger.info("Инициализация базы данных завершена успешно")
        return True
        
    except Exception as e:
        logger.error(f"Ошибка при инициализации базы данных: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False
