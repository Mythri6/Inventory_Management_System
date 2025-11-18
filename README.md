# Inventory_Management_System

_A Python + MySQL desktop application with login roles, orders, triggers, stored procedures, and a full GUI._

**Overview**

This project is a full-fledged Inventory Management System built using Python (Tkinter) and MySQL.
It handles products, suppliers, customers, orders, stock reports, DB triggers, stored procedures and gives different UI access depending on user roles (Admin / Manager / Staff).

**Tech Stack**

Python — Tkinter for GUI
MySQL — database, stored procedures, functions, triggers
mysql-connector-python — DB connectivity
SQL — everything from table creation to complex queries

**Features**

**1.Authentication**

Login + Registration system
Role-based access :
    Admin: full control
    Manager: limited deletes
    Staff: view-only for sensitive operations

**Product Management**

Add / update / delete products
Delete by product ID or name
Search & reload product list
View stock level via SQL function
Total stock value via stored function

**Orders**
    **Sales Orders**
         Adds order, updates stock
         Logged using trigger
         Uses stored procedure AddSalesOrder
      **Purchase Orders**
         Adds purchase, increases stock
         Uses stored procedure AddPurchaseOrder


**Reports & Queries**

Aggregate reports (total products, avg selling price, revenue…)
Customer purchase summary
JOIN queries
Nested queries
Low stock items

**Database Logic**

   **Stored Procedures**
        AddSalesOrder()
        AddPurchaseOrder()
   **Functions**
        GetTotalStockValue()
        CheckStockLevel()
        GetTotalSalesAmountByCustomer()
   **Triggers**
        AfterSalesOrderInsert → logs sales
        PreventNegativeStock → prevents invalid updates

**Project Structure**

Inventory_Management_System/
│── inventory_gui.py        # Main Python GUI app
│── inventory_sql.sql       # Database schema + sample data + triggers/SPs
│── README.md

**Setup Instructions**

**1. Install Dependencies**
$pip install mysql-connector-python

**2. Import the SQL File**
Open MySQL and run:
$SOURCE inventory_sql.sql;

This creates:
    All tables
    Sample data
    Triggers + procedures + functions

**3. Update DB Credentials (if needed)**

Inside inventory_gui.py → update:

$host=""
$user=""
$password=""

**4. Run the Application**
$python inventory_gui.py

**Default Roles**
You can create new users through the Register page.
Roles: Admin, Manager, Staff


