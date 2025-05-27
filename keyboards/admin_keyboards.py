from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_admin_main_kb():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats"),
        InlineKeyboardButton(text="📋 Заявки", callback_data="admin_tickets")
    )
    builder.row(
        InlineKeyboardButton(text="🔍 Поиск", callback_data="admin_search"),
        InlineKeyboardButton(text="⚙ Настройки", callback_data="admin_settings")
    )
    return builder.as_markup()

def get_ticket_actions_kb(ticket_id: int):
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="🔄 В работу",
            callback_data=f"status_progress_{ticket_id}"
        ),
        InlineKeyboardButton(
            text="✅ Завершить",
            callback_data=f"status_completed_{ticket_id}"
        )
    )
    return builder.as_markup()