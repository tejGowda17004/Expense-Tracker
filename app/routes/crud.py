from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models


def create_user(db: Session, name: str, email: str):
    user = models.User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_expense(db: Session, expense_data):
    expense = models.Expense(**expense_data)
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


def get_expenses_by_month_and_user(db: Session, user_id: int, month: str):
    month_expr = func.strftime('%Y-%m', models.Expense.date)
    return (
        db.query(models.Expense)
        .filter(models.Expense.user_id == user_id)
        .filter(month_expr == month)
        .all()
    )


def set_budget(db: Session, budget_data):
    budget = models.Budget(**budget_data)
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget


def get_budget(db: Session, user_id: int, month: str, category: str):
    return (
        db.query(models.Budget)
        .filter_by(user_id=user_id, month=month, category=category)
        .first()
    )


def sum_spent_by_category(db: Session, user_id: int, month: str):
    month_expr = func.strftime('%Y-%m', models.Expense.date)
    return (
        db.query(
            models.Expense.category,
            func.sum(models.Expense.amount).label('spent'),
        )
        .filter(models.Expense.user_id == user_id)
        .filter(month_expr == month)
        .group_by(models.Expense.category)
        .all()
    )

def create_or_update_budget(db, user_id, month, category, limit):
    existing = db.query(models.Budget).filter_by(
        user_id=user_id, month=month, category=category
    ).first()
    
    if existing:
        existing.limit = limit
    else:
        new_budget = models.Budget(
            user_id=user_id, month=month, category=category, limit=limit
        )
        db.add(new_budget)

    db.commit()
