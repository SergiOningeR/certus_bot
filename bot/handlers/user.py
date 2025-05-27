from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.db_operations import create_ticket, get_user_tickets, cancel_user_ticket
from bot.utils.validators import validate_phone
from bot.utils.messaging import save_user_image
import os

class TicketState(StatesGroup):
    title = State()
    description = State()
    phone = State()
    priority = State()
    company = State()
    image = State()

async def start_cmd(message: types.Message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔧 Создать заявку", callback_data="new_ticket"))
    await message.answer(
        "Приветствуем в компании Certus Telecom! Для создания технической заявки нажмите «Создать заявку».",
        reply_markup=markup
    )

async def new_ticket(callback: types.CallbackQuery):
    await TicketState.title.set()
    await callback.message.answer("Введите название задачи:")

async def process_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await TicketState.next()
    await message.answer("Введите описание задачи:")

async def process_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await TicketState.next()
    await message.answer("Введите контактный номер (в формате +7 (XXX) XXX-XX-XX):")

async def process_phone(message: types.Message, state: FSMContext):
    if not validate_phone(message.text):
        return await message.answer("Некорректный формат. Попробуйте снова.")
    await state.update_data(phone=message.text)
    await TicketState.next()
    await message.answer("Укажите важность задачи (от 1 до 5):")

async def process_priority(message: types.Message, state: FSMContext):
    if message.text not in ["1", "2", "3", "4", "5"]:
        return await message.answer("Введите число от 1 до 5.")
    await state.update_data(priority=int(message.text))
    await TicketState.next()
    await message.answer("Введите название вашей компании:")

async def process_company(message: types.Message, state: FSMContext):
    await state.update_data(company=message.text)
    await TicketState.next()
    await message.answer("Прикрепите изображение (опционально) или напишите 'пропустить':")

async def process_image(message: types.Message, state: FSMContext):
    data = await state.get_data()
    ticket_id = await create_ticket(data, message.from_user, None)

    if message.content_type == 'photo':
        image_path = f"media/v_{ticket_id}.png"
        await save_user_image(message, message.photo[-1].file_id, image_path)
    else:
        image_path = None

    await message.answer(f"Задача №{ticket_id} успешно создана и передана сотрудникам компании. Ожидайте обратную связь.")
    await state.finish()

def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(start_cmd, commands="start")
    dp.register_callback_query_handler(new_ticket, text="new_ticket")
    dp.register_message_handler(process_title, state=TicketState.title)
    dp.register_message_handler(process_description, state=TicketState.description)
    dp.register_message_handler(process_phone, state=TicketState.phone)
    dp.register_message_handler(process_priority, state=TicketState.priority)
    dp.register_message_handler(process_company, state=TicketState.company)
    dp.register_message_handler(process_image, content_types=types.ContentTypes.ANY, state=TicketState.image)
