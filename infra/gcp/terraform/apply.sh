#!/bin/bash
# 
# Apply Terraform manifests from Cloud Shell or any other
# 
# From Cloud Shell:
#   bash apply.sh
# 
# From any other:
#   gcloud config set project GCP_PROJECT_ID
#   bash apply.sh
# 
#   export GCP_PROJECT_ID=
#   bash apply.sh
# 
# Precedence for GCP_PROJECT_ID:
#   - .tfvars or .tfvars.json
#   - Cloud Shell
#   - exported variable
#   - gcloud project config value


set -e

TERRAFORM_DIR="$(realpath $(dirname $0))"

if [[ -d "${TERRAFORM_DIR}/.terraform" ]]; then
    echo "Terraform already initialized"
else
    terraform -chdir="${TERRAFORM_DIR}" init
fi

if [[ -f "${TERRAFORM_DIR}/.tfvars" || -f "${TERRAFORM_DIR}/.tfvars.json" ]]; then
    terraform -chdir="${TERRAFORM_DIR}" apply
    exit 0
fi

if [[ "${CLOUD_SHELL}" == true ]]; then
    GCP_PROJECT_ID="${DEVSHELL_PROJECT_ID}"
elif [[ -z "${GCP_PROJECT_ID}" ]]
    if [[ -z "$(which gcloud)" ]]; then
        echo >&2 'Unable to define GCP_PROJECT_ID'
        exit 1
    else
        GCP_PROJECT_ID="$(gcloud info --format='value(config.project)')"
    fi
fi

terraform -chdir="${TERRAFORM_DIR}" apply \
    -var "project_id=${GCP_PROJECT_ID}"

WRITE_OUTPUT_FILE=true bash "${TERRAFORM_DIR}/output.sh"
