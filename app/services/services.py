from apscheduler.schedulers.asyncio import AsyncIOScheduler

from crud.subscriber import subscribtion_crud


scheduler = AsyncIOScheduler()


async def check_almost_expired_subscribtions(bot, async_session):
    async with async_session() as session:
        expired_subscribtions = (
            await subscribtion_crud.get_almost_expired(session)
        )
        for subscribtion in expired_subscribtions:
            await bot.send_message(
                chat_id=subscribtion.id,
                text='Ваша подписка заканчивается через 3 дня'
            )


async def check_expired_subscribtions(bot, async_session):
    async with async_session() as session:
        expired_subscribtions = await subscribtion_crud.get_expired(session)
        for subscribtion in expired_subscribtions:
            await subscribtion_crud.remove(subscribtion, session)
            await bot.ban_chat_member(
                chat_id=-1002143176488,
                user_id=subscribtion.id
            )
            await bot.unban_chat_member(
                chat_id=-1002143176488,
                user_id=subscribtion.id
            )
            await bot.send_message(
                chat_id=subscribtion.id,
                text='Ваша подписка закончилась'
            )


def set_schedule_jobs(bot, session):
    scheduler.add_job(
        check_subscribtions,
        'interval',
        hours=24,
        args=(bot, session)
    )


async def check_subscribtions(bot, session):
    await check_almost_expired_subscribtions(bot, session)
    await check_expired_subscribtions(bot, session)
