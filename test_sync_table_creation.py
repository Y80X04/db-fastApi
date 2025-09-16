#!/usr/bin/env python3
"""
Синхронный тестовый скрипт для создания таблиц
"""

import sys
import os

# Добавляем src в путь поиска модулей
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_sync_table_creation():
    print("Синхронное создание таблиц...")
    print("=" * 30)
    
    try:
        # Импортируем функцию создания таблиц
        from src.auto_create_tables import sync_create_tables_if_not_exist
        
        # Создаем таблицы синхронно
        print("Создание таблиц...")
        success = sync_create_tables_if_not_exist()
        
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
    result = test_sync_table_creation()
    sys.exit(0 if result else 1)
