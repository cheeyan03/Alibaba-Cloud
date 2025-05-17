from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from oss_manage_file import upload_to_oss  # function to upload to OSS
from llm import parse_receipt_with_qwen  # function to parse receipt with Qwen
from connect_db import list_transactions, list_categories, insert_transaction, delete_transaction

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

def get_expenses_data(filters=None):
    if filters is None:
        filters = {}

    # Fetch from database
    categories = list_categories()  # Assume this returns list of strings like ['Software', 'Office']
    category_lookup = {c["id"]: c["name"] for c in categories if "id" in c and "name" in c}

    # User profile data (reused from dashboard)
    user_data = {
        "name": "John Doe",
        "role": "Freelancer",
        "avatar": "images/avatar.jpg"
    }
    
    # Filter options
    filter_options = {
        "categories" : [
            {"value": c["name"].lower(), "label": c["name"]}
            for c in sorted(categories, key=lambda x: x["name"])
            if c.get("type") == "Expense"
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

    # Fetch from database
    db_rows = list_transactions()

    # Convert to unified format
    all_transactions = []
    currencies_seen = set()

    for row in db_rows:
        all_transactions.append({
            "id": row["id"],
            "date": row["date"].strftime("%Y-%m-%d"),
            "description": row["description"],
            "category": category_lookup.get(row.get("category_id"), ""),   # assumed join with category
            "client_vendor": row["client_vendor"],
            "amount": float(row["amount"]),
            "currency": row["currency"],
            "type": row["transaction_type"].lower(),
            "tax_status": "",
            "receipt_url": row["receipt_url"],
            # "tax_status": row.get("tax_status", "non-taxable")  # fallback
        })
        currencies_seen.add(row["currency"])

    # Apply filters
    filtered_transactions = all_transactions.copy()
    
    if filters:
        # Filter by search term
        if filters.get('search'):
            search_term = filters['search'].lower()
            filtered_transactions = [
                t for t in filtered_transactions
                if search_term in t['description'].lower() or 
                   search_term in t['client_vendor'].lower() or
                   search_term in t['category'].lower()
            ]

        # Filter by type
        if filters.get('type') and filters['type'] != 'all':
            filtered_transactions = [
                t for t in filtered_transactions
                if t['type'] == filters['type']
            ]

        # Filter by category
        if filters.get('category') and filters['category'] != 'all':
            filtered_transactions = [
                t for t in filtered_transactions
                if t['category'].lower() == filters['category'].lower()
            ]

        # Filter by currency
        if filters.get('currency') and filters['currency'] != 'all':
            filtered_transactions = [
                t for t in filtered_transactions
                if t['currency'].lower() == filters['currency'].lower()
            ]

        # Filter by date range
        if filters.get('date_range'):
            today = datetime.now()
            start_date = None
            end_date = None

            if filters['date_range'] == 'this-month':
                start_date = today.replace(day=1)
                end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            elif filters['date_range'] == 'last-month':
                end_date = today.replace(day=1) - timedelta(days=1)
                start_date = end_date.replace(day=1)
            elif filters['date_range'] == 'this-quarter':
                current_quarter = (today.month - 1) // 3
                start_date = today.replace(month=current_quarter * 3 + 1, day=1)
                end_date = start_date.replace(month=start_date.month + 3) - timedelta(days=1)
            elif filters['date_range'] == 'last-quarter':
                current_quarter = (today.month - 1) // 3
                end_date = today.replace(month=current_quarter * 3 + 1, day=1) - timedelta(days=1)
                start_date = end_date.replace(month=end_date.month - 2, day=1)
            elif filters['date_range'] == 'this-year':
                start_date = today.replace(month=1, day=1)
                end_date = today.replace(month=12, day=31)
            elif filters['date_range'] == 'last-year':
                start_date = today.replace(year=today.year - 1, month=1, day=1)
                end_date = today.replace(year=today.year - 1, month=12, day=31)
            elif filters['date_range'] == 'custom':
                if filters.get('start_date'):
                    start_date = datetime.strptime(filters['start_date'], '%Y-%m-%d')
                if filters.get('end_date'):
                    end_date = datetime.strptime(filters['end_date'], '%Y-%m-%d')

            if start_date or end_date:
                filtered_transactions = [
                    t for t in filtered_transactions
                    if (not start_date or datetime.strptime(t['date'], '%Y-%m-%d') >= start_date) and
                       (not end_date or datetime.strptime(t['date'], '%Y-%m-%d') <= end_date)
                ]

    # Calculate summary data for filtered transactions
    income_total = sum(t['amount'] for t in filtered_transactions if t['type'] == 'income')
    expenses_total = sum(t['amount'] for t in filtered_transactions if t['type'] == 'expense')
    tax_deductibles_total = sum(t['amount'] for t in filtered_transactions if t['tax_status'] == 'deductible')

    summary_data = {
        "income": {
            "total": income_total,
            "currency": "MYR",
            "icon": "arrow-down"
        },
        "expenses": {
            "total": expenses_total,
            "currency": "MYR",
            "icon": "arrow-up"
        },
        "tax_deductibles": {
            "total": tax_deductibles_total,
            "currency": "MYR",
            "icon": "receipt"
        }
    }
    
    # Pagination data
    page = filters.get('page', 1)
    per_page = 10
    total_items = len(filtered_transactions)
    total_pages = (total_items + per_page - 1) // per_page
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page

    pagination = {
        "current_page": page,
        "total_pages": total_pages,
        "has_previous": page > 1,
        "has_next": page < total_pages
    }

    return {
        "user": user_data,
        "filter_options": filter_options,
        "summary": summary_data,
        "transactions": filtered_transactions[start_idx:end_idx],
        "pagination": pagination
    }

def get_tax_center_data():
    return {
        "user": {
            "name": "John Doe",
            "role": "Freelancer",
            "avatar": "images/avatar-placeholder.png"
        },
        "tax_year": {
            "current": "2025",
            "options": ["2025", "2024", "2023"]
        },
        "filing_status": {
            "deadline": "April 30, 2025",
            "days_remaining": 15,
            "completion": 65,
            "estimated_income": 125680.00,
            "potential_deductions": 24350.00,
            "estimated_tax": 15225.00
        },
        "income_summary": {
            "development": 85400.00,
            "design": 22680.00,
            "consulting": 17600.00
        },
        "deduction_summary": {
            "equipment": 8250.00,
            "home_office": 6100.00,
            "software": 5400.00,
            "training": 4600.00
        },
        "suggestions": [
            {
                "title": "Increase Home Office Deduction",
                "description": "Based on your work patterns, you might be eligible for a higher home office deduction. Consider claiming 25% of your home utility bills.",
                "impact": 1850.00,
                "priority": "high"
            },
            {
                "title": "Training & Professional Development",
                "description": "Your recent course payments qualify as professional development expenses. Add them to your tax deductions.",
                "impact": 950.00,
                "priority": "medium"
            },
            {
                "title": "Business Travel Deductions",
                "description": "Some of your travel expenses appear business-related but are not categorized for tax deductions. Review and recategorize them.",
                "impact": 720.00,
                "priority": "medium"
            },
            {
                "title": "Missing Receipt Alert",
                "description": "You have 3 transactions marked as deductible but missing receipt documentation. Upload receipts to strengthen your tax claims.",
                "impact": None,
                "items": 3,
                "priority": "low"
            }
        ],
        "recent_activity": [
            {
                "type": "check",
                "title": "New Deduction Added",
                "description": "Added \"Adobe Creative Cloud\" as a business expense",
                "time": "Today, 10:25 AM"
            },
            {
                "type": "file",
                "title": "Tax Form Generated",
                "description": "Generated and downloaded draft Tax Form B",
                "time": "Yesterday, 3:15 PM"
            },
            {
                "type": "receipt",
                "title": "Receipt Uploaded",
                "description": "Added receipt for \"Business Development Conference\"",
                "time": "April 12, 2025"
            },
            {
                "type": "calculator",
                "title": "Tax Calculation",
                "description": "Updated tax estimation based on Q1 2025 income",
                "time": "April 10, 2025"
            }
        ]
    }

def get_reports_data():
    return {
        "user": {
            "name": "John Doe",
            "role": "Freelancer",
            "avatar": "images/avatar-placeholder.png"
        },
        "date_ranges": {
            "options": [
                {"value": "this-month", "label": "This Month"},
                {"value": "last-month", "label": "Last Month"},
                {"value": "this-quarter", "label": "This Quarter"},
                {"value": "last-quarter", "label": "Last Quarter"},
                {"value": "this-year", "label": "This Year", "selected": True},
                {"value": "last-year", "label": "Last Year"},
                {"value": "custom", "label": "Custom Range"}
            ]
        },
        "summary": {
            "income": {
                "total": 126450.00,
                "currency": "MYR",
                "period": "Jan - Dec 2025"
            },
            "expenses": {
                "total": 42380.00,
                "currency": "MYR",
                "period": "Jan - Dec 2025"
            },
            "profit": {
                "total": 84070.00,
                "currency": "MYR",
                "period": "Jan - Dec 2025"
            }
        },
        "income_distribution": [
            {"category": "Development", "amount": 75870.00, "percentage": 60},
            {"category": "Design", "amount": 30348.00, "percentage": 24},
            {"category": "Consulting", "amount": 20232.00, "percentage": 16}
        ],
        "expense_distribution": [
            {"category": "Software", "amount": 12714.00, "percentage": 30},
            {"category": "Equipment", "amount": 10595.00, "percentage": 25},
            {"category": "Office", "amount": 10595.00, "percentage": 25},
            {"category": "Other", "amount": 8476.00, "percentage": 20}
        ],
        "recent_reports": [
            {
                "type": "pdf",
                "title": "Annual Income & Expense Report (2025)",
                "date": "15 May 2025"
            },
            {
                "type": "csv",
                "title": "Q1 Tax Summary (2025)",
                "date": "02 April 2025"
            },
            {
                "type": "doc",
                "title": "Client Revenue Analysis (2024)",
                "date": "10 January 2025"
            }
        ]
    }

def get_currencies_data(sort_by='date', sort_order='desc'):
    # Base data structure remains the same
    data = {
        "user": {
            "name": "John Doe",
            "role": "Freelancer",
            "avatar": "images/avatar-placeholder.png"
        },
        "last_update": "15 May 2025, 09:30 AM",
        "primary_currency": {
            "code": "MYR",
            "name": "Malaysian Ringgit",
            "income": 45680.00,
            "expenses": 12450.00,
            "balance": 33230.00
        },
        "currencies": [
            {
                "code": "USD",
                "name": "US Dollar",
                "symbol": "$",
                "rate": 4.20,
                "income": 5200.00,
                "expenses": 1350.00,
                "balance": 3850.00
            },
            {
                "code": "EUR",
                "name": "Euro",
                "symbol": "€",
                "rate": 4.95,
                "income": 2100.00,
                "expenses": 580.00,
                "balance": 1520.00
            },
            {
                "code": "GBP",
                "name": "British Pound",
                "symbol": "£",
                "rate": 5.80,
                "income": 1200.00,
                "expenses": 0.00,
                "balance": 1200.00
            }
        ],
        "recent_transactions": [
            {
                "date": "15 May 2025",
                "description": "UI/UX Design Project",
                "amount": 2500.00,
                "currency": "USD",
                "rate": 4.20,
                "myr_value": 10500.00,
                "type": "income"
            },
            {
                "date": "10 May 2025",
                "description": "Adobe Creative Cloud",
                "amount": 52.99,
                "currency": "USD",
                "rate": 4.18,
                "myr_value": 221.50,
                "type": "expense"
            },
            {
                "date": "05 May 2025",
                "description": "Web Development",
                "amount": 1800.00,
                "currency": "EUR",
                "rate": 4.95,
                "myr_value": 8910.00,
                "type": "income"
            },
            {
                "date": "28 Apr 2025",
                "description": "Digital Ocean Hosting",
                "amount": 25.00,
                "currency": "USD",
                "rate": 4.22,
                "myr_value": 105.50,
                "type": "expense"
            },
            {
                "date": "20 Apr 2025",
                "description": "Branding Project",
                "amount": 1200.00,
                "currency": "GBP",
                "rate": 5.80,
                "myr_value": 6960.00,
                "type": "income"
            }
        ]
    }

    # Sort transactions based on parameters
    if sort_by in ['date', 'description', 'amount', 'myr_value']:
        reverse = sort_order == 'desc'
        if sort_by == 'date':
            data['recent_transactions'].sort(key=lambda x: x['date'], reverse=reverse)
        elif sort_by == 'description':
            data['recent_transactions'].sort(key=lambda x: x['description'].lower(), reverse=reverse)
        elif sort_by == 'amount':
            data['recent_transactions'].sort(key=lambda x: x['amount'], reverse=reverse)
        elif sort_by == 'myr_value':
            data['recent_transactions'].sort(key=lambda x: x['myr_value'], reverse=reverse)

    return data

def get_settings_data():
    return {
        "user": {
            "name": "John Doe",
            "role": "Freelancer",
            "avatar": "images/avatar-placeholder.png",
            "email": "john.doe@example.com",
            "phone": "+60123456789"
        },
        "languages": [
            {"code": "en", "name": "English", "selected": True},
            {"code": "ms", "name": "Bahasa Malaysia"},
            {"code": "zh", "name": "Chinese"},
            {"code": "ta", "name": "Tamil"}
        ],
        "tax_info": {
            "tax_id": "MY12345678",
            "marital_status": [
                {"value": "single", "label": "Single"},
                {"value": "married", "label": "Married", "selected": True},
                {"value": "divorced", "label": "Divorced"},
                {"value": "widowed", "label": "Widowed"}
            ],
            "spouse_working": [
                {"value": "working", "label": "Working"},
                {"value": "not-working", "label": "Not Working", "selected": True}
            ],
            "children": {
                "total": 2,
                "higher_education": 1
            },
            "disability_status": [
                {"value": "none", "label": "None", "selected": True},
                {"value": "self", "label": "Self"},
                {"value": "spouse", "label": "Spouse"},
                {"value": "child", "label": "Child"}
            ],
            "business_type": [
                {"value": "sole-proprietor", "label": "Sole Proprietor", "selected": True},
                {"value": "partnership", "label": "Partnership"},
                {"value": "llp", "label": "Limited Liability Partnership"},
                {"value": "sdn-bhd", "label": "Sdn. Bhd."}
            ]
        },
        "tax_relief_categories": [
            {
                "name": "Medical Expenses",
                "limit": 8000.00,
                "current": 3600.00,
                "percentage": 45
            },
            {
                "name": "EPF & Life Insurance",
                "limit": 7000.00,
                "current": 5950.00,
                "percentage": 85
            },
            {
                "name": "Lifestyle Relief",
                "limit": 2500.00,
                "current": 1500.00,
                "percentage": 60
            },
            {
                "name": "Education Fees (Self)",
                "limit": 7000.00,
                "current": 2100.00,
                "percentage": 30
            },
            {
                "name": "SOCSO Contributions",
                "limit": 350.00,
                "current": 350.00,
                "percentage": 100
            }
        ],
        "currencies": {
            "primary": "MYR",
            "options": [
                {"code": "myr", "name": "Malaysian Ringgit (MYR)", "selected": True},
                {"code": "usd", "name": "US Dollar (USD)"},
                {"code": "sgd", "name": "Singapore Dollar (SGD)"},
                {"code": "gbp", "name": "British Pound (GBP)"},
                {"code": "eur", "name": "Euro (EUR)"}
            ],
            "active": [
                {"code": "myr", "name": "Malaysian Ringgit (MYR)", "active": True},
                {"code": "usd", "name": "US Dollar (USD)", "active": True},
                {"code": "sgd", "name": "Singapore Dollar (SGD)", "active": True},
                {"code": "gbp", "name": "British Pound (GBP)", "active": True},
                {"code": "eur", "name": "Euro (EUR)", "active": True},
                {"code": "aud", "name": "Australian Dollar (AUD)", "active": False},
                {"code": "jpy", "name": "Japanese Yen (JPY)", "active": False}
            ]
        },
        "storage": {
            "used": 30.5,
            "total": 100,
            "percentage": 35
        }
    }

def get_tax_summary_data():
    today = datetime.now()
    deadline = datetime(2025, 4, 30)
    days_remaining = (deadline - today).days

    return {
        "user": {
            "name": "John Doe",
            "role": "Freelancer",
            "avatar": "images/avatar-placeholder.png"
        },
        "tax_data": {
            "year": "2025",
            "last_updated": "15 May 2025",
            "total_income": 126450.00,
            "total_deductions": 24350.00,
            "taxable_income": 102100.00,
            "estimated_tax": 15225.00,
            "deadline": "April 30, 2025",
            "days_remaining": days_remaining,
            "completion_percentage": 65,
            "deductions": [
                {
                    "name": "Equipment & Supplies",
                    "description": "Computer equipment, office supplies, and software subscriptions",
                    "amount": 8250.00
                },
                {
                    "name": "Home Office",
                    "description": "Portion of rent, utilities, and internet expenses",
                    "amount": 6100.00
                },
                {
                    "name": "Software & Services",
                    "description": "Professional software licenses and cloud services",
                    "amount": 5400.00
                },
                {
                    "name": "Professional Development",
                    "description": "Online courses and training materials",
                    "amount": 4600.00
                }
            ],
            "requirements": [
                {
                    "name": "Income Documentation",
                    "description": "All income statements and invoices for the tax year",
                    "completed": True
                },
                {
                    "name": "Expense Receipts",
                    "description": "Receipts for all claimed deductions",
                    "completed": True
                },
                {
                    "name": "Bank Statements",
                    "description": "Statements showing business transactions",
                    "completed": False
                },
                {
                    "name": "Previous Tax Returns",
                    "description": "Last year's tax return for reference",
                    "completed": True
                }
            ],
            "advisory_items": [
                {
                    "title": "Missing Documentation",
                    "description": "Upload your bank statements to complete your documentation requirements.",
                    "icon": "fa-exclamation-triangle"
                },
                {
                    "title": "Deduction Opportunity",
                    "description": "You may be eligible for additional home office deductions based on your work patterns.",
                    "icon": "fa-lightbulb"
                },
                {
                    "title": "Tax Savings Tip",
                    "description": "Consider contributing to your EPF to maximize your tax relief for retirement savings.",
                    "icon": "fa-piggy-bank"
                }
            ]
        }
    }

# map each page to a route
@app.route("/")
def home():
    dashboard_data = get_dashboard_data()
    return render_template("index.html", **dashboard_data)

@app.route("/expenses")
def expenses():
    filters = {
        'search': request.args.get('search', ''),
        'type': request.args.get('type', 'all'),
        'category': request.args.get('category', 'all'),
        'currency': request.args.get('currency', 'all'),
        'date_range': request.args.get('date_range', 'all'),
        'start_date': request.args.get('start_date'),
        'end_date': request.args.get('end_date'),
        'page': int(request.args.get('page', 1))
    }
    
    expenses_data = get_expenses_data(filters)
    # expenses_data = get_expenses_data()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'transactions': expenses_data['transactions'],
            'summary': expenses_data['summary'],
            'pagination': expenses_data['pagination']
        })
    
    return render_template("expenses.html", **expenses_data, categories = list_categories())

