import json
from datetime import datetime
from typing import Dict, List, Union

from evidently import ColumnMapping
from evidently.metrics import (
    DatasetDriftMetric,
    RegressionQualityMetric,
)
from evidently.report import Report
from evidently.utils import NumpyEncoder

from io_tasks import write_to_database


class DefaultReport:
    evidently_report: Union[None, Report] = None

    def __init__(self, column_mapping: ColumnMapping):
        self.column_mapping = column_mapping
        self.evidently_report = Report(
            metrics=[
                DatasetDriftMetric(),
                RegressionQualityMetric(),
            ]
        )

    def run(self, current_data, reference_data):
        self.evidently_report.run(
            column_mapping=self.column_mapping,
            current_data=current_data,
            reference_data=reference_data,
        )

    def write_to_database(self, context, experiment_id, model_name, model_version):
        metrics = self.evidently_report.as_dict()["metrics"]
        query_template = """
            INSERT INTO metrics (
                context,
                experiment_id,
                model_name,
                model_version,
                name,
                results
            )
            VALUES
        """
        values = []
        for metric in metrics:
            query_template += "(%s, %s, %s, %s, %s, %s),"
            values.extend(
                [
                    context,
                    experiment_id,
                    model_name,
                    model_version,
                    metric["metric"],
                    json.dumps(metric["result"], cls=NumpyEncoder),
                ]
            )

        write_to_database(query_template[:-1], values, len(metrics))

    def write_to_html(self, reports_dir, model_name, experiment_id):
        ts = str(datetime.now().timestamp())[:10]
        file_path = f"{reports_dir}/{model_name}_{ts}_{experiment_id}.html"
        self.evidently_report.save_html(file_path)
        return file_path
