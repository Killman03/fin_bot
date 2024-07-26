__all__ = ['router']

from aiogram import Router

from core.handlers.basic import my_router
from core.handlers.categories_hd import cat_router
from core.handlers.start_hd import start_router
from core.handlers.add_hd import add_router

router = Router()

router.include_router(my_router)
router.include_router(cat_router)
router.include_router(start_router)
router.include_router(add_router)