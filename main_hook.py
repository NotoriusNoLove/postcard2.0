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
from aiohttp.web import run_app
from aiohttp.web_app import Application
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application


async def main():
    create_table()
    insert_users()
    register_handlers()
    dp.include_router(form_router)
    dp.shutdown.register(on_shutdown)
    dp.startup.register(on_startup)
    # dp.startup.register(send_postcard)
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(
        start_postcards, trigger='cron', hour=10, minute=0, start_date=datetime.now()
    )
    scheduler.start()

    dp['base_url'] = "notmeowmeow.ru"

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


async def on_startup():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(f'notmeowmeow.ru/bot/postcard2.0', drop_pending_updates=True)


async def on_shutdown():
    await bot.delete_webhook(drop_pending_updates=True)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')
