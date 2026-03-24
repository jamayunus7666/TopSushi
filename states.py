from aiogram.fsm.state import State, StatesGroup

class OrderProcess(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_address = State()

class Language(StatesGroup):
    choosing = State()

class AdminAddProduct(StatesGroup):
    waiting_for_category = State()
    waiting_for_name     = State()
    waiting_for_desc     = State()
    waiting_for_price    = State()
    waiting_for_photo    = State()