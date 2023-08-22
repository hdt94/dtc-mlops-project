#!/bin/bash
# 
# Examples:
#   # download green data to default directory
#   bash download-data.sh
# 
#   # download green data to custom directory
#   LOCAL_DATA_DIR="${PWD}/custom/raw" bash download-data.sh
# 
#   # download green data from custom dates (separate by space)
#   YEAR_MONTH_PAIRS='2019-11 2019-12' bash download-data.sh
# 
#   # download yellow data from custom dates (separate by space)
#   VEHICLE_TYPE=yellow YEAR_MONTH_PAIRS='2023-01 2023-02' bash download-data.sh

set -e


echo_default_year_month_pairs() {
    for year in 2021 2022 2023; do
        for month in 01 02 03; do
            echo "${year}-${month}"
        done
    done
}


DATA_BASE_URL=https://d37ci6vzurychx.cloudfront.net

LOCAL_DATA_DIR="${LOCAL_DATA_DIR:-"$(realpath $(dirname $0))/source"}"
VEHICLE_TYPE="${VEHICLE_TYPE:-green}"
YEAR_MONTH_PAIRS="${YEAR_MONTH_PAIRS:-"$(echo_default_year_month_pairs)"}"

echo "Downloading to: ${LOCAL_DATA_DIR}"
mkdir -p "${LOCAL_DATA_DIR}"
for YEAR_MONTH in $YEAR_MONTH_PAIRS; do
    wget -P "${LOCAL_DATA_DIR}" -q "${DATA_BASE_URL}/trip-data/${VEHICLE_TYPE}_tripdata_${YEAR_MONTH}.parquet"
done
