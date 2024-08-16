import os

from aiogram import Bot, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.state import StatesGroup, State

from keyboards.keyboards import get_callback_btns, get_start_kb
from utils.to_excel import export_to_xlsx

my_router = Router(name=__name__)


class SetCat(StatesGroup):
    incomes = State()
    expenses = State()


@my_router.callback_query(F.data == "cancel", StateFilter('*'))
async def cancel_handler(callback_query: CallbackQuery, state:FSMContext) -> None:
    current_state = await state.get_state()
    await state.clear()
    await callback_query.answer("Действия отменены", show_alert=True)

    text = f'Привет, {callback_query.from_user.first_name}! 👋 Для того, чтобы добавить источник доходов или расходов, ' \
           f'перейди в настройки ⚙️. Давай вместе придем к финансовой независимости! 💰💼'

    await callback_query.message.edit_text(text=text, reply_markup=await get_start_kb())


@my_router.callback_query(F.data == 'info')
async def info(callback_query: CallbackQuery, bot: Bot):
    text = 'ℹ️ Чтобы добавить сведения о доходах или расходах,' \
            ' введите число или математическое выражение, например, ' \
            '26*4 или 236+189.\nМожно также направить фотографию '\
            'QR-кода на чеке. \n\nЧтобы вывести отчет, введите '\
            'команду /report.'
    await bot.send_message(callback_query.from_user.id, text=text, reply_markup=get_callback_btns(btns={'🔙 Назад': 'delete_info'}))


@my_router.callback_query(F.data == 'delete_info')
async def delete_info(callback_query: CallbackQuery, bot: Bot):
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)


@my_router.callback_query(F.data == 'excel')
async def send_xl(callback_query: CallbackQuery):
    await export_to_xlsx()
    file_path = 'documents/budget.xlsx'
    await callback_query.message.reply_document(document=FSInputFile(path=file_path))
    os.remove('documents/budget.xlsx')