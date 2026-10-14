import os
import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark():
    if os.getenv("GITHUB_ACTIONS") == "true":
        spark_session = (
            SparkSession.builder
            .master("local[1]")
            .appName("silver-unit-tests")
            .getOrCreate()
        )

        yield spark_session

        spark_session.stop()

    else:
        yield SparkSession.builder.getOrCreate()