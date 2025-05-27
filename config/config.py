from aiogram import Bot
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

class Settings:
    BOT_TOKEN: str = "TOKEN"
    ADMIN_GROUP_ID: int = -GROUPID
    ADMINS: list[int] = [ADMINID]
    
    class DB:
        DB_NAME: str = "tickets.db"
        SQL_SCRIPTS_DIR: str = "database/sql/"

settings = Settings()

bot = Bot(token=settings.BOT_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(storage=storage)