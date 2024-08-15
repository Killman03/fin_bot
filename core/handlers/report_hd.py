import datetime

from aiogram import Bot, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from core.keyboards.keyboards import get_callback_btns
from core.database.requests import get_monthly_report


report_router = Router()


@report_router.callback_query(F.data.startswith('report_'))
async def report_navigation(callback_query: CallbackQuery, bot: Bot, state: FSMContext):
    # Извлекаем действие и текущий месяц из данных кнопки
    action, current_month, flag = callback_query.data.split('_')[1:]
    #current_month = datetime.datetime.now().strftime('%Y-%m')
    # Получаем отчет по месяцам
    report = await get_monthly_report()
    # Сортируем месяцы
    months = sorted(report.keys())

    # Определяем следующий или предыдущий месяц в зависимости от действия
    if action == 'next':
        next_index = (months.index(current_month) + 1) % len(months)
    elif action == 'prev':
        next_index = (months.index(current_month) - 1) % len(months)

    next_month = months[next_index]

    # Создаем кнопки для навигации
    btns = {
        '⬅️ Назад': f'report_prev_{next_month}_0',
        '➡️ Вперед': f'report_next_{next_month}_0',
        '🔙 Назад': 'start'
    }

    if flag == '1':
        data = report[current_month]
        text = f'Доходы в {current_month}: {data["income"]}\nРасходы: {data["expense"]}\nБаланс: {data["balance"]}'

        await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                    text=text, reply_markup=get_callback_btns(btns=btns))

    else:
        data = report[next_month]
        # Формируем текст отчета для следующего месяца
        text = f'Доходы в {next_month}: {data["income"]}\nРасходы: {data["expense"]}\nБаланс: {data["balance"]}'
        await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                    text=text, reply_markup=get_callback_btns(btns=btns))


