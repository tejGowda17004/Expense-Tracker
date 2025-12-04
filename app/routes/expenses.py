from datetime import datetime

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.routes import crud


router = APIRouter(prefix="/expenses")
templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/add", response_class=HTMLResponse)
async def add_expense_form(request: Request):
    return templates.TemplateResponse("add_expense.html", {"request": request})


@router.post("/add")
async def add_expense(
    date: str = Form(...),
    amount: float = Form(...),
    category: str = Form(...),
    description: str = Form(None),
    user_id: int = Form(...),
    db: Session = Depends(get_db),
):
    expense_payload = {
        "date": datetime.strptime(date, "%Y-%m-%d").date(),
        "amount": amount,
        "category": category,
        "description": description,
        "user_id": user_id,
    }
    crud.create_expense(db, expense_payload)
    redirect_url = f"/reports/monthly?user_id={user_id}&month={date[:7]}"
    return RedirectResponse(url=redirect_url, status_code=303)
