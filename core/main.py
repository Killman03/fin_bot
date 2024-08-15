import os
import asyncio
import logging
import sys

from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties

from core.database.engine import create_db, drop_db
from core.handlers.basic import *
from core.handlers.commands import set_commands
from core.handlers import router as main_router

from dotenv import load_dotenv


async def on_startup(bot: Bot):
    await set_commands(bot)
    # await drop_db()
    await create_db()
    await bot.send_message(os.getenv('ADMIN_ID'), text='Bot is running')


async def on_shutdown(bot: Bot):
    await bot.send_message(os.getenv('ADMIN_ID'), text='Bot shut down')


async def start():
    load_dotenv()

    bot = Bot(
        token=os.getenv("BOT_TOKEN"),
        default=DefaultBotProperties(parse_mode="HTML"),
    )
    dp = Dispatcher()

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.include_router(main_router)
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.ERROR, stream=sys.stdout)
        asyncio.run(start())
    except KeyboardInterrupt:
        print('Bot stopped')
