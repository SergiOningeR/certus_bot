import os
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

from config import BOT_TOKEN
from bot.handlers.user import register_user_handlers
from bot.handlers.admin import register_admin_handlers
from bot.database.db_operations import init_db

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

async def on_startup(dispatcher):
    os.makedirs("media", exist_ok=True)
    await init_db()
    print("✅ Бот запущен и подключен к базе данных.")

if __name__ == "__main__":
    register_user_handlers(dp)
    register_admin_handlers(dp)
    executor.start_polling(dp, on_startup=on_startup)
