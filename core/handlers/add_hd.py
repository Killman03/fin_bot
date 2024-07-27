import datetime

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter

from core.keyboards.keyboards import get_add_note_kb, get_callback_btns
from core.utils.arif import resolve
from core.database.requests import add_note, get_cat_info


add_router = Router()


class AddNote(StatesGroup):
    note = State()


################################## FSM for adding notes ##################################


@add_router.message()
async def arif_hd_message(message: Message, bot: Bot, state: FSMContext):
    table_num = 1 if message.text == 'to_inc' else 2
    msg = await resolve(message.text)
    kbrd = await get_add_note_kb(table_num=table_num)
    await state.update_data(amount=msg)
    await bot.send_message(chat_id=message.from_user.id, text=f'❔ В какую категорию добавить {msg} ₽?', reply_markup=kbrd)


@add_router.callback_query(F.data.in_(['to_inc', 'to_exp']))
async def arif_hd_callback(callback_query: CallbackQuery, bot: Bot, state: FSMContext):
    table_num = 1 if callback_query.data == 'to_inc' else 2
    kbrd = await get_add_note_kb(table_num=table_num)
    data = await state.get_data()
    msg = data['amount']
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                text=f'❔ В какую категорию добавить {msg} ₽?', reply_markup=kbrd)


@add_router.callback_query(StateFilter('*'), F.data.startswith('exp_add') | F.data.startswith('inc_add'))
async def add_note_callback(callback_query: CallbackQuery, bot: Bot, state: FSMContext):
    print(callback_query.data)
    await bot.send_message(chat_id=callback_query.from_user.id, text='❔ Уточните дату и комментарий к записи.')
    btns = {
        '📆 Уточнить дату': 'date',
        '📝 Комментарий': 'comment',
        '🚫 Отмена': 'cancel',
    }
    data = await state.get_data()
    msg = data['amount']

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
