from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states import OrderProcess
from database import get_basket_items, clear_basket, get_user_lang
from keyboards.reply import contact_keyboard, location_keyboard, main_keyboard, get_text
from keyboards.inline import admin_order_control
from config import ADMIN_ID  

router = Router(name="order")

@router.callback_query(F.data == "checkout")
async def start_naqd_checkout(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    t = lambda k: get_text(k, user_id)
    await callback.message.answer(t('name_prompt') or "Ismingizni kiriting:")
    await state.set_state(OrderProcess.waiting_for_name)
    await callback.answer()

@router.message(OrderProcess.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    user_id = message.from_user.id
    await message.answer(
        get_text('send_phone', user_id),
        reply_markup=contact_keyboard(user_id)
    )
    await state.set_state(OrderProcess.waiting_for_phone)

@router.message(OrderProcess.waiting_for_phone, F.contact | F.text)
async def process_phone(message: Message, state: FSMContext):
    phone = message.contact.phone_number if message.contact else message.text
    await state.update_data(phone=phone)
    user_id = message.from_user.id
    await message.answer(
        get_text('send_location', user_id) or "Lokatsiya yuboring yoki manzil yozing:",
        reply_markup=location_keyboard(user_id)
    )
    await state.set_state(OrderProcess.waiting_for_address)

@router.message(OrderProcess.waiting_for_address, F.location | F.text)
async def process_address(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()

    if message.location:
        lat, lon = message.location.latitude, message.location.longitude
        address = f"https://maps.google.com/?q={lat},{lon}"
    else:
        address = message.text

    items = get_basket_items(user_id)
    order_list = "\n".join([f"- {name} ({qty} dona)" for name, _, qty in items])

    admin_text = (
        f"🔔 **YANGI BUYURTMA!**\n"
        f"👤 Mijoz: {data.get('name')}\n"
        f"📞 Tel: {data.get('phone')}\n"
        f"📍 Manzil: {address}\n"
        f"🍱 Mahsulotlar:\n{order_list}"
    )

    await message.bot.send_message(
        ADMIN_ID,
        admin_text,
        reply_markup=admin_order_control(user_id, ADMIN_ID),
        parse_mode="Markdown"
    )

    await message.answer("Buyurtmangiz qabul qilindi! Tez orada bog'lanamiz 🍣",
                         reply_markup=main_keyboard(user_id))
    
    clear_basket(user_id)
    await state.clear()