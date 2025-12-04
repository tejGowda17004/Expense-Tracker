from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.routes import crud
from app.utils.calculator import compare_spending_vs_budget


router = APIRouter(prefix="/reports")
templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/report-form")
def report_form(request: Request):
    return templates.TemplateResponse("report_filter.html", {"request": request})


@router.get("/monthly")
async def monthly_report(request: Request, user_id: int, month: str, db: Session = Depends(get_db)):
    spent_rows = crud.sum_spent_by_category(db, user_id, month)
    budgets = (
        db.query(crud.models.Budget)
        .filter_by(user_id=user_id, month=month)
        .all()
    )
    budget_list = [{"category": b.category, "limit": b.limit} for b in budgets]
    spend_list = [{"category": row[0], "spent": float(row[1])} for row in spent_rows]
    comparison = compare_spending_vs_budget(budget_list, spend_list)
    context = {
        "request": request,
        "comparison": comparison,
        "month": month,
    }
    return templates.TemplateResponse("monthly_report.html", context)
