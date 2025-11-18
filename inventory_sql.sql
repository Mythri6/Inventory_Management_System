-- Create the database for the Inventory Management System
CREATE DATABASE IF NOT EXISTS InventoryManagementSystem;

-- Select the newly created database to work with
USE InventoryManagementSystem;

-- =================================================================
--                  TABLE CREATION
-- =================================================================

-- Create the Suppliers table
-- This table stores information about product suppliers.
CREATE TABLE Suppliers (
    SupplierID INT PRIMARY KEY AUTO_INCREMENT,
    SupplierName VARCHAR(255) NOT NULL,
    Phone VARCHAR(20),
    Email VARCHAR(255) UNIQUE,
    Address TEXT
);

-- Create the Employees table
-- This table stores information about employees who manage orders.
CREATE TABLE Employees (
    EmployeeID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255) NOT NULL,
    Role VARCHAR(100)
);

-- Create the Customers table
-- This table stores information about customers who place sales orders.
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255) NOT NULL,
    Phone VARCHAR(20),
    Email VARCHAR(255) UNIQUE,
    Address TEXT
);

-- Create the Products table
-- This table holds all product details. It references the Suppliers table.
CREATE TABLE Products (
    ProductID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255) NOT NULL,
    Category VARCHAR(100),
    CostPrice DECIMAL(10, 2) NOT NULL,
    SellingPrice DECIMAL(10, 2) NOT NULL,
    Quantity INT NOT NULL DEFAULT 0,
    SupplierID INT,
    FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID) ON DELETE SET NULL
);

-- Create the PurchaseOrders table
-- This table stores header information for orders placed with suppliers.
CREATE TABLE PurchaseOrders (
    POID INT PRIMARY KEY AUTO_INCREMENT,
    OrderDate DATE NOT NULL,
    ExpectedDeliveryDate DATE,
    Status VARCHAR(50) DEFAULT 'Pending',
    SupplierID INT,
    EmployeeID INT,
    FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID) ON DELETE RESTRICT,
    FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID) ON DELETE SET NULL
);

-- Create the SalesOrders table
-- This table stores header information for sales orders from customers.
CREATE TABLE SalesOrders (
    SOID INT PRIMARY KEY AUTO_INCREMENT,
    OrderDate DATE NOT NULL,
    ExpectedDeliveryDate DATE,
    Status VARCHAR(50) DEFAULT 'Pending',
    CustomerID INT,
    EmployeeID INT,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID) ON DELETE RESTRICT,
    FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID) ON DELETE SET NULL
);

-- Create the PurchaseOrderDetails table
-- This is a junction table linking PurchaseOrders and Products.
-- It details which products were in each purchase order.
CREATE TABLE PurchaseOrderDetails (
    POID INT,
    ProductID INT,
    Quantity INT NOT NULL,
    CostPrice DECIMAL(10, 2) NOT NULL, -- Price at the time of purchase
    PRIMARY KEY (POID, ProductID),
    FOREIGN KEY (POID) REFERENCES PurchaseOrders(POID) ON DELETE CASCADE,
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID) ON DELETE RESTRICT
);

-- Create the SalesOrderDetails table
-- This is a junction table linking SalesOrders and Products.
-- It details which products were in each sales order.
CREATE TABLE SalesOrderDetails (
    SOID INT,
    ProductID INT,
    Quantity INT NOT NULL,
    UnitPrice DECIMAL(10, 2) NOT NULL, -- Price at the time of sale
    PRIMARY KEY (SOID, ProductID),
    FOREIGN KEY (SOID) REFERENCES SalesOrders(SOID) ON DELETE CASCADE,
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID) ON DELETE RESTRICT
);
-- =============================================================
--   INSERT SAMPLE DATA FOR INVENTORY MANAGEMENT SYSTEM
-- =============================================================

