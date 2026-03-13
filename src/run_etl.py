from extract import read_customers_csv, read_orders_json, read_products_xml
from transform_etl import run_etl_transform
from load_postgres import load_sales_report
from load_postgres import load_sales_report, update_category_summary

def main():
    customers_raw = read_customers_csv()
    orders_raw = read_orders_json()
    products_raw = read_products_xml()

    sales_report = run_etl_transform(
        customers_raw,
        products_raw,
        orders_raw
    )

    load_sales_report(sales_report)

    update_category_summary()  # <--- optional step

    print("ETL completed successfully")

if __name__ == "__main__":
    main()


    

    