import datetime

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.keyboards import get_callback_btns
from database.requests import get_monthly_report


report_router = Router()


@report_router.callback_query(F.data.startswith('report'))
async def report_navigation(callback_query: CallbackQuery, bot: Bot, state: FSMContext):
    # Извлекаем действие и текущий месяц из данных кнопки
    action, current_month, flag = callback_query.data.split('_')[1:]
    user_id = callback_query.from_user
    # Получаем отчет по месяцам
    report = await get_monthly_report(user_id=user_id.id)
    # Сортируем месяцы
    months = sorted(report.keys())
    if flag == '1':
        current_month = list(report.keys())[0]

    # Определяем следующий или предыдущий месяц в зависимости от действия
    if action == 'next':
        next_index = (months.index(current_month) + 1) % len(months)
    elif action == 'prev':
        next_index = (months.index(current_month) - 1) % len(months)

    next_month = months[next_index]


    # Создаем кнопки для навигации
    btns = {
        '⬅️ Назад': f'report:{datetime.datetime.now()}_prev_{next_month}_0',
        '➡️ Вперед': f'report:{datetime.datetime.now()}_next_{next_month}_0',
        '🔙 Назад': 'start'
    }

    if flag == '1':
        data = report[current_month]
        text = f'{current_month}\n\nДоходы: {data["income"]}\nРасходы: {data["expense"]}\nБаланс: {data["balance"]}'

        await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                    text=text, reply_markup=get_callback_btns(btns=btns))

    else:
        data = report[next_month]
        # Формируем текст отчета для следующего месяца
        text = f'{next_month}\n\nДоходы: {data["income"]}\nРасходы: {data["expense"]}\nБаланс: {data["balance"]}'
        await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                    text=text, reply_markup=get_callback_btns(btns=btns))
