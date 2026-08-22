#include "stm32f4xx_hal.h"
#include "src/clock.h"
#include "src/gpio.h"

int main(void) {
    HAL_Init();
    clock_init();
    gpio_led_init();

    while (1) {
        gpio_led_toggle();
        HAL_Delay(500);
    }
}