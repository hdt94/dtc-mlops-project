#!/bin/bash

set -e

TERRAFORM_DIR="$(realpath $(dirname $0))"

if [[ -d "${TERRAFORM_DIR}/.terraform" ]]; then
    echo "Terraform already initialized"
else
    terraform -chdir="${TERRAFORM_DIR}" init
fi

if [[ -f "${TERRAFORM_DIR}/.tfvars" || -f "${TERRAFORM_DIR}/.tfvars.json" ]]; then
    terraform -chdir="${TERRAFORM_DIR}" apply
elif [[ -z "${GCP_PROJECT_ID}" ]]; then
    echo >&2 'Undefined GCP_PROJECT_ID'
    exit 1
else
    terraform -chdir="${TERRAFORM_DIR}" apply \
        -var "project_id=${GCP_PROJECT_ID}"
fi
