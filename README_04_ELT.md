# README 04 - ELT Pipeline Guide

# ELT Pipeline Guide

## Building the ELT Version of the Retail Sales Data Pipeline

---

## 1. Why this README exists

In this part of the project, you will build the **ELT version** of the pipeline.

ELT means:

* **Extract**
* **Load**
* **Transform**

In this design, the data is:

1. extracted from the source files
2. loaded into PostgreSQL in its raw form
3. transformed later inside PostgreSQL using SQL

This is also a real data engineering pattern used in industry.

In many modern data platforms, ELT is common because teams prefer to load raw data first and then transform it inside the database, warehouse, or analytics platform.

So this project is helping you practice a realistic architecture style that data engineers really use.

Take it seriously and imagine that your team lead asked you to preserve the raw source data first, then build transformations on top of it.

---

## 2. What you will build

In this ELT version, you will:

* read the raw source files with Python
* load the raw records into PostgreSQL raw tables
* create SQL transformations inside PostgreSQL
* build a final reporting table
* validate the results with SQL queries

The most important idea is this:

> In the ELT version, the transformation happens **after the raw data is loaded**.

That is the core concept you should keep in mind throughout this README.

---

## 3. ELT flow for this project

Here is the flow you are building:

```text id="8m3lki"
Raw files → Extract with Python → Load raw data into PostgreSQL → Transform with SQL in PostgreSQL
```

More specifically:

```text id="q1fj6e"
customers.csv
orders.json
products.xml
      ↓
  Python extraction
      ↓
 Load raw tables into PostgreSQL
      ↓
 SQL transformations inside PostgreSQL
      ↓
 Final reporting table
```

That order is what makes this pipeline ELT.

---

## 4. Before you begin

Make sure your project already has this structure:

```text id="nm2v3f"
retail-sales-data-pipeline/
├── data/
│   └── raw/
│       ├── customers.csv
│       ├── orders.json
│       └── products.xml
├── sql/
│   ├── create_tables.sql
│   ├── elt_transform.sql
│   └── reporting_queries.sql
├── src/
│   ├── extract.py
│   ├── load_postgres.py
│   └── run_elt.py
```

Also make sure PostgreSQL is running and that you already know how to connect to it.

---

## 5. Step 1 - Understand the ELT responsibility

### Your task

Before writing code, say the responsibility clearly:

### Extract

Read the raw files into Python.

### Load

Insert the raw source records into PostgreSQL raw tables.

### Transform

Use SQL inside PostgreSQL to clean, join, and prepare the final reporting table.

### Why this matters

In ETL, Python did the main transformation before loading.

In ELT, PostgreSQL becomes the place where the main transformation happens.

That is the main architectural difference.

---

## 6. Step 2 - Create the PostgreSQL raw and final tables

### Your task

Open:

```text id="swx1xv"
sql/create_tables.sql
```

and add the ELT table definitions below your existing ETL table if needed:

```sql id="k8fdoj"
CREATE TABLE IF NOT EXISTS raw_customers (
    customer_id TEXT,
    customer_name TEXT,
    city TEXT,
    signup_date TEXT
);

CREATE TABLE IF NOT EXISTS raw_orders (
    order_id TEXT,
    customer_id TEXT,
    product_id TEXT,
    quantity TEXT,
    order_date TEXT
);

CREATE TABLE IF NOT EXISTS raw_products (
    product_id TEXT,
    product_name TEXT,
    category TEXT,
    price TEXT
);

CREATE TABLE IF NOT EXISTS sales_report_elt (
    order_id INTEGER,
    order_date DATE,
    customer_id INTEGER,
    customer_name TEXT,
    city TEXT,
    product_id INTEGER,
    product_name TEXT,
    category TEXT,
    quantity INTEGER,
    price NUMERIC(10,2),
    total_amount NUMERIC(10,2)
);
```

### Why this matters

In the ELT version, you first preserve the raw data in PostgreSQL.

That is why the raw tables use `TEXT` for all columns here.

This is realistic for a beginner project because it allows you to load the source data first without worrying too much about type conversion at the beginning.

Later, the SQL transformation step will clean and convert the data.

---

## 7. Step 3 - Reuse the extraction layer

### Your task

You can reuse the extraction logic from `src/extract.py`.

Your file should already contain:

* `read_customers_csv()`
* `read_orders_json()`
* `read_products_xml()`

If it does not, make sure `src/extract.py` includes this code:

```python id="epj6t8"
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
```

