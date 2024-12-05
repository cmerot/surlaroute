#!/usr/bin/env bash

set -e

export PGPASSWORD=changethis
psql -h localhost -U postgres -c "drop database if exists app;"
psql -h localhost -U postgres -c "create database app;"
./scripts/run_pre_start.py
./scripts/run_load_fixtures.py
# fastapi dev app/main.py
