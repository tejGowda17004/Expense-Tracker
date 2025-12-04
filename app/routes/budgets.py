from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from ..database import SessionLocal
from app.routes import crud

router = APIRouter(prefix="/budgets")
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Show Set Budget Form
@router.get("/set-budget")
def set_budget_form(request: Request):
    return templates.TemplateResponse("set_budget.html", {"request": request})

# Handle Set Budget POST
@router.post("/set-budget")
def set_budget(
    month: str = Form(...),
    category: str = Form(...),
    limit: float = Form(...),
    user_id: int = Form(...),
    db: Session = Depends(get_db)
):
    crud.create_or_update_budget(db, user_id, month, category, limit)
    return RedirectResponse(url="/", status_code=303)
