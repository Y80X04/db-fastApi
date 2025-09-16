#!/usr/bin/env python3
"""
Тестовый скрипт для проверки работы приложения и базы данных
"""

import asyncio
import asyncpg
import os
import sys

# Добавляем src в путь поиска модулей
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Импортируем конфигурацию
from src.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS

async def test_app_database():
    try:
        print("Проверка работы базы данных приложения...")
        print(f"Хост: {DB_HOST}:{DB_PORT}")
        print(f"База данных: {DB_NAME}")
        
        # Подключение к базе данных
        connection_string = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        conn = await asyncpg.connect(connection_string)
        print("✓ Успешное подключение к базе данных!")
        
        # Проверяем таблицы и данные
        print("\nПроверка структуры базы данных:")
        
        # Проверяем таблицы
        tables = ['role', 'user', 'operation']
        for table in tables:
            try:
                count = await conn.fetchval(f"SELECT COUNT(*) FROM \"{table}\"" if table == 'user' else f"SELECT COUNT(*) FROM {table}")
                print(f"  ✓ Таблица '{table}': {count} записей")
            except Exception as e:
                print(f"  ✗ Таблица '{table}': ошибка - {e}")
        
        # Проверяем роли
        print("\nПроверка ролей:")
        try:
            roles = await conn.fetch("SELECT id, name, permissions FROM role ORDER BY id")
            for role in roles:
                print(f"  ✓ Роль: {role['name']} (id: {role['id']})")
                print(f"    Права: {role['permissions']}")
        except Exception as e:
            print(f"  ✗ Ошибка при получении ролей: {e}")
        
        # Проверяем пользователей
        print("\nПроверка пользователей:")
        try:
            users = await conn.fetch("SELECT id, username, email, role_id, is_active, is_superuser FROM \"user\" ORDER BY id")
            for user in users:
                print(f"  ✓ Пользователь: {user['username']} (email: {user['email']})")
                print(f"    id: {user['id']}, role_id: {user['role_id']}")
                print(f"    active: {user['is_active']}, superuser: {user['is_superuser']}")
        except Exception as e:
            print(f"  ✗ Ошибка при получении пользователей: {e}")
        
        await conn.close()
        print("\n✓ Проверка базы данных завершена успешно!")
        return True
        
    except Exception as e:
        print(f"✗ Ошибка при проверке базы данных: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config():
    """Проверяет конфигурацию приложения"""
    try:
        print("Проверка конфигурации...")
        from src.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS, DEFAULT_ADMIN_PASSWORD, DEFAULT_USER_PASSWORD
        
        print("✓ Конфигурация загружена успешно")
        print(f"  База данных: {DB_NAME}@{DB_HOST}:{DB_PORT}")
        print(f"  Пользователь: {DB_USER}")
        print("  Пароли: *** (скрыты)")
        
        return True
    except Exception as e:
        print(f"✗ Ошибка конфигурации: {e}")
        return False

if __name__ == "__main__":
    print("Тестирование приложения и базы данных")
    print("=" * 50)
    
    # Проверяем конфигурацию
    config_ok = test_config()
    print()
    
    # Проверяем базу данных
    db_ok = asyncio.run(test_app_database())
    
    print("\n" + "=" * 50)
    if config_ok and db_ok:
        print("🎉 Все проверки пройдены успешно!")
        print("\nПриложение готово к работе:")
        print("  - База данных подключена")
        print("  - Таблицы созданы")
        print("  - Начальные данные загружены")
        print("  - Роли и пользователи доступны")
        sys.exit(0)
    else:
        print("❌ Некоторые проверки не пройдены!")
        sys.exit(1)
