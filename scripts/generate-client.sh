#! /usr/bin/env bash

set -e
set -x

rm -rf frontend/src/lib/backend/client frontend/src/lib/backend/openapi.json
mkdir -p frontend/src/lib/backend

cd backend
python -c "import app.main; import json; print(json.dumps(app.main.app.openapi()))" > ../frontend/src/lib/backend/openapi.json
cd ..

cd frontend
pnpm run generate-client
pnpm run format
cd ..