@app.route("/currencies")
def currencies():
    sort_by = request.args.get('sort', 'date')
    sort_order = request.args.get('order', 'desc')
    currencies_data = get_currencies_data(sort_by, sort_order)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'transactions': currencies_data['recent_transactions']
        })
    return render_template("currencies.html", **currencies_data)

@app.route("/tax-center")
def tax_center():
    tax_data = get_tax_center_data()
    return render_template("tax-center.html", **tax_data)

@app.route("/reports")
def reports():
    reports_data = get_reports_data()
    return render_template("reports.html", **reports_data)

@app.route("/settings")
def settings():
    settings_data = get_settings_data()
    return render_template("settings.html", **settings_data)

@app.route("/tax-summary")
def tax_summary():
    tax_summary_data = get_tax_summary_data()
    return render_template("tax-summary.html", **tax_summary_data)

@app.route("/export-tax-summary")
def export_tax_summary():
    format = request.args.get('format', 'pdf')
    tax_data = get_tax_summary_data()

    if format == 'pdf':
        # Here you would generate a PDF using a library like reportlab or WeasyPrint
        # For now, we'll return a dummy response
        return Response(
            "PDF content here",
            mimetype='application/pdf',
            headers={'Content-Disposition': f'attachment;filename=tax_summary_{datetime.now().year}.pdf'}
        )
    elif format in ['excel', 'csv']:
        # Here you would generate Excel/CSV using a library like pandas or openpyxl
        return jsonify({
            "success": True,
            "message": f"Export to {format.upper()} completed successfully"
        })
    else:
        return jsonify({
            "error": "Unsupported export format"
        }), 400

