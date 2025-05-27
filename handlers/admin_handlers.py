from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from database.crud import get_all_tickets, update_ticket_status
from keyboards.admin_keyboards import get_admin_main_kb, get_ticket_actions_kb

admin_router = Router()

@admin_router.message(Command("admin"))
async def admin_panel(message: Message):
    await message.answer("⚙ Админ-панель:", reply_markup=get_admin_main_kb())

@admin_router.callback_query(F.data == "admin_stats")
async def show_stats(callback: CallbackQuery):  # Убрана лишняя скобка
    tickets = await get_all_tickets()
    stats = {
        "new": sum(1 for t in tickets if t.status == "new"),
        "in_progress": sum(1 for t in tickets if t.status == "in_progress"),
        "completed": sum(1 for t in tickets if t.status == "completed")
    }
    await callback.message.answer(
        f"📊 Статистика:\n"
        f"🆕 Новых: {stats['new']}\n"
        f"🔄 В работе: {stats['in_progress']}\n"
        f"✅ Завершено: {stats['completed']}"
    )

@admin_router.callback_query(F.data == "admin_tickets")
async def show_tickets(callback: CallbackQuery):  # Исправлено
    tickets = await get_all_tickets()
    if not tickets:
        return await callback.message.answer("📭 Нет активных заявок")
    
    response = ["📋 Все заявки:\n"]
    for ticket in tickets:
        response.append(
            f"🔸 #{ticket.id} | {ticket.title}\n"
            f"🔢 {ticket.priority}/5 | {ticket.status}"
        )
    await callback.message.answer("\n\n".join(response))

@admin_router.callback_query(F.data.startswith("status_"))
async def change_status(callback: CallbackQuery):
    action, ticket_id = callback.data.split("_")[1:]
    new_status = "in_progress" if action == "progress" else "completed"
    
    await update_ticket_status(int(ticket_id), new_status)
    await callback.message.edit_text(
        f"🔄 Статус заявки #{ticket_id} изменен на {new_status}"
    )
    await callback.answer()