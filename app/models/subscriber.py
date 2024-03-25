from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base


class Subscriber(Base):
    name: Mapped[str]
    start_date: Mapped[datetime] = mapped_column(
        default=datetime.now,
        onupdate=datetime.now
    )
    end_date: Mapped[datetime]
