#!/usr/bin/env bash

set -e
set -x


script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd $script_dir/..
coverage run --source=app -m pytest
coverage report --show-missing
coverage html --title "${@-coverage}"
