from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from database import get_basket_items, clear_basket, get_basket_total
from keyboards.inline import basket_actions_keyboard

router = Router(name="basket")

@router.message(F.text.in_(["🛍 Mening buyurtmalarim", "🛍 Мои заказы"]))
async def show_basket(message: Message):
    items = get_basket_items(message.from_user.id)
    if not items:
        await message.answer("Savatchangiz bo'sh 🛒")
        return

    text = "🛒 **Savatchangiz:**\n\n"
    total = 0
    for name, price, qty in items:
        subtotal = price * qty
        total += subtotal
        text += f"🔸 {name} × {qty} = {subtotal:,} so'm\n"
    text += f"\n💰 **Jami: {total:,} so'm**"

    await message.answer(text, reply_markup=basket_actions_keyboard(message.from_user.id), parse_mode="Markdown")

@router.callback_query(F.data == "clear_basket")
async def clear_basket_handler(callback: CallbackQuery):
    clear_basket(callback.from_user.id)
    await callback.message.edit_text("Savatcha tozalandi ✅")
    await callback.answer()