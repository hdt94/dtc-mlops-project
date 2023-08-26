Create virtual environment:
```bash
python3.8 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Start MLflow and Prefect servers: [infra/local/README.md](/infra/local/README.md)

Start Prefect worker as local process:
- [prefect-worker.sh](./prefect-worker.sh) creates `.prefect/` which is included in [root .gitignore](/.gitignore)
```bash
# using default server URL localhost:4200
bash prefect-worker.sh

# using custom server URL
export PREFECT_API_URL=
bash prefect-worker.sh
```

Optionally, download datasets to local directory: [analytics/data/README.md](/analytics/data/README.md)

Run pipeline:
- default experiment is "nyc-taxi-ride-duration"; you can overwrite it with "--mlflow-experiment"
- this is a basic modeling that must be further improved, it basically works as artifact for MLOps project work
```bash
export PREFECT_HOME="${PWD}/.prefect"

# accessing datasets from web source
prefect deployment run duration-linear-baseline-main/local-ml-duration \
    --param mlflow_uri=http://localhost:5000 \
    --param train_year_month=2023-01 \
    --param val_year_month=2023-02 \
    --param vehicle_type=green

# defining experiment; accessing datasets from web source
prefect deployment run duration-linear-baseline-main/local-ml-duration \
    --param mlflow_experiment=my-custom-experiment \
    --param mlflow_uri=http://localhost:5000 \
    --param train_year_month=2023-01 \
    --param val_year_month=2023-02 \
    --param vehicle_type=green

# accessing datasets from local directory source
LOCAL_DATA_DIR=
prefect deployment run duration-linear-baseline-main/local-ml-duration \
    --param mlflow_uri=http://localhost:5000 \
    --param train_year_month=2023-01 \
    --param val_year_month=2023-02 \
    --param vehicle_type=green
```

Alternatively, running flow directly although there is no trace of deployment neither work pool:
```bash
export PREFECT_HOME="${PWD}/.prefect"

# accessing datasets from web source
python3 src/duration_linear_baseline_flow.py \
    --mlflow-uri http://localhost:5000 \
    --train 2023-01 \
    --val 2023-02 \
    --vehicle-type green

# defining experiment; accessing datasets from web source
python3 src/duration_linear_baseline_flow.py \
    --mlflow-experiment my-custom-experiment \
    --mlflow-uri http://localhost:5000 \
    --train 2023-01 \
    --val 2023-02 \
    --vehicle-type green

# accessing datasets from local directory source
LOCAL_DATA_DIR=
python3 src/duration_linear_baseline_flow.py \
    --mlflow-uri http://localhost:5000 \
    --source "${LOCAL_DATA_DIR}" \
    --train 2023-01 \
    --val 2023-02 \
    --vehicle-type green
```

Connecting to metrics database:
```bash
export PGPASSWORD=
psql -d mlops -U postgres -h localhost
```

Querying metrics table:
```sql
SELECT context, experiment_id, model_name, model_version, name, timestamp FROM metrics;
```
