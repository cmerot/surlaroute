#! /usr/bin/env bash

set -e

rm -rf frontend/src/lib/backend/client frontend/src/lib/backend/openapi.json
mkdir -p frontend/src/lib/backend

cd backend
echo "⏳ Generating openapi.json from backend (FastAPI)"
python -c "import app.main; import json; print(json.dumps(app.main.app.openapi()))" > ../frontend/src/lib/backend/openapi.json
cd ..

cd frontend
echo "⏳ Generating TypeScript client from frontend (@hey-api/openapi-ts)"
pnpm run generate-client
cd ..
