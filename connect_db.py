import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

host = os.getenv("DB_HOST")
port = int(os.getenv("DB_PORT"))
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")

def get_connection():
    return pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        cursorclass=pymysql.cursors.DictCursor  # returns rows as dictionaries
    )
def list_transactions():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # cursor.execute("SELECT * FROM transactions")
            # return cursor.fetchall()
            
            # sort the transactions by date in descending order
            cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
            transactions = cursor.fetchall()
            return transactions
    finally:
        conn.close()

def insert_transaction(date, description, category_id, client_vendor, amount, currency, transaction_type, receipt_url=None):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO transactions 
                (date, description, category_id, client_vendor, amount, currency, transaction_type, receipt_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (date, description, category_id, client_vendor, amount, currency, transaction_type, receipt_url))
        conn.commit()
        return True
    finally:
        conn.close()

def delete_transaction(transaction_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM transactions WHERE id = %s", (transaction_id,))
        conn.commit()
        return True
    finally:
        conn.close()

def list_tax_limits():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT tl.id, c.name AS category, tl.yearly_limit
                FROM tax_limits tl
                JOIN categories c ON tl.category_id = c.id
            """)
            return cursor.fetchall()
    finally:
        conn.close()

def list_categories():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name, type FROM categories")
            return cursor.fetchall()
    finally:
        conn.close()
        
# print(list_categories())

def select_transaction(transaction_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM transactions WHERE id = %s", (transaction_id,))
            return cursor.fetchone()
    finally:
        conn.close()
        
# print(select_transaction(52))
