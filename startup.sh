#!/bin/bash
if [ "$(id -u)" -ne 0 ]; then
  echo "This script must executed as root (OR with the sudo command)"
  exit 1
fi

echo "Setting up Linux Kernel Module..."
cd kernel/
sudo ./load_module.sh
echo -e "SUCCESS: Loaded Linux Kernel Module"
cd ..

echo "Setting up Python Application..."
cd app
sudo ./load_python.sh