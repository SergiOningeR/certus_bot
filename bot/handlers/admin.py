from aiogram import Dispatcher, types
from config import ADMIN_GROUP_ID, ADMIN_THREAD_ID
from bot.database.db_operations import update_ticket_status, get_ticket_by_id, add_admin_comment, add_report
from bot.utils.messaging import notify_user, save_admin_image

async def admin_group_listener(message: types.Message):
    if message.chat.id != ADMIN_GROUP_ID or not message.reply_to_message:
        return

    if message.text.startswith("/ответ "):
        original_text = message.reply_to_message.text
        ticket_id = int(original_text.split('№')[1].split()[0])
        reply_text = message.text.replace("/ответ ", "").strip()
        ticket = await get_ticket_by_id(ticket_id)
        if ticket:
            await notify_user(ticket['user_telegram_id'], f"Ответ от поддержки:\n{reply_text}")

async def accept_ticket(callback: types.CallbackQuery):
    ticket_id = int(callback.data.split("_")[1])
    await update_ticket_status(ticket_id, "в работе")
    ticket = await get_ticket_by_id(ticket_id)
    await notify_user(ticket['user_telegram_id'], f"Задача №{ticket_id} взята в работу, ожидайте завершения.")
    await callback.answer("Заявка принята.")

async def cancel_ticket(callback: types.CallbackQuery):
    ticket_id = int(callback.data.split("_")[1])
    await callback.message.answer("Введите причину отмены заявки:")

    @callback.message.bot.message_handler()
    async def get_comment(msg: types.Message):
        await update_ticket_status(ticket_id, "отменена админом")
        await add_admin_comment(ticket_id, msg.text)
        ticket = await get_ticket_by_id(ticket_id)
        await notify_user(ticket['user_telegram_id'],
                          f"Задача №{ticket_id} отменена администратором. Комментарий: {msg.text}")

async def complete_ticket(callback: types.CallbackQuery):
    ticket_id = int(callback.data.split("_")[1])
    await callback.message.answer("Введите отчет о завершении:")

    @callback.message.bot.message_handler()
    async def get_report(msg: types.Message):
        report_text = msg.text
        image_path = None

        if msg.photo:
            image_path = f"media/o_{ticket_id}.png"
            await save_admin_image(msg, msg.photo[-1].file_id, image_path)

        await update_ticket_status(ticket_id, "завершена")
        await add_report(ticket_id, report_text, image_path)
        ticket = await get_ticket_by_id(ticket_id)
        await notify_user(ticket['user_telegram_id'],
                          f"Задача №{ticket_id} завершена. Отчет: {report_text}")
        await msg.answer("Заявка завершена.")

def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_group_listener, content_types=types.ContentType.TEXT)
    dp.register_callback_query_handler(accept_ticket, lambda c: c.data.startswith("accept_"))
    dp.register_callback_query_handler(cancel_ticket, lambda c: c.data.startswith("cancel_"))
    dp.register_callback_query_handler(complete_ticket, lambda c: c.data.startswith("complete_"))
