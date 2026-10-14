from pyspark import pipelines as dp
from config.primary_keys import PRIMARY_KEYS
from config.table_exp import EXPECTATIONS
from transformations.silver_utils import (
    build_valid_condition,
    build_quarantine_reason,
    deduplicate_latest
)


def create_silver_table(table_name, pk_columns):

    valid_condition = build_valid_condition(pk_columns)
    quarantine_reason = build_quarantine_reason(pk_columns)

    @dp.table(
        name=f"dbw_data_engineering_portfolio_dev.quarantine.{table_name}"
    )
    def quarantine_table():
        return (
            spark.read.table(
                f"dbw_data_engineering_portfolio_dev.bronze.{table_name}"
            )
            .filter(~valid_condition)
            .withColumn(
                "_quarantine_reason",
                quarantine_reason
            )
        )

    table_expectations = EXPECTATIONS.get(table_name, {})

    @dp.table(
        name=f"dbw_data_engineering_portfolio_dev.silver.{table_name}"
    )
    @dp.expect_all(table_expectations)
    def silver_table():

        df = (
            spark.read.table(
                f"dbw_data_engineering_portfolio_dev.bronze.{table_name}"
            )
            .filter(valid_condition)
        )

        return deduplicate_latest(
            df,
            pk_columns
        )


for table_name, pk_columns in PRIMARY_KEYS.items():
    create_silver_table(
        table_name,
        pk_columns
    )