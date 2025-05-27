from aiogram import Router
from aiogram.types import CallbackQuery, Message, ContentType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.database import db_operations
import config
import json

router = Router()

# FSM States for admin report
from aiogram.fsm.state import StatesGroup, State
class AdminStates(StatesGroup):
    wait_report = State()

@router.callback_query(lambda c: c.data and c.data.startswith("ticket:"))
async def process_ticket_action(query: CallbackQuery, state: FSMContext):
    data = query.data.split(":")
    if len(data) != 3:
        await query.answer("Некорректные данные.")
        return
    _, ticket_id_str, action = data
    ticket_id = int(ticket_id_str)
    user = query.from_user
    # Проверка прав администратора
    if user.id not in config.ADMINS:
        await query.answer("У вас нет прав для выполнения этого действия.", show_alert=True)
        return

    if action == "work":
        # Изменяем статус на "в работе"
        await db_operations.update_ticket_status(ticket_id, "в работе", user.id)
        await query.answer("Заявка помечена как 'в работе'.")
        # Уведомляем пользователя
        ticket = await db_operations.get_ticket(ticket_id)
        if ticket:
            await query.bot.send_message(ticket["user_id"], f"Ваша заявка #{ticket_id} принята в работу.")
        # Обновляем текст сообщения с заявкой
        text = query.message.text or ""
        await query.message.edit_text(text + "\n\n🔧 Статус: в работе")
    elif action == "cancel":
        # Изменяем статус на "отменена"
        await db_operations.update_ticket_status(ticket_id, "отменена", user.id)
        await query.answer("Заявка помечена как 'отменена'.")
        # Уведомляем пользователя
        ticket = await db_operations.get_ticket(ticket_id)
        if ticket:
            await query.bot.send_message(ticket["user_id"], f"Ваша заявка #{ticket_id} отменена.")
        # Обновляем текст сообщения
        text = query.message.text or ""
        await query.message.edit_text(text + "\n\n❌ Статус: отменена")
    elif action == "complete":
        # Помечаем, что ожидаем отчет
        await query.answer("Ожидаем отчёт.")
        # Удаляем кнопки, чтобы не нажимали повторно
        text = query.message.text or ""
        await query.message.edit_text(text + "\n\n📝 Ожидает отчёта")
        # Переходим в режим ожидания отчета для данного администратора
        await state.update_data(ticket_id=ticket_id)
        await state.set_state(AdminStates.wait_report)
        # Запрашиваем отчет у администратора в личке
        await query.bot.send_message(user.id, f"Пожалуйста, отправьте отчёт по заявке #{ticket_id}. Введите текст и прикрепите файлы, затем нажмите /done.")
    else:
        await query.answer()

@router.message(AdminStates.wait_report, content_types=[ContentType.TEXT, ContentType.PHOTO, ContentType.DOCUMENT])
async def process_report(message: Message, state: FSMContext):
    data = await state.get_data()
    ticket_id = data.get("ticket_id")
    if not ticket_id:
        return
    # Собираем отчёт и вложения
    report_text = data.get("report_text", "")
    attachments = data.get("attachments", [])
    if message.text and not message.text.startswith('/'):
        report_text += message.text + "\n"
        await state.update_data(report_text=report_text)
        await message.answer("Текст отчёта добавлен.")
    if message.photo:
        file_id = message.photo[-1].file_id
        attachments.append({"file_id": file_id, "type": "photo"})
        await state.update_data(attachments=attachments)
        await message.answer("Фото добавлено.")
    if message.document:
        file_id = message.document.file_id
        attachments.append({"file_id": file_id, "type": "document"})
        await state.update_data(attachments=attachments)
        await message.answer("Документ добавлен.")

@router.message(AdminStates.wait_report, Command("done"))
async def report_done(message: Message, state: FSMContext):
    data = await state.get_data()
    ticket_id = data.get("ticket_id")
    report_text = data.get("report_text", "")
    attachments = data.get("attachments", [])
    # Обновляем запись в БД
    attachments_json = json.dumps(attachments)
    await db_operations.add_ticket_report(ticket_id, report_text, attachments_json, message.from_user.id)
    # Получаем информацию о заявке для уведомления пользователя
    ticket = await db_operations.get_ticket(ticket_id)
    user_id = ticket["user_id"] if ticket else None
    # Отправляем отчёт пользователю
    if user_id:
        await message.bot.send_message(user_id, f"Ваша заявка #{ticket_id} завершена. Отчёт:\n{report_text}")
        for att in attachments:
            if att["type"] == "photo":
                await message.bot.send_photo(user_id, att["file_id"])
            elif att["type"] == "document":
                await message.bot.send_document(user_id, att["file_id"])
    await message.answer("Отчёт отправлен пользователю.")
    # Сбрасываем состояние
    await state.clear()
