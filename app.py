from flask import Flask, render_template, request, jsonify, Response
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from get_data import get_expenses_data, get_dashboard_data, get_tax_center_data, get_reports_data, get_currencies_data, get_settings_data, get_tax_summary_data
from oss_manage_file import upload_to_oss  # function to upload to OSS
from llm import parse_receipt_with_qwen  # function to parse receipt with Qwen
from connect_db import list_transactions, list_categories, insert_transaction, delete_transaction

app = Flask(
    __name__,
    static_folder="static",      # default, so you can omit
    template_folder="templates"  # default, so you can omit
)

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
