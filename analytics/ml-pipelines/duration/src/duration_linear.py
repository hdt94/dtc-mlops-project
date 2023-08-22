import argparse
from typing import Dict, List, Union

import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

import mlflow

from ingestion import read_dataframe


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


def train_model(df_train: pd.DataFrame, df_val: pd.DataFrame) -> None:
    y_train = df_train["duration"].values
    y_val = df_val["duration"].values

    with mlflow.start_run():
        pipeline = Pipeline(
            [
                ("preprocess_features", FunctionTransformer(preprocess_features)),
                ("DictVectorizer", DictVectorizer()),
                ("LinearRegression", LinearRegression()),
            ]
        )
        pipeline.fit(df_train, y_train)
        mlflow.sklearn.log_model(pipeline, artifact_path="model")

        y_pred = pipeline.predict(df_val)
        rmse = mean_squared_error(y_val, y_pred, squared=False)
        mlflow.log_metric("rmse", rmse)

    return None


def duration_xgboost_main(
    mlflow_experiment: str,
    mlflow_uri: str,
    train_year_month: str,
    val_year_month: str,
    vehicle_type: str,
    source: str = None,
) -> None:
    """Main training pipeline"""

    mlflow.set_tracking_uri(mlflow_uri)
    mlflow.set_experiment(mlflow_experiment)

    print("Reading data files...")
    df_train = read_dataframe(vehicle_type, train_year_month, source)
    df_val = read_dataframe(vehicle_type, val_year_month, source)

    print("Preprocessing dataframes...")
    df_train = preprocess_duration(df_train)
    df_val = preprocess_duration(df_val)

    print("Training model...")
    train_model(df_train, df_val)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mlflow-experiment", default="nyc-taxi-ride-duration")
    parser.add_argument("--mlflow-uri", default="localhost:5000")
    parser.add_argument("--source", default=None)
    parser.add_argument("--train-year-month", "--train", default="2022-01")
    parser.add_argument("--val-year-month", "--val", default="2022-02")
    parser.add_argument("--vehicle-type", default="green")
    kwargs = vars(parser.parse_args())
    duration_xgboost_main(**kwargs)
