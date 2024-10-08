import datetime

from sqlalchemy import select, update, delete, func, cast, DECIMAL, exists
from sqlalchemy.orm import aliased

from .models import User, ExpCategory, IncCategory, Expense, Income
from .engine import async_session


async def set_user(tg_id, user_name):
    """Check if the user exists in the database and greet them. If not, add them to the database."""
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, user_name=user_name))
            await session.commit()


########################### WORKING WITH CATEGORY ##############################

async def get_all_notes(table_num: int, user_id: int):
    if table_num == 1:
        table = IncCategory
    elif table_num == 2:
        table = ExpCategory
    async with async_session() as session:
        return await session.scalars(select(table).where(table.user_id == user_id))


async def get_cat_info(cat_type: int, cat_id: int):
    async with async_session() as session:
        if cat_type == 1:
            table = IncCategory
            table_2 = Income
        else:
            table = ExpCategory
            table_2 = Expense

        query = select(table).where(table.id == cat_id)
        name = await session.execute(query)
        await session.commit()

        # Total amount for all time
        total_all_time = await session.scalar(
            select(func.sum(cast(table_2.amount, DECIMAL)))
            .where(table_2.category_id == cat_id)
        )

        # Total amount for last month
        total_last_month = await session.scalar(
            select(func.sum(cast(table_2.amount, DECIMAL)))
            .where(Expense.category_id == 3)
            .where(func.date_trunc('month', table_2.created) == func.date_trunc('month', func.current_date()))
        )

        name = await session.scalar(select(table).where(table.id == cat_id))
        cat_info_dict = {
            'cat_info': name,
            'cat_month': total_last_month,
            'cat_year': total_all_time
            }

        return cat_info_dict


async def delete_cat(cat_id: int, cat_type: int):
    async with async_session() as session:
        if cat_type == 1:
            table = IncCategory
        else:
            table = ExpCategory
        query = delete(table).where(table.id == cat_id)
        await session.execute(query)
        await session.commit()


async def add_cat(cat_type: int, name: str, plan: int, user_id: int):
    async with async_session() as session:
        if cat_type == 1:
            table = IncCategory
        else:
            table = ExpCategory
        session.add(table(name=name, plan=plan, user_id=user_id))
        await session.commit()


async def change_cat_name(cat_id: int, cat_type: int, new_name: str):
    async with async_session() as session:
        if cat_type == 1:
            table = IncCategory
        else:
            table = ExpCategory
        query = update(table).where(table.id == cat_id).values(name=new_name)
        await session.execute(query)
        await session.commit()


async def add_note(cat_type: int, cat_id: int, amount: str, description: str, created=''):
    async with async_session() as session:
        if cat_type == 1:
            table = Income
        else:
            table = Expense

        if created != '':
            prod_id = table(amount=str(amount), description=description, category_id=cat_id, created=created)
            session.add(prod_id)
            await session.commit()
            return prod_id.id

        prod_id = table(amount=str(amount), description=description, category_id=cat_id)
        session.add(prod_id)

        await session.commit()
        return prod_id.id


async def get_created_date(cat_type: int, prod_id: int):
    async with async_session() as session:
        if cat_type == 1:
            table = Income
        else:
            table = Expense
        created_date = await session.scalar(select(table.created).where(table.id == prod_id))
        cr_date = created_date.strftime('%d.%B.%Y')
        return cr_date


async def change_date(cat_type: int, date: str, prod_id: int):
    async with async_session() as session:
        if cat_type == 1:
            table = Income
        else:
            table = Expense
        new_date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        query = update(table).where(table.id == prod_id).values(created=new_date).execution_options(
            synchronize_session=False)
        await session.execute(query)
        await session.commit()


async def delete_note(cat_type: int, prod_id: int):
    async with async_session() as session:
        if cat_type == 1:
            table = Income
        else:
            table = Expense
        query = delete(table).where(table.id == prod_id)
        await session.execute(query)
        await session.commit()


async def add_comment(cat_type: int, prod_id: int, comment: str):
    async with async_session() as session:
        if cat_type == 1:
            table = Income
        else:
            table = Expense
        query = update(table).where(table.id == prod_id).values(description=comment)
        await session.execute(query)
        await session.commit()


async def get_monthly_report(user_id: int):
    # Открываем асинхронную сессию с базой данных
    async with async_session() as session:

        # Запрос для получения доходов, сгруппированных по месяцам
        for i in [Income, Expense]:
            if i == Income:
                category_alias = aliased(IncCategory)
            else:
                category_alias = aliased(ExpCategory)
            query = (
                select(
                    func.date_trunc('month', i.created).label('month'),
                    func.sum(cast(i.amount, DECIMAL)).label(f'total_{'income' if i==Income else 'expense'}')
                ).join(
                    category_alias, i.category_id == category_alias.id
                ).filter(
                    category_alias.user_id == user_id
                ).group_by(
                    i.created,
                    func.date_trunc('month', i.created)
            ))
            if i == Income:
                income_results = await session.execute(query)
            else:
                expense_results = await session.execute(query)

        income_data = {row.month.strftime("%B %Y"): row.total_income for row in income_results}
        expense_data = {row.month.strftime("%B %Y"): row.total_expense for row in expense_results}


        # Формируем отчет, объединяя данные о доходах и расходах
        report = {}
        for month in income_data.keys() | expense_data.keys():
            report[month] = {
                'income': income_data.get(month, 0),
                'expense': expense_data.get(month, 0),
                'balance': income_data.get(month, 0) - expense_data.get(month, 0)
            }

        return report


async def get_all_db():
    async with async_session() as session:
        expenses = await session.execute(select(Expense))
        incomes = await session.execute(select(Income))

        expense_values = expenses.scalars().all()
        income_values = incomes.scalars().all()

        return expense_values, income_values


async def get_note_info(cat_type: int, cat_id: int):
    async with async_session() as session:
        if cat_type == 1:
            table = Income
        else:
            table = Expense

        result = await session.scalars(select(table).where(table.category_id == cat_id))

        return result


async def check_description_exists(description):
    async with async_session() as session:
        result = await session.execute(select(Expense).where(Expense.description == description))
        note = result.scalars().first()
        if note:
            return note.category_id
        return False

async def get_balance(user_id: int):
    async with async_session() as session:
        pass
