from pyspark.sql.functions import col, row_number, when, lit
from pyspark.sql.window import Window


def build_valid_condition(pk_columns):
    pk_condition = None

    for column in pk_columns:
        condition = col(column).isNotNull()

        if pk_condition is None:
            pk_condition = condition
        else:
            pk_condition = pk_condition & condition

    return (
        pk_condition
        & col("ModifiedDate").isNotNull()
    )


def build_quarantine_reason(pk_columns):
    pk_condition = None

    for column in pk_columns:
        condition = col(column).isNotNull()

        if pk_condition is None:
            pk_condition = condition
        else:
            pk_condition = pk_condition & condition

    return (
        when(~pk_condition, lit("NULL_PRIMARY_KEY"))
        .when(
            col("ModifiedDate").isNull(),
            lit("NULL_MODIFIED_DATE")
        )
        .otherwise(lit("UNKNOWN"))
    )


def deduplicate_latest(df, pk_columns):
    window_spec = (
        Window.partitionBy(*pk_columns)
        .orderBy(
            col("ModifiedDate").desc(),
            col("_ingestion_timestamp").desc()
        )
    )

    return (
        df
        .withColumn(
            "_row_number",
            row_number().over(window_spec)
        )
        .filter(col("_row_number") == 1)
        .drop("_row_number")
    )