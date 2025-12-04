from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .database import Base, engine
from .routes import alerts, budgets, expenses, reports, users


templates = Jinja2Templates(directory="app/templates")
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker App")

for router in (expenses.router, budgets.router, reports.router, alerts.router, users.router):
    app.include_router(router)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
