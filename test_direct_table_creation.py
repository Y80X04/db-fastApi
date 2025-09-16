#!/usr/bin/env python3
"""
Тестовый скрипт для прямого создания таблиц
"""

import asyncio
import sys
import os

# Добавляем src в путь поиска модулей
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_direct_creation():
    print("Прямое создание таблиц...")
    print("=" * 30)
    
    try:
        from src.database import Base, engine
        
        # Создаем таблицы синхронно
        print("Создание таблиц через Base.metadata.create_all...")
        Base.metadata.create_all(bind=engine)
        print("✅ Таблицы успешно созданы!")
        
        # Проверяем, какие таблицы созданы
        print("\nПроверка созданных таблиц:")
        for table_name, table in Base.metadata.tables.items():
            print(f"  - {table_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при создании таблиц: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = test_direct_creation()
    sys.exit(0 if result else 1)
