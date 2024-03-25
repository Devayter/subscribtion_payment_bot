import asyncio
import logging

# from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher
from core.config import settings
from core.db import create_db, async_session
from middlewares.middleware import DataBaseSession
from handlers import user_handler, other_handler
from logs.logger import configure_logging

from services.services import set_schedule_jobs, scheduler


async def main():
    configure_logging('sub_payment_bot')
    logging.info('Старт бота')

    bot = Bot(token=settings.bot_token, parse_mode='HTML')
    dp = Dispatcher()
    dp.update.middleware(DataBaseSession(async_session=async_session))
    dp.include_router(user_handler.router)
    dp.include_router(other_handler.router)

    # scheduler = AsyncIOScheduler()
    set_schedule_jobs(bot, async_session)
    scheduler.start()

    await create_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error('Ошибка запуска бота')
