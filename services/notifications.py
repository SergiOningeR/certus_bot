from aiogram.types import InputMediaPhoto
from config.config import bot, settings
from utils.logger import logger
from database.models import TicketCreate  # Добавлен импорт

async def notify_admins(ticket_id: int, ticket: TicketCreate):
    try:
        message_text = (
            f"🆕 Новая заявка #{ticket_id}\n"
            f"📌 {ticket.title}\n"
            f"🔢 Важность: {ticket.priority}/5\n"
            f"📱 Телефон: {ticket.phone}\n"
            f"📝 Описание: {ticket.description[:200]}..."
        )

        if ticket.attachments:
            media_group = [
                InputMediaPhoto(
                    media=file_id,
                    caption=message_text if i == 0 else ""
                )
                for i, file_id in enumerate(ticket.attachments)
            ]
            await bot.send_media_group(
                chat_id=settings.ADMIN_GROUP_ID,
                media=media_group
            )
        else:
            await bot.send_message(
                chat_id=settings.ADMIN_GROUP_ID,
                text=message_text
            )
    except Exception as e:
        logger.error(f"Ошибка уведомления: {str(e)}")