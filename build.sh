#!/bin/bash
set -e

echo "Starting build process..."

# Update package list and install poppler-utils
echo "Installing dependencies..."
apt-get update
apt-get install -y poppler-utils

# Upgrade pip and install requirements
echo "Installing Python packages..."
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# Create output directory if it doesn't exist
echo "Creating output directory..."
mkdir -p output/turnjs

# Copy static files to output directory
echo "Copying static files..."
if [ -d "turnjs" ]; then
    cp -r turnjs/* output/turnjs/
    echo "Copied turnjs files to output/turnjs/"
else
    echo "Warning: turnjs directory not found"
fi

# Generate the flipbook
echo "Generating flipbook..."
python main.py

# Verify flipbook was created
if [ ! -f "output/flipbook.html" ]; then
    echo "Error: flipbook.html was not generated!"
    exit 1
fi

echo "Build completed successfully!"

# Start the Flask server
if [ -f "output/flipbook.html" ]; then
    echo "Starting Flask server..."
    python app.py
else
    echo "Error: flipbook.html not found"
    exit 1
fi 