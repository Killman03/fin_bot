# from aiogram import BaseMiddleware
# from aiogram.types import TelegramObject
# from typing import Any, Awaitable, Callable, Dict
# from database.models import FinBD
# import asyncpg
#
#
# class UserDataMiddleware(BaseMiddleware):
#     def __init__(self, connector: asyncpg.pool.Pool):
#         super().__init__()
#         self.connector = connector
#
#     async def __call__(
#             self,
#             handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
#             event: TelegramObject,
#             data: Dict[str, Any],
#     ) -> Any:
#         async with self.connector.acquire() as conn:
#             data["request"] = FinBD(conn)
#             return await handler(event, data)
