#!/usr/bin/env python3
"""
Скрипт для инициализации базы данных
Запуск: python init_db.py
"""

import asyncio
import sys
import os

# Добавляем src в путь поиска модулей
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def main():
    try:
        from src.init_db import init_database
        print("Запуск инициализации базы данных...")
        print("=====================================")
        
        result = asyncio.run(init_database())
        
        if result:
            print("=====================================")
            print("Инициализация базы данных завершена успешно!")
            return 0
        else:
            print("=====================================")
            print("Ошибка при инициализации базы данных!")
            return 1
            
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
