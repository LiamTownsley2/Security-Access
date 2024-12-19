obj-m := led_toggle.o
all:
	make -C /lib/modules/5.4.51/build/ M=$(PWD) modules
clean:
	make -C /lib/modules/5.4.51/build/ M=$(PWD) clean