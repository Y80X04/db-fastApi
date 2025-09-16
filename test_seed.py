#!/usr/bin/env python3
"""
Тестовый скрипт для проверки создания начальных данных
"""

import asyncio
import sys
import os

# Добавляем src в путь поиска модулей
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

async def test_seed_data():
    try:
        from src.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS
        import asyncpg
        
        print("Проверка начальных данных...")
        print(f"Подключение к базе данных: {DB_NAME} на {DB_HOST}:{DB_PORT}")
        
        # Подключение к базе данных
        connection_string = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        conn = await asyncpg.connect(connection_string)
        
        # Проверяем роли
        print("\nПроверка ролей:")
        roles = await conn.fetch("SELECT id, name, permissions FROM role ORDER BY id")
        for role in roles:
            print(f"  Роль: {role['name']} (id: {role['id']})")
            print(f"    Права: {role['permissions']}")
        
        # Проверяем пользователей
        print("\nПроверка пользователей:")
        users = await conn.fetch("SELECT id, username, email, role_id, is_active, is_superuser FROM \"user\" ORDER BY id")
        for user in users:
            print(f"  Пользователь: {user['username']} (email: {user['email']})")
            print(f"    id: {user['id']}, role_id: {user['role_id']}")
            print(f"    active: {user['is_active']}, superuser: {user['is_superuser']}")
        
        await conn.close()
        
        print(f"\nНайдено ролей: {len(roles)}")
        print(f"Найдено пользователей: {len(users)}")
        
        if len(roles) >= 2 and len(users) >= 2:
            print("✓ Начальные данные успешно созданы!")
            return True
        else:
            print("⚠ Некоторые начальные данные отсутствуют")
            return False
            
    except Exception as e:
        print(f"Ошибка при проверке начальных данных: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_seed_data())
    if result:
        print("\nТест пройден успешно!")
    else:
        print("\nТест не пройден!")
        sys.exit(1)
