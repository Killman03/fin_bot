from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter

import keyboards.keyboards as kb
from database.requests import (
    get_cat_info,
    delete_cat,
    add_cat,
    change_cat_name,
)


cat_router = Router()


class ChangeCategoryState(StatesGroup):
    waiting_for_change = State()


class AddCategoryState(StatesGroup):
    add_name = State()
    add_plan = State()


@cat_router.callback_query(StateFilter('*'), F.data == 'settings')
async def settings(callback_query: CallbackQuery, bot: Bot, state: FSMContext):
    '''Settings menu'''
    if await state.get_state() is not None:
        await state.clear()
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, text='⚙️ Выберите раздел для настройки:',
                                reply_markup=kb.get_callback_btns(btns={'📈 Доходы': 'conf_inc', '📉 Расходы': 'conf_exp', '🔙 Назад': 'start'}))


@cat_router.callback_query(F.data.startswith('conf_'))
async def callback_query_keyboard(callback_query: CallbackQuery, bot: Bot):

    if callback_query.data.startswith('conf_inc'):
        cat_type = 1
    elif callback_query.data.startswith('conf_exp'):
        cat_type = 2

    keyboard = await kb.get_cat_list(table_num=cat_type)

    text = 'Выберите источник доходов 📈' if cat_type == 1 else 'Выберите категорию расходов 📉'

    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, text=text, reply_markup=keyboard)


@cat_router.callback_query(F.data.startswith('inc_') | F.data.startswith('exp_'))
async def callback_query_keyboard(callback_query: CallbackQuery, bot: Bot, state: FSMContext):

    cat_id = int(callback_query.data.split('_')[1])
    cat_type = 1 if callback_query.data.startswith('inc_') else 2

    btns = {
        '✏️Переименовать': f'rename_{cat_type}_{cat_id}',
        'Удалить': f'delete_{cat_type}_{cat_id}',
        'Удалить': f'delete_{cat_type}_{cat_id}',
        '⬆️Поднять в списке': f'up_{cat_type}_{cat_id}',
        '⬇️Опустить в списке': f'down_{cat_type}_{cat_id}',
        '🔙Назад': 'conf_inc' if cat_type == 1 else 'conf_exp'
    }

    cat = await get_cat_info(cat_type, cat_id)

    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, text=f'Выбрана категория: {cat.name}\nПлановая сумма: {cat.plan}',
                                reply_markup=kb.get_callback_btns(btns=btns))


@cat_router.callback_query(F.data.startswith('delete_'))
async def callback_query_keyboard(callback_query: CallbackQuery, bot: Bot):
    cat_type, cat_id = map(int, callback_query.data.split('_')[1:])
    await delete_cat(cat_id, cat_type)
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, text='Категория удалена')


################################## FSM for changing category name ##################################


@cat_router.callback_query(StateFilter(None), F.data.startswith('rename_'))
async def callback_query_keyboard(callback_query: CallbackQuery, bot: Bot, state: FSMContext):
    cat_type, cat_id = map(int, callback_query.data.split('_')[1:])

    text = 'Введите новое название категории доходов' if cat_type == 1 else 'Введите новое название категории расходов'

    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, text=text)
    await state.update_data(cat_id=cat_id, cat_type=cat_type)
    await state.set_state(ChangeCategoryState.waiting_for_change)


@cat_router.message(ChangeCategoryState.waiting_for_change)
async def change_inc_name(message: Message, state: FSMContext):
    data = await state.get_data()
    await change_cat_name(data['cat_id'], data['cat_type'], message.text)
    await state.clear()
    await message.answer('Название изменено')


########################### FSM for adding new category ###########################


@cat_router.callback_query(F.data.startswith('add_cat_exp') | F.data.startswith('add_cat_inc'))
async def callback_query_keyboard(callback_query: CallbackQuery, state: FSMContext):
    cat_type = 1 if callback_query.data == 'add_cat_inc' else 2

    text = 'Введите название новой категории доходов 📈' if cat_type == 1 else 'Введите название новой категории расходов 📉'

    await callback_query.answer()
    await callback_query.message.answer(text=text, reply_markup=kb.get_callback_btns(btns={'🚫 Cancel': 'settings'}))
    await state.update_data(cat_type=cat_type)
    await state.set_state(AddCategoryState.add_name)


@cat_router.message(AddCategoryState.add_name)
async def add_cat_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddCategoryState.add_plan)
    await message.answer('Введите плановую сумму', reply_markup=kb.get_callback_btns(btns={'🚫 Cancel': 'settings'}))


@cat_router.message(AddCategoryState.add_plan)
async def add_cat_plan(message: Message, state: FSMContext):
    data = await state.get_data()
    await add_cat(data['cat_type'], data['name'], int(message.text))
    await state.clear()
    await (message.answer('Категория добавлена', reply_markup=kb.get_callback_btns(btns={'🔙 Назад': 'settings',
                                                                                        'Главное меню': 'start'})))