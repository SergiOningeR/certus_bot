import asyncio
from aiogram import Bot, Dispatcher
from config.config import dp, bot
from handlers import user_router, admin_router, common_router
from database.crud import init_db

async def main():
    await init_db()
    
    dp.include_router(user_router)
    dp.include_router(admin_router)
    dp.include_router(common_router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())