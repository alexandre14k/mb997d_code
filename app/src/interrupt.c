#include "stm32f4xx_hal.h"
#include "interrupt.h"

void SysTick_Handler(void) {
    HAL_IncTick();
}