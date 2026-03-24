import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import TOKEN
from database import init_db
from routers.start import router as start_router
from routers.language import router as lang_router
from routers.menu import router as menu_router
from routers.basket import router as basket_router
from routers.order import router as order_router
from routers.payment import router as payment_router
from routers.admin import router as admin_router

async def main():
    init_db()
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(lang_router)
    dp.include_router(menu_router)
    dp.include_router(basket_router)
    dp.include_router(order_router)
    dp.include_router(payment_router)
    dp.include_router(admin_router)

    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main()) 