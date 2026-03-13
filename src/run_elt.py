from extract import read_customers_csv, read_orders_json, read_products_xml
from load_postgres import (
    load_raw_customers,
    load_raw_orders,
    load_raw_products,
    run_sql_file
)


def main():
    customers_raw = read_customers_csv()
    orders_raw = read_orders_json()
    products_raw = read_products_xml()

    load_raw_customers(customers_raw)
    load_raw_orders(orders_raw)
    load_raw_products(products_raw)

    run_sql_file("sql/elt_transform.sql")

    print("ELT completed successfully. Raw data loaded and SQL transformations applied.")


if __name__ == "__main__":
    main()