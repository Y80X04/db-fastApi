#!/usr/bin/env python3
"""
Скрипт для проверки и установки необходимых зависимостей
"""

import subprocess
import sys
import importlib

def check_and_install_package(package_name, import_name=None):
    """Проверяет наличие пакета и устанавливает его при необходимости"""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        print(f"✓ {package_name} уже установлен")
        return True
    except ImportError:
        print(f"✗ {package_name} не установлен, устанавливаем...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"✓ {package_name} успешно установлен")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Ошибка при установке {package_name}: {e}")
            return False

def main():
    print("Проверка и установка зависимостей...")
    print("=" * 50)
    
    packages = [
        ("asyncpg", None),
        ("sqlalchemy", None),
        ("alembic", None),
        ("python-dotenv", "dotenv"),
        ("fastapi", None),
        ("fastapi-users[sqlalchemy]", "fastapi_users"),
        ("uvicorn", None),
    ]
    
    success_count = 0
    total_count = len(packages)
    
    for package_name, import_name in packages:
        if check_and_install_package(package_name, import_name):
            success_count += 1
        print()
    
    print("=" * 50)
    print(f"Установлено пакетов: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("Все зависимости успешно установлены!")
        return 0
    else:
        print("Некоторые зависимости не удалось установить!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
