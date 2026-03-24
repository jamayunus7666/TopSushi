from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.inline import categories_keyboard, sushi_list_keyboard, count_keyboard
from database import get_sushis_by_category, get_sushi_by_id, add_to_basket
from aiogram.exceptions import TelegramBadRequest
from keyboards.reply import get_text

router = Router(name="menu")

@router.message(F.text.in_(["🍱 Menyu", "🍱 Меню"]))
async def show_menu(message: Message):
    await message.answer(
        get_text('choose_category', message.from_user.id),
        reply_markup=categories_keyboard(message.from_user.id)
    )

@router.callback_query(F.data.startswith("cat_"))
async def show_category_items(callback: CallbackQuery):
    cat = callback.data.split("_", 1)[1]
    items = get_sushis_by_category(cat)
    if not items:
        await callback.message.edit_text(f"{cat} bo'limida mahsulot yo'q.")
        return
    await callback.message.edit_text(
        f"**{cat}** bo'limi:",
        reply_markup=sushi_list_keyboard(items, callback.from_user.id),
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data.startswith("item_"))
async def show_sushi_detail(callback: CallbackQuery):
    s_id = int(callback.data.split("_")[1])
    sushi = get_sushi_by_id(s_id)
    if not sushi:
        await callback.answer("Mahsulot topilmadi", show_alert=True)
        return

    caption = f"🍣 **{sushi[2]}**\n\n📝 {sushi[3]}\n💰 {sushi[4]:,} so'm"
    await callback.message.answer_photo(
        photo=sushi[5],
        caption=caption,
        parse_mode="Markdown",
        reply_markup=count_keyboard(s_id, 1, callback.from_user.id)
    )
    try:
        await callback.message.delete()
    except:
        pass
    await callback.answer()

@router.callback_query(F.data.startswith("cnt_"))
async def update_count(callback: CallbackQuery):
    try:
        _, s_id_str, count_str = callback.data.split("_")
        s_id = int(s_id_str)
        count = max(1, int(count_str))
    except:
        await callback.answer("Xato", show_alert=True)
        return

    await callback.message.edit_reply_markup(
        reply_markup=count_keyboard(s_id, count)
    )
    await callback.answer(f"Miqdor: {count}")


@router.callback_query(F.data.startswith("add_"))
async def handler_add_to_basket(callback: CallbackQuery):
    try:
        _, s_id_str, count_str = callback.data.split("_")
        s_id = int(s_id_str)
        count = int(count_str)
    except:
        await callback.answer("Xato: noto'g'ri ma'lumot", show_alert=True)
        return

    add_to_basket(callback.from_user.id, s_id, count)
    await callback.answer("Savatchaga qo'shildi! ✅", show_alert=True)


@router.callback_query(F.data == "back_cats")
async def back_to_categories(callback: CallbackQuery):
    text = "Kategoriyani tanlang:"
    markup = categories_keyboard(user_id=callback.from_user.id)


    try:
        await callback.message.delete()
    except TelegramBadRequest:
        pass 

    await callback.message.answer(
        text,
        reply_markup=markup
    )

    await callback.answer()