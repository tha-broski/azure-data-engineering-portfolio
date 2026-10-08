PRIMARY_KEYS = {
    "address": ["AddressID"],
    "customer": ["CustomerID"],
    "customeraddress": ["CustomerID", "AddressID"],
    "product": ["ProductID"],
    "productcategory": ["ProductCategoryID"],
    "productdescription": ["ProductDescriptionID"],
    "productmodel": ["ProductModelID"],
    "productmodelproductdescription": [
        "ProductModelID",
        "ProductDescriptionID",
        "Culture"
    ],
    "salesorderdetail": ["SalesOrderID", "SalesOrderDetailID"],
    "salesorderheader": ["SalesOrderID"]
}