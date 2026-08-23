from fastapi import FastAPI

app = FastAPI(
    title="AI Expense Analyzer",
    version="0.1.0",
    description="AI-powered expense management API",
)


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