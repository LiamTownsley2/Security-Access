# CMP408 - Internet of Things: RFID Reader
Python App - app/
Linux Loadable Kernel Module - lkm/


# How to build the kernel
1. Use Fedora VM
2. Pull the Git Repository
3. Navigate to kernel/
4. Execute the 'make' command
5. SCP the files from Fedora VM -> Rasberry Pi

# How to insert the kernel
sudo insmod /home/pi/CMP408-Internet-of-Things/kernel/toggle_led.ko

# How to use the kernel to toggle the LED
