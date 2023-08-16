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


def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    create_table()
    insert_users()
    register_handlers()
    dp.include_router(form_router)
    # dp.startup.register(send_postcard)
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(
        start_postcards, trigger='cron', hour=10, minute=0, start_date=datetime.now()
    )
    scheduler.start()

    dp['base_url'] = "notmeowmeow.ru"
    app = Application()
    app["bot"] = bot

    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    ).register(app, path="/bot/postcards")
    setup_application(app, dp, bot=bot)

    run_app(app, host="127.0.0.1", port=8003)


async def on_startup():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(f'notmeowmeow.ru/bot/postcard2.0', drop_pending_updates=True)


async def on_shutdown():
    await bot.delete_webhook(drop_pending_updates=True)

if __name__ == '__main__':
    main()