--Suppliers
INSERT INTO Suppliers (SupplierName, Phone, Email, Address)
VALUES
('TechSource Pvt Ltd', '9876543210', 'techsource@gmail.com', 'Bangalore'),
('Alpha Distributors', '9823456781', 'alpha_distributors@gmail.com', 'Hyderabad'),
('SmartSupplies Ltd', '9898123456', 'smart_supplies@gmail.com', 'Chennai'),
('Vision Traders', '9723456789', 'visiontraders@gmail.com', 'Delhi'),
('OmniTech Supply Co.', '9988776655', 'omnitech@gmail.com', 'Mumbai'),
('Prime Components', '9090909090', 'primecomponents@gmail.com', 'Kolkata');

-- Employees
INSERT INTO Employees (Name, Role)
VALUES
('John Doe', 'Manager'),
('Priya Sharma', 'Sales Executive'),
('Rahul Mehta', 'Inventory Clerk'),
('Sneha Iyer', 'Procurement Officer'),
('Vikram Singh', 'Warehouse Staff'),
('Anita Das', 'Accountant');

-- Customers
INSERT INTO Customers (Name, Phone, Email, Address)
VALUES
('Ravi Kumar', '9001234567', 'ravi.kumar@gmail.com', 'Hyderabad'),
('Ananya Gupta', '9898989898', 'ananya.gupta@gmail.com', 'Pune'),
('Deepak Sharma', '9876501234', 'deepak.sharma@gmail.com', 'Delhi'),
('Sonal Patel', '9823409876', 'sonal.patel@gmail.com', 'Ahmedabad'),
('Krishna Nair', '9934567890', 'krishna.nair@gmail.com', 'Kochi'),
('Nikhil Verma', '9944556677', 'nikhil.verma@gmail.com', 'Bangalore');

-- Products
INSERT INTO Products (Name, Category, CostPrice, SellingPrice, Quantity, SupplierID)
VALUES
('Wireless Mouse', 'Accessories', 350.00, 550.00, 80, 1),
('Mechanical Keyboard', 'Accessories', 1200.00, 1600.00, 40, 1),
('HD Monitor', 'Display', 6500.00, 7500.00, 25, 2),
('External Hard Drive', 'Storage', 3000.00, 3600.00, 60, 3),
('USB-C Cable', 'Cables', 120.00, 200.00, 200, 4),
('Laptop Stand', 'Accessories', 800.00, 1100.00, 90, 5);

-- PurchaseOrders
INSERT INTO PurchaseOrders (OrderDate, ExpectedDeliveryDate, Status, SupplierID, EmployeeID)
VALUES
('2025-09-01', '2025-09-05', 'Received', 1, 4),
('2025-09-03', '2025-09-07', 'Received', 2, 4),
('2025-09-10', '2025-09-14', 'Pending', 3, 4),
('2025-09-15', '2025-09-20', 'Received', 4, 3),
('2025-09-20', '2025-09-25', 'Pending', 5, 3),
('2025-09-25', '2025-09-30', 'Shipped', 6, 3);

-- PurchaseOrderDetails
INSERT INTO PurchaseOrderDetails (POID, ProductID, Quantity, CostPrice)
VALUES
(1, 1, 50, 350.00),
(1, 2, 30, 1200.00),
(2, 3, 10, 6500.00),
(3, 4, 40, 3000.00),
(4, 5, 100, 120.00),
(5, 6, 60, 800.00);

-- SalesOrders
INSERT INTO SalesOrders (OrderDate, ExpectedDeliveryDate, Status, CustomerID, EmployeeID)
VALUES
('2025-09-05', '2025-09-10', 'Delivered', 1, 2),
('2025-09-08', '2025-09-13', 'Delivered', 2, 2),
('2025-09-12', '2025-09-16', 'Pending', 3, 5),
('2025-09-18', '2025-09-23', 'Shipped', 4, 5),
('2025-09-22', '2025-09-27', 'Pending', 5, 2),
('2025-09-28', '2025-10-02', 'Delivered', 6, 1);

