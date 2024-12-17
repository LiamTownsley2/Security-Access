#include <linux/module.h>
#include <linux/gpio.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/sysfs.h>

#define GPIO_PIN 17 

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Liam Townsley");
MODULE_DESCRIPTION("Module for toggling LED (Door Control Signal)");
MODULE_VERSION("1.0");

static int led_toggle = 0;
static struct kobject *led_kobj;
static struct kobj_attribute led_attribute = __ATTR(led_toggle, 0660, led_read, led_write); // 0660 = owner & group able to read/write 

static ssize_t led_read(struct kobject *kobj, struct kobj_attribute *attr, char *buffer) {
    return snprintf(buffer, PAGE_SIZE, "%d\n", led_toggle);
}

static ssize_t led_write(struct kobject *kobj, struct kobj_attribute *attr, const char *buffer, size_t count) {
    if (sscanf(buffer, "%d", &led_toggle) == 1) 
        gpio_set_value(GPIO_PIN, led_toggle); 
    return count;
}

static int setup_sysfs(void) {
    led_kobj = kobject_create_and_add("led_toggle", kernel_kobj);
    if (!led_kobj) return -ENOMEM;

    ret = sysfs_create_file(led_kobj, &led_attribute.attr);
    if (ret) {
        kobject_put(led_kobj);
        return -ENOMEM;
    }
    return 0;
}

static int lock_gpio(void) {
    gpio_request(GPIO_PIN, "sysfs");
    gpio_direction_output(GPIO_PIN, 0);
    gpio_export(GPIO_PIN, false);
}

static void free_gpio(void) {
    gpio_set_value(GPIO_PIN, 0);
    gpio_unexport(GPIO_PIN);
    gpio_free(GPIO_PIN); 
}

static int __init led_module_init(void) {
    if (!gpio_is_valid(GPIO_PIN)) return -ENODEV;
    lock_gpio();    
    setup_sysfs();
    return 0;
}

static void __exit led_module_exit(void) {
    sysfs_remove_file(led_kobj, &led_attribute.attr);
    kobject_put(led_kobj);
    free_gpio();
}

module_init(led_module_init);
module_exit(led_module_exit);