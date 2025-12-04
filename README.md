# Expense Tracker

A FastAPI sample application for recording expenses, creating user budgets, generating monthly reports, and emailing alerts when spending approaches category limits. The project ships with a lightweight SQLite database for local development plus Docker support for reproducible deployments.

## Features

- User management with a minimal HTML form
- Expense entry form backed by server-side validation and database persistence
- Monthly comparison report that contrasts category budgets vs. spending
- Threshold-based alert engine that can email users when a category nears its limit
- Simple Jinja2-powered UI so everything can be exercised from a browser

## Tech Stack

- FastAPI + Uvicorn
- SQLAlchemy ORM with SQLite (default) or any SQL database via `DATABASE_URL`
- Jinja2 templates for server-rendered pages
- Docker / docker-compose for containerized development

## Project Structure

```
expense-tracker/
│── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── crud.py
│   ├── schemas.py
│   ├── utils/
│   │   ├── calculator.py
│   │   └── emailer.py
│   ├── routes/
│   │   ├── users.py
│   │   ├── expenses.py
│   │   ├── budgets.py
│   │   ├── reports.py
│   │   └── alerts.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── create_user.html
│   │   ├── add_expense.html
│   │   └── monthly_report.html
│── Dockerfile
│── docker-compose.yml
│── README.md
│── requirements.txt

```

## Getting Started

### 1. Prerequisites

- Python 3.10+
- pip / virtualenv (or uv)
- Optional: Docker Desktop if you prefer containers

### 2. Local Environment Setup

```powershell
cd expense-tracker
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the API

```powershell
uvicorn app.main:app --reload 
```

Visit `http://localhost:8000` for the HTML UI or `http://localhost:8000/docs` for the swagger documentation.

## Core Workflows(for swagger documentation)

- **Create a user:** Navigate to `/users/create` and submit the form.
- **Set a budget:** POST to `/budgets/set` (via HTML form or an API client) to define category limits per month.
- **Add an expense:** Use `/expenses/add` to record spending apportioned to a user and category.
- **View monthly report:** Visit `/reports/monthly?user_id=<id>&month=<YYYY-MM>` to compare budgets vs. spending.
- **Trigger alerts manually:** POST `/alerts/run/{user_id}/{month}` to send warning emails when remaining budget percentage falls below the configured threshold (default 10%).
