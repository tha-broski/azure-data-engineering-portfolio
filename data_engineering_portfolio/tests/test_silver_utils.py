from datetime import datetime

from data_engineering_portfolio_etl.transformations.silver_utils import (
    build_valid_condition,
    build_quarantine_reason,
    deduplicate_latest,
)


def test_deduplicate_latest_keeps_newest_modified_date(spark):
    data = [
        (
            1,
            "old",
            datetime(2026, 1, 1),
            datetime(2026, 1, 1, 10, 0),
        ),
        (
            1,
            "new",
            datetime(2026, 2, 1),
            datetime(2026, 2, 1, 10, 0),
        ),
        (
            2,
            "second_customer",
            datetime(2026, 1, 15),
            datetime(2026, 1, 15, 10, 0),
        ),
    ]

    columns = [
        "CustomerID",
        "Name",
        "ModifiedDate",
        "_ingestion_timestamp",
    ]

    df = spark.createDataFrame(data, columns)

    result = deduplicate_latest(df, ["CustomerID"])

    rows = result.collect()

    assert len(rows) == 2

    customer_1 = [
        row for row in rows
        if row.CustomerID == 1
    ][0]

    assert customer_1.Name == "new"


def test_deduplicate_latest_uses_ingestion_timestamp_as_tiebreaker(spark):
    data = [
        (
            1,
            "older_ingestion",
            datetime(2026, 1, 1),
            datetime(2026, 1, 1, 10, 0),
        ),
        (
            1,
            "newer_ingestion",
            datetime(2026, 1, 1),
            datetime(2026, 1, 1, 12, 0),
        ),
    ]

    columns = [
        "CustomerID",
        "Name",
        "ModifiedDate",
        "_ingestion_timestamp",
    ]

    df = spark.createDataFrame(data, columns)

    result = deduplicate_latest(df, ["CustomerID"])

    rows = result.collect()

    assert len(rows) == 1
    assert rows[0].Name == "newer_ingestion"


def test_deduplicate_latest_supports_composite_primary_key(spark):
    data = [
        (
            1,
            10,
            "old",
            datetime(2026, 1, 1),
            datetime(2026, 1, 1, 10, 0),
        ),
        (
            1,
            10,
            "new",
            datetime(2026, 2, 1),
            datetime(2026, 2, 1, 10, 0),
        ),
        (
            1,
            20,
            "different_address",
            datetime(2026, 1, 1),
            datetime(2026, 1, 1, 10, 0),
        ),
    ]

    columns = [
        "CustomerID",
        "AddressID",
        "Name",
        "ModifiedDate",
        "_ingestion_timestamp",
    ]

    df = spark.createDataFrame(data, columns)

    result = deduplicate_latest(
        df,
        ["CustomerID", "AddressID"],
    )

    rows = result.collect()

    assert len(rows) == 2

    customer_address = [
        row for row in rows
        if row.CustomerID == 1
        and row.AddressID == 10
    ][0]

    assert customer_address.Name == "new"


def test_valid_condition_keeps_only_valid_rows(spark):
    data = [
        (
            1,
            datetime(2026, 1, 1),
        ),
        (
            None,
            datetime(2026, 1, 1),
        ),
        (
            2,
            None,
        ),
    ]

    columns = [
        "CustomerID",
        "ModifiedDate",
    ]

    df = spark.createDataFrame(data, columns)

    result = (
        df
        .filter(
            build_valid_condition(["CustomerID"])
        )
        .collect()
    )

    assert len(result) == 1
    assert result[0].CustomerID == 1


def test_quarantine_reason_is_assigned_correctly(spark):
    data = [
        (
            None,
            datetime(2026, 1, 1),
        ),
        (
            1,
            None,
        ),
        (
            2,
            datetime(2026, 1, 1),
        ),
    ]

    columns = [
        "CustomerID",
        "ModifiedDate",
    ]

    df = spark.createDataFrame(data, columns)

    result = (
        df
        .withColumn(
            "_quarantine_reason",
            build_quarantine_reason(["CustomerID"]),
        )
        .collect()
    )

    reasons = {
        row.CustomerID: row._quarantine_reason
        for row in result
    }

    assert reasons[None] == "NULL_PRIMARY_KEY"
    assert reasons[1] == "NULL_MODIFIED_DATE"
    assert reasons[2] == "UNKNOWN"