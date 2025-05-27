import aiosqlite
from pathlib import Path
from typing import List
from .models import Ticket, TicketCreate
from config.config import settings

async def init_db():
    async with aiosqlite.connect(settings.DB.DB_NAME) as db:
        with open(Path(settings.DB.SQL_SCRIPTS_DIR) / "init.sql", "r") as f:
            await db.executescript(f.read())
        await db.commit()

async def create_ticket(ticket: TicketCreate) -> int:
    async with aiosqlite.connect(settings.DB.DB_NAME) as db:
        cursor = await db.execute(
            """INSERT INTO tickets 
            (user_id, title, description, phone, priority, attachments, status) 
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                ticket.user_id,
                ticket.title,
                ticket.description,
                ticket.phone,
                ticket.priority,
                ",".join(ticket.attachments),
                ticket.status.value
            )
        )
        await db.commit()
        return cursor.lastrowid

async def get_user_tickets(user_id: int) -> List[Ticket]:
    async with aiosqlite.connect(settings.DB.DB_NAME) as db:
        cursor = await db.execute(
            "SELECT * FROM tickets WHERE user_id = ?",
            (user_id,)
        )
        rows = await cursor.fetchall()
        return [Ticket(**row) for row in rows]

async def delete_ticket(ticket_id: int, user_id: int):
    async with aiosqlite.connect(settings.DB.DB_NAME) as db:
        await db.execute(
            "DELETE FROM tickets WHERE id = ? AND user_id = ?",
            (ticket_id, user_id)
        )
        await db.commit()