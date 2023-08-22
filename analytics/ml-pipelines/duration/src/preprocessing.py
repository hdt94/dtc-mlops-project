from typing import Dict, List, Union

import pandas as pd


def to_dataframe(data: Union[Dict, List, pd.DataFrame]) -> pd.DataFrame:
    if isinstance(data, dict):
        # single record
        return pd.DataFrame([data])

    if isinstance(data, list):
        # list of records
        return pd.DataFrame(data)

    if isinstance(data, pd.DataFrame):
        return data.copy()

    raise TypeError(f"Unsuported input data type: {type(data)}")


def preprocess_duration(data: Union[Dict, List, pd.DataFrame]) -> pd.DataFrame:
    df = to_dataframe(data)

    if ("lpep_dropoff_datetime" in df) and ("lpep_pickup_datetime" in df):
        # green vehicle_type
        duration = df["lpep_dropoff_datetime"] - df["lpep_pickup_datetime"]
    elif ("tpep_dropoff_datetime" in df) and ("tpep_pickup_datetime" in df):
        # yellow vehicle_type
        duration = df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]
    else:
        raise ValueError("Unsupported datetime columns")

    df["duration"] = duration.dt.total_seconds() / 60
    df = df[(df["duration"] >= 1) & (df["duration"] <= 60)]

    return df


def preprocess_features(data: Union[Dict, List, pd.DataFrame]) -> List[Dict]:
    df = to_dataframe(data)

    categorical = ["PULocationID", "DOLocationID"]
    numerical = ["trip_distance"]

    df[categorical] = df[categorical].astype(str)
    df["PU_DO"] = df["PULocationID"] + "_" + df["DOLocationID"]

    features_df = df[numerical + ["PU_DO"]]
    features_records = features_df.to_dict(orient="records")

    return features_records
