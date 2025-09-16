#!/usr/bin/env python3
"""
Скрипт для заполнения базы данных начальными данными
"""

import asyncio
import asyncpg
import hashlib
import json
import os
import sys
from datetime import datetime

# Добавляем src в путь поиска модулей
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Импортируем конфигурацию
from src.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS, DEFAULT_ADMIN_PASSWORD, DEFAULT_USER_PASSWORD

async def seed_database():
    try:
        print("Заполнение базы данных начальными данными...")
        
        # Подключение к базе данных
        connection_string = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        conn = await asyncpg.connect(connection_string)
        print("✓ Успешное подключение к базе данных")
        
        # Создаем роли
        print("\nСоздание базовых ролей...")
        
        # Проверяем существование роли admin
        admin_role_exists = await conn.fetchval(
            "SELECT EXISTS (SELECT 1 FROM role WHERE name = $1)", 
            "admin"
        )
        
        if not admin_role_exists:
            admin_role_id = await conn.fetchval(
                "INSERT INTO role (name, permissions) VALUES ($1, $2) RETURNING id",
                "admin", 
                json.dumps({"admin": True, "read": True, "write": True, "delete": True})
            )
            print(f"✓ Создана роль admin с id={admin_role_id}")
        else:
            admin_role_id = await conn.fetchval("SELECT id FROM role WHERE name = $1", "admin")
            print(f"ℹ Роль admin уже существует с id={admin_role_id}")
        
        # Проверяем существование роли user
        user_role_exists = await conn.fetchval(
            "SELECT EXISTS (SELECT 1 FROM role WHERE name = $1)", 
            "user"
        )
        
        if not user_role_exists:
            user_role_id = await conn.fetchval(
                "INSERT INTO role (name, permissions) VALUES ($1, $2) RETURNING id",
                "user",
                json.dumps({"read": True, "write": True, "delete": False})
            )
            print(f"✓ Создана роль user с id={user_role_id}")
        else:
            user_role_id = await conn.fetchval("SELECT id FROM role WHERE name = $1", "user")
            print(f"ℹ Роль user уже существует с id={user_role_id}")
        
        # Хэшируем пароли
        def hash_password(password):
            return hashlib.sha256(password.encode()).hexdigest()
        
        # Создаем пользователей
        print("\nСоздание базовых пользователей...")
        
        # Пользователь admin
        admin_exists = await conn.fetchval(
            "SELECT EXISTS (SELECT 1 FROM \"user\" WHERE username = $1)", 
            "admin"
        )
        
        if not admin_exists:
            await conn.execute(
                """INSERT INTO "user" (email, username, role_id, hashed_password, is_active, is_superuser, is_verified, registered_at) 
                   VALUES ($1, $2, $3, $4, $5, $6, $7, $8)""",
                "admin@example.com",
                "admin",
                admin_role_id,
                hash_password(DEFAULT_ADMIN_PASSWORD),
                True,  # is_active
                True,  # is_superuser
                True,  # is_verified
                datetime.utcnow()
            )
            print("✓ Создан пользователь admin")
        else:
            print("ℹ Пользователь admin уже существует")
        
        # Пользователь user
        user_exists = await conn.fetchval(
            "SELECT EXISTS (SELECT 1 FROM \"user\" WHERE username = $1)", 
            "user"
        )
        
        if not user_exists:
            await conn.execute(
                """INSERT INTO "user" (email, username, role_id, hashed_password, is_active, is_superuser, is_verified, registered_at) 
                   VALUES ($1, $2, $3, $4, $5, $6, $7, $8)""",
                "user@example.com",
                "user",
                user_role_id,
                hash_password(DEFAULT_USER_PASSWORD),
                True,  # is_active
                False, # is_superuser
                True,  # is_verified
                datetime.utcnow()
            )
            print("✓ Создан пользователь user")
        else:
            print("ℹ Пользователь user уже существует")
        
        # Проверяем результаты
        print("\nПроверка результатов:")
        role_count = await conn.fetchval("SELECT COUNT(*) FROM role")
        user_count = await conn.fetchval("SELECT COUNT(*) FROM \"user\"")
        print(f"Всего ролей: {role_count}")
        print(f"Всего пользователей: {user_count}")
        
        await conn.close()
        print("\n✓ Заполнение начальными данными завершено успешно!")
        return True
        
    except Exception as e:
        print(f"✗ Ошибка при заполнении начальными данными: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Запуск заполнения базы данных начальными данными...")
    print("=" * 50)
    
    result = asyncio.run(seed_database())
    
    print("=" * 50)
    if result:
        print("Заполнение завершено успешно!")
        sys.exit(0)
    else:
        print("Заполнение не завершено!")
        sys.exit(1)
