#!/bin/bash
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

source venv/bin/activate

if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install --upgrade --upgrade-strategy only-if-needed -r requirements.txt
else
    echo "requirements.txt not found."
fi

python3 index.py
