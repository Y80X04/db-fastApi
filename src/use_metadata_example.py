"""
Пример использования подхода с метаданными
Этот файл демонстрирует, как можно использовать таблицы, определенные через MetaData
"""

from src.metadata_example import create_tables, drop_tables, role_table, user_table, operation_table
from src.database import engine
import asyncio

async def main():
    print("Демонстрация работы с метаданными")
    
    # Создаем таблицы через метаданные
    print("Создание таблиц через метаданные...")
    create_tables(engine)
    
    # Пример работы с таблицами через SQLAlchemy Core
    from sqlalchemy import select, insert
    
    # Добавляем тестовые данные
    async with engine.connect() as conn:
        # Добавляем роль
        await conn.execute(
            role_table.insert().values(
                name="test_role",
                permissions={"read": True, "write": True}
            )
        )
        
        # Получаем добавленную роль
        result = await conn.execute(
            select(role_table.c.id, role_table.c.name).where(role_table.c.name == "test_role")
        )
        role = result.fetchone()
        print(f"Добавлена роль: {role}")
        
        await conn.commit()
    
    print("Работа с метаданными завершена успешно")

if __name__ == "__main__":
    asyncio.run(main())
