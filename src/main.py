from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
import sys
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Добавляем путь к директории src для корректных импортов
src_path = os.path.dirname(os.path.abspath(__file__))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Импортируем маршруты и конфигурацию с абсолютными путями
from src.auth.base_config import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate
from src.operations.router import router as router_operation
from src.auto_create_tables import initialize_database_on_startup

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler - инициализируем базу данных при запуске
    """
    try:
        # Автоматическое создание таблиц и заполнение начальными данными при первом запуске
        await initialize_database_on_startup()
        logger.info("База данных успешно инициализирована при запуске")
        
    except Exception as e:
        logger.warning(f"Не удалось автоматически инициализировать базу данных: {e}")
        logger.info("Пожалуйста, запустите 'python init_complete.py' вручную для инициализации базы данных")
        pass
    
    yield
    
    # Очистка ресурсов при завершении (если нужно)
    logger.info("Приложение завершает работу")

app = FastAPI(
    title="Trading App",
    lifespan=lifespan
)

# Подключаем маршруты
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_operation)
