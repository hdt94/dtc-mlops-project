import pandas as pd
from prefect import task


BASE_URL = "https://d37ci6vzurychx.cloudfront.net"


@task(retries=3, retry_delay_seconds=30)
def read_dataframe(
    vehicle_type: str,
    year_month: str,
    source: str = None,
) -> pd.DataFrame:
    if source is None:
        source = f"{BASE_URL}/trip-data"
    elif source[-1] in ["/", "\\"]:
        source = source[:-1]

    file_location = f"{source}/{vehicle_type}_tripdata_{year_month}.parquet"
    df = pd.read_parquet(file_location)

    return df
