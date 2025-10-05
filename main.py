
import asyncio
import sys

from aiogram.types import MenuButtonDefault

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import router
import logging
from handlers.callbacks_handler import router as callbacks_router
#FSM - Машина состояний

async def main():
    logging.basicConfig(level=logging.INFO) #Логирование
    bot = Bot(TOKEN)  # Связывались с серверами тг с нашим токеном
    dp = Dispatcher()  # Ловит апдейты
    dp.include_router(router)
    await dp.start_polling(bot)

async def remove_menu_button(bot: Bot):
    await bot.set_chat_menu_button(
    menu_button=MenuButtonDefault()
    )


asyncio.run(main())

