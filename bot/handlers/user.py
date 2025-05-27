from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ContentType, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext

from bot.utils import messaging, validators
from bot.database import db_operations
import config
import json

router = Router()

# FSM States
from aiogram.fsm.state import StatesGroup, State

class TicketStates(StatesGroup):
    description = State()
    attachments = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет! Я бот для создания заявок. Чтобы создать новую заявку, отправьте команду /new.")

@router.message(Command("new"))
async def cmd_new(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(TicketStates.description)
    await message.answer(messaging.ASK_DESCRIPTION)

@router.message(TicketStates.description)
async def process_description(message: Message, state: FSMContext):
    text = message.text
    if not text or not validators.is_text_non_empty(text):
        await message.answer("Описание не может быть пустым. Пожалуйста, опишите проблему.")
        return
    await state.update_data(description=text)
    await state.set_state(TicketStates.attachments)
    await message.answer(messaging.ASK_ATTACHMENTS)

@router.message(TicketStates.attachments, content_types=[ContentType.PHOTO, ContentType.DOCUMENT])
async def process_attachments(message: Message, state: FSMContext):
    data = await state.get_data()
    attachments = data.get("attachments", [])
    # Сохраняем информацию о прикреплённых файлах
    if message.photo:
        file_id = message.photo[-1].file_id
        attachments.append({"file_id": file_id, "type": "photo"})
    elif message.document:
        file_id = message.document.file_id
        attachments.append({"file_id": file_id, "type": "document"})
    await state.update_data(attachments=attachments)
    await message.answer("Файл добавлен. Если у вас есть ещё файлы, прикрепите их. Когда закончите, нажмите /done.")

@router.message(TicketStates.attachments)
async def attachments_fallback(message: Message, state: FSMContext):
    await message.answer("Нажмите /done для завершения создания заявки или прикрепите файл.")

@router.message(TicketStates.attachments, Command("done"))
async def done_attachments(message: Message, state: FSMContext):
    data = await state.get_data()
    description = data.get("description")
    attachments = data.get("attachments", [])
    # Сохраняем заявку в БД
    attachments_json = json.dumps(attachments)
    ticket_id = await db_operations.create_ticket(
        user_id=message.from_user.id,
        user_username=message.from_user.username,
        user_first_name=message.from_user.first_name,
        user_last_name=message.from_user.last_name,
        description=description,
        attachments=attachments_json
    )
    # Отправляем заявку в группу
    user_name = message.from_user.username or f"{message.from_user.first_name or ''}"
    text = f"📥 <b>Новая заявка #{ticket_id}</b>\n" \
           f"От: {user_name}\n" \
           f"<b>Описание:</b> {description}"
    # Inline-кнопки для администраторов
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("Взять в работу", callback_data=f"ticket:{ticket_id}:work"),
        InlineKeyboardButton("Отменить", callback_data=f"ticket:{ticket_id}:cancel"),
        InlineKeyboardButton("Завершить", callback_data=f"ticket:{ticket_id}:complete")
    )
    # Отправляем сообщение с кнопками
    await message.bot.send_message(config.GROUP_ID, text, reply_markup=keyboard)
    # Отправляем вложения
    for att in attachments:
        if att["type"] == "photo":
            await message.bot.send_photo(config.GROUP_ID, att["file_id"])
        elif att["type"] == "document":
            await message.bot.send_document(config.GROUP_ID, att["file_id"])
    # Подтверждаем пользователю
    await message.answer(messaging.CREATE_SUCCESS.format(ticket_id=ticket_id))
    await state.clear()