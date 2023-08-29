MLflow setup:
- Optionally, use same virtual environment from `analytics/` by activating it
```bash
# Manual venv
python3.8 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Using python3 >= 3.8
REQUIREMENTS=requirements.txt ../utils/venv.sh

# Using custom Python interpreter for compatibility
PYTHON_BASE_INTERPRETER=python3.8 REQUIREMENTS=requirements.txt ../utils/venv.sh
```

MLflow server:
- [.gitignore](.gitignore) contains `.mlflow/`
- server backend is set to `.mlflow/mlflow.db`
- default artifacts destination is `.mlflow/artifacts/`
- use GS_ML_MODELS_BUCKET_ID env variable for artifacts destination on Google Cloud Storage
```bash
# listening on default localhost:5000
bash server.sh --workers 2

# listening all interfaces on custom port
bash server.sh --host 0.0.0.0 --port 8080 --workers 2

# storing artifacts to Google Cloud Storage
export GS_ML_MODELS_BUCKET_ID=
bash server.sh --workers 2

# listening all interfaces on custom port; storing artifacts to Google Cloud Storage
export GS_ML_MODELS_BUCKET_ID=
bash server.sh --host 0.0.0.0 --port 8080 --workers 2
```
