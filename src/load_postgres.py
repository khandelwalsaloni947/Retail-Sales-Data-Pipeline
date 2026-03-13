# src/load_postgres.py

import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="retail_project",
        user="postgres",
        password="8875",  #  PostgreSQL password  
        host="localhost",
        port="5432"
    )

def load_sales_report(records):
    connection = get_connection()
    cursor = connection.cursor()

    # Clean old data
    cursor.execute("DELETE FROM sales_report;")

    insert_query = """
        INSERT INTO sales_report (
            order_id,
            order_date,
            customer_id,
            customer_name,
            city,
            product_id,
            product_name,
            category,
            quantity,
            price,
            total_amount
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    for record in records:
        cursor.execute(
            insert_query,
            (
                record["order_id"],
                record["order_date"],
                record["customer_id"],
                record["customer_name"],
                record["city"],
                record["product_id"],
                record["product_name"],
                record["category"],
                record["quantity"],
                record["price"],
                record["total_amount"]
            )
        )

    connection.commit()
    cursor.close()
    connection.close()


# -----------------------------
# Optional: update category summary
# -----------------------------
def update_category_summary():
    connection = get_connection()
    cursor = connection.cursor()

    # Ensure the summary table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS category_summary (
            category TEXT,
            total_revenue NUMERIC(10,2)
        );
    """)

    # Clear old summary
    cursor.execute("DELETE FROM category_summary;")

    # Populate summary table
    cursor.execute("""
        INSERT INTO category_summary (category, total_revenue)
        SELECT category, SUM(total_amount)
        FROM sales_report
        GROUP BY category;
    """)

    connection.commit()
    cursor.close()
    connection.close()