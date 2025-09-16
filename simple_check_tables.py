#!/usr/bin/env python3
"""
Простой скрипт для проверки создания таблиц
"""

import sys
import os

# Добавляем src в путь поиска модулей
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def main():
    print("Проверка создания таблиц...")
    print("=" * 30)
    
    try:
        # Импортируем модели
        print("Импорт моделей...")
        from src.auth import models as auth_models
        from src.operations import models as operations_models
        from src.database import Base
        
        print(f"Найдено таблиц в metadata: {len(Base.metadata.tables)}")
        for table_name in Base.metadata.tables:
            print(f"  - {table_name}")
        
        # Создаем таблицы
        print("\nСоздание таблиц...")
        from sqlalchemy import create_engine
        from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
        
        sync_url = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        print(f"Подключение к: {sync_url}")
        
        engine = create_engine(sync_url)
        Base.metadata.create_all(bind=engine)
        print("✅ Таблицы созданы успешно!")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()
