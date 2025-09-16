#!/usr/bin/env python3
"""
Скрипт для проверки структуры базы данных и существующих таблиц
"""

import asyncio
import asyncpg
import os

# Загружаем конфигурацию из environment variables
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5439")
DB_NAME = os.environ.get("DB_NAME", "postgres")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASS = os.environ.get("DB_PASS", "postgres")

async def check_database_structure():
    print("Проверка структуры базы данных...")
    print("=" * 50)
    
    try:
        connection_string = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        conn = await asyncpg.connect(connection_string)
        print(f"✅ Подключение к базе данных успешно: {DB_HOST}:{DB_PORT}/{DB_NAME}")
        
        # Проверяем список таблиц
        print("\n📋 Список таблиц в базе данных:")
        tables = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        
        if tables:
            for table in tables:
                print(f"  - {table['table_name']}")
        else:
            print("  Нет таблиц в схеме public")
        
        # Проверяем структуру таблицы role, если она существует
        print("\n🔍 Проверка структуры таблицы 'role':")
        try:
            role_columns = await conn.fetch("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'role'
                ORDER BY ordinal_position
            """)
            
            if role_columns:
                print("  Столбцы таблицы 'role':")
                for col in role_columns:
                    nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
                    print(f"    - {col['column_name']} ({col['data_type']}, {nullable})")
            else:
                print("  Таблица 'role' не существует")
        except Exception as e:
            print(f"  Ошибка при проверке таблицы 'role': {e}")
        
        # Проверяем структуру таблицы user, если она существует
        print("\n🔍 Проверка структуры таблицы 'user':")
        try:
            user_columns = await conn.fetch("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'user'
                ORDER BY ordinal_position
            """)
            
            if user_columns:
                print("  Столбцы таблицы 'user':")
                for col in user_columns:
                    nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
                    print(f"    - {col['column_name']} ({col['data_type']}, {nullable})")
            else:
                print("  Таблица 'user' не существует")
        except Exception as e:
            print(f"  Ошибка при проверке таблицы 'user': {e}")
        
        # Проверяем структуру таблицы operation, если она существует
        print("\n🔍 Проверка структуры таблицы 'operation':")
        try:
            operation_columns = await conn.fetch("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = 'operation'
                ORDER BY ordinal_position
            """)
            
            if operation_columns:
                print("  Столбцы таблицы 'operation':")
                for col in operation_columns:
                    nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
                    print(f"    - {col['column_name']} ({col['data_type']}, {nullable})")
            else:
                print("  Таблица 'operation' не существует")
        except Exception as e:
            print(f"  Ошибка при проверке таблицы 'operation': {e}")
        
        await conn.close()
        print("\n✅ Проверка завершена")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка подключения к базе данных: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(check_database_structure())