### Why this matters

The extraction part is the same idea in both ETL and ELT.

The big difference comes later, when deciding **where** transformation happens.

---

## 8. Step 4 - Prepare the PostgreSQL connection

### Your task

Open:

```text id="qjyjcv"
src/load_postgres.py
```

and make sure it contains this connection function:

```python id="s7cn9b"
import psycopg2


def get_connection():
    return psycopg2.connect(
        dbname="retail_project",
        user="postgres",
        password="your_password",
        host="localhost",
        port="5432"
    )
```

### Important note

Replace `"your_password"` with your actual PostgreSQL password.

### Why this matters

The ELT pipeline still needs Python to load the raw data into PostgreSQL first.

So Python is still important here, but it is mainly helping with the **Extract** and **Load** steps.

---

## 9. Step 5 - Create a loader for raw customer data

### Your task

Inside `src/load_postgres.py`, add this function:

```python id="d2pss7"
def load_raw_customers(customers):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM raw_customers;")

    insert_query = """
        INSERT INTO raw_customers (
            customer_id,
            customer_name,
            city,
            signup_date
        )
        VALUES (%s, %s, %s, %s);
    """

    for customer in customers:
        cursor.execute(
            insert_query,
            (
                customer.get("customer_id"),
                customer.get("customer_name"),
                customer.get("city"),
                customer.get("signup_date")
            )
        )

    connection.commit()
    cursor.close()
    connection.close()
```

### What this code does

This function:

* connects to PostgreSQL
* clears the old `raw_customers` table
* inserts the customer records exactly as they came from the source file
* commits and closes the connection

### Why this matters

This is the ELT philosophy: load raw data first.

At this point, you are **not** cleaning the customer data yet.

---

## 10. Step 6 - Create a loader for raw order data

### Your task

Still inside `src/load_postgres.py`, add this function:

```python id="2fehoj"
def load_raw_orders(orders):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM raw_orders;")

    insert_query = """
        INSERT INTO raw_orders (
            order_id,
            customer_id,
            product_id,
            quantity,
            order_date
        )
        VALUES (%s, %s, %s, %s, %s);
    """

    for order in orders:
        cursor.execute(
            insert_query,
            (
                order.get("order_id"),
                order.get("customer_id"),
                order.get("product_id"),
                order.get("quantity"),
                order.get("order_date")
            )
        )

    connection.commit()
    cursor.close()
    connection.close()
```

### Why this matters

The orders are also loaded in raw form first.

Even if `quantity` is still text, that is okay for now.

The cleaning and conversion will happen later inside PostgreSQL.

---

## 11. Step 7 - Create a loader for raw product data

### Your task

Now add the product loader:

```python id="zmos28"
def load_raw_products(products):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM raw_products;")

    insert_query = """
        INSERT INTO raw_products (
            product_id,
            product_name,
            category,
            price
        )
        VALUES (%s, %s, %s, %s);
    """

    for product in products:
        cursor.execute(
            insert_query,
            (
                product.get("product_id"),
                product.get("product_name"),
                product.get("category"),
                product.get("price")
            )
        )

    connection.commit()
    cursor.close()
    connection.close()
```

### Why this matters

Now all three source datasets can be loaded into PostgreSQL exactly as they arrived.

This is one of the defining features of ELT.

---

## 12. Step 8 - Improve the loader by using one connection

### Your task

The previous three functions are clear for learning, but they open and close a new connection each time.

That is acceptable for beginners, but in real work it is often better to reuse the same connection when possible.

For now, keep the separate functions because they make the logic easier to understand.

### Why this note matters

Part of learning data engineering is knowing that there is a difference between:

* beginner-friendly structure
* production optimization

For this mini-project, clarity is more important than over-optimization.

---

## 13. Step 9 - Create the ELT transform SQL file

### Your task

Open:

```text id="2m4p62"
sql/elt_transform.sql
```

and start with this reset statement:

```sql id="szj2uj"
DELETE FROM sales_report_elt;
```

### Why this matters

Before inserting a new transformed result, it is often helpful to clear the old version first.

This keeps the final reporting table fresh and prevents duplicate rows from multiple runs.

---

## 14. Step 10 - Write the SQL transformation query

### Your task

Now add the main ELT transformation query inside `sql/elt_transform.sql`:

