#!/bin/bash
# 
# Create and/or source venv environment, optionally using custom base interpreter
# 
# Create venv at same location as requirements (if venv exists, activate it):
#   REQUIREMENTS=path/to/requirements.txt venv.sh
#   PYTHON_BASE_INTERPRETER=python3.8 REQUIREMENTS=path/to/requirements.txt venv.sh
# 
# Create venv at custom location:
#   REQUIREMENTS=path/to/requirements.txt VENV_DIR=custom/path/ venv.sh
#   PYTHON_BASE_INTERPRETER=python3.8 REQUIREMENTS=path/to/requirements.txt VENV_DIR=custom/path/ venv.sh
# 
# Source existing venv at custom location:
#   VENV_DIR=custom/path/ venv.sh


set -e


activate_venv() {
    source "${VENV_DIR}/bin/activate"
    echo "Python interpreter: $(which python3)"
}


if [[ -z "${REQUIREMENTS}" && -z "${VENV_DIR}" ]]; then
    echo "Undefined REQUIREMENTS and VENV_DIR" >&2
    exit 1
elif [[ -z "${REQUIREMENTS}" ]]; then
    activate_venv
else
    if [[ -z "${VENV_DIR}" ]]; then
        VENV_DIR="$(dirname "${REQUIREMENTS}")/venv"
    fi

    if [[ -d "${VENV_DIR}" ]]; then
        activate_venv
    else
        echo "Creating venv at: ${VENV_DIR}"
        ${PYTHON_BASE_INTERPRETER:-python3} -m venv "${VENV_DIR}"
        activate_venv
        echo "Updating pip..."
        pip3 install -U pip
        echo "Installing requirements: ${REQUIREMENTS}"
        pip3 install -r "${REQUIREMENTS}"
    fi
fi
