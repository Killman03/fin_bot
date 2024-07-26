from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.state import StatesGroup, State

my_router = Router(name=__name__)


class SetCat(StatesGroup):
    incomes = State()
    expenses = State()


@my_router.callback_query(F.data == 'info')
async def info(callback_query: CallbackQuery, bot: Bot):
    text = 'ℹ️ Чтобы добавить сведения о доходах или расходах,' \
            ' введите число или математическое выражение, например, ' \
            '26*4 или 236+189.\nМожно также направить фотографию '\
            'QR-кода на чеке. Бот сам распределит позиции в чеке так,'\
            ' как Вы его научите.\n\nЧтобы вывести отчет, введите '\
            'команду /report.\nДля произвольного периода используйте '\
            'формат /report_01072019_30092019.\n\nДля отображения в '\
            'отчете информации об остатке средств на начало и конец '\
            'периода, введите команду /saldo и укажите текущий остаток.'\
            '\nДля удаления информации об остатке средств используйте '\
            'команду /deletesaldo.'
    await bot.send_message(callback_query.from_user.id, text=text)

# @my_router.message(SetCat.incomes)
# async def set_exp(message: Message, state: FSMContext):
#     await state.update_data(incomes=message.text)
#     await state.set_state(SetCat.expenses)
#     await message.answer('✅ Источники доходов установлены. Теперь введите названия категорий расходов. Например:\n\n🍌 Категория 1 - 3900\n👚 Категория 2 - 50000\n🌿 Прочее\n\nP.S.: названия категорий расходов и плановые суммы можно будет изменить.')
#
#
# @my_router.message(SetCat.expenses)
# async def set_exp(message: Message, state: FSMContext):
#     await state.update_data(expends=message.text)
#     await add_fsm_data(state)
#     await state.clear()
#     await message.answer('👍 Всё готово!\nТеперь просто вводите числа или математические выражения, например, 26*4 или 236+189.\nМожно также направлять фотографии QR-кодов на чеках. Бот сам распределит позиции в чеке так, как Вы его научите.\n\nЧтобы вывести отчет, введите команду /report.\nДля произвольного периода используйте формат /report_01072019_30092019.\nДля отображения в отчете информации об остатке средств на начало и конец периода, введите команду /saldo и укажите текущий остаток.')



