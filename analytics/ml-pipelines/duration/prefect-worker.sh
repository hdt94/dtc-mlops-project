#!/bin/bash

set -e

BASE_DIR="$(realpath "$(dirname $0)")"

POOL=local-process-ml-duration
export PREFECT_HOME="${BASE_DIR}/.prefect"

# deployment definition requires base directory to be working directory
pushd "${BASE_DIR}" > /dev/null

prefect config set PREFECT_API_URL="${PREFECT_API_URL:-http://localhost:4200/api}"
prefect config view

if [[ -z "$(prefect work-pool ls | grep "${POOL}")" ]]; then
    prefect work-pool create --type process "${POOL}"
elif [[ -z "$(prefect work-pool inspect "${POOL}")" ]]; then
    prefect work-pool create --type process "${POOL}"
else
    echo "work pool found: ${POOL}"
fi

echo "validating deployments..."
prefect --no-prompt deploy --all > /dev/null  # will raise error if any

echo "starting worker..."
prefect worker start --pool "${POOL}"

popd > /dev/null
