from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# InlineKeyboardMarkup -> класс для настройки inline кнопок
# InlineKeyboardButton -> класс для контента в inline кнопке

btn_back = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Назад', callback_data='back_to_category')
    ]
])
