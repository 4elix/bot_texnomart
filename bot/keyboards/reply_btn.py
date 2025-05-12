from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from db.orm import get_categories, get_products


async def btn_categories_name():
    list_categories = await get_categories()

    btn = [
        [KeyboardButton(text=category.name)] for category in list_categories
    ]
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=btn)
    return markup


async def btn_products_name(category_name):
    list_products = await get_products(category_name)

    btn = [
        [KeyboardButton(text='Назад')]
    ] + [
        [KeyboardButton(text=product.title)] for product in list_products
    ]

    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=btn)
    return markup
