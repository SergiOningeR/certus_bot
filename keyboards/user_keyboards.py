from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Создать заявку")],
            [KeyboardButton(text="📋 Мои заявки"), KeyboardButton(text="❌ Удалить заявку")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    )

def get_cancel_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🚫 Отменить")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def get_skip_attachment_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📎 Прикрепить файл")],
            [KeyboardButton(text="⏭ Пропустить")]
        ],
        resize_keyboard=True
    )

def get_tickets_list_kb(tickets: list):
    builder = InlineKeyboardBuilder()
    for ticket in tickets:
        builder.button(
            text=f"#{ticket.id} - {ticket.title}",
            callback_data=f"view_ticket_{ticket.id}"
        )
    builder.adjust(1)
    return builder.as_markup()