-- SalesOrderDetails
INSERT INTO SalesOrderDetails (SOID, ProductID, Quantity, UnitPrice)
VALUES
(1, 1, 5, 550.00),
(1, 2, 3, 1600.00),
(2, 3, 1, 7500.00),
(3, 4, 2, 3600.00),
(4, 5, 10, 200.00),
(5, 6, 4, 1100.00);


SELECT * FROM Suppliers;
SELECT * FROM Employees;
SELECT * FROM Customers;
SELECT * FROM Products;
SELECT * FROM PurchaseOrders;
SELECT * FROM PurchaseOrderDetails;
SELECT * FROM SalesOrders;
SELECT * FROM SalesOrderDetails;


DELIMITER //
CREATE PROCEDURE AddSalesOrder(
    IN p_customerID INT,
    IN p_employeeID INT,
    IN p_productID INT,
    IN p_quantity INT
)
BEGIN
    DECLARE p_price DECIMAL(10,2);
    SELECT SellingPrice INTO p_price FROM Products WHERE ProductID = p_productID;

    INSERT INTO SalesOrders (OrderDate, ExpectedDeliveryDate, Status, CustomerID, EmployeeID)
    VALUES (CURDATE(), DATE_ADD(CURDATE(), INTERVAL 5 DAY), 'Pending', p_customerID, p_employeeID);

    SET @soid = LAST_INSERT_ID();

    INSERT INTO SalesOrderDetails (SOID, ProductID, Quantity, UnitPrice)
    VALUES (@soid, p_productID, p_quantity, p_price);

    UPDATE Products SET Quantity = Quantity - p_quantity WHERE ProductID = p_productID;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE AddPurchaseOrder(
    IN p_supplierID INT,
    IN p_employeeID INT,
    IN p_productID INT,
    IN p_quantity INT
)
BEGIN
    DECLARE p_cost DECIMAL(10,2);
    SELECT CostPrice INTO p_cost FROM Products WHERE ProductID = p_productID;

    INSERT INTO PurchaseOrders (OrderDate, ExpectedDeliveryDate, Status, SupplierID, EmployeeID)
    VALUES (CURDATE(), DATE_ADD(CURDATE(), INTERVAL 7 DAY), 'Pending', p_supplierID, p_employeeID);

    SET @poid = LAST_INSERT_ID();

    INSERT INTO PurchaseOrderDetails (POID, ProductID, Quantity, CostPrice)
    VALUES (@poid, p_productID, p_quantity, p_cost);

    UPDATE Products SET Quantity = Quantity + p_quantity WHERE ProductID = p_productID;
END //
DELIMITER ;

DELIMITER //
CREATE FUNCTION GetTotalStockValue()
RETURNS DECIMAL(15,2)
DETERMINISTIC
BEGIN
    DECLARE total_value DECIMAL(15,2);
    SELECT SUM(Quantity * CostPrice) INTO total_value FROM Products;
    RETURN total_value;
END //
DELIMITER ;

DELIMITER //
CREATE FUNCTION CheckStockLevel(p_productID INT)
RETURNS VARCHAR(50)
DETERMINISTIC
BEGIN
    DECLARE stock INT;
    SELECT Quantity INTO stock FROM Products WHERE ProductID = p_productID;
    IF stock < 10 THEN
        RETURN 'Low Stock';
    ELSEIF stock BETWEEN 10 AND 50 THEN
        RETURN 'Moderate Stock';
    ELSE
        RETURN 'In Stock';
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE FUNCTION GetTotalSalesAmountByCustomer(p_customerID INT)
RETURNS DECIMAL(15,2)
DETERMINISTIC
BEGIN
    DECLARE total_amount DECIMAL(15,2);

    SELECT SUM(sod.Quantity * sod.UnitPrice) INTO total_amount
    FROM SalesOrders so
    JOIN SalesOrderDetails sod ON so.SOID = sod.SOID
    WHERE so.CustomerID = p_customerID;

    RETURN IFNULL(total_amount, 0);
END //
DELIMITER ;

