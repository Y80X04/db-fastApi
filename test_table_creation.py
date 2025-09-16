#!/usr/bin/env python3
"""
Тестовый скрипт для проверки создания таблиц
"""

import asyncio
import sys
import os

# Добавляем src в путь поиска модулей
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

async def test_table_creation():
    print("Тестирование создания таблиц...")
    print("=" * 40)
    
    try:
        from src.auto_create_tables import initialize_database_on_startup
        
        # Пытаемся создать таблицы
        success = await initialize_database_on_startup()
        
        if success:
            print("✅ Таблицы успешно созданы!")
            return True
        else:
            print("❌ Ошибка при создании таблиц")
            return False
            
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_table_creation())
    sys.exit(0 if result else 1)
