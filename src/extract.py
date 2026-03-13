from pathlib import Path
import csv
import json
import xml.etree.ElementTree as ET

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