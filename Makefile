SHELL := /bin/bash

TERRAFORM_OUTPUT_SCRIPT=./infra/gcp/terraform/output.sh

# read Terraform output once
TERRAFORM_OUTPUT := $(shell bash $(TERRAFORM_OUTPUT_SCRIPT) | jq -c '.')

define get_terraform_output
	TERRAFORM_OUTPUT='$(TERRAFORM_OUTPUT)' bash $(TERRAFORM_OUTPUT_SCRIPT) $(1)
endef

CONTAINER_REGISTRY_URL=$(shell $(get_terraform_output) WEB_CONTAINER_REGISTRY_URL)
GS_ML_MODELS_BUCKET_ID=$(shell $(get_terraform_output) GS_ML_MODELS_BUCKET_ID)

compose_up:
	docker compose -f infra/local/docker-compose.yaml up ml_metrics_db prefect_server

# venv from venv_mlflow is deactivated (as sourced in inner scope) but reactivated by server.sh
mlflow_server: venv_mlflow
	GS_ML_MODELS_BUCKET_ID=$(GS_ML_MODELS_BUCKET_ID) bash ./infra/local/mlflow/server.sh --workers 2

rides_build_deploy:
	CONTAINER_REGISTRY_URL=$(CONTAINER_REGISTRY_URL) bash services/rides/build_deploy.sh

terraform_apply:
	bash ./infra/gcp/terraform/apply.sh

venv_mlflow:
	REQUIREMENTS=infra/local/mlflow/requirements.txt bash infra/local/utils/venv.sh
