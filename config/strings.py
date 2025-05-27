class Strings:
    START = "Добро пожаловать! Для создания заявки используйте /new_ticket"
    NEW_TICKET_DESC = "Опишите вашу проблему или запрос:"
    PHONE_REQUEST = "Укажите ваш номер телефона для связи:"
    PHONE_ERROR = "❌ Некорректный формат номера. Пример: +79991234567"
    ATTACHMENTS_REQUEST = "Прикрепите файлы или нажмите 'Пропустить'"
    
    class Admin:
        NEW_TICKET_NOTIFY = "🆕 Новая заявка #{ticket_id}\nПользователь: {user_id}\nТелефон: {phone}"

strings = Strings()