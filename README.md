Развертывание
Создать виртуальное окружение:

```bash
<<<<<<< HEAD
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
Установить зависимости:
=======
git clone https://github.com/sergioninger/certus_bot.git
cd certus_bot
apt install python3.11-venv
python3 -m venv venv
source venv/bin/activate
```
Установите зависимости из requirements.txt:
```bash
pip install -r requirements.txt
```
Создайте и настройте базу данных MariaDB:
Создайте базу данных, например certus_tasks_db.
Выполните SQL-структуру для создания таблицы tickets (см. ниже).
Настройте файл config.py:
Укажите токен бота BOT_TOKEN.
Установите GROUP_ID (ID группы для админов, в формате -100...).
Добавьте идентификаторы администраторов в список ADMINS.
Укажите параметры подключения к базе данных (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME).
Запустите бота:

```bash
python main.py
```
systemd-сервис (опционально)
Для автоматического запуска бота можно создать systemd-сервис. Пример файла certus_bot.service:
```ini
[Unit]
Description=Телеграм-бот Certus Telecom Tasks Bot
After=network.target
>>>>>>> 7901509f15c0116b1e56d8b5b171ac475bdabbf1

```bash
pip install -r requirements.txt
```
Создать файл config/config.py с настройками:

<<<<<<< HEAD
```python
BOT_TOKEN = "your_bot_token"
ADMIN_GROUP_ID = -123456789  # ID группы администраторов
ADMINS = ["admin_user_id"]   # Список ID администраторов
```
Запустить бота:
```bash
python main.py
=======
[Install]
WantedBy=multi-user.target
```
Замените User и пути на свои.
SQL-структура таблицы tickets
Ниже приведена структура таблицы tickets для базы данных MariaDB:

```sql
CREATE TABLE tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    user_username VARCHAR(255),
    user_first_name VARCHAR(255),
    user_last_name VARCHAR(255),
    description TEXT NOT NULL,
    attachments TEXT,
    status ENUM('новая','в работе','отменена','завершена') NOT NULL DEFAULT 'новая',
    report TEXT,
    report_attachments TEXT,
    admin_id BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
>>>>>>> 7901509f15c0116b1e56d8b5b171ac475bdabbf1
```
