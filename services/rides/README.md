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
curl -X POST \
    -H 'Content-type: application/json' \
    -d '{"PULocationID": 43, "DOLocationID": 151, "trip_distance": 1.01}' \
    http://localhost:4000/predict
```
