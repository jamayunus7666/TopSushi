from aiogram import Router, F
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.fsm.context import FSMContext
from config import ADMIN_ID
from states import AdminAddProduct
from database import add_sushi
from keyboards.inline import admin_main_keyboard

router = Router(name="admin")

@router.message(F.text == "🛠 Admin panel")
async def admin_panel_open(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Sizda ruxsat yo‘q!")
        return
    
    await message.answer(
        "🛠 <b>Admin panel</b>",
        reply_markup=admin_main_keyboard(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "admin_add_sushi")
async def start_add_sushi(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Ruxsat yo'q!", show_alert=True)
        return
    
    await callback.message.edit_text(
        "1. Kategoriyani kiriting (masalan: Klassik, Issiq rollar, Setlar, Vegetarian...)",
        reply_markup=None
    )
    await state.set_state(AdminAddProduct.waiting_for_category)
    await callback.answer()

@router.message(AdminAddProduct.waiting_for_category)
async def process_category(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
    
    await state.update_data(category=message.text.strip())
    await message.answer("2. Sushi nomini kiriting:")
    await state.set_state(AdminAddProduct.waiting_for_name)

@router.message(AdminAddProduct.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
    
    await state.update_data(name=message.text.strip())
    await message.answer("3. Tavsifini kiriting:")
    await state.set_state(AdminAddProduct.waiting_for_desc)

@router.message(AdminAddProduct.waiting_for_desc)
async def process_desc(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
    
    await state.update_data(desc=message.text.strip())
    await message.answer("4. Narxini kiriting (faqat raqam, masalan: 45000):")
    await state.set_state(AdminAddProduct.waiting_for_price)

@router.message(AdminAddProduct.waiting_for_price)
async def process_price(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        price = int(message.text.strip())
    except ValueError:
        await message.answer("❌ Iltimos, faqat raqam kiriting!")
        return
    
    await state.update_data(price=price)
    await message.answer("5. Rasm yuboring (yoki rasm URL manzilini yozing):")
    await state.set_state(AdminAddProduct.waiting_for_photo)



@router.message(AdminAddProduct.waiting_for_photo, F.photo | F.text)
async def process_photo(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
    
    data = await state.get_data()
    
    if message.photo:
        photo_url = message.photo[-1].file_id
    else:
        photo_url = message.text.strip()
        if not photo_url.startswith("http"):
            await message.answer("URL noto‘g‘ri ko‘rinadi. Rasm yuboring yoki to‘g‘ri URL kiriting.")
            return

    try:
        add_sushi(
            category=data["category"],
            name=data["name"],
            description=data["desc"],
            price=data["price"],
            photo_url=photo_url
        )
        await message.answer(
            f"✅ <b>{data['name']}</b> muvaffaqiyatli qo‘shildi!\n"
            f"Kategoriya: {data['category']}\n"
            f"Narx: {data['price']:,} so‘m",
            parse_mode="HTML",
            reply_markup=admin_main_keyboard()
        )
    except Exception as e:
        await message.answer(f"Xato yuz berdi: {str(e)}")
    
    await state.clear()

@router.callback_query(F.data.startswith("st_"))
async def change_order_status(callback: CallbackQuery):
    parts = callback.data.split("_")
    if len(parts) != 3:
        await callback.answer("Noto'g'ri ma'lumot", show_alert=True)
        return

    status, target_user_id_str = parts[1], parts[2]
    target_user_id = int(target_user_id_str)

    if status == "road":
        text = "🚀 Buyurtmangiz yo'lga chiqdi!"
    elif status == "done":
        text = "✅ Buyurtma yakunlandi! Rahmat!"
    else:
        await callback.answer("Noma'lum status", show_alert=True)
        return

    try:
        await callback.bot.send_message(target_user_id, text)
        await callback.answer("Mijozga xabar yuborildi ✅")
    except Exception as e:
        await callback.answer(f"Xabar yuborishda xato: {str(e)}", show_alert=True)