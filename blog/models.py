from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, DateTime, ForeignKey
from datetime import datetime
from core.database import Base
from authentication.models import User


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(Text(), nullable=False)
    author: Mapped[str] = mapped_column(ForeignKey("users.id"))
    at: Mapped[str] = mapped_column(DateTime(), default=datetime.utcnow)

    author_relationship: Mapped["User"] = relationship(back_populates="articles")


class Subscriber(Base):
    __tablename__ = "subscribers"

    id: Mapped[str] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
