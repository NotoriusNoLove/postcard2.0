import asyncio
from bot.dispatcher import *
from bot.tasks import start_postcards, send_postcard
from config import *
from database import *
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database.users import *
from bot.handler import register_handlers
from bot.callback import form_router
from datetime import datetime


async def main():
    create_table()
    insert_users()
    register_handlers()
    dp.include_router(form_router)
    dp.startup.register(send_postcard)
    # scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    # scheduler.add_job(
    #     start_postcards, trigger='cron', hour=1, minute=13, start_date=datetime.now()
    # )
    # scheduler.start()
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')
