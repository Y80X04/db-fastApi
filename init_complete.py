#!/usr/bin/env python3
"""
Полный скрипт инициализации базы данных:
1. Создание базы данных (если не существует)
2. Выполнение миграций
3. Заполнение начальными данными
"""

import asyncio
import asyncpg
import os
import sys

# Добавляем src в путь поиска модулей
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Импортируем конфигурацию
from src.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS

async def create_database_if_not_exists():
    """Создает базу данных, если она не существует"""
    try:
        print("Проверка существования базы данных...")
        
        # Подключение к PostgreSQL серверу (без указания конкретной базы данных)
        connection_string = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/postgres"
        conn = await asyncpg.connect(connection_string)
        
        # Проверяем, существует ли база данных
        exists = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1", 
            DB_NAME
        )
        
        if not exists:
            print(f"База данных '{DB_NAME}' не найдена, создаем...")
            # Создаем базу данных
            await conn.execute(f'CREATE DATABASE "{DB_NAME}"')
            print(f"✓ База данных '{DB_NAME}' успешно создана")
        else:
            print(f"ℹ База данных '{DB_NAME}' уже существует")
            
        await conn.close()
        return True
        
    except Exception as e:
        print(f"✗ Ошибка при создании базы данных: {e}")
        return False

def run_migrations():
    """Выполняет миграции Alembic"""
    try:
        print("\nВыполнение миграций...")
        from alembic.config import Config
        from alembic import command
        import os
        
        # Путь к файлу alembic.ini
        alembic_cfg = Config("alembic.ini")
        
        # Выполняем миграции
        command.upgrade(alembic_cfg, "head")
        print("✓ Миграции успешно выполнены")
        return True
        
    except Exception as e:
        print(f"✗ Ошибка при выполнении миграций: {e}")
        import traceback
        print(traceback.format_exc())
        return False

async def seed_initial_data():
    """Заполняет базу данных начальными данными"""
    try:
        print("\nЗаполнение начальными данными...")
        
        # Импортируем скрипт заполнения данных
        from seed_data import seed_database
        result = await seed_database()
        
        if result:
            print("✓ Начальные данные успешно добавлены")
            return True
        else:
            print("✗ Ошибка при добавлении начальных данных")
            return False
            
    except Exception as e:
        print(f"✗ Ошибка при заполнении начальными данными: {e}")
        import traceback
        print(traceback.format_exc())
        return False

async def main():
    """Основная функция инициализации"""
    print("Полная инициализация базы данных")
    print("=" * 50)
    
    try:
        # 1. Создаем базу данных
        db_created = await create_database_if_not_exists()
        if not db_created:
            print("✗ Не удалось создать базу данных")
            return False
        
        # 2. Выполняем миграции
        migrations_ok = run_migrations()
        if not migrations_ok:
            print("✗ Не удалось выполнить миграции")
            return False
        
        # 3. Заполняем начальными данными
        seed_ok = await seed_initial_data()
        if not seed_ok:
            print("✗ Не удалось заполнить начальными данными")
            return False
        
        print("\n" + "=" * 50)
        print("✓ Полная инициализация завершена успешно!")
        print("\nСозданы:")
        print("  - База данных: postgres")
        print("  - Таблицы: role, user, operation")
        print("  - Роли: admin, user")
        print("  - Пользователи: admin (пароль: admin123), user (пароль: user123)")
        return True
        
    except Exception as e:
        print(f"✗ Критическая ошибка: {e}")
        import traceback
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    result = asyncio.run(main())
    
    if result:
        print("\n🎉 Инициализация успешно завершена!")
        sys.exit(0)
    else:
        print("\n❌ Инициализация не завершена!")
        sys.exit(1)
