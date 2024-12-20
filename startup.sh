#!/bin/bash
echo "Setting up Linux Kernel Module..."
cd kernel/
sudo ./load_module.sh
echo -e "SUCCESS: Loaded Linux Kernel Module"
cd ..

echo "Setting up Python Application..."
cd app
./load_python.sh
