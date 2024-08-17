import os
from datetime import datetime
import pprint

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from aiogram import Router, Bot, F

from utils.scan import scan_qr_code, process_receipt, TEST_DATA
from database.requests import add_note, check_description_exists
from keyboards.keyboards import get_scan_kb, get_start_kb

scan_router = Router()


class ScanState(StatesGroup):
    wait_category = State()


@scan_router.message(F.photo)
async def handle_receipt(message: Message, bot: Bot, state: FSMContext):
    try:
        photo_id = message.photo[-1].file_id
        photo = await bot.get_file(photo_id)
        photo_path = photo.file_path
        await bot.download_file(photo_path, 'photos/check.jpg')

        qr_text = scan_qr_code('photos/check.jpg')
        if qr_text is None:
            await message.reply("Не могу прочитать qr код на чеке😕\n Попробуй ещё раз.")
            os.remove('photos/check.jpg')
            return

        products = await process_receipt(qr_text)
        #products = TEST_DATA
        os.remove('photos/check.jpg')
        qr_time = qr_text.split('=')[1]
        dt = datetime.strptime(qr_time[:-2], "%Y%m%dT%H%M")
        count = 1
        await state.update_data(products=products, datetime=dt)

        for item in products['data']['json']['items']:
            kbrd = await get_scan_kb()
            price = str(item['sum'] / 100)
            name = item['name']

            cat_id = await check_description_exists(name)

            if cat_id is not False:
                await add_note(cat_type=2, cat_id=int(cat_id), amount=price, description=name,
                               created=dt)
                count += 1
                continue

            else:
                await message.answer(text=f'К какой категории привязать "{name}" с стоимостью {price}?',
                                     reply_markup=kbrd)
                await state.update_data(amount=price, name=name, count=count, datatime=dt)
                await state.set_state(ScanState.wait_category)
                break


    except Exception as e:
        print(f"Error: {e}")


@scan_router.message(ScanState.wait_category)
@scan_router.callback_query(F.data.startswith('qr_'))
async def add_qr_callback(callback_query: CallbackQuery, state: FSMContext):
    cat_id = callback_query.data.split('_')[-1]

    data = await state.get_data()

    await add_note(cat_type=2, cat_id=int(cat_id), amount=data['amount'], description=data['name'],
                   created=data['datatime'])
    count = data['count']
    dt = data['datatime']
    products = data['products']
    prod_list = products['data']['json']['items']
    try:
        for _ in range(len(list(prod_list))):
            if count != len(list(prod_list))-1:
                d = prod_list[count]
                price = d['sum'] / 100
                name = d['name']
                category_id = await check_description_exists(name)

                if category_id is not False:
                    await add_note(cat_type=2, cat_id=int(category_id), amount=price, description=name,
                                   created=dt)
                    count += 1
                    continue

                else:
                    count += 1
                    kbrd = await get_scan_kb()
                    await state.update_data(count=count, amount=price, name=name)
                    await callback_query.bot.edit_message_text(chat_id=callback_query.from_user.id,
                                                message_id=callback_query.message.message_id,
                                                text=f'К какой категории привязать "{name}" стоимостью {price}?',
                                                reply_markup=kbrd)
                    await state.set_state(ScanState.wait_category)
                    break

            elif count == len(list(prod_list)):
                kbrd = await get_start_kb()

                text = f'Привет, {callback_query.from_user.first_name}! 👋 Для того, чтобы добавить источник доходов или расходов, ' \
                       f'перейди в настройки ⚙️. Давай вместе придем к финансовой независимости! 💰💼'

                await callback_query.bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, text=text, reply_markup=kbrd)
                await state.clear()

    except Exception as e:
        print(e)
