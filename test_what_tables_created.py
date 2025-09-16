#!/usr/bin/env python3
"""
Тестовый скрипт для проверки, какие таблицы создаются в metadata
"""

import sys
import os

# Добавляем src в путь поиска модулей
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_what_tables_exist():
    print("Проверка существующих таблиц в metadata...")
    print("=" * 40)
    
    try:
        # Импортируем модели, чтобы они были зарегистрированы в Base.metadata
        from src.auth import models as auth_models
        from src.operations import models as operations_models
        from src.database import Base
        
        print("Таблицы, определенные в Base.metadata:")
        if Base.metadata.tables:
            for table_name, table in Base.metadata.tables.items():
                print(f"  - {table_name}")
                # Показываем столбцы
                print(f"    Столбцы:")
                for column in table.columns:
                    nullable = "NULL" if column.nullable else "NOT NULL"
                    print(f"      - {column.name} ({column.type}, {nullable})")
        else:
            print("  Нет таблиц в metadata")
        
        print(f"\nОбщее количество таблиц: {len(Base.metadata.tables)}")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_what_tables_exist()
