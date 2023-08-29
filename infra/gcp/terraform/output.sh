#!/bin/bash
# 
# Examples:
#   WRITE_OUTPUT_FILE=true bash output.sh
#
#   TERRAFORM_OUTPUT="$(bash output.sh)"
#
#   GS_ML_MODELS_BUCKET_ID="$(bash output.sh GS_ML_MODELS_BUCKET_ID)"
#   GS_ML_MODELS_BUCKET_ID="$(TERRAFORM_OUTPUT="${TERRAFORM_OUTPUT}" bash output.sh GS_ML_MODELS_BUCKET_ID)"
# 
#   WEB_CONTAINER_REGISTRY_URL="$(bash output.sh WEB_CONTAINER_REGISTRY_URL)"

set -e

TERRAFORM_DIR="$(realpath $(dirname $0))"
TERRAFORM_OUTPUT_FILE="${TERRAFORM_DIR}/output.json"

EXTRACT_VALUE="$1"

if [[ -z "${TERRAFORM_OUTPUT}" ]]; then 
  if [[ -f "${TERRAFORM_OUTPUT_FILE}" ]]; then
    TERRAFORM_OUTPUT="$(jq '.' "${TERRAFORM_OUTPUT_FILE}")"
  else
    TERRAFORM_OUTPUT="$(terraform -chdir="${TERRAFORM_DIR}" output -json)"
    if [[ "${WRITE_OUTPUT_FILE}" == 1 || "${WRITE_OUTPUT_FILE}" == true ]]; then
      echo "${TERRAFORM_OUTPUT}" > "${TERRAFORM_OUTPUT_FILE}"
      exit 0
    fi
  fi
fi

if [[ -z "${EXTRACT_VALUE}" ]]; then
  echo "${TERRAFORM_OUTPUT}"
  exit 0
fi

case "${EXTRACT_VALUE}" in
  GS_ML_MODELS_BUCKET_ID)
    echo "$(jq -r '.ml_models_bucket.value.id' <<< "${TERRAFORM_OUTPUT}")";;

  WEB_CONTAINER_REGISTRY_URL)
    echo "$(jq -r '.web_containers.value.registry_url' <<< "${TERRAFORM_OUTPUT}")";;

  *)
    echo >&2 "Unknown EXTRACT_VALUE: \"${EXTRACT_VALUE}\""
    exit 1
    ;;
esac
