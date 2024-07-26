import datetime

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.filters import or_f

from core.keyboards.keyboards import get_add_note_kb, get_callback_btns
from core.utils.arif import resolve
from core.database.requests import add_note, get_cat_info


add_router = Router()


class AddNote(StatesGroup):
    note = State()


@add_router.message()
@add_router.callback_query(or_f(F.text == 'to_inc', F.text == 'to_exp'))
async def arif_hd(event, bot: Bot, state: FSMContext, message: Message, callback_query: CallbackQuery):
    table_num = 1 if callback_query.data == 'to_inc' else 2
    msg = await resolve(callback_query.data)
    kbrd = await get_add_note_kb(table_num=table_num)

    if isinstance(event, Message):
        msg = await resolve(message.text)
        kbrd = await get_add_note_kb()
        await bot.send_message(chat_id=message.from_user.id, text=f'❔ В какую категорию добавить {msg} ₽?',
                               reply_markup=kbrd)

    elif isinstance(event, CallbackQuery):
        await bot.send_message(chat_id=callback_query.from_user.id, text=f'❔ В какую категорию добавить {msg} ₽?',
                               reply_markup=kbrd)

@add_router.callback_query(or_f(F.data.startswith('inc_add_'), F.data.startswith('exp_add_')))
async def add_note_callback(callback_query, bot: Bot, state: FSMContext):
    btns = {
        '📆 Уточнить дату': 'date',
        '📝 Комментарий': 'comment',
        '🚫 Отмена': 'cancel',
    }
    msg = await state.get_data()['note']

    if callback_query.data.startswith('inc_add_'):
        cat_name = await get_cat_info(cat_id=int(callback_query.data.split('_')[2]), cat_type=1)

        await add_note(cat_type=1, cat_id=int(callback_query.data.split('_')[2]), amount=int(msg))
        text = f'Добавлено {msg} ₽ в источник доходов {cat_name}.\n{datetime.datetime.now()}'
    else:
        cat_name = await get_cat_info(cat_id=int(callback_query.data.split('_')[2]), cat_type=2)
        await add_note(cat_type=2, cat_id=int(callback_query.data.split('_')[2]), amount=int(msg))
        text = f'Добавлено {msg} ₽ в категорию расходов {cat_name}.\n{datetime.datetime.now()}'

    await bot.send_message(chat_id=callback_query.from_user.id, text=text,
                           reply_markup=get_callback_btns(btns=btns))
    await state.clear()
