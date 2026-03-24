from aiogram.utils.keyboard import ReplyKeyboardBuilder
from database import get_user_lang

TEXTS = {
    'uz': {
            'welcome': "Xush kelibsiz! 🍣\nBot avtomatik ravishda o‘zbek tilida ishlaydi.",
            'welcome_change': "✅ Til o'zbek tiliga o'zgartirildi!",
            'lang_prompt': "Tilni tanlang:",
            'menu': "🍱 Menyu",
            'choose_category': "📋Kategoriyani tanlang:",
            'my_orders': "🛍 Mening buyurtmalarim",
            'change_lang': "🌐 Tilni o'zgartirish",
            'chat': "💬 Chat",
            'name_prompt': "🧖‍♂️Ismingizni kiriting:",
            'send_phone': "📞 Telefon yuborish",
            'send_location': "📍 Lokatsiya yuboring yoki manzilni yozing:",
            'back': "⬅️ Orqaga",
            'add_to_cart': "🛒 Savatga qo'shish",
            'pay_card': "💳 Karta orqali",
            'pay_cash': "💵 Naqd pul",
            'clear': "❌ Tozalash",
            'on_way': "🚀 Yo'lga chiqdi",
            'completed': "✅ Yakunlandi",
    },
    'ru': {
            'welcome': "Добро пожаловать! 🍣\nБот автоматически работает на русском.",
            'welcome_change': "✅ Язык изменён на русский!",
            'lang_prompt': "Выберите язык:",
            'menu': "🍱 Меню",
            'choose_category': "📋Выберите категорию:",
            'my_orders': "🛍 Мои заказы",
            'change_lang': "🌐 Сменить язык",
            'chat': "💬 Чат",
            'name_prompt': "🧖‍♂️Введите ваше имя:",
            'send_phone': "📞 Отправить номер",
            'send_location': "📍 Отправьте локацию или напишите адрес:",
            'back': "⬅️ Назад",
            'add_to_cart': "🛒 Добавить в корзину",
            'pay_card': "💳 Картой",
            'pay_cash': "💵 Наличными",
            'clear': "❌ Очистить",
            'on_way': "🚀 В пути",
            'completed': "✅ Завершено",
    }
}

def get_text(key: str, user_id: int) -> str:
    lang = get_user_lang(user_id)
    return TEXTS.get(lang, TEXTS['uz']).get(key, key)

def main_keyboard(user_id: int):
    t = lambda k: get_text(k, user_id)
    b = ReplyKeyboardBuilder()
    
    b.button(text=t('menu'))
    b.button(text=t('my_orders'))
    
    from config import ADMIN_ID
    if user_id == ADMIN_ID:
        b.button(text="🛠 Admin panel")
    
    b.button(text=t('change_lang'))
    b.button(text=t('chat'))
    
    b.adjust(2)
    return b.as_markup(resize_keyboard=True)

def contact_keyboard(user_id: int):
    t = lambda k: get_text(k, user_id)
    b = ReplyKeyboardBuilder()
    b.button(text=t('send_phone'), request_contact=True)
    return b.as_markup(resize_keyboard=True)

def location_keyboard(user_id: int):
    t = lambda k: get_text(k, user_id)
    b = ReplyKeyboardBuilder()
    b.button(text=t('send_location'), request_location=True)
    b.button(text=t('write_address'))
    b.adjust(1)
    return b.as_markup(resize_keyboard=True)