#!/usr/bin/env python3
"""
Тест подключения к базе данных
"""

import sys
import os

# Добавляем src в путь поиска модулей
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_connection():
    print("Тест подключения к базе данных...")
    print("=" * 30)
    
    try:
        from sqlalchemy import create_engine
        from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
        
        sync_url = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        print(f"Подключение к: {sync_url}")
        
        engine = create_engine(sync_url)
        print("✅ Engine создан успешно")
        
        # Проверяем подключение
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print(f"✅ Подключение успешно: {result.fetchone()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_connection()
