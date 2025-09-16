#!/usr/bin/env python3
"""
Скрипт для проверки работы с базой данных
"""

import sys
import os

# Добавляем src в путь поиска модулей
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def check_db_config():
    try:
        from src.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS
        print("Конфигурация базы данных:")
        print(f"  Хост: {DB_HOST}")
        print(f"  Порт: {DB_PORT}")
        print(f"  Имя БД: {DB_NAME}")
        print(f"  Пользователь: {DB_USER}")
        print("  Пароль: ***")
        return True
    except Exception as e:
        print(f"Ошибка при загрузке конфигурации: {e}")
        return False

def check_dependencies():
    try:
        import asyncpg
        print("✓ asyncpg установлен")
    except ImportError:
        print("✗ asyncpg не установлен")
        return False
        
    try:
        import sqlalchemy
        print("✓ sqlalchemy установлен")
    except ImportError:
        print("✗ sqlalchemy не установлен")
        return False
        
    try:
        import alembic
        print("✓ alembic установлен")
    except ImportError:
        print("✗ alembic не установлен")
        return False
        
    return True

if __name__ == "__main__":
    print("Проверка конфигурации и зависимостей...")
    print()
    
    if check_db_config() and check_dependencies():
        print()
        print("Все зависимости установлены и конфигурация загружена успешно!")
        print("Можно запускать инициализацию базы данных.")
    else:
        print()
        print("Требуется установка недостающих зависимостей.")
