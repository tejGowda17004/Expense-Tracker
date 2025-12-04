from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


class UserCreate(BaseModel):
    name: str
    email: EmailStr


class ExpenseCreate(BaseModel):
    date: date
    amount: float
    category: str
    description: Optional[str] = None
    user_id: int


class BudgetCreate(BaseModel):
    month: str
    category: str
    limit: float
    user_id: int


class ReportRequest(BaseModel):
    month: str # YYYY-MM
    user_id: int