```sql id="s25qph"
INSERT INTO sales_report_elt (
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
SELECT
    CAST(ro.order_id AS INTEGER) AS order_id,
    CAST(ro.order_date AS DATE) AS order_date,
    CAST(ro.customer_id AS INTEGER) AS customer_id,
    INITCAP(TRIM(rc.customer_name)) AS customer_name,
    INITCAP(TRIM(rc.city)) AS city,
    CAST(ro.product_id AS INTEGER) AS product_id,
    INITCAP(TRIM(rp.product_name)) AS product_name,
    INITCAP(TRIM(rp.category)) AS category,
    CAST(ro.quantity AS INTEGER) AS quantity,
    CAST(rp.price AS NUMERIC(10,2)) AS price,
    CAST(ro.quantity AS INTEGER) * CAST(rp.price AS NUMERIC(10,2)) AS total_amount
FROM raw_orders ro
JOIN raw_customers rc
    ON ro.customer_id = rc.customer_id
JOIN raw_products rp
    ON ro.product_id = rp.product_id
WHERE ro.order_id ~ '^[0-9]+$'
  AND ro.customer_id ~ '^[0-9]+$'
  AND ro.product_id ~ '^[0-9]+$'
  AND ro.quantity ~ '^[0-9]+$'
  AND rp.price ~ '^[0-9]+(\.[0-9]+)?$';
```

### What this SQL does

This query:

* reads from the raw tables
* trims extra spaces
* standardizes text using `INITCAP`
* converts IDs and numbers into proper types
* joins customers, orders, and products together
* calculates `total_amount`
* inserts the final clean result into `sales_report_elt`

### Why this matters

This is the heart of the ELT design.

In the ETL version, Python performed these transformations.

In the ELT version, PostgreSQL performs them with SQL.

That is the big difference students should feel and understand.

---

## 15. Step 11 - Why the WHERE clause is important

### Your task

Study this part carefully:

```sql id="44jvbf"
WHERE ro.order_id ~ '^[0-9]+$'
  AND ro.customer_id ~ '^[0-9]+$'
  AND ro.product_id ~ '^[0-9]+$'
  AND ro.quantity ~ '^[0-9]+$'
  AND rp.price ~ '^[0-9]+(\.[0-9]+)?$';
```

### Why this matters

Because the raw tables store everything as text.

If you try to cast invalid values directly to integers or numeric types, PostgreSQL may raise an error.

This filter helps protect the transformation step by keeping only rows with valid numeric-looking values.

This is a realistic ELT concern.

When raw data is loaded first, the transformation logic must be careful.

---

## 16. Step 12 - Create reporting SQL queries

### Your task

Open:

```text id="vce0uu"
sql/reporting_queries.sql
```

and add these queries:

```sql id="baiwiv"
SELECT COUNT(*) FROM sales_report_elt;
```

```sql id="fgv6ir"
SELECT * FROM sales_report_elt LIMIT 10;
```

```sql id="zdb5kz"
SELECT category, SUM(total_amount) AS total_revenue
FROM sales_report_elt
GROUP BY category
ORDER BY total_revenue DESC;
```

```sql id="6g2q5p"
SELECT city, COUNT(*) AS total_orders
FROM sales_report_elt
GROUP BY city
ORDER BY total_orders DESC;
```

### Why this matters

The project is not complete until you can actually verify the business output.

These queries help you inspect:

* row counts
* sample output
* revenue by category
* order activity by city

That makes the project feel real and useful.

---

## 17. Step 13 - Create a helper to run SQL files

### Your task

Now go back to `src/load_postgres.py` and add this utility function:

```python id="rbe9f6"
from pathlib import Path


def run_sql_file(file_path):
    connection = get_connection()
    cursor = connection.cursor()

    sql_path = Path(file_path)
    sql_content = sql_path.read_text(encoding="utf-8")

    cursor.execute(sql_content)

    connection.commit()
    cursor.close()
    connection.close()
```

### What this code does

This function:

* opens a SQL file
* reads its content
* executes it in PostgreSQL
* commits and closes the connection

### Why this matters

In real engineering projects, SQL logic is often stored in separate `.sql` files instead of being buried inside Python strings.

This is a useful and realistic habit.

---

## 18. Step 14 - Create the ELT runner script

### Your task

Open:

```text id="0cg2ji"
src/run_elt.py
```

and add this code:

```python id="25uinu"
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
```

### What this code does

This script runs the ELT flow in order:

1. extract the raw data
2. load the raw tables into PostgreSQL
3. run SQL transformations inside PostgreSQL

### Why this matters

This runner shows the ELT architecture very clearly.

