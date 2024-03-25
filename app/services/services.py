from apscheduler.schedulers.asyncio import AsyncIOScheduler

from crud.subscriber import subscription_crud


scheduler = AsyncIOScheduler()


async def check_expired_subscriptions(bot, async_session):
    async with async_session() as session:
        expired_subscriptions = await subscription_crud.get_expired(session)
        for subscription in expired_subscriptions:
            await subscription_crud.remove(subscription, session)
            await bot.send_message(
                chat_id=subscription.id,
                text='конец подписки'
            )


def set_schedule_jobs(bot, session):
    scheduler.add_job(
        check_expired_subscriptions,
        'interval',
        seconds=5,
        args=(bot, session)
    )
