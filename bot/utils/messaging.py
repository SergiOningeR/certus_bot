import os
from aiogram import types
from aiogram.dispatcher import Dispatcher
from config import ADMIN_GROUP_ID, ADMIN_THREAD_ID

async def notify_user(user_id: int, message: str):
    from main import bot  # импорт из main для доступа к экземпляру бота
    await bot.send_message(user_id, message)

async def forward_to_admins(ticket_id: int, data: dict, image_path: str = None):
    from main import bot
    text = (
        f"📥 Новая заявка №{ticket_id}\n"
        f"Название: {data['title']}\n"
        f"Описание: {data['description']}\n"
        f"Телефон: {data['phone']}\n"
        f"Важность: {data['priority']}\n"
        f"Компания: {data['company']}\n"
        f"Пользователь: @{data['user_username'] or 'N/A'}\n"
        f"ID: {data['user_telegram_id']}"
    )

    buttons = types.InlineKeyboardMarkup(row_width=3)
    buttons.add(
        types.InlineKeyboardButton("✅ Принять", callback_data=f"accept_{ticket_id}"),
        types.InlineKeyboardButton("❌ Отменить", callback_data=f"cancel_{ticket_id}"),
        types.InlineKeyboardButton("🏁 Завершить", callback_data=f"complete_{ticket_id}")
    )

    if image_path and os.path.exists(image_path):
        with open(image_path, 'rb') as img:
            await bot.send_photo(ADMIN_GROUP_ID, img, caption=text, reply_markup=buttons, message_thread_id=ADMIN_THREAD_ID)
    else:
        await bot.send_message(ADMIN_GROUP_ID, text, reply_markup=buttons, message_thread_id=ADMIN_THREAD_ID)

async def save_user_image(message: types.Message, file_id: str, path: str):
    from main import bot
    file = await bot.get_file(file_id)
    await bot.download_file(file.file_path, destination=path)

async def save_admin_image(message: types.Message, file_id: str, path: str):
    from main import bot
    file = await bot.get_file(file_id)
    await bot.download_file(file.file_path, destination=path)
