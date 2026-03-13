import csv
import json
import xml.etree.ElementTree as ET
from pathlib import Path

RAW_DATA_FOLDER = Path("data") / "raw"

def read_customers_csv():
    customers_file = RAW_DATA_FOLDER / "customers.csv"
    customers = []

    with open(customers_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            customers.append(row)

    return customers


def read_orders_json():
    orders_file = RAW_DATA_FOLDER / "orders.json"

    with open(orders_file, mode="r", encoding="utf-8") as file:
        orders = json.load(file)

    return orders


def read_products_xml():
    products_file = RAW_DATA_FOLDER / "products.xml"
    tree = ET.parse(products_file)
    root = tree.getroot()

    products = []

    for product in root.findall("product"):
        products.append({
            "product_id": product.find("product_id").text,
            "product_name": product.find("product_name").text,
            "category": product.find("category").text,
            "price": product.find("price").text
        })

    return products


if __name__ == "__main__":
    customers = read_customers_csv()
    orders = read_orders_json()
    products = read_products_xml()

    print("Customers:", customers[:2])
    print("Orders:", orders[:2])
    print("Products:", products[:2])