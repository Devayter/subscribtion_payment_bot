from apscheduler.schedulers.asyncio import AsyncIOScheduler

from crud.subscriber import subscription_crud


scheduler = AsyncIOScheduler()


async def check_almost_expired_subscriptions(bot, async_session):
    async with async_session() as session:
        expired_subscriptions = (
            await subscription_crud.get_almost_expired(session)
        )
        for subscription in expired_subscriptions:
            await bot.send_message(
                chat_id=subscription.id,
                text='Ваша подписка заканчивается через 3 дня'
            )


async def check_expired_subscriptions(bot, async_session):
    async with async_session() as session:
        expired_subscriptions = await subscription_crud.get_expired(session)
        for subscription in expired_subscriptions:
            await subscription_crud.remove(subscription, session)
            await bot.send_message(
                chat_id=subscription.id,
                text='Ваша подписка закончилась'
            )


def set_schedule_jobs(bot, session):
    scheduler.add_job(
        check_subscriptions,
        'interval',
        hours=24,
        args=(bot, session)
    )


async def check_subscriptions(bot, session):
    await check_almost_expired_subscriptions(bot, session)
    await check_expired_subscriptions(bot, session)
