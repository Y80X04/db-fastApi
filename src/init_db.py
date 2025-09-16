#!/usr/bin/env python3
"""
Основной скрипт инициализации базы данных
"""

import asyncio
import sys
import os

# Добавляем текущую директорию в путь поиска модулей
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    try:
        # Импортируем асинхронную функцию инициализации
        from database_init import init_database
        
        print("Запуск инициализации базы данных...")
        print("=" * 50)
        
        # Запускаем асинхронную инициализацию
        result = asyncio.run(init_database())
        
        print("=" * 50)
        if result:
            print("Инициализация базы данных завершена успешно!")
            return 0
        else:
            print("Ошибка при инициализации базы данных!")
            return 1
            
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
