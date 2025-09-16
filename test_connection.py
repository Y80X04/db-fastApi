#!/usr/bin/env python3
"""
Простой скрипт для тестирования подключения к базе данных
"""

import asyncio
import asyncpg
import os
import sys

# Добавляем src в путь поиска модулей
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS
    print("✓ Конфигурация загружена успешно")
    print(f"  Хост: {DB_HOST}:{DB_PORT}")
    print(f"  База данных: {DB_NAME}")
    print(f"  Пользователь: {DB_USER}")
except Exception as e:
    print(f"✗ Ошибка загрузки конфигурации: {e}")
    sys.exit(1)

async def test_db_connection():
    """Тестирует подключение к базе данных"""
    try:
        # Подключение к PostgreSQL серверу
        connection_string = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        print(f"\nПопытка подключения к: {connection_string}")
        
        conn = await asyncpg.connect(connection_string)
        print("✓ Успешное подключение к базе данных!")
        
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
        print("\n✓ Тест подключения завершен успешно!")
        return True
        
    except Exception as e:
        print(f"✗ Ошибка подключения к базе данных: {e}")
        return False

if __name__ == "__main__":
    print("Тестирование подключения к базе данных...")
    print("=" * 50)
    
    result = asyncio.run(test_db_connection())
    
    print("=" * 50)
    if result:
        print("Тест пройден успешно!")
        sys.exit(0)
    else:
        print("Тест не пройден!")
        sys.exit(1)
