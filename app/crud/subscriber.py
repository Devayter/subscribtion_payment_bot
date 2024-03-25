from datetime import datetime

from dateutil.relativedelta import relativedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.subscriber import Subscriber


class CRUDSubscriber():

    def __init__(self, model):
        self.model = model

    async def create(
            self,
            session: AsyncSession,
            id: int,
            name: str,
            subscribtion_period: int
    ):
        subscription = self.model(
            id=id,
            name=name,
            end_date=(
                datetime.now() + relativedelta(months=subscribtion_period)
            )
        )
        session.add(subscription)
        await session.commit()
        await session.refresh(subscription)
        return subscription

    async def get(self, session: AsyncSession, id: int):
        return (
            await session.execute(
                select(self.model).where(self.model.id == id)
            )
        ).scalars().first()

    async def get_expired(self, session: AsyncSession):
        current_time = datetime.now()
        return (
            await session.execute(
                select(self.model).where(self.model.end_date < current_time)
            )
        ).scalars().all()

    async def update(
            self,
            session: AsyncSession,
            subscription: Subscriber,
            subscribtion_period: int
    ):
        subscription.end_date += relativedelta(months=subscribtion_period)
        session.add(subscription)
        await session.commit()
        await session.refresh(subscription)
        return subscription

    async def remove(
            self,
            subscription: Subscriber,
            session: AsyncSession
    ):
        await session.delete(subscription)
        await session.commit()


subscription_crud = CRUDSubscriber(Subscriber)
