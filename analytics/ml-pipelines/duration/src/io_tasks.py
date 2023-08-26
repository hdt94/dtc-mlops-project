import os

import pandas as pd
import psycopg
from prefect import task


BASE_URL = "https://d37ci6vzurychx.cloudfront.net"


def get_dataset_uri(vehicle_type: str, year_month: str, source: str = None):
    if source is None:
        source = f"{BASE_URL}/trip-data"
    elif source[-1] in ["/", "\\"]:
        source = source[:-1]

    return f"{source}/{vehicle_type}_tripdata_{year_month}.parquet"


@task(retries=3, retry_delay_seconds=30)
def read_dataframe(file_location: str) -> pd.DataFrame:
    df = pd.read_parquet(file_location)

    return df


@task(retries=3, retry_delay_seconds=30)
def write_to_database(query_template, values, expected_inserts: int = None):
    conn_kwargs = dict(
        host=os.environ.get("PGHOST", "localhost"),
        port=os.environ.get("PGPORT", "5432"),
        dbname=os.environ.get("PGDATABASE", "mlops"),
        user=os.environ.get("PGUSER", "postgres"),
        password=os.environ.get("PGPASSWORD", "uTcdEf43"),
    )
    with psycopg.connect(**conn_kwargs) as conn:
        results = conn.execute(query_template, values)

    if expected_inserts is not None:
        assert (
            results.rowcount == expected_inserts
        ), f"Unexpected {results.rowcount} inserts instead of {expected_inserts}"
