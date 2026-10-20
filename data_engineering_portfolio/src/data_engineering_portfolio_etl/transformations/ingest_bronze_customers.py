from pyspark import pipelines as dp
from pyspark.sql.functions import current_timestamp, col


# This file defines a sample transformation.
# Edit the sample below or add new transformations
# using "+ Add" in the file browser.

tables = [
    "customer",
    "product",
    "address",
    "customeraddress",
    "productcategory",
    "productdescription",
    "productmodel",
    "productmodelproductdescription",
    "salesorderdetail",
    "salesorderheader"
]

def create_bronze_table(table_name):
    @dp.table(
        name=table_name
    )
    def bronze_table():
        return(
            spark.readStream.
            format("cloudFiles").
            option("cloudFiles.format", "parquet").
            load(f"abfss://landing@stdeportfoliodev01.dfs.core.windows.net/adventureworkslt/{table_name}/").
            withColumn("_ingestion_timestamp", current_timestamp()).
            withColumn("_source_file", col("_metadata.file_path"))
        )

for table in tables:
    create_bronze_table(table)