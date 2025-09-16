#!/usr/bin/env python3
"""
Простой тестовый скрипт для проверки работы с базой данных
"""

import asyncio
import asyncpg
import os
import sys

# Добавляем src в путь поиска модулей
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Импортируем конфигурацию
from src.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS

async def test_database():
    try:
        print("Тестирование базы данных...")
        print(f"Хост: {DB_HOST}:{DB_PORT}")
        print(f"База данных: {DB_NAME}")
        
        # Подключение к PostgreSQL серверу
        connection_string = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        print(f"Строка подключения: {connection_string}")
        
        conn = await asyncpg.connect(connection_string)
        print("✓ Успешное подключение к базе данных!")
        
        # Проверяем существование базы данных
        db_exists = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1", 
            DB_NAME
        )
        print(f"База данных '{DB_NAME}' существует: {bool(db_exists)}")
        
        # Проверяем существование таблиц
        tables = ['role', 'user', 'operation']
        print("\nПроверка таблиц:")
        
        for table in tables:
            try:
                exists = await conn.fetchval(
                    "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = $1)", 
                    table
                )
                if exists:
                    count = await conn.fetchval(f"SELECT COUNT(*) FROM \"{table}\"" if table == 'user' else f"SELECT COUNT(*) FROM {table}")
                    print(f"  ✓ Таблица '{table}' существует ({count} записей)")
                else:
                    print(f"  ✗ Таблица '{table}' не найдена")
            except Exception as e:
                print(f"  ✗ Ошибка проверки таблицы '{table}': {e}")
        
        await conn.close()
        print("\n✓ Тест завершен успешно!")
        return True
        
    except Exception as e:
        print(f"✗ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_database())
    if result:
        print("\nТест пройден!")
        sys.exit(0)
    else:
        print("\nТест не пройден!")
        sys.exit(1)
