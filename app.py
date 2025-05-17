from flask import Flask, render_template
from datetime import datetime, timedelta

app = Flask(
    __name__,
    static_folder="static",      # default, so you can omit
    template_folder="templates"  # default, so you can omit
)

def get_dashboard_data():
    # User profile data
    user_data = {
        "name": "John Doe",
        "role": "Freelancer",
        "avatar": "images/avatar.jpg"
    }
    
    # Financial summary
    financial_summary = {
        "income": {
            "total": 45680.00,
            "change": 12,
            "trend": "positive"
        },
        "expenses": {
            "total": 12450.00,
            "change": 8,
            "trend": "negative"
        },
        "savings": {
            "total": 33230.00,
            "change": 15,
            "trend": "positive"
        },
        "tax_due": {
            "total": 5325.00,
            "deadline": "2025-04-30"
        }
    }
    
    # Tax deduction opportunities
    tax_deductions = [
        {
            "name": "Equipment & Supplies",
            "icon": "laptop",
            "current_amount": 3200,
            "max_amount": 5000,
            "percentage": 64,
            "impact": "high"
        },
        {
            "name": "Home Office",
            "icon": "home",
            "current_amount": 1800,
            "max_amount": 2000,
            "percentage": 90,
            "impact": "medium"
        },
        {
            "name": "Professional Development",
            "icon": "briefcase",
            "current_amount": 950,
            "max_amount": 3000,
            "percentage": 32,
            "impact": "medium"
        }
    ]
    
    # Recent transactions
    transactions = [
        {
            "type": "income",
            "title": "Website Development",
            "client": "ABC Corp",
            "amount": 5200.00,
            "date": "2025-05-15",
            "icon": "arrow-down"
        },
        {
            "type": "expense",
            "title": "Adobe Creative Cloud",
            "category": "Software",
            "amount": 280.00,
            "date": "2025-05-12",
            "icon": "arrow-up"
        },
        {
            "type": "income",
            "title": "Logo Design Project",
            "client": "XYZ StartUp",
            "amount": 1800.00,
            "date": "2025-05-10",
            "icon": "arrow-down"
        },
        {
            "type": "expense",
            "title": "Office Supplies",
            "category": "Equipment",
            "amount": 150.00,
            "date": "2025-05-08",
            "icon": "arrow-up"
        }
    ]
    
    # Tax reminders
    tax_reminders = [
        {
            "title": "Income Tax Filing Due",
            "deadline": "2025-04-30",
            "days_remaining": 15,
            "icon": "exclamation-circle",
            "urgency": "urgent",
            "action": "Prepare Now"
        },
        {
            "title": "Quarterly Tax Estimate",
            "deadline": "2025-06-30",
            "days_remaining": 45,
            "icon": "file-invoice",
            "urgency": "normal",
            "action": "Review"
        }
    ]
    
    return {
        "user": user_data,
        "financial_summary": financial_summary,
        "tax_deductions": tax_deductions,
        "transactions": transactions,
        "tax_reminders": tax_reminders
    }

