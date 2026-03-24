from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from database import get_user_lang,get_categories
from keyboards.reply import get_text  
from config import ADMIN_ID 


def categories_keyboard(user_id: int):
    cats = get_categories()
    builder = InlineKeyboardBuilder()
    for cat in cats:
        builder.button(text=cat, callback_data=f"cat_{cat}")
    builder.button(text=get_text('back', user_id), callback_data="back_main")
    builder.adjust(2)
    return builder.as_markup()

def sushi_list_keyboard(sushis: list, user_id: int):
    builder = InlineKeyboardBuilder()
    for sid, name in sushis:
        builder.button(text=name, callback_data=f"item_{sid}")
    builder.adjust(1)
    return builder.as_markup()

def count_keyboard(sushi_id: int, count: int = 1,user_id=None):
    builder = InlineKeyboardBuilder()
    builder.button(text="➖", callback_data=f"cnt_{sushi_id}_{count-1}")
    builder.button(text=str(count), callback_data="ignore")
    builder.button(text="➕", callback_data=f"cnt_{sushi_id}_{count+1}")
    builder.button(text="🛒 Savatga qo'shish", callback_data=f"add_{sushi_id}_{count}")
    builder.button(text="⬅️ Orqaga", callback_data="back_cats")
    builder.adjust(3, 1, 1)
    return builder.as_markup()

def basket_actions_keyboard(user_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text=get_text('pay_cash', user_id), callback_data="checkout")
    builder.button(text=get_text('pay_card', user_id), callback_data="start_pay")
    builder.button(text=get_text('clear', user_id), callback_data="clear_basket")
    builder.adjust(1)
    return builder.as_markup()

 

def admin_order_control(user_id: int, current_admin_id: int):

    builder = InlineKeyboardBuilder()
    

    if current_admin_id == ADMIN_ID:
        builder.button(
            text="🚀 Yo'lga chiqdi",
            callback_data=f"st_road_{user_id}"
        )
        builder.button(
            text="✅ Yakunlandi",
            callback_data=f"st_done_{user_id}"
        )
    
    builder.adjust(1)
    return builder.as_markup()


def admin_main_keyboard():
    b = InlineKeyboardBuilder()
    b.button(text="➕ Yangi sushi qo'shish", callback_data="admin_add_sushi")
    b.adjust(1)
    return b.as_markup()