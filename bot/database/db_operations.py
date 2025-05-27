import mysql.connector
from datetime import datetime
from config import DB_CONFIG

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

async def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title TEXT,
            description TEXT,
            phone VARCHAR(20),
            priority TINYINT,
            company TEXT,
            status ENUM('новая', 'в работе', 'завершена', 'отменена клиентом', 'отменена админом'),
            created_at DATETIME,
            user_telegram_id BIGINT,
            user_username VARCHAR(64),
            image_path TEXT,
            report_text TEXT,
            report_image TEXT,
            admin_comment TEXT
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

async def create_ticket(data, user, image_path=None):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO tickets (
            title, description, phone, priority, company, status, created_at,
            user_telegram_id, user_username, image_path
        )
        VALUES (%s, %s, %s, %s, %s, 'новая', %s, %s, %s, %s)
    """
    values = (
        data['title'], data['description'], data['phone'], data['priority'], data['company'],
        datetime.now(), user.id, user.username, image_path
    )
    cursor.execute(query, values)
    ticket_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()
    return ticket_id

async def get_user_tickets(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tickets WHERE user_telegram_id = %s", (user_id,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

async def get_ticket_by_id(ticket_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tickets WHERE id = %s", (ticket_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

async def update_ticket_status(ticket_id, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tickets SET status = %s WHERE id = %s", (status, ticket_id))
    conn.commit()
    cursor.close()
    conn.close()

async def add_admin_comment(ticket_id, comment):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tickets SET admin_comment = %s WHERE id = %s", (comment, ticket_id))
    conn.commit()
    cursor.close()
    conn.close()

async def add_report(ticket_id, report_text, image_path=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tickets SET report_text = %s, report_image = %s WHERE id = %s",
        (report_text, image_path, ticket_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

async def cancel_user_ticket(ticket_id):
    await update_ticket_status(ticket_id, "отменена клиентом")