#!/bin/bash
# 
# Examples:
#   TERRAFORM_OUTPUT="$(bash output.sh)"
#   GS_ML_MODELS_BUCKET_ID="$(bash output.sh GS_ML_MODELS_BUCKET_ID)"
#   GS_ML_MODELS_BUCKET_ID="$(TERRAFORM_OUTPUT="${TERRAFORM_OUTPUT}" bash output.sh GS_ML_MODELS_BUCKET_ID)"

set -e

TERRAFORM_DIR="$(realpath $(dirname $0))"
EXTRACT_VALUE="$1"

if [[ -z "${EXTRACT_VALUE}" ]]; then
    echo "$(terraform -chdir="${TERRAFORM_DIR}" output -json)"
    exit 0
elif [[ -z "${TERRAFORM_OUTPUT}" ]]; then
    TERRAFORM_OUTPUT="$(terraform -chdir="${TERRAFORM_DIR}" output -json)"
fi

case "${EXTRACT_VALUE}" in
  GS_ML_MODELS_BUCKET_ID)
    echo "$(jq -r '.ml_models_bucket.value.id' <<< "${TERRAFORM_OUTPUT}")";;

  *)
    echo >&2 "Unknown EXTRACT_VALUE: \"${EXTRACT_VALUE}\""
    exit 1
    ;;
esac
