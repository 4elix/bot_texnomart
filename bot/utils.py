# utils
from aiogram.fsm.state import StatesGroup, State


class ShowProductInfo(StatesGroup):
    title = State()
