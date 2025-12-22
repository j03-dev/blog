from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Text, DateTime, ForeignKey
from datetime import datetime
from typing import List


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    articles: Mapped[List["Article"]] = relationship(
        back_populates="author_relationship"
    )


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(Text(), nullable=False)
    author: Mapped[str] = mapped_column(ForeignKey("users.id"))
    at: Mapped[str] = mapped_column(DateTime(), default=datetime.utcnow)

    author_relationship: Mapped["User"] = relationship(
        back_populates="articles",
    )


class Subscriber(Base):
    __tablename__ = "subscribers"

    id: Mapped[str] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
