from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from core.database.requests import set_user
from core.keyboards.keyboards import get_start_kb


start_router = Router()


@start_router.message(Command(commands='start'))
@start_router.callback_query(F.data == 'start')
async def get_start(event, bot: Bot):
    """Check if the user exists in the database and greet them."""
    user_id = event.from_user.id
    first_name = event.from_user.first_name

    text = f'Привет, {first_name}! 👋 Для того, чтобы добавить источник доходов или расходов, ' \
           f'перейди в настройки ⚙️. Давай вместе придем к финансовой независимости! 💰💼'

    if isinstance(event, Message):
        await set_user(user_id, first_name)
        await bot.send_message(user_id, text=text, reply_markup=await get_start_kb())

    elif isinstance(event, CallbackQuery):
        await bot.edit_message_text(chat_id=user_id, message_id=event.message.message_id, text=text,
                                    reply_markup=await get_start_kb())
