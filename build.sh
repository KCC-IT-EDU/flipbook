#!/bin/bash

# Update package list and install poppler-utils
apt-get update
apt-get install -y poppler-utils

# Upgrade pip and install requirements
python -m pip install --upgrade pip
pip install -r requirements.txt

# Generate the flipbook
python main.py

# Start the Flask server
if [ -f "output/flipbook.html" ]; then
    echo "Starting Flask server..."
    python app.py
else
    echo "Error: flipbook.html not found"
    exit 1
fi 