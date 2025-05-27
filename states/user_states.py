from aiogram.fsm.state import StatesGroup, State

class TicketCreation(StatesGroup):
    title = State()
    description = State()
    priority = State()
    phone = State()
    attachments = State()
    confirmation = State()

class TicketDeletion(StatesGroup):
    ticket_id = State()