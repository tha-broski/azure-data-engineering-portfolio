CREATE OR REFRESH MATERIALIZED VIEW
dbw_data_engineering_portfolio_dev.gold.fact_sales (
    SalesOrderID INT NOT NULL,
    SalesOrderDetailID INT NOT NULL,
    CustomerID INT,
    ProductID INT,
    OrderDateKey INT,
    DueDateKey INT,
    ShipDateKey INT,
    ShipToAddressID INT,
    BillToAddressID INT,
    OrderQty INT,
    UnitPrice DECIMAL(19,4),
    UnitPriceDiscount DECIMAL(19,4),
    LineTotal DECIMAL(38,6),

    CONSTRAINT fact_sales_pk
        PRIMARY KEY (SalesOrderID, SalesOrderDetailID),

    CONSTRAINT fact_sales_product_fk
        FOREIGN KEY (ProductID)
        REFERENCES dbw_data_engineering_portfolio_dev.gold.dim_product(ProductID),

    CONSTRAINT fact_sales_customer_fk
        FOREIGN KEY (CustomerID)
        REFERENCES dbw_data_engineering_portfolio_dev.gold.dim_customer(CustomerID),

    CONSTRAINT fact_sales_order_date_fk
        FOREIGN KEY (OrderDateKey)
        REFERENCES dbw_data_engineering_portfolio_dev.gold.dim_date(DateKey),

    CONSTRAINT fact_sales_due_date_fk
        FOREIGN KEY (DueDateKey)
        REFERENCES dbw_data_engineering_portfolio_dev.gold.dim_date(DateKey),

    CONSTRAINT fact_sales_ship_date_fk
        FOREIGN KEY (ShipDateKey)
        REFERENCES dbw_data_engineering_portfolio_dev.gold.dim_date(DateKey),

    CONSTRAINT fact_sales_ship_address_fk
        FOREIGN KEY (ShipToAddressID)
        REFERENCES dbw_data_engineering_portfolio_dev.gold.dim_address(AddressID),

    CONSTRAINT fact_sales_bill_address_fk
        FOREIGN KEY (BillToAddressID)
        REFERENCES dbw_data_engineering_portfolio_dev.gold.dim_address(AddressID)
)
AS
SELECT
    d.SalesOrderID,
    d.SalesOrderDetailID,
    h.CustomerID,
    d.ProductID,
    CAST(DATE_FORMAT(h.OrderDate, 'yyyyMMdd') AS INT) AS OrderDateKey,
    CAST(DATE_FORMAT(h.DueDate, 'yyyyMMdd') AS INT) AS DueDateKey,
    CAST(DATE_FORMAT(h.ShipDate, 'yyyyMMdd') AS INT) AS ShipDateKey,
    h.ShipToAddressID,
    h.BillToAddressID,
    d.OrderQty,
    d.UnitPrice,
    d.UnitPriceDiscount,
    d.LineTotal
FROM dbw_data_engineering_portfolio_dev.silver.salesorderdetail d
JOIN dbw_data_engineering_portfolio_dev.silver.salesorderheader h
    ON d.SalesOrderID = h.SalesOrderID;

CREATE OR REFRESH MATERIALIZED VIEW
dbw_data_engineering_portfolio_dev.gold.dim_product_category(
    ProductCategoryID INT NOT NULL,
    ParentProductCategoryID INT,
    Name STRING,

    CONSTRAINT dim_product_category_pk
        PRIMARY KEY (ProductCategoryID)
)
AS
SELECT
    ProductCategoryID,
    ParentProductCategoryID,
    Name
FROM dbw_data_engineering_portfolio_dev.silver.productcategory;

CREATE OR REFRESH MATERIALIZED VIEW
dbw_data_engineering_portfolio_dev.gold.dim_product_model(
    ProductModelID INT NOT NULL,
    Name STRING,

    CONSTRAINT dim_product_model_pk
        PRIMARY KEY (ProductModelID)
)
AS
SELECT
    ProductModelID,
    Name
FROM dbw_data_engineering_portfolio_dev.silver.productmodel;

