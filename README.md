# Certus Telecom Tasks Bot

Телеграм-бот для создания и управления заявками (Tasks) с сохранением в базе данных MariaDB. Поддерживает создание заявки пользователем, пересылку заявки в группу администраторов, изменение статуса заявки и отправку отчёта с вложениями.

## Функции

- Пользователь может создать заявку через последовательность вопросов (FSM): описать проблему, при необходимости прикрепить файлы.
- Заявка сохраняется в таблицу `tickets` базы данных.
- Заявки пересылаются в указанный Telegram-групповой чат для администраторов.
- Администраторы могут изменять статус заявки (новая, в работе, отменена, завершена) с помощью inline-кнопок.
- После завершения заявки администратор может отправить отчёт (текст и вложения), который будет переслан автору заявки.
- Пользователь получает уведомления о создании заявки и её изменениях.

## Установка

1. **Склонируйте репозиторий** и перейдите в папку проекта:
```bash
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

[Service]
Type=simple
User=botuser
WorkingDirectory=/path/to/your/project
ExecStart=/usr/bin/python3 /path/to/your/project/main.py
Restart=on-failure

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
```
