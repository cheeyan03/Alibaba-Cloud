# 🧾 FinTrack — Expense Tracker & Tax Filing Assistant

FinTrack is a modern, user-friendly web application tailored for freelancers and small business owners in Malaysia. It simplifies **expense tracking**, **income management**, and **tax filing**, all in one place — with smart features like OCR-based receipt extraction and AI-assisted tax suggestions.

---

## 🚀 Overview

This project helps users:

* Upload receipts and auto-extract data using OCR
* Categorize transactions (Income / Expense)
* Monitor multi-currency finances
* Track deductible items for tax purposes
* Export reports for submission or analysis

---

## ✨ Features

* 📊 **Dashboard** — Snapshot of financial health
* 🧾 **Expenses & Income** — Add, filter, and view transaction history
* 🧠 **Receipt Scanner** — Upload image/PDF and auto-extract vendor, amount, date, etc.
* 💹 **Currency Tracker** — Convert and manage foreign currency transactions
* 📑 **Tax Center** — Suggest deductible expenses, view tax status per transaction
* 📈 **Reports** — Export financial summaries

---

## 🛠️ Technology Stack

* **Backend**: Python (Flask)
* **Frontend**: HTML, CSS, JavaScript
* **Database**: ApsaraDB RDS for MySQL
* **OCR & AI**: Qwen LLMs from Model Studio
* **Visualization**: QuickBI
* **File Upload & Management**: Alibaba Cloud Object Storage Service (OSS)

---

## 🧰 Project Structure (Key Files)

```
.
├── app.py                     # Main Flask application
├── llm.py                     # Qwen LLM logic for parsing
├── oss_manage_file.py         # Upload to Alibaba Cloud OSS
├── templates/                 # HTML templates (Jinja2)
├── static/                    # CSS, JS, images
├── requirements.txt           # Python dependencies
└── .env / example.env         # Environment variables
```

---

## ⚙️ Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/cheeyan03/Alibaba-Cloud.git
cd Alibaba-Cloud
```

2. **Create and activate a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Rename the example file and fill in your own secrets:

```bash
cp example.env .env
# Edit .env to insert your OSS keys, DB credentials, etc.
```

5. **Run the app**

```bash
python app.py
```

Access it on: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---
