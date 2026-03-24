from aiogram import Router, F,types
from aiogram.types import PreCheckoutQuery, Message,CallbackQuery
from aiogram.fsm.context import FSMContext
from config import PAYMENT_TOKEN
from database import get_basket_total
from states import OrderProcess

router = Router(name="payment")

@router.callback_query(F.data == "start_pay")
async def start_card_payment(callback: CallbackQuery):
    user_id = callback.from_user.id
    total = get_basket_total(user_id)
    
    if total <= 0:
        await callback.answer("Savatcha bo'sh!", show_alert=True)
        return

    prices = [types.LabeledPrice(label="Sushi buyurtmasi", amount=total * 100)]  # tiyinlarda

    await callback.bot.send_invoice(
        chat_id=user_id,
        title="Sushi To'lovi",
        description="Buyurtma uchun to'lov",
        provider_token=PAYMENT_TOKEN,
        currency="UZS",
        prices=prices,
        payload="sushi_order_payment"
    )
    await callback.answer()

@router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout: PreCheckoutQuery):
    await pre_checkout.bot.answer_pre_checkout_query(pre_checkout.id, ok=True)

@router.message(F.successful_payment)
async def successful_payment(message: Message, state: FSMContext):
    await message.answer("To'lov muvaffaqiyatli amalga oshirildi! ✅\nEndi ismingizni kiriting:")
    await state.set_state(OrderProcess.waiting_for_name)