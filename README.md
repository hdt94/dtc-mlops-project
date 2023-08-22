# MLOps project - course from DataTalksClub


## Up and running

Provision infrastructure:
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
