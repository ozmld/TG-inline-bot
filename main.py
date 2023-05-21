from create_bot import dp
from database import sqlite_db
from aiogram.utils import executor
from handlers import admin, general
import asyncio

async def on_startup(_):
    print("Online")
    sqlite_db.sql_start()
    asyncio.create_task(general.scheduler())



admin.register_handlers_admin(dp)
general.register_handlers_general(dp)

try:
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
except:
    print("bad internet")