The raw data reaches PostgreSQL **before** transformation.

---

## 19. Step 15 - Run the ELT pipeline

### Your task

From the project root, run:

```bash id="9yegtx"
python src/run_elt.py
```

### What you should expect

If everything is correct, you should see:

```text id="fqc4nn"
ELT completed successfully. Raw data loaded and SQL transformations applied.
```

If you get an error, check:

* PostgreSQL connection settings
* table creation not executed yet
* invalid file paths
* source files missing
* SQL syntax problems
* Python import issues

This is a normal part of engineering work.

---

## 20. Step 16 - Validate the raw tables first

### Your task

Before checking the final table, inspect the raw tables in PostgreSQL.

Run:

```sql id="ffpqj4"
SELECT * FROM raw_customers LIMIT 10;
```

```sql id="g0k6zj"
SELECT * FROM raw_orders LIMIT 10;
```

```sql id="kuqnzs"
SELECT * FROM raw_products LIMIT 10;
```

### Why this matters

In ELT, the raw tables are an important part of the architecture.

You should confirm that the source data was preserved correctly before transformation.

This is realistic because many ELT workflows intentionally keep raw layers for traceability and reprocessing.

---

## 21. Step 17 - Validate the final reporting table

### Your task

Now inspect the final transformed result:

```sql id="muh0ji"
SELECT COUNT(*) FROM sales_report_elt;
```

```sql id="tc8cuj"
SELECT * FROM sales_report_elt LIMIT 10;
```

```sql id="o2x7mg"
SELECT category, SUM(total_amount) AS total_revenue
FROM sales_report_elt
GROUP BY category
ORDER BY total_revenue DESC;
```

```sql id="00syr8"
SELECT city, COUNT(*) AS total_orders
FROM sales_report_elt
GROUP BY city
ORDER BY total_orders DESC;
```

### Why this matters

The final reporting table is the business-ready result of the ELT pipeline.

You should confirm that:

* the joins worked
* the values are clean
* the totals make sense
* the business output is usable

---

## 22. Step 18 - Optional improvement: create a summary table

### Your task

If you want to extend the project a little, add another table for summaries.

In `sql/create_tables.sql`, add:

```sql id="ecl5ob"
CREATE TABLE IF NOT EXISTS category_summary_elt (
    category TEXT,
    total_revenue NUMERIC(10,2)
);
```

Then in `sql/elt_transform.sql`, after the main insert, add:

```sql id="7dfx4s"
DELETE FROM category_summary_elt;

INSERT INTO category_summary_elt (category, total_revenue)
SELECT category, SUM(total_amount)
FROM sales_report_elt
GROUP BY category;
```

### Why this helps

This makes the ELT project feel more like a real reporting workflow.

The detailed table supports row-level analysis, and the summary table supports business reporting.

---

## 23. Step 19 - What makes this ELT design realistic

This ELT pipeline reflects real engineering work because it includes:

* multiple raw source systems
* loading raw source data first
* preserving raw data in database tables
* transforming with SQL inside PostgreSQL
* using SQL-based joins and calculations
* creating final reporting-ready tables

This is very close to how modern ELT thinking works in many data platforms.

That is why this project should be taken seriously.

---

## 24. Step 20 - Compare ELT with ETL

### Your task

Now pause and compare the two pipeline styles.

### In ETL

* Python reads the raw files
* Python cleans and joins the data
* PostgreSQL receives the final clean result

### In ELT

* Python reads the raw files
* PostgreSQL receives the raw data first
* SQL inside PostgreSQL performs the cleaning and joining

### Why this matters

This comparison is the most important learning outcome of the whole mini-project.

Students should not only build both versions.
They should clearly understand **why** they are different.

---

## 25. Step 21 - Full code overview by file

At this stage, your ELT version should look roughly like this:

### `src/extract.py`

Contains:

* `read_customers_csv()`
* `read_orders_json()`
* `read_products_xml()`

### `src/load_postgres.py`

Contains:

* `get_connection()`
* `load_raw_customers()`
* `load_raw_orders()`
* `load_raw_products()`
* `run_sql_file()`

### `src/run_elt.py`

Contains:

* `main()`

### `sql/create_tables.sql`

Contains:

* `raw_customers`
* `raw_orders`
* `raw_products`
* `sales_report_elt`

### `sql/elt_transform.sql`

Contains:

* reset logic
* insert into `sales_report_elt`
* optional summary logic

This helps you see the project clearly.

