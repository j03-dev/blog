from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import String, Text, DateTime, ForeignKey

from typing import List

from datetime import datetime


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    articles: Mapped[List["Article"]] = relationship(
        back_populates="author_relationship"
    )
    images: Mapped[List["Image"]] = relationship(back_populates="owner_relationship")


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(ForeignKey("users.id"))
    at: Mapped[str] = mapped_column(DateTime, default=datetime.utcnow)

    author_relationship: Mapped["User"] = relationship(back_populates="articles")
    images: Mapped[List["Image"]] = relationship(back_populates="article")


class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    path: Mapped[str] = mapped_column(String)
    owner: Mapped[str] = mapped_column(ForeignKey("users.id"))
    article_id: Mapped[int] = mapped_column(ForeignKey("articles.id"))

    owner_relationship: Mapped["User"] = relationship(back_populates="images")
    article: Mapped["Article"] = relationship(back_populates="images")
