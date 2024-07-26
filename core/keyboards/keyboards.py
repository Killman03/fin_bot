from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder

from core.database.requests import get_all_notes


def get_callback_btns(*, btns: dict[str, str], size: tuple[int] = (2, )):
    keyboard = InlineKeyboardBuilder()

    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*size).as_markup()


async def get_cat_list(table_num: int):
    items = await get_all_notes(table_num=table_num)
    keyboard = InlineKeyboardBuilder()
    callback_prefix = 'inc' if table_num == 1 else 'exp'
    add_cat = 'add_inc' if table_num == 1 else 'add_exp'

    for item in items:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f'{callback_prefix}_{item.id}'))
    keyboard.add(InlineKeyboardButton(text='➕Добавить категорию', callback_data=    add_cat))
    keyboard.add(InlineKeyboardButton(text='🔙Назад', callback_data='settings'))

    return keyboard.adjust(1).as_markup()


async def get_add_note_kb(table_num: int = 2):
    items = await get_all_notes(table_num)
    keyboard = InlineKeyboardBuilder()
    callback_prefix = 'inc_add' if table_num == 1 else 'exp_add'
    to_anthr = 'to_inc' if table_num == 2 else 'to_exp'

    for item in items:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f'{callback_prefix}_{item.id}'))
    if table_num == 2:
        keyboard.add(InlineKeyboardButton(text='К доходам', callback_data=to_anthr))
    else:
        keyboard.add(InlineKeyboardButton(text='К расходам', callback_data=to_anthr))

    return keyboard.adjust(1).as_markup()
