#!/bin/bash

set -e

# Run migrations
echo "Running migrations..."
alembic upgrade head

# Start application
echo "Starting application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
