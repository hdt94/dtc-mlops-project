# MLOps project - course from DataTalksClub

Online service for prediction of duration taxi ride.

![](diagram.png)

You can request online service:
```bash
URL=https://rides-ucpkfmi6pq-ue.a.run.app/predict  # Cloud Run service URL
curl -X POST \
    -H 'Content-type: application/json' \
    -d '{"PULocationID": 43, "DOLocationID": 151, "trip_distance": 1.01}' \
    "${URL}"
```

## Up and running

Provision cloud infrastructure on existing Google Cloud project:
- if using [Cloud Shell](https://console.cloud.google.com/?cloudshell=true):
    ```bash
    export GCP_PROJECT_ID="${DEVSHELL_PROJECT_ID}"
    bash ./infra/gcp/terraform/apply.sh
    ```
- if using other than [Cloud Shell](https://console.cloud.google.com/?cloudshell=true):
    ```bash
    gcloud auth application-default login

    export GCP_PROJECT_ID=
    gcloud config set project "${GCP_PROJECT_ID}"

    bash ./infra/gcp/terraform/apply.sh
    ```

MLflow server (locally):
- create virtual environment and check more server options at [infra/local/README.md](infra/local/README.md)
```bash
export GS_ML_MODELS_BUCKET_ID="$(bash ./infra/gcp/terraform/output.sh GS_ML_MODELS_BUCKET_ID)"
bash ./infra/local/mlflow-server.sh
```

Run ML pipelines:
- [analytics/ml-pipelines/duration/README.md](./analytics/ml-pipelines/duration/README.md)

Deploy web service to Cloud Run: [services/rides/README.md](./services/rides/README.md)
```bash
export CONTAINER_REGISTRY_URL="$(bash ./infra/gcp/terraform/output.sh WEB_CONTAINER_REGISTRY_URL)"
export MLFLOW_MODEL_URI=
export MLFLOW_MODEL_VERSION=
export REGION=us-east1
bash services/rides/build_deploy.sh
```

Test service:
```bash
URL=  # Cloud Run service URL
curl -X POST \
    -H 'Content-type: application/json' \
    -d '{"PULocationID": 43, "DOLocationID": 151, "trip_distance": 1.01}' \
    "${URL}"
```
