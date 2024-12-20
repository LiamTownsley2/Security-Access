KERNEL := /lib/modules/$(shell uname -r)/build
PWD := $(shell pwd)

obj-m += led_toggle.o
all:
	make ARCH=arm -C $(KERNEL) M=$(PWD) modules
clean:
	make -C $(KERNEL) M=$(PWD) clean