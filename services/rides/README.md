## Deploy locally

Create environment:
```bash
python3.8 -m venv venv
source venv/bin/activate
pip install -U pip pipenv
pipenv install
```

Run web server in development:
```bash
export MLFLOW_MODEL_URI=
export MLFLOW_MODEL_VERSION=

python3 src/app.py
```

Test endpoint:
```bash
URL=http://localhost:4000/predict
curl -X POST \
    -H 'Content-type: application/json' \
    -d '{"PULocationID": 43, "DOLocationID": 151, "trip_distance": 1.01}' \
    "${URL}"
```

## Deploy to Google Cloud

Build and deploy service to Cloud Run:
- 
```bash
export CONTAINER_REGISTRY_URL="$(bash ../../infra/gcp/terraform/output.sh WEB_CONTAINER_REGISTRY_URL)"
export MLFLOW_MODEL_URI=
export MLFLOW_MODEL_VERSION=
export REGION=us-east1
bash build_deploy.sh
```

Test service:
- check request example in [root README.md](/README.md)
```bash
URL=  # Cloud Run service URL
curl -X POST \
    -H 'Content-type: application/json' \
    -d '{"PULocationID": 43, "DOLocationID": 151, "trip_distance": 1.01}' \
    "${URL}"
```
