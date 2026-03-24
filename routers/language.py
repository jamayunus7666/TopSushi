from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import Language
from database import set_user_lang, get_user_lang
from keyboards.reply import main_keyboard, get_text
from aiogram.utils.keyboard import ReplyKeyboardBuilder

router = Router(name="language")

@router.message(F.text.in_(["🌐 Tilni o'zgartirish", "🌐 Сменить язык"]))
async def change_language_start(message: Message, state: FSMContext):
    await message.answer(
        "Tilni tanlang:\nВыберите язык:",
        reply_markup=ReplyKeyboardBuilder()
            .button(text="🇺🇿 O'zbekcha")
            .button(text="🇷🇺 Русский")
            .adjust(2)
            .as_markup(resize_keyboard=True)
    )
    await state.set_state(Language.choosing)

@router.message(Language.choosing)
async def process_language(message: Message, state: FSMContext):
    text = message.text.lower()
    user_id = message.from_user.id
    lang = 'uz'

    if "o'zbek" in text or "uzbek" in text or "🇺🇿" in text:
        lang = 'uz'
    elif "рус" in text or "russ" in text or "🇷🇺" in text:
        lang = 'ru'

    set_user_lang(user_id, lang)
    await message.answer(
        "✅ Til o'zgartirildi!" if lang == 'uz' else "✅ Язык изменён!",
        reply_markup=main_keyboard(user_id)
    )
    await state.clear()