---

## 26. Step 22 - What you should understand after finishing

By the end of this ELT part, you should understand that:

* ELT means load before transform
* PostgreSQL stores the raw source data first
* SQL performs the main transformation in this version
* the raw layer is intentionally preserved
* the pipeline order defines the architecture

That is the main learning goal.

---

## 27. Step 23 - Suggested ELT deliverables

By the end of the ELT version, you should have:

* working extraction code
* raw tables populated in PostgreSQL
* SQL transformation logic in `elt_transform.sql`
* a final `sales_report_elt` table
* validation SQL queries
* a clear understanding of why this is ELT

These are strong beginner-level ELT deliverables and reflect real engineering logic.

---

## 28. Final message

Treat this ELT pipeline like a real junior engineering task.

The goal is not only to make the code run.

The goal is to understand how data engineers can preserve raw data first, then transform it later inside the database using SQL.

That is a real and important architecture style.

By practicing both ETL and ELT, you are not just coding — you are learning how pipeline design decisions work.

---

## 29. Final comparison reminder

After completing both README 03 and README 04, you should be able to explain this clearly:

* In **ETL**, transformation happens before the final load.
* In **ELT**, loading happens first, and transformation happens afterward inside the target system.

If you understand that clearly, then this mini-project has already taught you something very important and very real.

---

## 30. What to do after finishing

Once you complete both pipeline versions, go back to the main project and review:

* the business problem
* the technical structure
* the ETL approach
* the ELT approach

That full picture is what makes this mini-project valuable.

It is not just about files and scripts.
It is about understanding how a data engineer solves a real business problem through pipeline design.

---

## 31. Submission, GitHub Workflow, and Checkpoint Questions

This mini-project is **mandatory**.

It is not only a classroom task.
It is a **capstone-style mini project** that represents an important step in your journey toward thinking and working like a real data engineer.

Please take this seriously.

The way you complete, organize, document, and submit this project will influence your next steps in this course, because this project brings together many of the most important ideas you have learned so far.

---

### Why this submission is important

You are required to complete this project in **your own public GitHub repository**.

Why?

Because this project is not only for today.

It can also become part of your future professional portfolio.

In future job interviews, technical screenings, internship applications, or junior data roles, it is very helpful to have a project that you can:

* show publicly
* explain clearly
* discuss with confidence
* use as proof that you understand real pipeline thinking

This is why we are asking you to place the project in your own GitHub account.

This helps you build not only technical practice, but also a visible professional project that you may present later.

Think of this as one of your first portfolio-ready data engineering projects.

---

### Submission requirement

Each student must:

* create their **own GitHub repository**
* make it **public**
* clone the **shared starter repository**
* connect that local project to their **own GitHub repository**
* push their work step by step as they complete the mini-project
* keep the repository organized and professional
* include the required README files
* answer the checkpoint questions

---

## 31.1 Create your own public GitHub repository

Create a new repository in your own GitHub account.

A good repository name could be:

```text
retail-sales-data-pipeline
```

or

```text
etl-elt-retail-mini-project
```

Make sure the repository is:

* **public**
* clearly named
* professional-looking

Do not use unclear names like:

* `test-repo`
* `project123`
* `new-folder-final`

Choose a clean and meaningful repository name.

That is part of professional practice.

---

## 31.2 Clone the shared starter repository

Your instructor will share a starter repository with you.

Clone that shared repository to your local machine.

Example:

```bash
git clone <SHARED_REPOSITORY_URL>
```

Then move into the project folder:

```bash
cd retail-sales-data-pipeline
```

---

## 31.3 Connect the local cloned project to your own GitHub repository

After cloning the shared project, you must connect the local repository to **your own public GitHub repository**.

One common approach is:

### First, rename the original remote

```bash
git remote rename origin upstream
```

This keeps the shared repository as a reference remote called `upstream`.

### Then add your own GitHub repository as the new origin

```bash
git remote add origin <YOUR_GITHUB_REPOSITORY_URL>
```

### Check your remotes

```bash
git remote -v
```

You should now see:

* `upstream` → the shared repository
* `origin` → your own GitHub repository

This is a very realistic Git workflow and a good habit to learn.

---

## 31.4 Push your work step by step

Do **not** wait until the whole project is finished to push once.

Instead, every time you complete an important step, you should:

1. add your changes
2. commit your changes
3. push your changes

Example:

```bash
git add .
git commit -m "Create project folder structure"
git push -u origin main
```