def get_expenses_data():
    # User profile data (reused from dashboard)
    user_data = {
        "name": "John Doe",
        "role": "Freelancer",
        "avatar": "images/avatar.jpg"
    }
    
    # Filter options
    filter_options = {
        "categories": [
            {"value": "software", "label": "Software"},
            {"value": "equipment", "label": "Equipment"},
            {"value": "travel", "label": "Travel"},
            {"value": "office", "label": "Office"},
            {"value": "professional", "label": "Professional Services"},
            {"value": "utilities", "label": "Utilities"},
            {"value": "development", "label": "Development"},
            {"value": "design", "label": "Design"},
            {"value": "consulting", "label": "Consulting"}
        ],
        "currencies": [
            {"code": "myr", "label": "MYR"},
            {"code": "usd", "label": "USD"},
            {"code": "eur", "label": "EUR"},
            {"code": "gbp", "label": "GBP"},
            {"code": "sgd", "label": "SGD"}
        ],
        "date_ranges": [
            {"value": "all", "label": "All Time"},
            {"value": "this-month", "label": "This Month"},
            {"value": "last-month", "label": "Last Month"},
            {"value": "this-quarter", "label": "This Quarter"},
            {"value": "last-quarter", "label": "Last Quarter"},
            {"value": "this-year", "label": "This Year"},
            {"value": "last-year", "label": "Last Year"},
            {"value": "custom", "label": "Custom Range"}
        ]
    }
    
    # Summary data for selected period
    summary_data = {
        "income": {
            "total": 45680.00,
            "currency": "MYR",
            "icon": "arrow-down"
        },
        "expenses": {
            "total": 12450.00,
            "currency": "MYR",
            "icon": "arrow-up"
        },
        "tax_deductibles": {
            "total": 8750.00,
            "currency": "MYR",
            "icon": "receipt"
        }
    }
    
    # Transactions data
    transactions = [
        {
            "date": "2025-05-15",
            "description": "Website Development",
            "category": "Development",
            "client_vendor": "ABC Corp",
            "amount": 5200.00,
            "currency": "MYR",
            "type": "income",
            "tax_status": "taxable"
        },
        {
            "date": "2025-05-12",
            "description": "Adobe Creative Cloud",
            "category": "Software",
            "client_vendor": "Adobe Inc",
            "amount": 280.00,
            "currency": "MYR",
            "type": "expense",
            "tax_status": "deductible"
        },
        {
            "date": "2025-05-10",
            "description": "Logo Design Project",
            "category": "Design",
            "client_vendor": "XYZ StartUp",
            "amount": 1800.00,
            "currency": "MYR",
            "type": "income",
            "tax_status": "taxable"
        },
        {
            "date": "2025-05-08",
            "description": "Office Supplies",
            "category": "Equipment",
            "client_vendor": "Office Depot",
            "amount": 150.00,
            "currency": "MYR",
            "type": "expense",
            "tax_status": "deductible"
        },
        {
            "date": "2025-05-05",
            "description": "Business Networking Event",
            "category": "Professional",
            "client_vendor": "KL Tech Conference",
            "amount": 350.00,
            "currency": "MYR",
            "type": "expense",
            "tax_status": "deductible"
        },
        {
            "date": "2025-05-01",
            "description": "UI/UX Consulting",
            "category": "Consulting",
            "client_vendor": "Tech Solutions Inc",
            "amount": 1200.00,
            "currency": "USD",
            "type": "income",
            "tax_status": "taxable"
        },
        {
            "date": "2025-04-28",
            "description": "Web Hosting (Annual)",
            "category": "Utilities",
            "client_vendor": "DigitalOcean",
            "amount": 240.00,
            "currency": "USD",
            "type": "expense",
            "tax_status": "deductible"
        }
    ]
    
    # Pagination data
    pagination = {
        "current_page": 1,
        "total_pages": 10,
        "has_previous": False,
        "has_next": True
    }
    
    return {
        "user": user_data,
        "filter_options": filter_options,
        "summary": summary_data,
        "transactions": transactions,
        "pagination": pagination
    }

# map each page to a route
@app.route("/")
def home():
    dashboard_data = get_dashboard_data()
    return render_template("index.html", **dashboard_data)

@app.route("/expenses")
def expenses():
    expenses_data = get_expenses_data()
    return render_template("expenses.html", **expenses_data)

@app.route("/currencies")
def currencies():
    return render_template("currencies.html")

@app.route("/tax-center")
def tax_center():
    # file is tax-center.html in templates/
    return render_template("tax-center.html")

@app.route("/reports")
def reports():
    return render_template("reports.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")

if __name__ == "__main__":
    # debug=True for live reload during development
    app.run(host="0.0.0.0", port=5000, debug=True)
