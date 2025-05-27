from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy
import asyncio
import logging

import config
from bot.handlers import user, admin
from bot.database import db_operations

async def main():
    # Включаем логирование
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
    # Инициализируем хранилище FSM
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage, fsm_strategy=FSMStrategy.USER)
    # Регистрируем роутеры (обработчики)
    dp.include_router(user.router)
    dp.include_router(admin.router)
    # Подключаемся к базе данных
    await db_operations.create_pool()
    # Запуск поллинга
    try:
        await dp.start_polling(bot)
    finally:
        # Закрываем соединения
        await bot.session.close()
        await db_operations.close_pool()

if __name__ == "__main__":
    asyncio.run(main())
