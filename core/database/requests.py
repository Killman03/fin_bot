from .models import User, ExpCategory, IncCategory, Expense, Income
from .engine import async_session

from sqlalchemy import select, update, delete, insert

import logging
import json

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


async def set_user(tg_id, user_name):
    """Check if the user exists in the database and greet them. If not, add them to the database."""
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, user_name=user_name))
            await session.commit()


########################### WORKING WITH CATEGORY ##############################


async def get_all_notes(table_num: int):
    if table_num == 1:
        table = IncCategory
    elif table_num == 2:
        table = ExpCategory
    async with async_session() as session:
        return await session.scalars(select(table))


async def org_data(datas):
    datas = datas.split('\n')

    for data in datas:
        data = data.split(' - ')
        if len(data) > 1:
            data[1] = data[1].strip()
        if len(data) == 2:
            yield data[0], data[1]
        else:
            yield data[0], None


async def get_cat_info(cat_type: int, cat_id: int):
    async with async_session() as session:
        if cat_type == 1:
            table = IncCategory
        else:
            table = ExpCategory
        return await session.scalar(select(table).where(table.id == cat_id))


async def delete_cat(cat_id: int, cat_type: int):
    async with async_session() as session:
        if cat_type == 1:
            table = IncCategory
        else:
            table = ExpCategory
        query = delete(table).where(table.id == cat_id)
        await session.execute(query)
        await session.commit()


async def add_cat(cat_type: int, name: str, plan: int):
    async with async_session() as session:
        if cat_type == 1:
            table = IncCategory
        else:
            table = ExpCategory
        session.add(table(name=name, plan=plan))
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


async def add_note(cat_type: int, cat_id: int, amount: int, description: str):
    async with async_session() as session:
        if cat_type == 1:
            table = Income
        else:
            table = Expense
        session.add(table(category_id=cat_id, amount=amount, description=description))
        await session.commit()


async def get_cat_name(cat_type: int, cat_id: int):
    async with async_session() as session:
        if cat_type == 1:
            table = IncCategory
        else:
            table = ExpCategory
        return await session.scalar(select(table.name).where(table.id == cat_id))