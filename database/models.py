from enum import Enum
import re
from pydantic import BaseModel, validator, ValidationError
from datetime import datetime

class TicketStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class TicketCreate(BaseModel):
    user_id: int
    title: str
    description: str
    phone: str
    priority: int
    attachments: list[str] = []
    status: TicketStatus = TicketStatus.NEW

    @validator('phone')
    def validate_phone(cls, v):
        # Удаляем все символы, кроме цифр и плюса
        cleaned = re.sub(r'[^\d+]', '', v)
        
        # Оставляем только первый плюс
        if '+' in cleaned:
            parts = cleaned.split('+', 1)  # Разделяем только по первому плюсу
            cleaned = '+' + parts[1].replace('+', '') if len(parts) > 1 else '+'
        else:
            cleaned = cleaned
        
        # Извлекаем цифры (без плюса)
        digits = cleaned.lstrip('+')
        
        if not (10 <= len(digits) <= 15):
            raise ValueError("Номер должен содержать 10-15 цифр")
        
        return f"+{digits}"

    @validator('priority')
    def validate_priority(cls, v):
        if 1 <= v <= 5:
            return v
        raise ValueError("Важность должна быть от 1 до 5")

class Ticket(TicketCreate):
    id: int
    created_at: datetime