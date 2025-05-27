Развертывание
Создать виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
Установить зависимости:

```bash
pip install -r requirements.txt
```
Создать файл config/config.py с настройками:

```python
BOT_TOKEN = "your_bot_token"
ADMIN_GROUP_ID = -123456789  # ID группы администраторов
ADMINS = ["admin_user_id"]   # Список ID администраторов
```
Запустить бота:
```bash
python main.py
```
