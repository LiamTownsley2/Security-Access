KERNEL := /home/cmp408/rpisrc/linux
PWD := $(shell pwd)
CROSS := arm-linux-gnu-

obj-m += led_toggle.o
all:
	make ARCH=arm CROSS_COMPILE=$(CROSS) -C $(KERNEL) M=$(PWD) modules
clean:
	make -C $(KERNEL) M=$(PWD) clean