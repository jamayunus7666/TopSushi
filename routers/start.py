from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from database import init_db, get_user_lang
from keyboards.reply import main_keyboard

router = Router(name="start")

@router.message(CommandStart())
async def cmd_start(message: Message):
    init_db()  
    user_id = message.from_user.id
    lang = get_user_lang(user_id)
    await message.answer(
        f"Xush kelibsiz, {message.from_user.full_name}! 🍣",
        reply_markup=main_keyboard(user_id)
    )