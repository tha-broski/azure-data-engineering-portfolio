from pyspark import pipelines as dp
from pyspark.sql.functions import col, row_number, when, lit
from pyspark.sql.window import Window
from config.primary_keys import PRIMARY_KEYS
from config.table_exp import EXPECTATIONS

def create_silver_table(table_name, pk_columns):

    pk_condition = None
    for column in pk_columns:
        condition = col(column).isNotNull()
        if pk_condition is None:
            pk_condition = condition
        else:
            pk_condition = pk_condition & condition

    valid_condition = (
        pk_condition
        & col("ModifiedDate").isNotNull()
    )

    quarantine_reason = (
        when(~pk_condition, lit("NULL_PRIMARY_KEY"))
        .when(col("ModifiedDate").isNull(), lit("NULL_MODIFIED_DATE"))
        .otherwise(lit("UNKNOWN"))
    )

    @dp.table(name=f"dbw_data_engineering_portfolio_dev.quarantine.{table_name}")
    def quarantine_table():
        return(
            spark.read.table(
                f"dbw_data_engineering_portfolio_dev.bronze.{table_name}"
            )
            .filter(~valid_condition)
            .withColumn("_quarantine_reason", quarantine_reason)
        )


    table_expectations = EXPECTATIONS.get(table_name, {})

    @dp.table(name=f"dbw_data_engineering_portfolio_dev.silver.{table_name}")
    @dp.expect_all(table_expectations)
    def silver_table():
        window_spec = (
            Window.partitionBy(*pk_columns)
            .orderBy(
                col("ModifiedDate").desc(),
                col("_ingestion_timestamp").desc()
            )
        )

        return(
            spark.read.table(
                f"dbw_data_engineering_portfolio_dev.bronze.{table_name}"
            )
            .filter(valid_condition)
            .withColumn(
                "_row_number",
                row_number().over(window_spec)
            )
            .filter(col("_row_number") == 1)
            .drop("_row_number")
        )
            
for table_name, pk_columns in PRIMARY_KEYS.items():
    create_silver_table(table_name, pk_columns)