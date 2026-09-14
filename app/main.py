from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.api.expenses import router as expenses_router


app = FastAPI(
    title="AI Expense Analyzer API",
    description=(
        "AI-powered expense tracking backend built with "
        "Python, FastAPI, PostgreSQL and Gemini."
    ),
    version="1.0.0",
)


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Expense Analyzer</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                background: #f5f7fb;
                color: #1f2937;
            }

            .container {
                max-width: 950px;
                margin: auto;
                padding: 50px 24px;
            }

            .hero {
                text-align: center;
                margin-bottom: 45px;
            }

            .hero h1 {
                font-size: 42px;
                margin-bottom: 12px;
            }

            .hero p {
                font-size: 18px;
                color: #6b7280;
            }

            .card {
                background: white;
                border-radius: 14px;
                padding: 28px;
                margin-bottom: 24px;
                box-shadow: 0 4px 18px rgba(0, 0, 0, 0.06);
            }

            .card h2 {
                margin-top: 0;
            }

            .flow {
                display: flex;
                flex-wrap: wrap;
                align-items: center;
                justify-content: center;
                gap: 10px;
                margin-top: 20px;
            }

            .step {
                background: #eef2ff;
                padding: 14px 18px;
                border-radius: 10px;
                font-weight: bold;
                text-align: center;
            }

            .arrow {
                font-size: 22px;
                color: #6b7280;
            }

            .transaction {
                background: #f9fafb;
                border: 1px solid #e5e7eb;
                border-radius: 10px;
                padding: 20px;
            }

            .transaction-row {
                display: flex;
                justify-content: space-between;
                padding: 8px 0;
                border-bottom: 1px solid #e5e7eb;
            }

            .transaction-row:last-child {
                border-bottom: none;
            }

            .label {
                color: #6b7280;
            }

            .value {
                font-weight: bold;
            }

            .buttons {
                display: flex;
                flex-wrap: wrap;
                gap: 12px;
                margin-top: 20px;
            }

            .button {
                display: inline-block;
                padding: 12px 18px;
                border-radius: 8px;
                text-decoration: none;
                font-weight: bold;
                background: #111827;
                color: white;
            }

            .button.secondary {
                background: #e5e7eb;
                color: #111827;
            }

            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 14px;
                margin-top: 20px;
            }

            .feature {
                background: #f9fafb;
                padding: 16px;
                border-radius: 10px;
            }

            .footer {
                text-align: center;
                color: #6b7280;
                margin-top: 40px;
                font-size: 14px;
            }
        </style>
    </head>

    <body>
        <div class="container">

            <div class="hero">
                <h1>💰 AI Expense Analyzer</h1>

                <p>
                    Smart expense tracking powered by Python, FastAPI,
                    PostgreSQL and AI.
                </p>
            </div>


            <div class="card">
                <h2>How It Works</h2>

                <div class="flow">
                    <div class="step">
                        📱 Payment Notification
                    </div>

                    <div class="arrow">→</div>

                    <div class="step">
                        🐍 FastAPI
                    </div>

                    <div class="arrow">→</div>

                    <div class="step">
                        🧠 Categorization
                    </div>

                    <div class="arrow">→</div>

                    <div class="step">
                        🗄️ PostgreSQL
                    </div>
                </div>

                <p style="margin-top: 25px;">
                    The Android application detects supported payment
                    notifications and sends transaction data to this
                    backend. The backend normalizes the merchant,
                    checks known rules and user preferences, and uses
                    AI as a fallback for unknown transactions.
                </p>
            </div>


            <div class="card">
                <h2>Sample Transaction</h2>

                <div class="transaction">

                    <div class="transaction-row">
                        <span class="label">Notification</span>
                        <span class="value">
                            ₹1,250 paid to ABC Lifestyle Store
                        </span>
                    </div>

                    <div class="transaction-row">
                        <span class="label">Amount</span>
                        <span class="value">₹1,250</span>
                    </div>

                    <div class="transaction-row">
                        <span class="label">Merchant</span>
                        <span class="value">
                            ABC Lifestyle Store
                        </span>
                    </div>

                    <div class="transaction-row">
                        <span class="label">Category</span>
                        <span class="value">Shopping</span>
                    </div>

                    <div class="transaction-row">
                        <span class="label">Categorization</span>
                        <span class="value">AI</span>
                    </div>

                    <div class="transaction-row">
                        <span class="label">Confidence</span>
                        <span class="value">95%</span>
                    </div>

                    <div class="transaction-row">
                        <span class="label">Status</span>
                        <span class="value">Completed</span>
                    </div>

                </div>
            </div>


            <div class="card">
                <h2>Key Features</h2>

                <div class="features">

                    <div class="feature">
                        📱 Android notification-based
                        transaction capture
                    </div>

                    <div class="feature">
                        🐍 Python + FastAPI REST API
                    </div>

                    <div class="feature">
                        🤖 Gemini AI categorization
                    </div>

                    <div class="feature">
                        🧠 Merchant preference learning
                    </div>

                    <div class="feature">
                        🔄 Duplicate transaction detection
                    </div>

                    <div class="feature">
                        🗄️ PostgreSQL persistence
                    </div>

                    <div class="feature">
                        📊 Transaction tracking
                    </div>

                    <div class="feature">
                        ☁️ Cloud deployed backend
                    </div>

                </div>
            </div>


            <div class="card">
                <h2>Developer API</h2>

                <p>
                    This project exposes REST APIs for transaction
                    ingestion, retrieval, categorization and deletion.
                </p>

                <div class="buttons">

                    <a
                        class="button"
                        href="/docs"
                    >
                        Open API Documentation
                    </a>

                    <a
                        class="button secondary"
                        href="/health"
                    >
                        Check API Health
                    </a>

                </div>
            </div>


            <div class="footer">
                AI Expense Analyzer · Python · FastAPI · PostgreSQL · Gemini
            </div>

        </div>
    </body>
    </html>
    """


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AI Expense Analyzer API",
    }


app.include_router(
    expenses_router,
    prefix="/expenses",
)
