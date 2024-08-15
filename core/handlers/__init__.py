# Define the list of imported modules
__all__ = ['router']

# Import the necessary modules
from aiogram import Router

# Import handlers from different modules
from core.handlers import (
    basic,
    categories_hd,
    start_hd,
    add_hd,
    scan_hd,
    report_hd
)

# Create a new router instance
router = Router()

# Include routers from different handlers
router.include_router(scan_hd.scan_router)
router.include_router(basic.my_router)
router.include_router(categories_hd.cat_router)
router.include_router(start_hd.start_router)
router.include_router(add_hd.add_router)
router.include_router(report_hd.report_router)