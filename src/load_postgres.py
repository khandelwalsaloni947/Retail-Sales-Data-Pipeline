# src/load_postgres.py

import psycopg2
from pathlib import Path

# -------------------------
# PostgreSQL Connection
# -------------------------
def get_connection():
    return psycopg2.connect(
        dbname="retail_project",
        user="postgres",
        password="8875",  # Replace with actual password
        host="localhost",
        port="5432"
    )

# -------------------------
# ETL Load Functions
# -------------------------
def load_sales_report(df):
    """ETL: Load final DataFrame into sales_report table"""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM sales_report;")

    insert_query = """
        INSERT INTO sales_report (
            order_id, order_date, customer_id, customer_name,
            city, product_id, product_name, category,
            quantity, price, total_amount
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
    """

    for _, row in df.iterrows():
        cursor.execute(insert_query, (
            row['order_id'], row['order_date'], row['customer_id'], row['customer_name'],
            row['city'], row['product_id'], row['product_name'], row['category'],
            row['quantity'], row['price'], row['total_amount']
        ))

    connection.commit()
    cursor.close()
    connection.close()


# -------------------------
# ELT Load Functions
# -------------------------
def load_raw_customers(customers):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM raw_customers;")
    insert_query = """
        INSERT INTO raw_customers (
            customer_id, customer_name, city, signup_date
        ) VALUES (%s,%s,%s,%s);
    """
    for c in customers:
        cursor.execute(insert_query, (
            c.get("customer_id"), c.get("customer_name"),
            c.get("city"), c.get("signup_date")
        ))
    connection.commit()
    cursor.close()
    connection.close()


def load_raw_orders(orders):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM raw_orders;")
    insert_query = """
        INSERT INTO raw_orders (
            order_id, customer_id, product_id, quantity, order_date
        ) VALUES (%s,%s,%s,%s,%s);
    """
    for o in orders:
        cursor.execute(insert_query, (
            o.get("order_id"), o.get("customer_id"),
            o.get("product_id"), o.get("quantity"), o.get("order_date")
        ))
    connection.commit()
    cursor.close()
    connection.close()


def load_raw_products(products):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM raw_products;")
    insert_query = """
        INSERT INTO raw_products (
            product_id, product_name, category, price
        ) VALUES (%s,%s,%s,%s);
    """
    for p in products:
        cursor.execute(insert_query, (
            p.get("product_id"), p.get("product_name"),
            p.get("category"), p.get("price")
        ))
    connection.commit()
    cursor.close()
    connection.close()


# -------------------------
# Utility to Run SQL Files
# -------------------------
def run_sql_file(file_path):
    connection = get_connection()
    cursor = connection.cursor()
    sql_path = Path(file_path)
    sql_content = sql_path.read_text(encoding="utf-8")
    cursor.execute(sql_content)
    connection.commit()
    cursor.close()
    connection.close()