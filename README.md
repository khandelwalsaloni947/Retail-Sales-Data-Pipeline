# Retail Sales Data Pipeline Project

## Real-World Data Engineering Mini Project

Welcome to this project.

This repository contains a **beginner-friendly but realistic data engineering mini project** designed to simulate the type of work a **junior data engineer** may receive in a real company.

This is not just a coding exercise.
It is a small professional-style project based on a realistic business situation in the **retail / e-commerce sector**, where data comes from multiple systems and must be prepared for reporting and business use.

In this project, you will work with raw business data from different file formats and understand how a data engineer organizes, processes, and prepares that data through both:

* **ETL**
* **ELT**

---

# Project Purpose

The goal of this project is to help you understand how real data engineering work begins.

In many real companies, data engineers do not start with one perfect clean table.
Instead, they often receive:

* separate files from different systems
* different formats such as CSV, JSON, and XML
* inconsistent or messy data
* business requests that require clean final outputs

Your task in this project is to experience that process in a simplified but realistic way.

You will act as a **junior data engineer** working on a local pipeline project for a retail company.

---

# Business Scenario

Imagine you have joined a retail company as a junior data engineer.

The company uses different internal systems for different types of data:

* a CRM system for customer information
* an ordering system for online purchases
* a product system for catalog data

Because these systems are different, the company exports data into separate files instead of one ready-made reporting table.

The business team now wants usable data to answer questions such as:

* Which customers placed orders?
* Which products were sold?
* Which categories generated the most revenue?
* Which cities had the most activity?
* Which records contain missing or problematic values?

At the moment, the raw files are not ready for direct reporting.

That is where your work begins.

---

# Your Role

In this project, you are working as a:

## **Junior Data Engineer**

Your responsibility is to help transform raw business data into useful reporting-ready data.

That means you will need to:

* understand the source files
* think about pipeline structure
* organize your project clearly
* build technical steps carefully
* and understand the difference between ETL and ELT

This is exactly the kind of mindset that matters in real data engineering work.

---

# Why This Project Matters

This project is designed to help you practice both **technical thinking** and **professional thinking**.

Even though this is a learning project, it reflects real engineering situations such as:

* receiving raw files from multiple systems
* dealing with mixed formats
* handling imperfect data
* building structured pipelines
* preparing final outputs for business use

Please take this project seriously.

The more seriously you treat it, the more value you will get from it.

This is your opportunity to practice something close to real workplace data engineering in a safe and guided way.

---

# Source Data Overview

The project is based on three source files from three different systems:

* **customers.csv** → customer information
* **orders.json** → order transactions
* **products.xml** → product catalog data

This is realistic because real businesses often store and export data in different formats depending on the system.

The source data may also contain realistic issues such as:

* missing values
* duplicate rows
* inconsistent formatting
* extra spaces
* invalid values
* mismatched records

That is intentional, because real data engineering work is rarely perfectly clean.

---

# What You Will Build

This project includes **two pipeline approaches**:

## 1. ETL Pipeline

You will work on a version where data is:

* **Extracted**
* **Transformed**
* **Loaded**

This means the data is cleaned or adjusted before loading into the target system.

## 2. ELT Pipeline

You will also work on a version where data is:

* **Extracted**
* **Loaded**
* **Transformed**

This means raw data is loaded first, and transformation happens later inside the target system.

By working on both versions, you will understand one of the most important foundational ideas in data engineering.

---

# Why This Feels Like Real Work

A junior data engineer is often asked to do work like this:

* receive files from different sources
* understand the structure of the data
* prepare it for business use
* create clean outputs
* organize the work properly
* explain the technical approach clearly

That is exactly the spirit of this project.

So while this repository is beginner-friendly, the project itself is built to feel like a real assignment from a data team.

---

# Project Guide

This repository is organized into multiple README files so that you can move through the project step by step.

Please read them in order.

## Documentation Files

* [README 02 - Technical Data Engineering Structure](./README_02_Technical_Structure.md)
* [README 03 - ETL Pipeline Guide](./README_03_ETL.md)
* [README 04 - ELT Pipeline Guide](./README_04_ELT.md)

---

# How to Use This Repository

Start with this main README first.

This file gives you:

* the business context
* the project scenario
* the purpose of the work
* the mindset you should have while doing the project

Then continue with the technical READMEs:

* **README 02** explains the engineering structure of the project
* **README 03** walks you through the ETL version
* **README 04** walks you through the ELT version

The technical READMEs are **guided**, which means they do not just describe tasks.
They also help you build the solution step by step.

---

# What Success Looks Like

A successful project means that you can:

* understand the business need
* work with the raw source files
* follow the project structure correctly
* build both ETL and ELT versions
* produce a clean final result
* explain the difference between ETL and ELT clearly

Success is not only about making the code run.

Success also means understanding:

* what problem the company is trying to solve
* why pipeline design matters
* and how data engineering supports real business decisions

---

# Final Note

Treat this project like your first small professional data engineering assignment.

Be organized.
Read carefully.
Think step by step.
And remember that the goal is not only to complete tasks, but to start thinking like a data engineer.

This project is designed to help you build that mindset.


