from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    expenses = relationship("Expense", back_populates="user")
    budgets = relationship("Budget", back_populates="user")


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="expenses")


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    month = Column(String, nullable=False)  # YYYY-MM
    category = Column(String, nullable=False)
    limit = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="budgets")


class AlertLog(Base):
    __tablename__ = "alert_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    budget_id = Column(Integer, nullable=True)
    triggered_at = Column(Date, nullable=False)
    alert_type = Column(String, nullable=False)
    delivered = Column(Boolean, default=False)