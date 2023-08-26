CREATE TYPE context_type AS ENUM ('batch', 'training');
CREATE TABLE metrics (
    context context_type,
    experiment_id VARCHAR,
    model_name VARCHAR,
    model_version VARCHAR,
    name VARCHAR,
    results JSONB,
    timestamp TIMESTAMP DEFAULT NOW()
);