@app.route("/upload-receipt", methods=["POST"])
def upload_receipt():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    filename = secure_filename(file.filename)
    content = file.read()

    try:
        oss_url = upload_to_oss(filename, content)
        return jsonify({"success": True, "url": oss_url}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/extract-receipt-data", methods=["POST"])
def extract_receipt_data():
    data = request.get_json()
    image_url = data.get("image_url")
    if not image_url:
        return jsonify({"success": False, "error": "Missing image_url"}), 400

    result = parse_receipt_with_qwen(image_url)

    return jsonify({"success": True, "data": result})

from flask import request

@app.route("/insert-transaction", methods=["POST"])
def insert_transaction_api():
    data = request.get_json()

    try:
        # Extract from JSON
        date = data.get("date")
        description = data.get("description", "")
        category_id = data.get("category_id")
        client_vendor = data.get("client_vendor")
        amount = data.get("amount")
        currency = data.get("currency")
        transaction_type = data.get("transaction_type")
        receipt_url = data.get("receipt_url")

        # Validate required fields
        if not all([date, category_id, client_vendor, amount, currency, transaction_type]):
            return jsonify({"success": False, "error": "Missing required fields"}), 400

        # Insert into DB
        success = insert_transaction(
            date, description, category_id, client_vendor,
            amount, currency, transaction_type, receipt_url
        )

        return jsonify({"success": success})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/delete-transaction", methods=["POST"])
def delete_transaction_api():
    data = request.get_json()
    transaction_id = data.get("transaction_id")
    
    if not transaction_id:
        return jsonify({"success": False, "error": "Missing transaction_id"}), 400

    try:
        success = delete_transaction(transaction_id)
        return jsonify({"success": success})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    # debug=True for live reload during development
    app.run(host="0.0.0.0", port=5000, debug=True)
