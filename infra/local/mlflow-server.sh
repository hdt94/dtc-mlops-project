#!/bin/bash
#
# Examples:
#   # listening on default localhost:5000
#   bash mlflow-server.sh --workers 2
#
#   # listening all interfaces on custom port
#   bash mlflow-server.sh --host 0.0.0.0 --port 8080 --workers 2
#
#   # storing artifacts to Google Cloud Storage
#   export GS_ML_MODELS_BUCKET_ID=
#   bash mlflow-server.sh --workers 2
#
#   # listening all interfaces on custom port; storing artifacts to Google Cloud Storage
#   export GS_ML_MODELS_BUCKET_ID=
#   bash mlflow-server.sh --host 0.0.0.0 --port 8080 --workers 2

set -e

LOCAL_DIR="$(realpath $(dirname $0))"

MLFLOW_HOME="${LOCAL_DIR}/.mlflow"

MLFLOW_BACKEND_STORE_URI="sqlite:///${MLFLOW_HOME}/mlflow.db"

if [[ -z "${GS_ML_MODELS_BUCKET_ID}" ]]; then
    MLFLOW_ARTIFACTS_URI="${MLFLOW_HOME}/artifacts"
else
    MLFLOW_ARTIFACTS_URI="gs://${GS_ML_MODELS_BUCKET_ID}/models_mlflow"
fi

mkdir -p "${MLFLOW_HOME}"
mlflow server \
    --backend-store-uri "${MLFLOW_BACKEND_STORE_URI}" \
    --default-artifact-root "${MLFLOW_ARTIFACTS_URI}" \
    "$@"
