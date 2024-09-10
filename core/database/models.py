from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import mapped_column, Mapped, relationship, DeclarativeBase
from sqlalchemy import ForeignKey, Integer, String, BigInteger, DateTime, func, Numeric


class Base(AsyncAttrs, DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, unique=True)
    user_name: Mapped[str] = mapped_column(String(30), nullable=True)

    inc_categories = relationship("IncCategory", back_populates="user")
    exp_categories = relationship("ExpCategory", back_populates="user")


class IncCategory(Base):
    __tablename__ = "inc_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    plan: Mapped[int] = mapped_column(Numeric, nullable=True)
    user_id = mapped_column(BigInteger, ForeignKey('users.tg_id', ondelete='CASCADE'), nullable=False)

    user = relationship("User", back_populates="inc_categories")
    incomes = relationship("Income", back_populates="inc_category")


class ExpCategory(Base):
    __tablename__ = "exp_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    plan: Mapped[int] = mapped_column(Numeric, nullable=True)
    user_id = mapped_column(BigInteger, ForeignKey('users.tg_id', ondelete='CASCADE'), nullable=False)

    user = relationship("User", back_populates="exp_categories")
    expenses = relationship("Expense", back_populates="exp_category")


class Income(Base):
    __tablename__ = "incomes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    amount: Mapped[str] = mapped_column(String(10))
    description: Mapped[int] = mapped_column(String(255), nullable=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('inc_categories.id', ondelete='CASCADE'))

    inc_category: Mapped['IncCategory'] = relationship('IncCategory', back_populates='incomes'
                                                                                     '')

class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    amount: Mapped[str] = mapped_column(String(10))
    description: Mapped[int] = mapped_column(String(255), nullable=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('exp_categories.id', ondelete='CASCADE'))

    exp_category: Mapped['ExpCategory'] = relationship('ExpCategory', back_populates='expenses')
