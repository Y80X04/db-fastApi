#!/usr/bin/env python3
"""
Тестовый скрипт для создания таблиц с начальными данными
"""

import sys
import os

# Добавляем src в путь поиска модулей
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_create_tables_with_data():
    print("Создание таблиц с начальными данными...")
    print("=" * 40)
    
    try:
        from src.auto_create_tables import sync_create_tables_and_seed_data
        
        print("Создание таблиц и заполнение данными...")
        success = sync_create_tables_and_seed_data()
        
        if success:
            print("✅ Таблицы успешно созданы и заполнены данными!")
            return True
        else:
            print("❌ Ошибка при создании таблиц или данных")
            return False
            
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = test_create_tables_with_data()
    sys.exit(0 if result else 1)
