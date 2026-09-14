from fastapi import FastAPI,Depends
from app.db.database import Base, engine
from app.models.transaction import Transaction
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.database import get_db


from app.api.expenses import router as expenses_router

from app.models.merchant_preference import MerchantPreference

app = FastAPI(
    title="AI Expense Analyzer",
    version="0.1.0",
    description="AI-powered expense management API",
)


app.include_router(expenses_router)


@app.get("/")
async def root():
    return {
        "message": "AI Expense Analyzer API is running"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }

@app.get("/db-health")
def database_health_check(
    db: Session = Depends(get_db),
):
    result = db.execute(text("SELECT 1"))

    return {
        "database": "connected",
        "result": result.scalar(),
    }