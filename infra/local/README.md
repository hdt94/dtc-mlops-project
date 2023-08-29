## MLflow
- TODO integrate MLflow with Docker Compose, requiring creating a service account and mapping credentials to container
- check MLflow server options and notes in [mlflow/README.md](mlflow/README.md)
```bash
# listening all interfaces on custom port
bash mlflow/server.sh --host 0.0.0.0 --port 8080 --workers 2

# listening all interfaces on custom port; storing artifacts to Google Cloud Storage
export GS_ML_MODELS_BUCKET_ID=
bash mlflow/server.sh --host 0.0.0.0 --port 8080 --workers 2
```

## Metrics database + Prefect

Start Prefect server using Docker Compose:
```
docker compose up ml_metrics_db prefect_server
```
