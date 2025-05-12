import os
import json
import asyncio
import aiofiles

# postgres+asyncpg://user:password@host/database

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from parser.support import transform_info_in_text
from models import Base, Category, Product

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


async def create_delete_tables():
    # подключения к базе данных, через который потом можно будет выполнять асинхронные операции с базой
    engine = create_async_engine(DATABASE_URL, echo=True)

    # engine.begin() -> создаёт новое подключение к базе данных и начинает транзакцию
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.drop_all)
        await connect.run_sync(Base.metadata.create_all)

    # engine.dispose() -> полностью закрыть все соединения с базой данных и выключить движок
    await engine.dispose()


async def insert_category():
    engine = create_async_engine(DATABASE_URL, echo=True)
    # sessionmaker -> это фабрика сессий, она создаёт готовые сессии для работы с базой данных.
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    # expire_on_commit=False -> Это удобно, чтобы после сохранения сразу продолжать работать с
    # данными без повторной загрузки из базы.

    async with async_session() as session:

        async with aiofiles.open('../parser/categories.json', mode='r', encoding='UTF-8') as file:
            content = await file.read()
            json_categories = json.loads(content)

        categories_data = []
        for name in json_categories.keys():
            # сохраняем категорию в базу
            category = Category(name=name)
            session.add(category)

        await session.commit()

    await engine.dispose()


async def insert_products():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        async with aiofiles.open('../parser/products.json', mode='r', encoding='UTF-8') as file:
            content = await file.read()
            products_data = json.loads(content)
            category_id = 1
            for items in products_data.values():
                # await session.get(Category, category_id) -> получаем категорию по её ID
                category = await session.get(Category, category_id)
                category_id += 1

                try:
                    for item in items:
                        product = Product(
                            title=str(item['title']),
                            price=item['current_price'],
                            image_url=item['path_image'],
                            info=await transform_info_in_text(item['info']),
                            category=category
                        )
                        session.add(product)

                    await session.commit()
                except Exception as error:
                    print(error)

    await engine.dispose()


async def main_db():
    await create_delete_tables()
    await insert_category()
    await insert_products()


if __name__ == '__main__':
    asyncio.run(main_db())
