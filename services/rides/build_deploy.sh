#!/bin/bash
#
# Example:
#   export REGION=
#   export CONTAINER_REGISTRY_URL="${REGION}-docker.pkg.dev/PROJECT_ID/REPO_NAME"  # Docker Artifact registry repository URL
#   bash build_deploy.sh

set -e

SERVICE_DIR="$(realpath $(dirname $0))"

if [[ -z "$CONTAINER_REGISTRY_URL" ]]; then
    echo >&2 'Undefined CONTAINER_REGISTRY_URL'
    exit 1
elif [[ -z "$REGION" ]]; then
    echo >&2 'Undefined REGION'
    exit 1
fi

IMAGE="${CONTAINER_REGISTRY_URL}/rides-service"
IMAGE_VERSION="$(date +%F_%H-%M-%S)"

IMAGE_TAG="${IMAGE}:${IMAGE_VERSION}"

echo "Building image: ${IMAGE_TAG}"
gcloud builds submit "$SERVICE_DIR" --tag "${IMAGE_TAG}"

if [[ -z "${MLFLOW_MODEL_URI}" ]]; then
    echo >&2 'Undefined MLFLOW_MODEL_URI'
    exit 1
elif [[ -z "${MLFLOW_MODEL_VERSION}" ]]; then
    echo >&2 'Undefined MLFLOW_MODEL_VERSION'
    exit 1
fi

echo "Deploying image: ${IMAGE_TAG}"
gcloud run deploy rides \
    --allow-unauthenticated \
    --image="${IMAGE_TAG}" \
    --region="${REGION}" \
    --set-env-vars MLFLOW_MODEL_URI="${MLFLOW_MODEL_URI}",MLFLOW_MODEL_VERSION="${MLFLOW_MODEL_VERSION}"
