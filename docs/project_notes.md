# Project Notes

## Overview
This project builds a retail sales data pipeline using both ETL and ELT approaches.  
The data comes from three different source files: CSV, JSON, and XML.

The goal of the project is to combine these datasets and produce a final sales reporting table in PostgreSQL.



## Source Data Observations

While working with the raw files, I noticed some common data quality issues:

- Some customer names had extra spaces.
- Some names were written in uppercase or lowercase inconsistently.
- One customer record had an empty city value.
- Some numeric values in the raw data needed type conversion.

These issues are typical examples of real-world raw data problems.


## Data Cleaning Decisions

During the ETL process, the data was cleaned in Python before loading into PostgreSQL.

Some cleaning steps included:

- Removing extra spaces using trim functions
- Standardizing text format using capitalization
- Converting numeric fields to the correct data types
- Skipping invalid rows that could break the pipeline



## ETL Pipeline Notes

In the ETL pipeline:

1. Data is extracted from CSV, JSON, and XML files using Python.
2. Data is cleaned and transformed in Python.
3. The final cleaned dataset is loaded into PostgreSQL as a reporting table.

This approach ensures that the database only receives clean data.



## ELT Pipeline Notes

In the ELT pipeline:

1. Raw data is extracted from the files.
2. Raw records are loaded directly into PostgreSQL raw tables.
3. SQL transformations are executed inside PostgreSQL to clean and join the data.
4. A final reporting table is generated from the SQL transformation.

This approach preserves the raw data in the database.



## Key Learning Points

From this project, I learned:

- How ETL and ELT pipelines are different.
- How to read CSV, JSON, and XML files using Python.
- How to load and query data in PostgreSQL.
- How to structure a data engineering project with folders, scripts, and SQL files.
- How to document a project clearly for GitHub.



## Final Thoughts

This project helped me understand how a real data engineering pipeline works from raw data to final reporting tables.  
It also showed the importance of organizing code, SQL, and documentation in a professional way.