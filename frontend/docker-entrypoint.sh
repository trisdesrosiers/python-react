#!/bin/sh
set -e

# Create cache directory if it doesn't exist (needed for eslint/webpack)
mkdir -p /app/node_modules/.cache
chmod -R 777 /app/node_modules/.cache 2>/dev/null || true

exec "$@"

