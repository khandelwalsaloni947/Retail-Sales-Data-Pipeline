# Checkpoint Answers

## Question 1
What is the main difference between ETL and ELT in this mini-project?

The main difference is when the data transformation happens.  
In the ETL pipeline, the data is extracted from the files and then cleaned and transformed in Python before it is loaded into PostgreSQL.  
In the ELT pipeline, the raw data is first loaded into PostgreSQL and the transformation happens later using SQL inside the database.



## Question 2
Why does the ETL version transform data in Python before loading it into PostgreSQL?

In the ETL version, Python is responsible for cleaning and preparing the data before sending it to the database.  
This includes fixing formatting issues, joining the datasets, and calculating values like the total amount.  
After the data is cleaned and structured, it is loaded into PostgreSQL as the final table.



## Question 3
Why does the ELT version load raw data into PostgreSQL first before transforming it?

In the ELT version, the raw data is loaded into PostgreSQL first so that the original data is preserved.  
Then the transformation is done later using SQL queries inside the database.  
This approach allows the database to handle the data processing and makes it easier to reuse the raw data if needed.



## Question 4
What are the three raw source files in this project, and what does each one represent in the business scenario?

There are three raw source files in this project:

customers.csv – contains information about customers such as their name, city, and signup date.  

orders.json – contains order transaction data like which customer bought which product and the quantity.  

products.xml – contains product details such as product name, category, and price.

Together these files represent the basic data of a retail sales system.



## Question 5
Why is this project useful as a portfolio project for future job interviews?

This project is useful because it shows important data engineering skills.  
It demonstrates how to work with different file formats like CSV, JSON, and XML, how to build ETL and ELT pipelines, and how to use PostgreSQL for storing and transforming data.  
It also shows that the project is organized in GitHub with proper documentation, which is something employers like to see.