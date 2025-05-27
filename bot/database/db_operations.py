import aiomysql
from aiomysql import DictCursor
import config

pool = None

async def create_pool():
    global pool
    pool = await aiomysql.create_pool(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        db=config.DB_NAME,
        autocommit=True
    )

async def close_pool():
    global pool
    if pool:
        pool.close()
        await pool.wait_closed()

async def create_ticket(user_id: int, user_username: str, user_first_name: str, user_last_name: str, description: str, attachments: str) -> int:
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            sql = """
                INSERT INTO tickets (user_id, user_username, user_first_name, user_last_name, description, attachments)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            await cur.execute(sql, (user_id, user_username, user_first_name, user_last_name, description, attachments))
            await conn.commit()
            return cur.lastrowid

async def update_ticket_status(ticket_id: int, status: str, admin_id: int):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            sql = "UPDATE tickets SET status=%s, admin_id=%s WHERE id=%s"
            await cur.execute(sql, (status, admin_id, ticket_id))
            await conn.commit()

async def add_ticket_report(ticket_id: int, report: str, report_attachments: str, admin_id: int):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            sql = """
                UPDATE tickets
                SET status='завершена', report=%s, report_attachments=%s, admin_id=%s
                WHERE id=%s
            """
            await cur.execute(sql, (report, report_attachments, admin_id, ticket_id))
            await conn.commit()

async def get_ticket(ticket_id: int):
    async with pool.acquire() as conn:
        async with conn.cursor(DictCursor) as cur:
            sql = "SELECT * FROM tickets WHERE id=%s"
            await cur.execute(sql, (ticket_id,))
            result = await cur.fetchone()
            return result
