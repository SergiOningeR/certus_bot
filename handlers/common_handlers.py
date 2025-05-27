from aiogram import Router
from aiogram.types import Message, ErrorEvent
from aiogram.filters import Command

from utils.logger import logger
from keyboards.user_keyboards import get_main_menu_kb
from config.strings import strings

common_router = Router()

@common_router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Справка по командам:\n/new_ticket - Новая заявка\n/my_tickets - Мои заявки")

@common_router.errors()
async def error_handler(event: ErrorEvent):
    logger.error(f"Error: {event.exception}")
    if event.update.message:
        await event.update.message.answer("⚠️ Произошла ошибка. Попробуйте позже")
    return True