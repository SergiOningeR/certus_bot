from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from pydantic import ValidationError
from datetime import datetime

from states.user_states import TicketCreation, TicketDeletion
from database.models import TicketCreate
from database.crud import create_ticket, get_user_tickets, delete_ticket
from services.notifications import notify_admins
from keyboards.user_keyboards import (
    get_main_menu_kb,
    get_cancel_kb,
    get_skip_attachment_kb,
    get_tickets_list_kb
)
from utils.logger import logger

user_router = Router()

@user_router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Добро пожаловать!", reply_markup=get_main_menu_kb())

@user_router.message(F.text == "🚫 Отменить")
@user_router.message(Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Действие отменено", reply_markup=get_main_menu_kb())

@user_router.message(Command("new_ticket"))
@user_router.message(F.text == "📝 Создать заявку")
async def cmd_new_ticket(message: Message, state: FSMContext):
    await state.set_state(TicketCreation.title)
    await message.answer("📌 Введите название задачи:", reply_markup=get_cancel_kb())

@user_router.message(TicketCreation.title)
async def process_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(TicketCreation.description)
    await message.answer("📝 Опишите задачу подробно:")

@user_router.message(TicketCreation.description)
async def process_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(TicketCreation.priority)
    await message.answer("🔢 Оцените важность (1-5):")

@user_router.message(TicketCreation.priority)
async def process_priority(message: Message, state: FSMContext):
    try:
        priority = int(message.text)
        if 1 <= priority <= 5:
            await state.update_data(priority=priority)
            await state.set_state(TicketCreation.phone)
            await message.answer("📱 Укажите ваш телефон:")
        else:
            await message.answer("❌ Число должно быть от 1 до 5")
    except ValueError:
        await message.answer("❌ Введите число!")

@user_router.message(TicketCreation.phone)
async def process_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(TicketCreation.attachments)
    await message.answer(
        "📎 Прикрепите файлы (фото/документы) или нажмите 'Пропустить':",
        reply_markup=get_skip_attachment_kb()
    )

@user_router.message(TicketCreation.attachments, F.photo | F.document)
async def process_attachment(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id if message.photo else message.document.file_id
    async with state.update_data() as data:
        data.setdefault("attachments", [])
        data["attachments"].append(file_id)
    await message.answer("✅ Файл добавлен! Отправьте еще или нажмите 'Пропустить'.")

@user_router.message(TicketCreation.attachments, F.text == "⏭ Пропустить")
async def skip_attachments(message: Message, state: FSMContext):
    data = await state.get_data()
    data.setdefault("attachments", [])
    await state.set_state(TicketCreation.confirmation)
    await message.answer(
        f"📋 Подтвердите заявку:\n\n"
        f"Название: {data['title']}\n"
        f"Описание: {data['description']}\n"
        f"Важность: {data['priority']}/5\n"
        f"Телефон: {data['phone']}",
        reply_markup=ReplyKeyboardRemove()
    )

@user_router.message(TicketCreation.confirmation)
async def confirm_ticket(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        ticket = TicketCreate(
            user_id=message.from_user.id,
            title=data["title"],
            description=data["description"],
            priority=data["priority"],
            phone=data["phone"],
            attachments=data.get("attachments", [])
        )
        ticket_id = await create_ticket(ticket)
        await notify_admins(ticket_id, ticket)
        await message.answer(f"✅ Заявка #{ticket_id} создана!", reply_markup=get_main_menu_kb())
        await state.clear()
    except ValidationError as e:
        await message.answer(f"❌ Ошибка: {e.errors()[0]['msg']}")
    except Exception as e:
        logger.error(f"Ошибка создания заявки: {str(e)}")
        await message.answer("⚠️ Внутренняя ошибка. Попробуйте позже")

@user_router.message(F.text == "📋 Мои заявки")
@user_router.message(Command("my_tickets"))
async def cmd_my_tickets(message: Message):
    try:
        tickets = await get_user_tickets(message.from_user.id)
        if not tickets:
            return await message.answer("📭 У вас нет заявок", reply_markup=get_main_menu_kb())
        
        response = []
        for ticket in tickets:
            ticket_info = (
                f"🔸 #{ticket.id}\n"
                f"📌 {ticket.title}\n"
                f"📅 {ticket.created_at.strftime('%d.%m.%Y %H:%M')}\n"
                f"🔢 Важность: {ticket.priority}/5\n"
                f"📱 Телефон: {ticket.phone}\n"
                f"📝 Описание: {ticket.description[:50]}...\n"
                f"🔄 Статус: {ticket.status.value}"
            )
            response.append(ticket_info)
        
        await message.answer(
            "📋 Ваши заявки:\n\n" + "\n\n".join(response),
            reply_markup=get_main_menu_kb()
        )
    except Exception as e:
        logger.error(f"Ошибка получения заявок: {str(e)}")
        await message.answer("⚠️ Ошибка загрузки заявок", reply_markup=get_main_menu_kb())

@user_router.message(F.text == "❌ Удалить заявку")
async def delete_ticket_handler(message: Message, state: FSMContext):
    await state.set_state(TicketDeletion.ticket_id)
    await message.answer("🔢 Введите ID заявки для удаления:")

@user_router.message(TicketDeletion.ticket_id)
async def process_ticket_id(message: Message, state: FSMContext):
    try:
        ticket_id = int(message.text)
        await delete_ticket(ticket_id, message.from_user.id)
        await message.answer("✅ Заявка удалена!", reply_markup=get_main_menu_kb())
        await state.clear()
    except ValueError:
        await message.answer("❌ Введите число!")
    except Exception as e:
        logger.error(f"Ошибка удаления: {str(e)}")
        await message.answer("⚠️ Не удалось удалить заявку")