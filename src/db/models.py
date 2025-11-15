from sqlalchemy import BigInteger, String, Date, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from src.db.database import Base

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    username: Mapped[str] = mapped_column(String(32), unique=True, nullable=True)
    full_name: Mapped[str] = mapped_column(String(128))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    events: Mapped[list["Event"]] = relationship(back_populates="user")
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

class Event(Base):
    __tablename__ = 'events'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(255))
    event_date: Mapped[datetime] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    user: Mapped["User"] = relationship(back_populates="events")
    def __repr__(self):
        return f"<Event(id={self.id}, name='{self.name}', user_id={self.user_id})>"
