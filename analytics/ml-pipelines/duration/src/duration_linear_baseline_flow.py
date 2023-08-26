import argparse
import tempfile
from typing import Dict, List, Union

import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

import mlflow
from evidently import ColumnMapping
from prefect import flow, task

from DefaultReport import DefaultReport
from io_tasks import get_dataset_uri, read_dataframe


MODEL_NAME = "duration_linear"

FEATURES_CAT = ["DOLocationID", "PULocationID"]
FEATURES_NUM = ["trip_distance"]
PREDICTION = "duration_in_minutes_prediction"
TARGET = "duration_in_minutes"

FEATURES = FEATURES_CAT + FEATURES_NUM


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

    df["duration_in_minutes"] = duration.dt.total_seconds() / 60
    df = df[(df["duration_in_minutes"] >= 1) & (df["duration_in_minutes"] <= 60)]

    return df


def preprocess_features(data: Union[Dict, List, pd.DataFrame]) -> List[Dict]:
    df = to_dataframe(data)

    df[FEATURES_CAT] = df[FEATURES_CAT].astype(str)
    df["PU_DO"] = df["PULocationID"] + "_" + df["DOLocationID"]

    features_df = df[FEATURES_NUM + ["PU_DO"]]
    features_records = features_df.to_dict(orient="records")

    return features_records


@flow(retries=2, retry_delay_seconds=60)
def report_metrics(df_current, df_reference, run_id, reports_dir=None):
    column_mapping = ColumnMapping(
        categorical_features=FEATURES_CAT,
        numerical_features=FEATURES_NUM,
        prediction=PREDICTION,
        target=TARGET,
    )
    report = DefaultReport(column_mapping)
    report.run(current_data=df_current, reference_data=df_reference)

    if reports_dir:
        file_path = report.write_to_html(reports_dir, MODEL_NAME, run_id)
        mlflow.log_artifact(file_path, artifact_path="report")
    else:
        with tempfile.TemporaryDirectory() as reports_dir:
            file_path = report.write_to_html(reports_dir, MODEL_NAME, run_id)
            mlflow.log_artifact(file_path, artifact_path="report")

    report.write_to_database("training", run_id, MODEL_NAME, run_id)


@task(log_prints=True)
def train_model(df_train: pd.DataFrame, df_val: pd.DataFrame) -> None:
    y_train = df_train[TARGET].values
    y_val = df_val[TARGET].values

    pipeline = Pipeline(
        [
            ("preprocess_features", FunctionTransformer(preprocess_features)),
            ("DictVectorizer", DictVectorizer()),
            ("LinearRegression", LinearRegression()),
        ]
    )
    pipeline.fit(df_train[FEATURES], y_train)
    mlflow.sklearn.log_model(pipeline, artifact_path="model")

    pred_train = pipeline.predict(df_train[FEATURES])
    pred_val = pipeline.predict(df_val[FEATURES])

    return (pred_train, pred_val)


@flow(log_prints=True)
def duration_linear_baseline_main(
    mlflow_uri: str,
    train_year_month: str,
    val_year_month: str,
    vehicle_type: str,
    mlflow_experiment: str = "nyc-taxi-ride-duration",
    reports_dir: str = None,
    source: str = None,
) -> None:
    """Main training pipeline"""

    mlflow.set_tracking_uri(mlflow_uri)
    mlflow.set_experiment(mlflow_experiment)

    source_uri_train = get_dataset_uri(vehicle_type, train_year_month, source)
    source_uri_val = get_dataset_uri(vehicle_type, val_year_month, source)

    print("Reading data files...")
    df_train = read_dataframe(source_uri_train)
    df_val = read_dataframe(source_uri_val)

    print("Preprocessing dataframes...")
    df_train = preprocess_duration(df_train)[FEATURES + [TARGET]]
    df_val = preprocess_duration(df_val)[FEATURES + [TARGET]]

    with mlflow.start_run() as run:
        print("Training model...")
        pred_train, pred_val = train_model(df_train, df_val)

        df_reference = df_train.assign(**({PREDICTION: pred_train}))
        df_current = df_val.assign(**({PREDICTION: pred_val}))

        reference_dataset = mlflow.data.from_pandas(df_reference, source_uri_train)
        mlflow.log_input(reference_dataset, context="training")

        print("Reporting metrics...")
        report_metrics(df_current, df_reference, run.info.run_id, reports_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mlflow-experiment", default="nyc-taxi-ride-duration")
    parser.add_argument("--mlflow-uri", default="localhost:5000")
    parser.add_argument("--source", default=None)
    parser.add_argument("--reports-dir", default=None)
    parser.add_argument("--train-year-month", "--train", default="2022-01")
    parser.add_argument("--val-year-month", "--val", default="2022-02")
    parser.add_argument("--vehicle-type", default="green")
    kwargs = vars(parser.parse_args())
    duration_linear_baseline_main(**kwargs)
