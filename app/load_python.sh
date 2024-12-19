#!/bin/bash
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
python3 index.py
