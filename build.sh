#!/bin/bash

# Build script for deployment

echo "Installing dependencies..."
pip install -r requirements-prod.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate --noinput

echo "Build complete!"
