#!/usr/bin/env python3
"""
Скрипт для запуска FastAPI приложения
"""

import uvicorn
import sys
import os

def main():
    try:
        print("Запуск FastAPI приложения Trading App...")
        print("=====================================")
        
        # Добавляем текущую директорию в путь поиска модулей
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        # Запуск приложения с правильными параметрами
        uvicorn.run(
            "src.main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
        )
        
    except Exception as e:
        print(f"Ошибка при запуске приложения: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
