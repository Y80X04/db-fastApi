#!/usr/bin/env python3
"""
Тестовый скрипт для проверки подключения к базе данных
"""

import asyncio
import asyncpg
from src.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS

async def test_connection():
    try:
        # Подключение к PostgreSQL серверу
        connection_string = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/postgres"
        print(f"Попытка подключения к: {connection_string}")
        
        conn = await asyncpg.connect(connection_string)
        print("Успешное подключение к PostgreSQL серверу")
        
        # Проверяем существование базы данных
        exists = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1", 
            DB_NAME
        )
        
        if exists:
            print(f"База данных '{DB_NAME}' существует")
        else:
            print(f"База данных '{DB_NAME}' не существует")
            
        await conn.close()
        
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())
