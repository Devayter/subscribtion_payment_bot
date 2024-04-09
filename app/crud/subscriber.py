from datetime import datetime

from dateutil.relativedelta import relativedelta
from sqlalchemy import and_, select
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
        subscribtion = self.model(
            id=id,
            name=name,
            end_date=(
                datetime.now() + relativedelta(months=subscribtion_period)
            )
        )
        session.add(subscribtion)
        await session.commit()
        await session.refresh(subscribtion)
        return subscribtion

    async def get(self, session: AsyncSession, id: int):
        return (
            await session.execute(
                select(self.model).where(self.model.id == id)
            )
        ).scalars().first()

    async def get_almost_expired(self, session: AsyncSession):
        current_time = datetime.now()
        day_of_expire = current_time + relativedelta(days=3)
        return (
            await session.execute(
                select(self.model).where(
                    and_(
                        self.model.end_date > current_time,
                        self.model.end_date <= day_of_expire
                    )
                )
            )
        )

    async def get_expired(self, session: AsyncSession):
        current_time = datetime.now()
        return (
            await session.execute(
                select(self.model).where(

                    self.model.end_date < current_time
                )
            )
        ).scalars().all()

    async def update(
            self,
            session: AsyncSession,
            subscribtion: Subscriber,
            subscribtion_period: int
    ):
        subscribtion.end_date += relativedelta(months=subscribtion_period)
        session.add(subscribtion)
        await session.commit()
        await session.refresh(subscribtion)
        return subscribtion

    async def remove(
            self,
            subscribtion: Subscriber,
            session: AsyncSession
    ):
        await session.delete(subscribtion)
        await session.commit()


subscribtion_crud = CRUDSubscriber(Subscriber)
