#!/bin/sh
set -e

echo "Entrypoint: Running poetry install..."
poetry install --no-root

echo "Entrypoint: Handing over to CMD..."
exec "$@"
