#include "stm32f4xx_hal.h"
#include "src/driver/clock.h"
#include "src/driver/gpio.h"
#include "src/kernel/queue.h"
#include "src/kernel/statemachine.h"
#include "src/interrupt/interrupt.h"

int main(void)
{
    HAL_Init();

    clock_init();
    gpio_init();

    queue_init();
    statemachine_init();
    interrupt_init();

    while (1) {
        statemachine_process();
    }
}