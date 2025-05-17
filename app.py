from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from oss_manage_file import upload_to_oss  # function to upload to OSS
from llm import parse_receipt_with_qwen  # function to parse receipt with Qwen


app = Flask(
    __name__,
    static_folder="static",      # default, so you can omit
    template_folder="templates"  # default, so you can omit
)

# map each page to a route
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/expenses")
def expenses():
    return render_template("expenses.html")

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


if __name__ == "__main__":
    # debug=True for live reload during development
    app.run(host="0.0.0.0", port=5000, debug=True)
