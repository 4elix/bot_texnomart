from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from keyboards.reply_btn import btn_categories_name


# cmd_router -> переменная для обработки команд
cmd_router = Router()


@cmd_router.message(Command('start'))
async def react_start(message: Message):
    # .answer('') -> метод для отправки сообщений

    await message.answer('Привет, нажми на кнопку нижу. Это список наших категорий',
                         reply_markup=await btn_categories_name())