Then later, after another step:

```bash
git add .
git commit -m "Add ETL extraction functions"
git push
```

Then later:

```bash
git add .
git commit -m "Add ETL transformation logic"
git push
```

This is strongly recommended because it helps you:

* save your progress
* avoid losing work
* build a clear project history
* practice real development workflow

In real jobs, engineers do not usually finish everything first and then push once at the end.

---

## 31.5 Suggested commit style

Use clear commit messages.

Good examples:

* `Create project folder structure`
* `Add raw source files`
* `Add PostgreSQL table creation SQL`
* `Implement ETL extraction step`
* `Implement ETL transformation logic`
* `Implement ETL PostgreSQL loading`
* `Implement ELT raw table loading`
* `Add ELT SQL transformations`
* `Update README files`
* `Add checkpoint answers`

Avoid unclear commit messages like:

* `update`
* `new changes`
* `done`
* `final`
* `test`

A good commit message helps others understand your work.

That is a real engineering habit.

---

## 31.6 Required README files

Your repository must include the README structure explained earlier.

That means you should have:

* `README.md`
* `README_02_Technical_Structure.md`
* `README_03_ETL.md`
* `README_04_ELT.md`

These README files are not optional.

They are part of the project deliverables.

They help show that you can:

* explain a business problem
* organize a technical project
* describe an ETL pipeline
* describe an ELT pipeline

This is very important in real professional work.

A strong project is not only code.
A strong project is also clearly explained.

---

## 31.7 What to include in each README file

### Main `README.md`

This should include:

* project title
* business scenario
* why the project matters
* source data overview
* ETL and ELT overview
* links to the other README files
* why this project is realistic for a junior data engineer

### `README_02_Technical_Structure.md`

This should include:

* project folder structure
* explanation of each main folder
* explanation of each important script
* explanation of SQL files
* explanation of PostgreSQL tables
* explanation of the technical data flow

### `README_03_ETL.md`

This should include:

* ETL explanation
* ETL pipeline steps
* extraction logic
* transformation logic
* loading logic
* final target table explanation
* validation steps
* explanation of why this version is ETL

### `README_04_ELT.md`

This should include:

* ELT explanation
* raw loading logic
* raw PostgreSQL tables
* SQL transformation logic
* final reporting table explanation
* validation steps
* explanation of why this version is ELT

---

## 31.8 Submission checklist

Before submission, make sure your repository contains:

* your own public GitHub repository
* all project folders
* source data files
* Python scripts
* SQL files
* all required README files
* ETL implementation
* ELT implementation
* checkpoint answers
* regular commits showing progress

If one of these is missing, your submission is incomplete.

---

## 31.9 Mandatory checkpoint questions

Answer the following **five checkpoint questions** in your repository.

You can place your answers in a file such as:

```text
docs/checkpoint_answers.md
```

or inside a section in your main `README.md`.

### Checkpoint Question 1

**What is the main difference between ETL and ELT in this mini-project?**

### Checkpoint Question 2

**Why does the ETL version transform data in Python before loading it into PostgreSQL?**

### Checkpoint Question 3

**Why does the ELT version load raw data into PostgreSQL first before transforming it?**

### Checkpoint Question 4

**What are the three raw source files in this project, and what does each one represent in the business scenario?**

### Checkpoint Question 5

**Why is this project useful as a portfolio project for future job interviews?**

These checkpoint answers are required.

They are important because they help confirm that you do not only have code, but that you also understand the project and can explain it.

That ability matters a lot in interviews and real jobs.

---

## 31.10 Why this project can help you in interviews

This mini-project can become something you talk about later in interviews.

For example, you may be able to say:

* you built a local retail data pipeline
* you worked with CSV, JSON, and XML
* you used PostgreSQL
* you implemented both ETL and ELT
* you documented the business scenario and technical design
* you organized the project in GitHub professionally

That is already a strong beginner project story.

This is why your GitHub repository matters.

A project that is clean, public, documented, and understandable is much more valuable than code hidden only on your computer.

---

## 31.11 Final submission reminder

This mini-project is **very important and mandatory**.

It is not only about completing today’s class.

It is helping you build:

* technical pipeline thinking
* Git and GitHub workflow habits
* project documentation habits
* portfolio material for the future
* confidence in explaining your own work

Please treat it seriously and professionally.

Push your work step by step.
Document your project clearly.
Answer the checkpoint questions honestly.
And make sure your final repository is something you would be proud to show later.



