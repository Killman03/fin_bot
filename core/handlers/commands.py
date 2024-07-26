from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начало работы'
        ),
        BotCommand(
            command='help',
            description='Помощь'
        ),
        BotCommand(
            command='export',
            description='Экспорт данных в xlsx'
        ),
        BotCommand(
            command='setup',
            description='Настройка категорий доходов и расходов'
        ),
        BotCommand(
            command='report',
            description='Отчет по данным'
        ),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())

