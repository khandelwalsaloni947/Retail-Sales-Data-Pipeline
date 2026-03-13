# src/transform_etl.py

# -----------------------------
# Helper function to clean text
# -----------------------------
def clean_text(value):
    if value is None:
        return ""
    return value.strip().title()


# -----------------------------
# Clean customer records
# -----------------------------
def clean_customers(customers):
    cleaned_customers = []
    seen_customer_ids = set()

    for customer in customers:
        customer_id = customer.get("customer_id", "").strip()

        if not customer_id:
            continue

        if customer_id in seen_customer_ids:
            continue

        seen_customer_ids.add(customer_id)

        cleaned_customers.append({
            "customer_id": int(customer_id),
            "customer_name": clean_text(customer.get("customer_name")),
            "city": clean_text(customer.get("city")) or "Unknown",
            "signup_date": customer.get("signup_date", "").strip()
        })

    return cleaned_customers


# -----------------------------
# Clean product records
# -----------------------------
def clean_products(products):
    cleaned_products = []

    for product in products:
        product_id = str(product.get("product_id", "")).strip()
        price_value = str(product.get("price", "")).strip()

        if not product_id:
            continue

        try:
            price = float(price_value)
        except ValueError:
            continue

        cleaned_products.append({
            "product_id": int(product_id),
            "product_name": clean_text(product.get("product_name")),
            "category": clean_text(product.get("category")),
            "price": price
        })

    return cleaned_products


# -----------------------------
# Clean order records
# -----------------------------
def clean_orders(orders):
    cleaned_orders = []

    for order in orders:
        order_id = str(order.get("order_id", "")).strip()
        customer_id = str(order.get("customer_id", "")).strip()
        product_id = str(order.get("product_id", "")).strip()
        quantity_value = str(order.get("quantity", "")).strip()
        order_date = str(order.get("order_date", "")).strip()

        if not order_id or not customer_id or not product_id:
            continue

        try:
            quantity = int(quantity_value)
        except ValueError:
            continue

        cleaned_orders.append({
            "order_id": int(order_id),
            "customer_id": int(customer_id),
            "product_id": int(product_id),
            "quantity": quantity,
            "order_date": order_date
        })

    return cleaned_orders


# -----------------------------
# Build lookup dictionaries
# -----------------------------
def build_lookup(records, key_field):
    lookup = {}
    for record in records:
        lookup[record[key_field]] = record
    return lookup


# -----------------------------
# Join datasets to build sales_report
# -----------------------------
def build_sales_report(customers, products, orders):
    customer_lookup = build_lookup(customers, "customer_id")
    product_lookup = build_lookup(products, "product_id")

    sales_report = []

    for order in orders:
        customer = customer_lookup.get(order["customer_id"])
        product = product_lookup.get(order["product_id"])

        if not customer or not product:
            continue

        total_amount = order["quantity"] * product["price"]

        sales_report.append({
            "order_id": order["order_id"],
            "order_date": order["order_date"],
            "customer_id": customer["customer_id"],
            "customer_name": customer["customer_name"],
            "city": customer["city"],
            "product_id": product["product_id"],
            "product_name": product["product_name"],
            "category": product["category"],
            "quantity": order["quantity"],
            "price": product["price"],
            "total_amount": round(total_amount, 2)
        })

    return sales_report


# -----------------------------
# ETL Transformation Entry Point
# -----------------------------
def run_etl_transform(customers_raw, products_raw, orders_raw):
    customers_clean = clean_customers(customers_raw)
    products_clean = clean_products(products_raw)
    orders_clean = clean_orders(orders_raw)

    sales_report = build_sales_report(
        customers_clean,
        products_clean,
        orders_clean
    )

    return sales_report