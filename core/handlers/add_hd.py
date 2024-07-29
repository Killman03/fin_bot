import datetime
import locale

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter

from core.keyboards.keyboards import get_add_note_kb, get_callback_btns
from core.utils.arif import resolve
from core.database.requests import add_note, get_cat_info
from core.filters.noletter_ft import NoLettersFilter

add_router = Router()


class AddNote(StatesGroup):
    note = State()


locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"  # Note: do not use "de_DE" as it doesn't work
)


################################## FSM for adding notes ##################################


@add_router.message(NoLettersFilter())
async def arif_hd_message(message: Message, bot: Bot, state: FSMContext):
    table_num = 1 if message.text == 'to_inc' else 2
    msg = await resolve(message.text)
    kbrd = await get_add_note_kb(table_num=table_num)
    await state.update_data(amount=msg)
    await bot.send_message(chat_id=message.from_user.id, text=f'❔ В какую категорию добавить {msg} ₽?',
                           reply_markup=kbrd)


@add_router.callback_query(F.data.in_(['to_inc', 'to_exp']))
async def arif_hd_callback(callback_query: CallbackQuery, bot: Bot, state: FSMContext):
    table_num = 1 if callback_query.data == 'to_inc' else 2
    kbrd = await get_add_note_kb(table_num=table_num)
    data = await state.get_data()
    msg = data['amount']
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                text=f'❔ В какую категорию добавить {msg} ₽?', reply_markup=kbrd)


@add_router.callback_query(StateFilter(None), F.data.startswith('add_exp') | F.data.startswith('add_inc'))
async def add_note_callback(callback_query: CallbackQuery, bot: Bot, state: FSMContext):
    btns = {
        '📆 Уточнить дату': 'date',
        '📝 Комментарий': 'comment',
        '🗑 Удалить': 'delete_note',
        '🏠 Домой': 'start',
    }
    data = await state.get_data()
    msg = data['amount']
    cat_id = int(callback_query.data.split('_')[2])
    date = datetime.datetime.now().strftime('%d.%B.%Y')
    await state.update_data(cat_id=cat_id, date=date)

    if callback_query.data.startswith('inc_add_'):
        cat_name = await get_cat_info(cat_id=int(callback_query.data.split('_')[2]), cat_type=1)
        await add_note(cat_type=1, cat_id=cat_id, amount=int(msg), description='')
        text = f'Добавлено {msg} ₽ в источник доходов {cat_name.name}.\n{date}'

    else:
        cat_name = await get_cat_info(cat_id=int(callback_query.data.split('_')[2]), cat_type=2)
        await add_note(cat_type=2, cat_id=cat_id, amount=int(msg), description='')
        text = f'Добавлено {msg} ₽ в категорию расходов {cat_name.name}.\n{date}'

    await bot.edit_message_text(text=text, chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                           reply_markup=get_callback_btns(btns=btns))


@add_router.callback_query(F.data == 'date')
async def date_callback(callback_query: CallbackQuery, bot: Bot, state: FSMContext):
    date = await state.get_data()
    date = date['date']
    date = date.split('.')
    btns = {
        f'{date[0]}': 'day',
        f'{date[1]}': 'month',
        f'{date[2]}': 'year',
        '✔️ Готово': 'done'
    }
    kbrd = get_callback_btns(btns=btns, size=(3,))
    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                        message_id=callback_query.message.message_id, reply_markup=kbrd)


@add_router.callback_query(F.data.in_(['day', 'month', 'year']))
async def date_callback(callback_query: CallbackQuery, bot: Bot, state: FSMContext):
    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
              'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

    if callback_query.data == 'day':
        for i in range(1, 32):
        btns = {str(i): f'day_{1}' for i in range(1, 32)}
        btns['<< Назад'] = 'date'
        kbrd = get_callback_btns(btns=btns, size=(7,))
        await state.update_data(day=i-1)
    elif callback_query.data == 'month':
        btns = {str(i): f'month_{i}' for i in months}
        btns['<< Назад'] = 'date'
        kbrd = get_callback_btns(btns=btns, size=(4,))
    elif callback_query.data == 'year':
        year_now = datetime.datetime.now().year
        btns = {str(i): f'year_{i}' for i in range(year_now-7, year_now + 1)}
        btns['<< Назад'] = 'date'
        kbrd = get_callback_btns(btns=btns, size=(4,))

    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                        message_id=callback_query.message.message_id, reply_markup=kbrd)


@add_router.callback_query(F.data == 'done')
async def done_callback(callback_query: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                        message_id=callback_query.message.message_id, reply_markup=None)
    await bot.send_message(chat_id=callback_query.from_user.id, text='Дата добавлена')
