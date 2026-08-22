#include "stm32f4xx_hal.h"
#include "gpio.h"

#define GPIO_LED_PORT GPIOD
#define GPIO_LED_PIN  GPIO_PIN_12

void gpio_led_init(void) {
    GPIO_InitTypeDef init = {0};

    __HAL_RCC_GPIOD_CLK_ENABLE();

    init.Pin = GPIO_LED_PIN;
    init.Mode = GPIO_MODE_OUTPUT_PP;
    init.Pull = GPIO_NOPULL;
    init.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(GPIO_LED_PORT, &init);

    HAL_GPIO_WritePin(
        GPIO_LED_PORT,
        GPIO_LED_PIN,
        GPIO_PIN_SET
    );
}

void gpio_led_toggle(void) {
    HAL_GPIO_TogglePin(GPIO_LED_PORT, GPIO_LED_PIN);
}