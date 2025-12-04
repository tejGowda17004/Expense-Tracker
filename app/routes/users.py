from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.routes import crud


router = APIRouter(prefix="/users")
templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/create")
def create_user_form(request: Request):
    return templates.TemplateResponse("create_user.html", {"request": request})


@router.post("/create")
def create_user(
    name: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db),
):
    crud.create_user(db, name, email)
    return RedirectResponse(url="/", status_code=303)
