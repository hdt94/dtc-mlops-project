
## MLflow

MLflow setup:
- Optionally, use same virtual environment from `analytics/` by activating it
```
python3.8 -m venv venv
source venv/bin/activate
pip install -r requirements.mlflow.txt
```

MLflow server:
- [.gitignore](.gitignore) contains `.mlflow/`
- server backend is set to `.mlflow/mlflow.db`
- default artifacts destination is `.mlflow/artifacts/`
- use GS_ML_MODELS_BUCKET_ID env variable for artifacts destination on Google Cloud Storage
```bash
# listening on default localhost:5000
bash mlflow-server.sh --workers 2

# listening all interfaces on custom port
bash mlflow-server.sh --host 0.0.0.0 --port 8080 --workers 2

# storing artifacts to Google Cloud Storage
export GS_ML_MODELS_BUCKET_ID=
bash mlflow-server.sh --workers 2

# listening all interfaces on custom port; storing artifacts to Google Cloud Storage
export GS_ML_MODELS_BUCKET_ID=
bash mlflow-server.sh --host 0.0.0.0 --port 8080 --workers 2
```

## Prefect

Start Prefect server using Docker Compose:
```
docker compose up prefect_server
```
