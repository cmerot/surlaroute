#!/usr/bin/env bash

set -e
set -x

mypy app scripts tests
ruff check app scripts tests
ruff format app scripts tests --check
