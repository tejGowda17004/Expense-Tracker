from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.routes import crud
from app.utils.calculator import compare_spending_vs_budget
from app.utils.emailer import send_email

router = APIRouter(prefix="/alerts")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def evaluate_and_send(db: Session, user_id: int, month: str, threshold: float = 0.1):
    spent_rows = crud.sum_spent_by_category(db, user_id, month)
    budget_rows = (
        db.query(crud.models.Budget)
        .filter_by(user_id=user_id, month=month)
        .all()
    )

    budgets = [{"category": b.category, "limit": b.limit} for b in budget_rows]
    spending = [{"category": row[0], "spent": float(row[1])} for row in spent_rows]
    comparison = compare_spending_vs_budget(budgets, spending)

    user = db.query(crud.models.User).filter_by(id=user_id).first()
    if not user:
        return {"error": f"User with id {user_id} does not exist"}

    for category_summary in comparison:
        pct_left = category_summary.get("pct_left")
        if pct_left is None or pct_left > threshold:
            continue

        subject = f"Budget Alert: {category_summary['category']} — {month}"
        body = (
            f"Hello {user.name},\n\n"
            f"You have only {category_summary['remaining']:.2f} remaining "
            f"for category '{category_summary['category']}'.\n"
            f"Date: {date.today().isoformat()}"
        )
        try:
            await send_email(user.email, subject, body)
        except Exception as exc:
            print("Email send failed:", exc)

    return comparison


@router.post("/run/{user_id}/{month}")
async def run_alerts(user_id: int, month: str, db: Session = Depends(get_db)):
    """Trigger budget alerts manually."""
    result = await evaluate_and_send(db, user_id, month)
    return {
        "status": "ok",
        "evaluated_categories": len(result),
        "details": result,
    }
