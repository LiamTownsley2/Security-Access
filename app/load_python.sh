#!/bin/bash
# Generate & Active Virtual Environment
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3.8 -m venv venv
fi
source venv/bin/activate

# Check Requirements
if [ -f "requirements.txt" ]; then
    echo "Installing Python Dependencies..."
    pip install --upgrade --upgrade-strategy only-if-needed -r requirements.txt
    echo -e"SUCCESS\tPython dependancies installed successfully."
else
    echo -e "ERROR\t'requirements.txt' file not found."
    exit 1
fi

echo "Starting App..."
# Start App
python index.py