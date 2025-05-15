#!/bin/bash
# This script starts a simplified version of the application
# that doesn't require a database connection

echo "Starting simplified API..."
uvicorn app.simple:app --host 0.0.0.0 --port ${PORT:-8000}
