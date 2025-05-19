import os
import ast
from openai import OpenAI
from dotenv import load_dotenv
from connect_db import list_categories

load_dotenv()

# category_list = ["Development", "Software", "Design", "Equipment", "Professional", "Consulting", "Utilities"]
# category_list = [{'id': 1, 'name': 'Salary', 'type': 'Income'}, {'id': 2, 'name': 'Rental Income', 'type': 'Income'}, {'id': 3, 'name': 'Dividends', 'type': 'Income'}, {'id': 4, 'name': 'Interests', 'type': 'Income'}, {'id': 5, 'name': 'Pensions', 'type': 'Income'}, {'id': 6, 'name': 'Annuities or Other Periodic Payments', 'type': 'Income'}, {'id': 7, 'name': 'Aggregate of Other Statutory Income from Sources Outside Malaysia', 'type': 'Income'}, {'id': 8, 'name': 'Self Relief', 'type': 'Expense'}, {'id': 9, 'name': 'EPF (KWSP) + Life Insurance', 'type': 'Expense'}, {'id': 10, 'name': 'Medical Expenses (Self & Parents)', 'type': 'Expense'}, {'id': 11, 'name': 'Lifestyle Expenses', 'type': 'Expense'}, {'id': 12, 'name': 'Lifestyle (Additional for Tech)', 'type': 'Expense'}, {'id': 13, 'name': 'Parental Care', 'type': 'Expense'}, {'id': 14, 'name': 'Education Fee (Self)', 'type': 'Expense'}, {'id': 15, 'name': 'Childcare/Education (Children)', 'type': 'Expense'}, {'id': 16, 'name': 'Breastfeeding Equipment', 'type': 'Expense'}, {'id': 17, 'name': 'Disabled Individual / Spouse / Child', 'type': 'Expense'}, {'id': 18, 'name': 'SSPN Savings', 'type': 'Expense'}, {'id': 19, 'name': 'Education & Medical Insurance', 'type': 'Expense'}, {'id': 20, 'name': 'SOCSO / EIS Contributions', 'type': 'Expense'}, {'id': 21, 'name': 'Zakat / Fitrah', 'type': 'Expense'}, {'id': 22, 'name': 'EPF and Life Insurance Premium', 'type': 'Expense'}]
category_list = list_categories()

def parse_receipt_with_qwen(image_url: str) -> dict:
    prompt = f"""
Extract all the text from the receipt and identify the following fields from the receipt image:

- Date
- Vendor
- Total Amount
- Currency
- Type
- Category
- Description

Return the result as a Python dictionary.

Rules:
1. Only extract what is visible in the image.
2. For 'Category', match exactly with this list (case-insensitive): {category_list}.
   - If not found, return '23' means Others.
3. If 'Currency' or the currency symbol is not explicitly shown in the image, default to "MYR".

Return format example:
{{
  "Date": "2024-04-15",
  "Vendor": "Tech Supplies Inc",
  "Total Amount": "185.00",
  "Currency": "MYR",
  "Type": "Expense",
  "Category": "12",
  "Description": "Laptop Purchase",
}}
    """

    try:
        client = OpenAI(
            api_key=os.environ["DASHSCOPE_API_KEY"],
            base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
        )

        response = client.chat.completions.create(
            model="qwen-vl-max",
            messages=[
                {
                    "role": "system",
                    "content": [{"type": "text", "text": "You are a receipt-reading assistant."}],
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": image_url}},
                        {"type": "text", "text": prompt},
                    ],
                },
            ],
        )

        content = response.choices[0].message.content.strip()

        # Remove any markdown like ```python or ```
        if content.startswith("```"):
            content = content.strip("` \n")
            if content.startswith("python"):
                content = content[len("python"):].strip()

        # Convert string to dictionary safely
        receipt_data = ast.literal_eval(content)
        
        # --- Post-process fields ---
        from datetime import datetime

        if "Date" in receipt_data:
            try:
                # receipt_data["Date"] = datetime.strptime(receipt_data["Date"], "%d/%m/%Y").date()
                # convert it to YYYY-MM-DD format
                receipt_data["Date"] = datetime.strptime(receipt_data["Date"], "%d/%m/%Y").strftime("%Y-%m-%d")
            except ValueError:
                pass  # Optionally log or handle unsupported date format

        if "Total Amount" in receipt_data:
            try:
                receipt_data["Total Amount"] = float(receipt_data["Total Amount"])
            except ValueError:
                receipt_data["Total Amount"] = None

        return receipt_data

    except Exception as e:
        print(f"Error message: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    # Example usage
    image_url = "https://ai-hackathon-transaction1.oss-ap-southeast-3.aliyuncs.com/ocr_test.jpg"
    result = parse_receipt_with_qwen(image_url)
    print(result)
    print(type(result))
