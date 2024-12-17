#!/bin/bash
echo "Setting up Linux Kernel Module..."
./kernel/load_module.sh
echo -e "SUCCESS: Loaded Linux Kernel Module"

echo "Setting up Python Application..."
./app/load_python.sh