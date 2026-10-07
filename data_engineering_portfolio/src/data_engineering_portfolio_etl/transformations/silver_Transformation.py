from pyspark import pipelines as dp
from pyspark.sql.functions import col, row_number
from pyspark.sql.window import Window

@dp.table(name="dbw_data_engineering_portfolio_dev.silver.customer")
def customer():
    window_spec = (
        Window
        .partitionBy("CustomerID")
        .orderBy(
            col("ModifiedDate").desc(),
            col("_ingestion_timestamp").desc()
        )
    )

    return(
        spark.read.table(
            "dbw_data_engineering_portfolio_dev.bronze.customer"
        )
        .filter(col("CustomerID").isNotNull())
        .withColumn(
            "_row_number",
            row_number().over(window_spec)
        )
        .filter(col("_row_number") == 1)
        .drop("_row_number")
    )