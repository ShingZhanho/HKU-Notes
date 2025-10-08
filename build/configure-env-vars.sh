#!/bin/bash
# This script sets up environment variables for the build process.
# Run this script in the depository root directory.

# update python
python3 -m pip install --upgrade pip

# export the env var
export_var() {
    local var_name=$1
    local var_value=$2
    echo ${var_name}=${var_value} >> "$GITHUB_ENV"
}

# get metadata key value with python script
get_metadata_value() {
    local key=$1
    local output
    output=$(python3 ./build/get-metadata.py "${METADATA_FILE}" "${key}")
    local status=$?
    if [ $status -eq 0 ]; then
        echo "$output"
    else
        echo "Error: Failed to get metadata value for key '${key}'." >&2
        exit 1
    fi
}

BUILD_TARGET_NAME=$1
export_var "BUILD_TARGET_NAME" "${BUILD_TARGET_NAME}"
METADATA_FILE="./src/${BUILD_TARGET_NAME}/metadata.json"
export_var "METADATA_FILE" "${METADATA_FILE}"

# Handle build target requirements
if [ $(get_metadata_value build__requires | grep "python-minted-pkgs" | wc -l) -eq 1 ]; then
    export_var "DYENV_REQUIRE_PYTHON_MINTED_PKGS" "true"
else
    export_var "DYENV_REQUIRE_PYTHON_MINTED_PKGS" "false"
fi

# Handle build target prebuild command
export_var "DYENV_PREBUILD_COMMAND" "$(get_metadata_value build__prebuild_command)"

# Handle build target build command
export_var "DYENV_BUILD_COMMAND" "$(get_metadata_value build__build_command)"

# Handle build target postbuild command
export_var "DYENV_POSTBUILD_COMMAND" "$(get_metadata_value build__postbuild_command)"

# Handle build target output file
export_var "DYENV_OUTPUT_FILE" "$(get_metadata_value output_file)"

# Handle build target miktex package file
export_var "DYENV_TEX_PACKAGE_HASH" "$(get_metadata_value computed__tex_pkg_hash)"

# Handle build target alias properties
export_var "DYENV_IS_ALIAS" "$(get_metadata_value computed__is_alias)"
export_var "DYENV_ALIAS_TO" "$(get_metadata_value static_site__alias_to)"