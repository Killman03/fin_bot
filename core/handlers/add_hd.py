import datetime
import locale

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter

from keyboards.keyboards import get_add_note_kb, get_callback_btns, get_note_kb
from utils.arif import resolve
from utils.correct_date import is_valid_date
from database.requests import add_note, get_cat_info, get_created_date, change_date, delete_note, add_comment
from filters.noletter_ft import NoLettersFilter

add_router = Router()


class AddNote(StatesGroup):
    comment = State()


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


################################## FSM for edit notes ##################################


@add_router.callback_query(StateFilter(None), F.data.startswith('add_exp') | F.data.startswith('add_inc'))
async def add_note_callback(callback_query: CallbackQuery, bot: Bot, state: FSMContext):

    data = await state.get_data()
    amount = data['amount']
    cat_id = int(callback_query.data.split('_')[2])

    if callback_query.data.startswith('add_inc_'):
        cat_name = await get_cat_info(cat_id=int(callback_query.data.split('_')[2]), cat_type=1)
        prod_id = await add_note(cat_type=1, cat_id=cat_id, amount=int(amount), description='')
        date = await get_created_date(cat_type=1, prod_id=prod_id)
        await state.update_data(prod_id=prod_id, date=date, cat_type=1, cat_name=cat_name.name)

    else:
        cat_name = await get_cat_info(cat_id=int(callback_query.data.split('_')[2]), cat_type=2)
        prod_id = await add_note(cat_type=2, cat_id=cat_id, amount=int(amount), description='')
        date = await get_created_date(cat_type=2, prod_id=prod_id)
        await state.update_data(prod_id=prod_id, date=date, cat_type=2, cat_name=cat_name.name)

    text = f'Добавлено {amount} ₽ в категорию расходов "{cat_name.name}".\n{date}'

    await bot.edit_message_text(text=text, chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                reply_markup=await get_note_kb())

############################# Change date ##################################


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
async def date_callback(callback_query: CallbackQuery, bot: Bot):
    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
              'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

    if callback_query.data == 'day':
        btns = {str(i): f'day_{i}' for i in range(1, 32)}
        btns['<< Назад'] = 'date'
        kbrd = get_callback_btns(btns=btns, size=(7,))

    elif callback_query.data == 'month':
        btns = {str(i): f'month_{i}' for i in months}
        btns['<< Назад'] = 'date'
        kbrd = get_callback_btns(btns=btns, size=(4,))

    elif callback_query.data == 'year':
        year_now = datetime.datetime.now().year
        btns = {str(i): f'year_{i}' for i in range(year_now - 7, year_now + 1)}
        btns['<< Назад'] = 'date'
        kbrd = get_callback_btns(btns=btns, size=(4,))

    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                        message_id=callback_query.message.message_id, reply_markup=kbrd)


@add_router.callback_query(F.data.startswith('day_') | F.data.startswith('month_') | F.data.startswith('year_'))
async def date_callback(callback_query: CallbackQuery, bot: Bot, state: FSMContext):
    date = await state.get_data()
    date = date['date']
    date = date.split('.')
    if callback_query.data.startswith('day_'):
        date[0] = callback_query.data.split('_')[1]
    elif callback_query.data.startswith('month_'):
        date[1] = callback_query.data.split('_')[1]
    elif callback_query.data.startswith('year_'):
        date[2] = callback_query.data.split('_')[1]
    date = '.'.join(date)
    await state.update_data(date=date)
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


@add_router.callback_query(F.data == 'done')
async def date_callback(callback_query: CallbackQuery, bot: Bot, state: FSMContext):
    MONTH_NAMES = {
        'Январь': 1, 'Февраль': 2, 'Март': 3, 'Апрель': 4, 'Май': 5, 'Июнь': 6,
        'Июль': 7, 'Август': 8, 'Сентябрь': 9, 'Октябрь': 10, 'Ноябрь': 11, 'Декабрь': 12
    }

    data = await state.get_data()
    date = data['date']
    date = date.split('.')
    date = datetime.datetime(int(date[2]), MONTH_NAMES[date[1]], int(date[0]))
    cat_type = await state.get_data()
    await change_date(date=str(date), cat_type=cat_type['cat_type'], prod_id=data['prod_id'])
    fsm_data = await state.get_data()
    fsm_data['date'] = date.strftime("%d.%B.%Y")
    text = f'Добавлено {fsm_data['amount']} ₽ в категорию расходов "{fsm_data['cat_name']}".\n{date.strftime('%d.%B.%Y')}'
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                text=text, reply_markup=await get_note_kb())


##################### delete note #####################


@add_router.callback_query(F.data == 'delete-note')
async def delete_note_callback(callback_query: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    await delete_note(cat_type=data['cat_type'], prod_id=data['prod_id'])
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await callback_query.message.answer('Запись удалена')

############################ FSM for comment ############################


@add_router.callback_query(F.data == 'comment')
async def comment_callback(callback_query: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, text='Введите комментарий')
    await state.set_state(AddNote.comment)


@add_router.message(AddNote.comment)
async def comment_callback(message: Message, bot: Bot, state: FSMContext):
    fsm_data = await state.get_data()
    await add_comment(cat_type=fsm_data['cat_type'], prod_id=fsm_data['prod_id'], comment=message.text)

    text = f'Добавлено {fsm_data['amount']} ₽ в категорию расходов "{fsm_data['cat_name']}".\n{fsm_data['date']}\n "_{message.text}_"'
    await message.answer(text=text, reply_markup=await get_note_kb(), parse_mode='Markdown')
