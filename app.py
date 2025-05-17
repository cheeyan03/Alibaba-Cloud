from flask import Flask, render_template

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

if __name__ == "__main__":
    # debug=True for live reload during development
    app.run(host="0.0.0.0", port=5000, debug=True)
