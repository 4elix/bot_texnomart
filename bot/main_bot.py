import os
import asyncio

from dotenv import load_dotenv
from aiogram import Dispatcher, Bot

from handlers_command import cmd_router
from handlers_text import txt_router, setup_categories

# load_dotenv -> функция для нахождения файла .env
load_dotenv()


async def main_bot():
    await setup_categories()

    # os.getenv('TOKEN') -> забираем из файла .env ссылку для базы данных
    token = os.getenv('TOKEN')

    # bot = Bot(token) -> инициализация бота
    bot = Bot(token)

    # dp = Dispatcher() -> диспетчер сообщений
    dp = Dispatcher()

    # dp.include_router(cmd_router)
    dp.include_routers(
        cmd_router,
        txt_router
    )

    # bot.delete_webhook(drop_pending_updates=True) -> при включении бота, он не будет обрабатывать
    # сообщения который были отправлены в момент выключения бота
    await bot.delete_webhook(drop_pending_updates=True)

    # dp.start_polling(bot) -> запуск бота
    await dp.start_polling(bot)


if __name__ == '__main__':
    print('start bot')
    asyncio.run(main_bot())