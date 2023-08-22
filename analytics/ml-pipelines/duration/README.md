Create virtual environment:
```bash
python3.8 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Start MLflow: [infra/local/README.md](/infra/local/README.md)

Optionally, download datasets to local directory: [analytics/data/README.md](/analytics/data/README.md)

Run pipeline:
- default experiment is "nyc-taxi-ride-duration"; you can overwrite it with "--mlflow-experiment"
- this is a basic modeling that must be further improved, it basically works as artifact for MLOps project work
```bash
# accessing datasets from web source
python3 src/duration_linear.py \
    --mlflow-uri http://localhost:5000 \
    --train 2023-01 \
    --val 2023-02 \
    --vehicle-type green

# defining experiment; accessing datasets from web source
python3 src/duration_linear.py \
    --mlflow-experiment my-custom-experiment \
    --mlflow-uri http://localhost:5000 \
    --train 2023-01 \
    --val 2023-02 \
    --vehicle-type green

# accessing datasets from local directory source
LOCAL_DATA_DIR=
python3 src/duration_linear.py \
    --mlflow-uri http://localhost:5000 \
    --source "${LOCAL_DATA_DIR}" \
    --train 2023-01 \
    --val 2023-02 \
    --vehicle-type green
```
