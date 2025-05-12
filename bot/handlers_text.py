from aiogram import Router
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext

from db.orm import get_categories, get_product_info
from keyboards.reply_btn import btn_products_name, btn_categories_name
from keyboards.inline_btn import btn_back
from handlers_command import react_start
from utils import ShowProductInfo

txt_router = Router()


categories_name = []


async def setup_categories():
    # global categories_names -> делает нашу переменную глобальной, то есть она существует вне функции и внутри функции
    global categories_name

    # получаем из orm категории
    categories = await get_categories()

    # меняем пустой список, на список с категориями
    categories_name = [cat.name for cat in categories]


@txt_router.message(lambda msg: msg.text in categories_name)
async def react_btn_category(message: Message, state: FSMContext):
    category_name = message.text
    await message.answer('Хорошо, ниже есть кнопки с название продукта данной категории',
                         reply_markup=await btn_products_name(category_name))

    await state.set_state(ShowProductInfo.title)


@txt_router.message(ShowProductInfo.title)
async def show_product_info(message: Message, state: FSMContext):
    await state.clear()

    result = message.text

    if result == 'Назад':
        await react_start(message)
    else:
        # ReplyKeyboardRemove() -> класс для скрытия клавиатуры
        await message.answer('Выбранный товар', reply_markup=ReplyKeyboardRemove())
        product = await get_product_info(result)
        info = product.info
        text = f'''
Название: {product.title}

Стоимость: {product.price}

Коротко о товаре: \n{"\n".join(info.split('! '))}
'''
        await message.answer_photo(photo=FSInputFile('../parser/' + product.image_url), caption=text,
                                   reply_markup=btn_back)


@txt_router.callback_query(lambda call: 'back_to_category' in call.data)
async def react_btn_back(callback: CallbackQuery):
    # удаления сообщения
    await callback.message.delete()
    await callback.message.answer('Хорошо, ниже кнопки с категориями', reply_markup=await btn_categories_name())