CREATE TABLE IF NOT EXISTS SalesLog (
    LogID INT AUTO_INCREMENT PRIMARY KEY,
    ProductID INT,
    Quantity INT,
    ActionTime DATETIME,
    Message VARCHAR(255)
);

DELIMITER //
CREATE TRIGGER AfterSalesOrderInsert
AFTER INSERT ON SalesOrderDetails
FOR EACH ROW
BEGIN
    INSERT INTO SalesLog (ProductID, Quantity, ActionTime, Message)
    VALUES (NEW.ProductID, NEW.Quantity, NOW(),
            CONCAT('Sold ', NEW.Quantity, ' units of Product ID ', NEW.ProductID));
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER PreventNegativeStock
BEFORE UPDATE ON Products
FOR EACH ROW
BEGIN
    IF NEW.Quantity < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Stock cannot go below zero.';
    END IF;
END //
DELIMITER ;

CALL AddSalesOrder(1, 2, 1, 3);
SELECT * FROM SalesOrderDetails;
SELECT * FROM Products;
SELECT GetTotalStockValue() AS TotalInventoryValue;
SELECT Name, CheckStockLevel(ProductID) AS StockStatus FROM Products;
INSERT INTO SalesOrderDetails (SOID, ProductID, Quantity, UnitPrice)
VALUES (6, 2, 5, 1600.00);
SELECT * FROM SalesLog;
UPDATE Products SET Quantity = -5 WHERE ProductID = 1;


SELECT COUNT(*) AS TotalProducts
FROM Products;

SELECT SUM(Quantity) AS TotalQuantityInStock
FROM Products;

SELECT AVG(SellingPrice) AS AverageSellingPrice
FROM Products;

SELECT SUM(Quantity * UnitPrice) AS TotalRevenue
FROM SalesOrderDetails;

SELECT Category ,SUM(Quantity * CostPrice) AS TotalStockValue
FROM Products
GROUP BY Category;

SELECT p.ProductID, p.Name AS ProductName, p.Category, 
       s.SupplierName, s.Phone
FROM Products p
JOIN Suppliers s ON p.SupplierID = s.SupplierID;

SELECT so.SOID, c.Name AS CustomerName, e.Name AS EmployeeName, 
       so.OrderDate, so.Status
FROM SalesOrders so
JOIN Customers c ON so.CustomerID = c.CustomerID
JOIN Employees e ON so.EmployeeID = e.EmployeeID;

SELECT po.POID, s.SupplierName, p.Name AS ProductName, 
       pod.Quantity, pod.CostPrice
FROM PurchaseOrders po
JOIN Suppliers s ON po.SupplierID = s.SupplierID
JOIN PurchaseOrderDetails pod ON po.POID = pod.POID;

SELECT c.Name AS CustomerName,
       SUM(sod.Quantity) AS TotalItemsBought,
       SUM(sod.Quantity * sod.UnitPrice) AS TotalSpent
FROM Customers c
JOIN SalesOrders so ON c.CustomerID = so.CustomerID
JOIN SalesOrderDetails sod ON so.SOID = sod.SOID
GROUP BY c.CustomerID;

SELECT Name, Quantity
FROM Products
WHERE Quantity > (SELECT AVG(Quantity) FROM Products);

SELECT Name
FROM Customers
WHERE CustomerID IN (SELECT CustomerID FROM SalesOrders);

SELECT Name
FROM Products
WHERE ProductID NOT IN (SELECT ProductID FROM SalesOrderDetails);

SELECT SupplierName
FROM Suppliers
WHERE SupplierID = (
    SELECT SupplierID
    FROM Products
    GROUP BY SupplierID
    ORDER BY COUNT(ProductID) DESC
    LIMIT 1
);

SELECT c.Name,
       GetTotalSalesAmountByCustomer(c.CustomerID) AS TotalSpent
FROM Customers c
WHERE GetTotalSalesAmountByCustomer(c.CustomerID) > (
    SELECT AVG(GetTotalSalesAmountByCustomer(CustomerID)) 
    FROM Customers
);


-- should throw error










