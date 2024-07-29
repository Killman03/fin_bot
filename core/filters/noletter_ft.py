from aiogram.filters import BaseFilter
from aiogram.types import Message
import re


class NoLettersFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return not bool(re.search(r'[a-zA-Zа-яА-Я]', message.text))