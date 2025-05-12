import os

from sqlalchemy import select
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from .models import Base, Category, Product

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


async def get_categories():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        obj_category = await session.execute(select(Category))
        categories = obj_category.scalars().all()  # получаем список объектов Category

    await engine.dispose()
    return categories


async def get_products(category_name):
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        obj_category = await session.execute(
            select(Category).where(Category.name == category_name)
        )
        category_id = obj_category.scalars().one_or_none().id

        category = await session.get(Category, category_id)

        # чтобы подгрузить связанные продукты
        await session.refresh(category)

    await engine.dispose()
    return category.products


async def get_product_info(product_name):
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        obj_product = await session.execute(
            select(Product).where(Product.title == product_name)
        )
        product_info = obj_product.scalars().all()[0]

    await engine.dispose()
    return product_info
