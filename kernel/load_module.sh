#!/bin/bash
# Compile LKM
echo "Cleaning up......"
make clean

echo "Compiling Linux Kernel Module (led_toggle)..."
make

# Ensure Compilation Success
if [ ! -f "led_toggle.ko" ]; then
    echo -e "ERROR\tCompilation failed. Exiting."
    exit 1
fi

# Load LKM
echo "Loading the kernel module..."
sudo insmod led_toggle.ko

# Ensure LKM Load Success
if lsmod | grep -q "led_toggle"; then
    echo "Kernel module loaded successfully."
else
    echo -e "ERROR\tKernel Module unable to load."
    exit 1
fi

# Ensure Module Init Success
SYSFS_PATH="/sys/kernel/led_toggle/led_toggle"
if [ -f "$SYSFS_PATH" ]; then
    echo -e "SUCCESS\tSysfs file exists. Module Initialisation Success."
else
    echo -e "ERROR\tSysfs file not found. Module Initialisation Fail."
    exit 1
fi