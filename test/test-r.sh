#!/usr/bin/env bash
set -ex

SCRIPT_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"

R_HOME=/opt/R/${R_VERSION}/lib/R
"${R_HOME}/bin/R" --version
"${R_HOME}/bin/Rscript" -e 'sessionInfo()'

# List R devel dependencies
$("${R_HOME}/bin/R" CMD config CC)  --version
$("${R_HOME}/bin/R" CMD config CXX) --version
$("${R_HOME}/bin/R" CMD config FC)  --version

# List shared library dependencies (e.g. BLAS/LAPACK)
LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${R_HOME}/lib ldd "${R_HOME}/lib/libR.so"
LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${R_HOME}/lib ldd "${R_HOME}/lib/libRblas.so"

ls -la "${R_HOME}/lib/"

DIR=$SCRIPT_DIR "${R_HOME}/bin/Rscript" "${SCRIPT_DIR}/test.R"
