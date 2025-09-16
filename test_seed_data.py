#!/usr/bin/env python3
"""
Тестовый скрипт для проверки заполнения начальными данными
"""

import asyncio
import sys
import os

# Добавляем src в путь поиска модулей
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

async def test_seed_data():
    print("Тестирование заполнения начальными данными...")
    print("=" * 50)
    
    try:
        from src.seed_only import seed_database
        
        # Пытаемся заполнить начальными данными
        success = await seed_database()
        
        if success:
            print("✅ Начальные данные успешно добавлены!")
            return True
        else:
            print("❌ Ошибка при добавлении начальных данных")
            return False
            
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_seed_data())
    sys.exit(0 if result else 1)
