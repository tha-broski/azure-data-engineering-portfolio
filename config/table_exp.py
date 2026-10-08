EXPECTATIONS = {
    "product": {
        "non_negative_list_price": "ListPrice >= 0",
        "non_negative_standard_cost": "StandardCost >= 0"
    },
    "salesorderdetail": {
        "positive_order_quantity": "OrderQty > 0",
        "non_negative_unit_price": "UnitPrice >= 0"
    },
    "salesorderheader": {
        "non_negative_subtotal": "SubTotal >= 0",
        "non_negative_total_due": "TotalDue >= 0"
    }
}