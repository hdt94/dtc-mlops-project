Download Parquet raw source data files:
- default directory is `source/`; [.gitignore](.gitignore) includes `source/`
```bash
# download green data to default directory
bash download-datasets.sh

# download green data to custom directory
LOCAL_DATA_DIR="${PWD}/source/custom/" bash download-datasets.sh

# download green data from custom dates (separate by space)
YEAR_MONTH_PAIRS='2019-11 2019-12' bash download-datasets.sh

# download yellow data from custom dates (separate by space)
VEHICLE_TYPE=yellow YEAR_MONTH_PAIRS='2023-01 2023-02' bash download-datasets.sh
```
