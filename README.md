# Certus Telecom – Tasks Bot

Телеграм-бот технической поддержки для компании **Certus Telecom**.  
Позволяет клиентам создавать заявки прямо в мессенджере, а администраторам — обрабатывать их.

## 📂 Структура проекта

certus_bot/
├── main.py
├── config.py
├── requirements.txt
├── systemd/
│ └── certus_bot.service
├── media/
├── bot/
│ ├── handlers/
│ │ ├── user.py
│ │ └── admin.py
│ ├── database/
│ │ └── db_operations.py
│ └── utils/
│ ├── validators.py
│ └── messaging.py
└── README.md

## 🚀 Возможности

- **Пользовательский функционал**  
  - Создание заявки: название, описание, телефон, приоритет (1-5), компания, опционально изображение  
  - Просмотр всех заявок  
  - Отмена заявки

- **Административный функционал**  
  - Автопубликация новой заявки в админ-группе (тред)  
  - Кнопки: принять в работу, отменить (с комментарием), завершить (с отчетом и фото)  
  - Ответ клиенту через команду `/ответ`

- **Хранение данных** в MySQL:
  - Таблица `tickets` с необходимыми полями  
  - Папка `media/` для пользовательских и админ-изображений

## ⚙️ Установка

1. Клонировать репозиторий:  
   ```bash
   git clone https://github.com/sergioninger/certus_bot.git
   cd certus_bot```
Создать виртуальное окружение и установить зависимости:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt```
Создать базу данных и таблицу tickets:

sql
```
CREATE DATABASE certus_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE certus_db;```
-- Таблица создаётся автоматически при первом запуске бота
Настроить переменные в config.py (токен бота, данные для MySQL, ID группы).

🏃 Запуск
Локально

```bash
python3 main.py```
Через systemd

```bash
sudo cp systemd/certus_bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable certus_bot
sudo systemctl start certus_bot```
📬 Контакты
Разработчик: @sergioninger