CREATE OR REFRESH MATERIALIZED VIEW
dbw_data_engineering_portfolio_dev.gold.dim_product (
    ProductID INT NOT NULL,
    Name STRING,
    ProductNumber STRING,
    Color STRING,
    StandardCost DECIMAL(19,4),
    ListPrice DECIMAL(19,4),
    Size STRING,
    Weight DECIMAL(8,2),
    ProductCategoryID INT,
    ProductModelID INT,
    SellStartDate TIMESTAMP,
    SellEndDate TIMESTAMP,
    DiscontinuedDate TIMESTAMP,

    CONSTRAINT dim_product_pk
        PRIMARY KEY (ProductID),

    CONSTRAINT dim_product_category_fk
        FOREIGN KEY (ProductCategoryID)
        REFERENCES dbw_data_engineering_portfolio_dev.gold.dim_product_category(ProductCategoryID),

    CONSTRAINT dim_product_model_fk
        FOREIGN KEY (ProductModelID)
        REFERENCES dbw_data_engineering_portfolio_dev.gold.dim_product_model(ProductModelID)
)
AS
SELECT
    ProductID,
    Name,
    ProductNumber,
    Color,
    StandardCost,
    ListPrice,
    Size,
    Weight,
    ProductCategoryID,
    ProductModelID,
    SellStartDate,
    SellEndDate,
    DiscontinuedDate
FROM dbw_data_engineering_portfolio_dev.silver.product;

CREATE OR REFRESH MATERIALIZED VIEW
dbw_data_engineering_portfolio_dev.gold.dim_customer(
    CustomerID INT NOT NULL,
    Title STRING,
    FirstName STRING,
    MiddleName STRING,
    LastName STRING,
    Suffix STRING,
    CompanyName STRING,
    SalesPerson STRING,
    EmailAddress STRING,
    Phone STRING,

    CONSTRAINT dim_customer_pk
        PRIMARY KEY (CustomerID)
)
AS
SELECT
    CustomerID,
    Title,
    FirstName,
    MiddleName,
    LastName,
    Suffix,
    CompanyName,
    SalesPerson,
    EmailAddress,
    Phone
FROM dbw_data_engineering_portfolio_dev.silver.customer;

CREATE OR REFRESH MATERIALIZED VIEW
dbw_data_engineering_portfolio_dev.gold.dim_address(
    AddressID INT NOT NULL,
    AddressLine1 STRING,
    AddressLine2 STRING,
    City STRING,
    StateProvince STRING,
    CountryRegion STRING,
    PostalCode STRING,

    CONSTRAINT dim_address_pk
        PRIMARY KEY (AddressID)
)
AS
SELECT
    AddressID,
    AddressLine1,
    AddressLine2,
    City,
    StateProvince,
    CountryRegion,
    PostalCode
FROM dbw_data_engineering_portfolio_dev.silver.address;

CREATE OR REFRESH MATERIALIZED VIEW
dbw_data_engineering_portfolio_dev.gold.bridge_customer_address(
    CustomerID INT NOT NULL,
    AddressID INT NOT NULL,
    AddressType STRING,

    CONSTRAINT bridge_customer_address_pk
        PRIMARY KEY (CustomerID, AddressID),

    CONSTRAINT bridge_customer_fk
        FOREIGN KEY (CustomerID)
        REFERENCES dbw_data_engineering_portfolio_dev.gold.dim_customer(CustomerID),

    CONSTRAINT bridge_address_fk
        FOREIGN KEY (AddressID)
        REFERENCES dbw_data_engineering_portfolio_dev.gold.dim_address(AddressID)
)
AS
SELECT
    CustomerID,
    AddressID,
    AddressType
FROM dbw_data_engineering_portfolio_dev.silver.customeraddress;

CREATE OR REFRESH MATERIALIZED VIEW
dbw_data_engineering_portfolio_dev.gold.dim_date(
    DateKey INT NOT NULL,
    FullDate DATE,
    Year INT,
    Quarter INT,
    Month INT,
    MonthName STRING,
    Day INT,
    DayOfWeek INT,
    DayOfWeekName STRING,

    CONSTRAINT dim_date_pk
        PRIMARY KEY (DateKey)
)
AS

WITH date_bounds AS (
    SELECT
        CAST(MIN(OrderDate) AS DATE) AS min_date,
        CAST(MAX(OrderDate) AS DATE) AS max_date
    FROM dbw_data_engineering_portfolio_dev.silver.salesorderheader
),

dates AS (
    SELECT
        EXPLODE(
            SEQUENCE(
                min_date,
                max_date,
                INTERVAL 1 DAY
            )
        ) AS FullDate
    FROM date_bounds
)

SELECT
    CAST(DATE_FORMAT(FullDate, 'yyyyMMdd') AS INT) AS DateKey,
    FullDate,
    YEAR(FullDate) AS Year,
    QUARTER(FullDate) AS Quarter,
    MONTH(FullDate) AS Month,
    DATE_FORMAT(FullDate, 'MMMM') AS MonthName,
    DAY(FullDate) AS Day,
    DAYOFWEEK(FullDate) AS DayOfWeek,
    DATE_FORMAT(FullDate, 'EEEE') AS DayOfWeekName
FROM dates;